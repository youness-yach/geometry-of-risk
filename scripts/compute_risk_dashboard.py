#!/usr/bin/env python3
"""
compute_risk_dashboard.py — Daily-refit live risk dashboard data.

Computes the four metrics shown on the "Geometry of Risk" live dashboard:
  1. Rolling Absorption Ratio (60-day, PCA-based systemic risk gauge)
  2. Standardised AR Delta ("the accelerator") — 15-day change, 30-day z-scored
  3. HMM regime state (3-state Gaussian HMM on [PC1 return, AR, accelerator])
  4. Current rolling correlation matrix (last 60-day window)

This intentionally diverges from notebooks/geometry_of_risk.ipynb (the
peer-reviewed analysis, which uses a single HMM fit validated out-of-sample)
in one way: the HMM here is refit fresh on every run, on the latest
available history. This script is meant to demonstrate the framework
running live as a usable tool, not to reproduce the manuscript's fixed-model
results. Because HMM state labels can flip between independent fits, states
are relabelled every run by mean Absorption Ratio (lowest -> Calm, highest
-> Stress) so the output stays semantically consistent day to day even
though the model itself is not.

Usage:
    python scripts/compute_risk_dashboard.py [output_path]

Output: a JSON file (default: risk-dashboard.json) with time series for all
four metrics, current snapshot values, and a generation timestamp.
"""

import json
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import yfinance as yf
from hmmlearn import hmm
from sklearn.decomposition import PCA

TICKERS = [
    "^GSPC",      # S&P 500 (US Equity)
    "^STOXX50E",  # Euro Stoxx 50 (EU Equity)
    "^N225",      # Nikkei 225 (Japan Equity)
    "000300.SS",  # CSI 300 (China Equity)
    "EEM",        # iShares MSCI Emerging Markets ETF
    "GLD",        # SPDR Gold Shares
    "DX-Y.NYB",   # US Dollar Index
    "BZ=F",       # Brent Crude Oil
    "^TNX",       # 10-Year Treasury Yield
]

TICKER_TO_NAME = {
    "^GSPC": "US_Equity",
    "^STOXX50E": "EU_Equity",
    "^N225": "Japan_Equity",
    "000300.SS": "China_Equity",
    "EEM": "Emerging_Mkts",
    "GLD": "Gold",
    "DX-Y.NYB": "USD_Index",
    "BZ=F": "Oil",
    "^TNX": "US_10Y_Yield",
}

START_DATE = "2007-01-01"
AR_WINDOW = 60
DELTA_PERIOD = 15
DELTA_ZSCORE_WINDOW = 30
HMM_STATES = 3
OUTPUT_SERIES_DAYS = 500  # trim output JSON to the last ~2 trading years


def fetch_prices():
    end_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    raw = yf.download(TICKERS, start=START_DATE, end=end_date, auto_adjust=True, progress=False)
    prices = raw["Close"].rename(columns=TICKER_TO_NAME)
    prices = prices[list(TICKER_TO_NAME.values())].ffill().dropna()
    return prices


def rolling_absorption_ratio(returns, window=AR_WINDOW):
    """AR = (variance of PC1) / (total variance), rolling `window`-day, via SVD."""
    ar_series, dates = [], []
    for i in range(window, len(returns)):
        window_data = returns.iloc[i - window : i]
        standardized = (window_data - window_data.mean()) / window_data.std()
        try:
            _, s, _ = np.linalg.svd(standardized, full_matrices=False)
            eigenvalues = (s ** 2) / (window - 1)
            ar = eigenvalues[0] / np.sum(eigenvalues)
            ar_series.append(ar)
            dates.append(returns.index[i])
        except np.linalg.LinAlgError:
            continue
    return pd.Series(ar_series, index=dates, name="absorption_ratio")


def compute_dashboard(returns):
    # Global PCA (full available history) for PC1 loadings -> PC1 factor returns
    pca = PCA(n_components=1)
    standardized_full = (returns - returns.mean()) / returns.std()
    pca.fit(standardized_full)
    pc1_loadings = pd.Series(pca.components_[0], index=returns.columns)
    pc1_returns = returns.dot(pc1_loadings)

    absorption_ratio = rolling_absorption_ratio(returns)

    delta_ar = absorption_ratio.diff(DELTA_PERIOD)
    mu_delta = delta_ar.rolling(DELTA_ZSCORE_WINDOW).mean()
    sigma_delta = delta_ar.rolling(DELTA_ZSCORE_WINDOW).std()
    accelerator = (delta_ar - mu_delta) / sigma_delta

    features = pd.DataFrame(
        {"pc1_returns": pc1_returns, "absorption_ratio": absorption_ratio, "accelerator": accelerator}
    ).dropna()

    model = hmm.GaussianHMM(n_components=HMM_STATES, covariance_type="full", n_iter=1000, random_state=42)
    model.fit(features.values)
    raw_states = model.predict(features.values)

    # Relabel states by mean Absorption Ratio: lowest -> Calm, highest -> Stress.
    mean_ar_by_state = model.means_[:, 1]
    order = np.argsort(mean_ar_by_state)
    label_map = {order[0]: "Calm", order[1]: "Transitional", order[2]: "Stress"}
    regime = pd.Series([label_map[s] for s in raw_states], index=features.index, name="regime")

    corr_matrix = returns.tail(AR_WINDOW).corr()

    return absorption_ratio, accelerator, regime, corr_matrix


def trim(series, days=OUTPUT_SERIES_DAYS):
    return series.tail(days)


def series_to_json(series):
    return [{"date": idx.strftime("%Y-%m-%d"), "value": None if pd.isna(v) else round(float(v), 6)} for idx, v in series.items()]


def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else "risk-dashboard.json"

    prices = fetch_prices()
    log_returns = np.log(prices / prices.shift(1)).dropna()

    absorption_ratio, accelerator, regime, corr_matrix = compute_dashboard(log_returns)

    current_regime = regime.iloc[-1]
    current_ar = float(absorption_ratio.iloc[-1])
    current_accel = float(accelerator.dropna().iloc[-1]) if not accelerator.dropna().empty else None

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "methodology_note": (
            "HMM regime model is refit on every run (not the fixed, "
            "out-of-sample-validated model used in the manuscript). "
            "See the repository README for details."
        ),
        "current": {
            "absorption_ratio": round(current_ar, 4),
            "accelerator_zscore": round(current_accel, 4) if current_accel is not None else None,
            "regime": current_regime,
            "as_of": absorption_ratio.index[-1].strftime("%Y-%m-%d"),
        },
        "absorption_ratio": series_to_json(trim(absorption_ratio)),
        "accelerator": series_to_json(trim(accelerator)),
        "regime": [
            {"date": idx.strftime("%Y-%m-%d"), "state": state}
            for idx, state in trim(regime).items()
        ],
        "correlation_matrix": {
            "assets": list(corr_matrix.columns),
            "values": [[round(float(v), 4) for v in row] for row in corr_matrix.values],
        },
    }

    with open(output_path, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {output_path}: {len(payload['absorption_ratio'])} AR points, "
          f"current regime = {current_regime} (AR = {current_ar:.3f})")


if __name__ == "__main__":
    main()
