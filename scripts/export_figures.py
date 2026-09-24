#!/usr/bin/env python3
"""Copy the notebook's key charts into figures/ for the README.

    python scripts/export_figures.py      # run after executing the notebook

Charts are matched by the plotting code that draws them, so they always show
the notebook's saved outputs.
"""
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHARTS = {  # text in the plotting cell -> output file
    "The Macro Matrix: Global Correlation Structure": "1_correlation_matrix.png",
    "The Global Risk Skeleton (Minimum Spanning Tree)\")": "2_minimum_spanning_tree.png",
    "Granger Causality Significance Matrix": "3_granger_bonferroni.png",
    "Tail Dependence Matrix": "4_tail_dependence.png",
    "DCC-GARCH Dynamic Conditional Correlations": "5_dcc_garch.png",
    "Multi-Crisis Validation of the Systemic Absorption Ratio": "6_absorption_ratio_multi_crisis.png",
    "Mode A: OOS Regime Classification": "7_hmm_out_of_sample.png",
}

cells = json.loads((ROOT / "notebooks" / "geometry_of_risk.ipynb").read_text())["cells"]
out = ROOT / "figures"
out.mkdir(exist_ok=True)
for key, name in CHARTS.items():
    matches = [c for c in cells if c["cell_type"] == "code" and key in "".join(c["source"])]
    assert len(matches) == 1, (key, len(matches))
    png = [o["data"]["image/png"] for o in matches[0]["outputs"] if "image/png" in o.get("data", {})][0]
    (out / name).write_bytes(base64.b64decode(png))
    print("wrote", name)
