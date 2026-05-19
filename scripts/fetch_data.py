#!/usr/bin/env python3
"""
fetch_data.py — Pull fresh asset price data from Yahoo Finance.

Downloads daily adjusted closing prices for the nine-asset universe used in the
Geometry of Risk framework, covering January 2007 to the current date. The
output CSV is written to data/asset_prices_long_history.csv, overwriting the
bundled file.

Usage:
    python scripts/fetch_data.py

For reproducibility of the published manuscript, use the bundled CSV in the
data/ directory rather than running this script.
"""

import os
import sys
from datetime import datetime

try:
    import yfinance as yf
    import pandas as pd
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


TICKERS = [
    '^GSPC',      # S&P 500 (US Equity)
    '^STOXX50E',  # Euro Stoxx 50 (EU Equity)
    '^N225',      # Nikkei 225 (Japan Equity)
    '000300.SS',  # CSI 300 (China Equity)
    'EEM',        # iShares MSCI Emerging Markets ETF
    'GLD',        # SPDR Gold Shares
    'DX-Y.NYB',   # US Dollar Index
    'BZ=F',       # Brent Crude Oil
    '^TNX',       # 10-Year Treasury Yield
]

TICKER_TO_NAME = {
    '^GSPC':     'US_Equity',
    '^STOXX50E': 'EU_Equity',
    '^N225':     'Japan_Equity',
    '000300.SS': 'China_Equity',
    'EEM':       'Emerging_Mkts',
    'GLD':       'Gold',
    'DX-Y.NYB':  'USD_Index',
    'BZ=F':      'Oil',
    '^TNX':      'US_10Y_Yield',
}

START_DATE = '2007-01-01'
END_DATE = datetime.now().strftime('%Y-%m-%d')


def main():
    # Resolve path to data/ relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    output_path = os.path.join(repo_root, 'data', 'asset_prices_long_history.csv')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"Fetching {len(TICKERS)} tickers from {START_DATE} to {END_DATE}...")
    print(f"Tickers: {', '.join(TICKERS)}")
    print()

    try:
        data = yf.download(
            TICKERS,
            start=START_DATE,
            end=END_DATE,
            auto_adjust=True,
            progress=True,
        )
    except Exception as e:
        print(f"\nDownload failed: {e}")
        print("If this is a network issue, check connectivity and try again.")
        sys.exit(1)

    # Use Close prices (auto_adjust=True applies splits/dividends to Close)
    if 'Close' in data.columns.get_level_values(0):
        prices = data['Close']
    else:
        prices = data

    # Rename columns to friendly labels matching the notebook
    prices = prices.rename(columns=TICKER_TO_NAME)

    # Validate
    print(f"\nDownloaded {len(prices)} rows × {prices.shape[1]} columns")
    print(f"Date range: {prices.index.min().date()} to {prices.index.max().date()}")
    print(f"\nNaN counts per asset:")
    for col in prices.columns:
        nan_count = prices[col].isna().sum()
        first_valid = prices[col].first_valid_index()
        print(f"  {col:<15}: {nan_count} NaN, first valid: {first_valid.date() if first_valid else 'N/A'}")

    # Save
    prices.to_csv(output_path)
    print(f"\nSaved to: {output_path}")
    print("Done.")


if __name__ == '__main__':
    main()
