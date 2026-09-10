# BERTopic Health Education and Health Promotion (2016–2025)

Reproducibility materials for the study:

**From Behavioral Interventions to Digital Health Ecosystems: Mapping Thematic Transformation in Health Education and Health Promotion Research, 2016–2025**

## Scope of this repository

This repository archives the verified computational configuration and analytical outputs recovered from the BERTopic analysis run on **May 24, 2026**.

The historical run loaded 4,235 PubMed records and retained **4,234 records after cleaning**. The original execution log reports **73 topic IDs in total when the BERTopic outlier class (-1) is included**: 72 non-outlier topic clusters plus the outlier class. The outlier class contains 1,021 documents.

## Repository contents

- `scripts/pubmed_retrieval_20260524.py` — sanitized reproducibility copy of the May 24 PubMed retrieval/preprocessing script; the original Entrez email address was replaced with a placeholder.
- `scripts/fit_bertopic_verified.py` — reconstruction of the BERTopic model configuration using settings recovered from the serialized fitted model.
- `scripts/inspect_saved_model.py` — utility for inspecting a locally available serialized BERTopic model.
- `docs/PARAMETERS.md` — UMAP, HDBSCAN, BERTopic, vectorizer, and c-TF-IDF settings read directly from the original fitted model.
- `requirements-model.txt` — package versions documented for the original analysis environment.
- `requirements-retrieval.txt` — dependencies for PubMed retrieval.
- `outputs/Topic_Frequency.csv` — CSV transcription of the original May 24 topic-frequency workbook.
- `outputs/Topic_Labels.csv` — CSV transcription of the original May 24 topic-label workbook.
- `outputs/Journal_Topic_Comparison.csv` — CSV transcription of the original May 24 journal-level comparison workbook.
- `outputs/Year_Topic_Distribution.csv` — CSV transcription of the original May 24 year-by-topic distribution workbook.
- `model/SHA256SUMS.txt` — SHA-256 checksum for the original serialized BERTopic model.

The original `Topics_Over_Time.xlsx` workbook and May 24 execution-log text file are preserved by the study author but are not currently committed here. The original serialized model is also preserved by the study author.

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
The `outputs/` directory contains CSV transcriptions of four original May 24 Excel workbooks. These preserve the worksheet cell values and can be used to compare a reconstructed run with the historical results.

## Serialized fitted model
The original serialized BERTopic model was recovered and used to verify the model settings. Its SHA-256 checksum is provided in `model/SHA256SUMS.txt`.

The model file itself is approximately 116 MB, which exceeds GitHub's 100 MB per-file limit for ordinary Git storage, so it is not committed here. It should be distributed through Git LFS or a research-data archive such as OSF or Zenodo if public model download is desired.

## Reproducibility limitation
The unavailable historical `final_df.csv` means that a future PubMed retrieval cannot be guaranteed to reproduce the exact same 4,234 input records. The repository therefore supports transparent reconstruction of the analysis workflow and direct verification of the recovered model parameters, but it does not claim bit-for-bit recreation of the historical input corpus.
