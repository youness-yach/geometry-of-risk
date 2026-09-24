#!/usr/bin/env python3
"""
fetch_snapshot.py: freeze the manuscript's current-study window.

The notebook's current-study sections originally called yf.download(period="1y"),
so every run pulled a different trailing year. This script downloads that year
once, ending 24 April 2026 as in the manuscript, and saves it to
data/snapshot/. The notebook then reads it through snapshot_download() and
snapshot_fred(), so results no longer depend on the run date.

Usage:
    python scripts/fetch_snapshot.py      # needs yfinance (pip install yfinance)
"""

import io
import sys
import urllib.request
from pathlib import Path

try:
    import pandas as pd
    import yfinance as yf
except ImportError as e:
    sys.exit(f"Missing dependency: {e}. Run: pip install yfinance pandas")

START, END = "2025-04-24", "2026-04-25"          # yfinance end is exclusive -> through 24 Apr 2026
FRED = {"CPIAUCSL": ("2024-01-01", "2026-04-22"), "DGS10": ("2024-01-01", "2026-04-22")}
SYMBOLS = [
    "^GSPC", "^STOXX50E", "^N225", "MCHI", "EEM", "DX-Y.NYB", "GC=F", "CL=F", "^TNX",  # 9-asset universe
    "UUP", "IEF", "SPY",                                                                # volume proxies
    "^MOVE", "^VIX",                                                                    # volatility indices
]
OUT = Path(__file__).resolve().parent.parent / "data" / "snapshot"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    raw = yf.download(SYMBOLS, start=START, end=END, progress=False)
    raw.to_csv(OUT / "yahoo.csv")
    print(f"yahoo.csv: {raw.shape[0]} days, {raw.index.min().date()} -> {raw.index.max().date()}, "
          f"fields {sorted(set(raw.columns.get_level_values(0)))}")
    missing = [s for s in SYMBOLS if raw["Close"][s].dropna().empty]
    if missing:
        print("WARNING: no data for", missing)

    for sid, (start, end) in FRED.items():
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd={start}&coed={end}"
        with urllib.request.urlopen(url, timeout=60) as r:
            df = pd.read_csv(io.BytesIO(r.read()))
        df.columns = ["DATE", sid]
        df.to_csv(OUT / f"fred_{sid}.csv", index=False)
        print(f"fred_{sid}.csv: {len(df)} rows")
    print(f"yfinance {yf.__version__}; snapshot written to {OUT}")


if __name__ == "__main__":
    main()
