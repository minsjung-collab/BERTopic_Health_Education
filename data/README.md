# Data

## Included

`Document_Topic_Assignments.csv` lists all 4,234 articles in the analytic corpus, with these columns:

- `PMID`: PubMed identifier
- `DOI`: digital object identifier
- `Journal`: AJHP, HEB, HER, or HPI
- `Year`: publication year from the MEDLINE date field. Ninety-three articles show 2026; they met the 2016–2025 PubMed date query and are excluded from year-specific summaries.
- `Topic`: BERTopic topic assigned by the original May 24, 2026 model (−1 = outlier class)
- `Domain`: one of the 16 thematic domains used in the manuscript, or "Outlier class"

The topic assignments were read from the original fitted model and aligned with the archived corpus. Rebuilding the archived output tables from this file reproduces them exactly (`python scripts/verify_outputs.py`).

## Not included

The full-text corpus, `Health_Promotion_BERTopic_2016_2025.csv` (4,235 records; one duplicate removed before modeling), contains publisher-copyrighted abstracts. It is available from the author on request. It can also be regenerated with `scripts/pubmed_retrieval_20260524.py` or from the PMIDs above. To refit the model, place the file in this folder.
