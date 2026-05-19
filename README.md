# The Geometry of Risk

### An Integrated Monitoring Framework for Multi-Asset Systemic Stress

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

This repository contains the complete code and data pipeline for the Geometry of
Risk research project: a four-layer empirical monitoring framework for multi-asset
systemic stress diagnostics.

The framework is positioned within the empirical systemic-risk monitoring
tradition of Kritzman et al. (2011) and Diebold and Yilmaz (2014). It is not a
structural equilibrium asset-pricing model, a forecasting system, or an attempt
to derive prices from first principles. The statistical objects produced—
correlation distances, minimum spanning trees, principal components, Granger
predictability matrices, and HMM latent states—are descriptive characterisations
of the empirical joint distribution of returns.

## Overview

The framework integrates four methodological layers applied to nine globally
representative asset classes (US, EU, Japan, China, and Emerging Markets
equity; Gold; the US Dollar Index; Brent crude oil; and the US 10-Year Treasury
Yield):

| Layer | Methods |
|---|---|
| **1. Network topology** | Correlation distance, Multidimensional Scaling, Ward hierarchical clustering, Minimum Spanning Trees (price-based and volume-weighted) |
| **2. Dynamic causality** | Pairwise Granger causality with Bonferroni correction, lead-lag cross-correlation, joint F-tests for asset exogeneity, variance decomposition |
| **3. Tail-risk quantification** | Conditional Value-at-Risk, lower tail dependence, MOVE/VIX sensitivities with Newey–West standard errors |
| **4. Regime classification** | Rolling Absorption Ratio, Hidden Markov Model with BIC selection, posterior entropy, out-of-sample evaluation on multi-crisis training history |

**Sample windows:**
- Current-study analytical core: April 2025 to 24 April 2026 (N = 261)
- Long-history validation sample: 31 March 2011 to 24 April 2026 (N = 3,472)

**Robustness components:**
1. Multi-crisis Absorption Ratio replication across the 2007–2009 GFC, the
   2019–2020 COVID-19 dislocation, the 2022–2023 Federal Reserve tightening cycle,
   and the current-study window — all four episodes breach the Kritzman et al.
   (2011) 0.50 threshold
2. Dynamic Conditional Correlation GARCH baseline (Engle, 2002) on the
   long-history sample, providing a parametric benchmark for the network-
   topological approach (MST Jaccard similarity = 0.455)
3. Out-of-sample HMM evaluation calibrated on the 14-year multi-crisis training
   history, correctly identifying the April 2026 stress regime with bounded
   posterior entropy

## Repository structure

```
geometry-of-risk/
├── README.md                        This file
├── LICENSE                          MIT License (code)
├── requirements.txt                 Python dependencies
├── notebooks/
│   └── geometry_of_risk.ipynb       Main reproducible notebook
├── data/
│   └── asset_prices_long_history.csv  Bundled dataset (April 2025–April 2026 + long history)
├── scripts/
│   └── fetch_data.py                Optional: pull fresh data from Yahoo Finance
└── manuscript/
    └── README.md                    Pointer to the working paper
```

## Getting started

### Prerequisites

- Python 3.10 or higher
- Approximately 500 MB of disk space (mostly for libraries)
- Internet access (only for first-time setup or fresh-data option)

### Installation

```bash
# Clone the repository
git clone https://github.com/youness-yach/geometry-of-risk.git
cd geometry-of-risk

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Two ways to run the analysis

#### Option 1 — Reproduce the manuscript results exactly

The bundled `data/asset_prices_long_history.csv` contains the exact data used
in the manuscript (April 2025 to 24 April 2026, with long history back to 2007).

```bash
jupyter notebook notebooks/geometry_of_risk.ipynb
```

Run all cells in order. Results will match the published manuscript.

#### Option 2 — Run with fresh data

Pull a current copy of the data from Yahoo Finance:

```bash
python scripts/fetch_data.py
jupyter notebook notebooks/geometry_of_risk.ipynb
```

This overwrites the bundled CSV with current data. Results will reflect the
data as of the date of download and may differ from the published manuscript.

## Reproducibility notes

- All random seeds are set to `42` throughout the analysis.
- Sample-specific results (correlations, MST topology, HMM states) may differ
  slightly across yfinance API versions or if data is pulled on different dates.
- The DCC-GARCH parameter estimation depends on numerical optimisation and may
  produce parameters that differ at the 4th decimal place across runs.

## Citation

If you use this code or methodology, please cite:

> Yachruti, Y. (2026). The Geometry of Risk: An Integrated Monitoring Framework
> for Multi-Asset Systemic Stress. *Working paper.* Available at
> https://github.com/youness-yach/geometry-of-risk

## License

**Code:** MIT License — see [LICENSE](LICENSE).

**Data:** The bundled CSV is derived from Yahoo Finance public data. Users are
responsible for compliance with Yahoo Finance's terms of service.

**Manuscript:** The accompanying working paper is currently under peer review;
reuse of the manuscript text is subject to the journal's eventual license
terms.

## Contact

Youness Yachruti — yyachruti@gmail.com

## References

The full reference list is provided in the accompanying manuscript. Key
foundational references include:

- Kritzman, M., Li, Y., Page, S., & Rigobon, R. (2011). Principal components as
  a measure of systemic risk. *Journal of Portfolio Management*, 37(4), 112–126.
- Engle, R. F. (2002). Dynamic conditional correlation. *Journal of Business
  and Economic Statistics*, 20(3), 339–350.
- Mantegna, R. N. (1999). Hierarchical structure in financial markets.
  *European Physical Journal B*, 11(1), 193–197.
- Granger, C. W. J. (1969). Investigating causal relations by econometric
  models and cross-spectral methods. *Econometrica*, 37(3), 424–438.
- Hamilton, J. D. (1989). A new approach to the economic analysis of
  nonstationary time series and the business cycle. *Econometrica*, 57(2),
  357–384.
- Diebold, F. X., & Yilmaz, K. (2014). On the network topology of variance
  decompositions. *Journal of Econometrics*, 182(1), 119–134.
- Cont, R. (2001). Empirical properties of asset returns: Stylized facts and
  statistical issues. *Quantitative Finance*, 1(2), 223–236.
