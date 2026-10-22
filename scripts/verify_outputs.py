"""Verify the archived output tables from the article-level topic assignments.

Rebuilds Topic_Frequency, Journal_Topic_Comparison, and Year_Topic_Distribution
from data/Document_Topic_Assignments.csv and checks that every cell matches the
archived CSV copies of the original May 24, 2026 workbooks in outputs/.

Usage: python scripts/verify_outputs.py   (requires pandas)
"""
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
docs = pd.read_csv(ROOT / "data" / "Document_Topic_Assignments.csv")

freq = pd.read_csv(ROOT / "outputs" / "Topic_Frequency.csv").set_index("Topic")["Count"]
jour = pd.read_csv(ROOT / "outputs" / "Journal_Topic_Comparison.csv").set_index("Journal")
year = pd.read_csv(ROOT / "outputs" / "Year_Topic_Distribution.csv").set_index("Year")
jour.columns = jour.columns.astype(int)
year.columns = year.columns.astype(int)

ok = True

rebuilt_freq = docs["Topic"].value_counts().reindex(freq.index, fill_value=0)
match = (rebuilt_freq.values == freq.values).all()
print(f"Topic_Frequency:          {'MATCH' if match else 'MISMATCH'}")
ok &= bool(match)

rebuilt_jour = pd.crosstab(docs["Journal"], docs["Topic"]).reindex(index=jour.index, columns=jour.columns, fill_value=0)
match = (rebuilt_jour.values == jour.values).all()
print(f"Journal_Topic_Comparison: {'MATCH' if match else 'MISMATCH'}")
ok &= bool(match)

rebuilt_year = pd.crosstab(docs["Year"], docs["Topic"]).reindex(index=year.index, columns=year.columns, fill_value=0)
match = (rebuilt_year.values == year.values).all()
print(f"Year_Topic_Distribution:  {'MATCH' if match else 'MISMATCH'}")
ok &= bool(match)

print(f"Articles: {len(docs)}; topics (excluding -1): {docs.loc[docs.Topic >= 0, 'Topic'].nunique()}")
sys.exit(0 if ok else 1)
