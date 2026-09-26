# Manuscript

**The Geometry of Risk: An Integrated Monitoring Framework for Multi-Asset Systemic Stress**
Youness Yachruti · Independent Researcher · yyachruti@gmail.com

| | |
|---|---|
| Preprint (SSRN) | https://ssrn.com/abstract=7521018 |
| DOI | [10.2139/ssrn.7521018](https://doi.org/10.2139/ssrn.7521018) |
| PDF | [`geometry_of_risk_preprint.pdf`](geometry_of_risk_preprint.pdf) (manuscript version of May 2026) |
| Status | Preprint, not peer reviewed · posted 26 Sep 2026 · 34 pages |
| Licence | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): free to share and adapt, with credit to the author |

The preprint has not been peer reviewed. It contains the full methodology, the
econometric-limitations discussion, the complete reference list and the formal
write-up of the results produced by this codebase.

## Cite

> Yachruti, Y. (2026). The Geometry of Risk: An Integrated Monitoring Framework
> for Multi-Asset Systemic Stress. SSRN preprint. https://doi.org/10.2139/ssrn.7521018

```bibtex
@misc{yachruti2026geometry,
  author       = {Yachruti, Youness},
  title        = {The Geometry of Risk: An Integrated Monitoring Framework for Multi-Asset Systemic Stress},
  year         = {2026},
  howpublished = {SSRN preprint},
  doi          = {10.2139/ssrn.7521018},
  url          = {https://ssrn.com/abstract=7521018},
  note         = {Preprint}
}
```

## Reproducing the paper

The code in this repository reproduces the paper's method and its headline
findings. A few secondary numbers differ, and the reason is the data, not the
method.

**Why.** The paper's current-study figures were computed in late May 2026, when
the notebook downloaded "the last year" of prices live from Yahoo Finance. In
September 2026 that window was frozen to exactly the period the paper
describes, 24 April 2025 to 24 April 2026 (261 trading days, in
`data/snapshot/`), so every run now gives the same answer. The two windows
overlap almost entirely but aren't identical, and small sample shifts move
p-values and variance shares.

| Result | Paper (late-May 2026 download) | This repo (frozen window) |
|---|---|---|
| Absorption Ratio above 0.50 in all four crisis windows | Yes | Yes |
| Bonferroni-surviving Granger links (all into Japan Equity) | 4 | 4 |
| Uncorrected Granger links (of 72) | 15 | 16 |
| Oil joint F-tests (oil → system / system → oil), p-values | 0.765 / 0.252 | 0.379 / 0.328 |
| Oil's share of 10-day forecast-error variance (EU equity, EM, US 10Y) | 16–21% | 11–16% |
| Out-of-sample HMM flags the April 2026 stress regime | Yes | Yes |

The conclusions are unchanged. Oil stays quasi-exogenous: neither F-test
rejects at 5%. Its volatility-channel contribution stays material, and every
Bonferroni-robust link still points into Japan Equity.

## Licence

The paper is distributed under the [Creative Commons Attribution 4.0
International licence (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
Anyone may share and adapt it, including commercially, provided they credit the
author and cite the preprint (see [Cite](#cite)). The code in this repository is
separately MIT-licensed.
