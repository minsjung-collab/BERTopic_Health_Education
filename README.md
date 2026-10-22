# BERTopic Health Education and Health Promotion (2016–2025)

Reproducibility materials for:

**Jung, M. Mapping Thematic Structure and Change in Health Education and Health Promotion Research, 2016–2025: A BERTopic Analysis.** *Health Promotion Practice* (under review, manuscript HPP-26-0413).

## Scope

This repository archives the PubMed retrieval script, the BERTopic configuration verified from the original fitted model, the archived analytical outputs, and an article-level file of topic assignments for the analysis run on **May 24, 2026**.

- Corpus: 4,235 PubMed records from *Health Education & Behavior* (HEB), *Health Education Research* (HER), *Health Promotion International* (HPI), and the *American Journal of Health Promotion* (AJHP), 2016–2025.
- One duplicate record was removed before modeling (the same AJHP 2024 article indexed under two PMIDs, 39390725 and 39390726, with identical text), leaving **4,234 articles**.
- BERTopic identified **72 topics** plus an outlier class (Topic −1; 1,021 articles). The manuscript groups the 72 topics into 16 thematic domains.

## Repository contents

| Path | Description |
|---|---|
| `scripts/pubmed_retrieval_20260524.py` | Sanitized copy of the May 24, 2026 PubMed retrieval and preprocessing script (Entrez email replaced with a placeholder). Writes `Health_Promotion_BERTopic_2016_2025.csv` / `.xlsx`. |
| `scripts/fit_bertopic_verified.py` | BERTopic configuration using the settings read from the original fitted model. |
| `scripts/verify_outputs.py` | Rebuilds the archived topic, journal, and year tables from the article-level file and checks that they match exactly. |
| `scripts/inspect_saved_model.py` | Prints key settings from a locally available serialized model. |
| `data/Document_Topic_Assignments.csv` | Article-level file: PMID, DOI, journal, publication year, assigned topic, and thematic domain for all 4,234 articles. |
| `docs/PARAMETERS.md` | UMAP, HDBSCAN, vectorizer, c-TF-IDF, and BERTopic settings read from the fitted model. |
| `outputs/*.csv` | CSV copies of the original May 24 workbooks: `Topic_Frequency`, `Topic_Labels`, `Journal_Topic_Comparison`, `Year_Topic_Distribution`. |
| `model/SHA256SUMS.txt` | SHA-256 checksum of the original serialized BERTopic model. |
| `requirements-*.txt` | Software versions for retrieval and modeling. |

## Corpus and reproduction

The analytical corpus is the file written by the retrieval script, `Health_Promotion_BERTopic_2016_2025.csv` (4,235 records), after removal of the duplicate record (`drop_duplicates` on the `CombinedText` column). Earlier documentation referred to this corpus as `final_df.csv`; `final_df` was the name of the in-memory table in the analysis script, not a separate file.

Reproduction was verified on October 22, 2026. The archived corpus was combined with the topic assignments stored in the original fitted model (checksum in `model/SHA256SUMS.txt`). The result reproduces all four archived output tables exactly. Anyone can rerun this check from the public files:

```bash
python scripts/verify_outputs.py
```

The corpus file is not committed here because it contains the full text of publisher-copyrighted abstracts. It is available from the author on request. It can also be regenerated from the PMIDs in `data/Document_Topic_Assignments.csv`, or by rerunning the retrieval script. A later PubMed retrieval may differ slightly from the May 24, 2026 corpus, because PubMed records can be corrected or re-indexed retrospectively.

To refit the model:

```bash
pip install -r requirements-model.txt
python scripts/fit_bertopic_verified.py   # expects data/Health_Promotion_BERTopic_2016_2025.csv
```

Topic numbering in a refit can differ from the archived run unless the same corpus, software versions, and hardware are used, because UMAP and HDBSCAN are sensitive to the computing environment.

## Fitted model

The original serialized BERTopic model (about 116 MB) exceeds GitHub's per-file limit and is not committed. Its checksum is provided, and the model is available from the author on request.

## Citation

See `CITATION.cff`.

## License

Scripts and documentation: MIT (see `LICENSE`). Third-party components remain under their own licenses (see `THIRD_PARTY_NOTICE.md`).
