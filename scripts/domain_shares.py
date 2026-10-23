"""Recompute Table 3, Panel A (domain shares, ratios, and patterns) from the article-level file.

Usage: python scripts/domain_shares.py   (requires pandas)

Definitions (as in the manuscript):
- Share: a domain's articles as a percentage of all articles published in a period
  (2016-2019, n = 1,426; 2022-2025, n = 1,928). Articles dated 2026 are excluded.
- Ratio: later share / 2016-2019 share (crude); pooled 2024-2025 share / 2016-2019 share
  (persistence check); and journal-standardized ratio, weighting each journal by its
  share of the full 4,234-article corpus.
- Pattern: surge = increase (ratio >= 1.5) that peaked in 2020-2022 with a 2025 annual
  count more than one third below the peak (takes precedence); sustained increase/decrease
  = ratio >= 1.5 or <= 0.67 and the pooled 2024-2025 ratio beyond the same threshold;
  decrease, partly reversed = decrease that did not persist in 2024-2025.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
d = pd.read_csv(ROOT / "data" / "Document_Topic_Assignments.csv")
EARLY, LATE, LAST = [2016, 2017, 2018, 2019], [2022, 2023, 2024, 2025], [2024, 2025]
YEARS = list(range(2016, 2026))
w = d["Journal"].value_counts(normalize=True)


def share(sub, dom, years):
    s = sub[sub["Year"].isin(years)]
    return (s["Domain"] == dom).mean()


def std_share(dom, years):
    return sum(wj * share(d[d["Journal"] == j], dom, years) for j, wj in w.items())


rows = []
for dom in sorted(set(d["Domain"]) - {"Outlier class"}):
    e, l, ll = share(d, dom, EARLY), share(d, dom, LATE), share(d, dom, LAST)
    r, rll = l / e, ll / e
    rs = std_share(dom, LATE) / std_share(dom, EARLY)
    counts = [int(((d["Year"] == y) & (d["Domain"] == dom)).sum()) for y in YEARS]
    peak_year = YEARS[counts.index(max(counts))]
    if r >= 1.5 and peak_year in (2020, 2021, 2022) and counts[-1] < (2 / 3) * max(counts):
        pattern = "Surge"
    elif r >= 1.5 and rll >= 1.5:
        pattern = "Sustained increase"
    elif r <= 2 / 3 and rll <= 2 / 3:
        pattern = "Sustained decrease"
    elif r <= 2 / 3:
        pattern = "Decrease, partly reversed"
    else:
        pattern = "Below threshold"
    n = int((d["Domain"] == dom).sum())
    rows.append(dict(Domain=dom, n=n, pct=round(100 * n / len(d), 1), share_2016_2019=round(100 * e, 1),
                     share_2022_2025=round(100 * l, 1), ratio=round(r, 2), ratio_2024_2025=round(rll, 2),
                     ratio_journal_standardized=round(rs, 2), pattern=pattern))

out = pd.DataFrame(rows).sort_values("n", ascending=False)
pd.set_option("display.width", 200)
print(out.to_string(index=False))
