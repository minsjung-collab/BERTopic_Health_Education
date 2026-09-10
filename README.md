# BERTopic Health Education and Health Promotion (2016–2025)

Reproducibility materials for the study:

**From Behavioral Interventions to Digital Health Ecosystems: Mapping Thematic Transformation in Health Education and Health Promotion Research, 2016–2025**

## Scope of this repository

This repository archives the code, verified model configuration, execution log, and analytical outputs recovered from the BERTopic analysis run on **May 24, 2026**.

The historical run loaded 4,235 PubMed records and retained **4,234 records after cleaning**. The saved execution log reports **73 topic IDs in total when the BERTopic outlier class (-1) is included**: 72 non-outlier topic clusters plus the outlier class. The outlier class contains 1,021 documents.

## Repository contents

- `scripts/pubmed_retrieval_20260524.py` — original PubMed retrieval and preprocessing script executed May 24, 2026.
- `scripts/fit_bertopic_verified.py` — reconstruction of the BERTopic model configuration using settings recovered from the serialized fitted model.
- `scripts/inspect_saved_model.py` — utility for inspecting a locally available serialized BERTopic model.
- `docs/PARAMETERS.md` — UMAP, HDBSCAN, BERTopic, vectorizer, and c-TF-IDF settings read directly from the original fitted model.
- `requirements-model.txt` — package versions documented for the original analysis environment.
- `requirements-retrieval.txt` — requirements for PubMed retrieval.
- `logs/BERTopic_Results_20260524.txt` — original May 24 execution log.
- `outputs/Topic_Frequency.xlsx` — topic-frequency table from the original run.
- `outputs/Topic_Labels.xlsx` — topic-label output from the original run.
- `outputs/Topics_Over_Time.xlsx` — temporal topic output from the original run.
- `outputs/Journal_Topic_Comparison.xlsx` — journal-level topic comparison from the original run.
- `outputs/Year_Topic_Distribution.xlsx` — year-by-topic distribution from the original run.
- `model/SHA256SUMS.txt` — SHA-256 integrity information for the original serialized model and retrieval script.

## Verified model settings

### UMAP

- `n_neighbors=10`
- `n_components=5`
- `min_dist=0.0`
- `metric='cosine'`
- `random_state=42`

### HDBSCAN

- `min_cluster_size=15`
- `min_samples=5`
- `metric='euclidean'`
- `cluster_selection_method='eom'`
- `prediction_data=True`

### Other core settings

- Sentence embedding model: `sentence-transformers/all-MiniLM-L6-v2`
- CountVectorizer: `ngram_range=(1, 2)`, `min_df=5`, `max_df=0.9`, English stop words
- BERTopic: `top_n_words=10`, `min_topic_size=10`, `nr_topics=None`, `calculate_probabilities=True`

The parameter values above were recovered from the serialized fitted BERTopic object itself and were **not inferred from package defaults**.

## Reproduction pathways

### 1. Re-create the PubMed corpus

Run:

```bash
python scripts/pubmed_retrieval_20260524.py
```

The script applies the original 2016–2025 journal searches, abstract processing, PMID/DOI deduplication, and text preparation. A PubMed query run at a later date may differ slightly from the May 24, 2026 historical corpus because PubMed metadata can be corrected or re-indexed retrospectively.

### 2. Refit BERTopic with the verified historical settings

After generating/preparing the analytical corpus, install the pinned model dependencies and run:

```bash
pip install -r requirements-model.txt
python scripts/fit_bertopic_verified.py
```

Exact document-level replication is strongest when using the original May 24 analytical corpus (`final_df.csv`). That file could not be recovered. Therefore, this repository supports transparent reconstruction of the pipeline and model configuration but does not claim bit-for-bit re-creation of the unavailable historical input corpus.

### 3. Compare against archived outputs

The `outputs/` directory contains the original May 24 topic-frequency, labels, temporal, journal-comparison, and year-distribution files. These can be used to compare a reconstructed run with the historical results.

## Serialized fitted model

The original serialized BERTopic model was recovered and used to verify the model settings. Its SHA-256 checksum is provided in `model/SHA256SUMS.txt`.

The model file itself is approximately 116 MB, which exceeds GitHub's 100 MB per-file limit for normal Git storage, so it is not committed here. For archival distribution, it should be deposited using Git LFS or a research-data archive such as OSF/Zenodo and linked from this README.

## Reproducibility limitation

The unavailable historical `final_df.csv` means that a future PubMed retrieval cannot be guaranteed to reproduce the exact same 4,234 input records. The original execution log and five archived output workbooks are provided to document and validate the historical run.
