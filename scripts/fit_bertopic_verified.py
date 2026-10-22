"""Reconstruct the BERTopic configuration verified from the saved May 2026 model.

Expected input: the corpus written by scripts/pubmed_retrieval_20260524.py,
`data/Health_Promotion_BERTopic_2016_2025.csv` (4,235 records). As in the original
run, the one duplicate record (identical `CombinedText`) is dropped, leaving 4,234.

Important: Exact topic-number/assignment reproduction requires the exact historical
analytical corpus and compatible software versions. PubMed re-downloads can change
if records are retrospectively corrected or re-indexed.
"""

import random
import numpy as np
import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

INPUT_CSV = "data/Health_Promotion_BERTopic_2016_2025.csv"
TEXT_COLUMN = "CombinedText"

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

umap_model = UMAP(
    n_neighbors=10,
    n_components=5,
    min_dist=0.0,
    metric="cosine",
    output_metric="euclidean",
    init="spectral",
    random_state=42,
    transform_seed=42,
    n_jobs=1,
    negative_sample_rate=5,
    spread=1.0,
    learning_rate=1.0,
    repulsion_strength=1.0,
)

hdbscan_model = HDBSCAN(
    min_cluster_size=15,
    min_samples=5,
    metric="euclidean",
    alpha=1.0,
    cluster_selection_method="eom",
    prediction_data=True,
    algorithm="best",
    approx_min_span_tree=True,
    gen_min_span_tree=False,
    core_dist_n_jobs=4,
    cluster_selection_epsilon=0.0,
    allow_single_cluster=False,
)

vectorizer_model = CountVectorizer(
    stop_words=list(ENGLISH_STOP_WORDS),
    ngram_range=(1, 2),
    min_df=5,
    max_df=0.9,
    lowercase=True,
)

topic_model = BERTopic(
    embedding_model=embedding_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer_model,
    top_n_words=10,
    min_topic_size=10,
    nr_topics=None,
    calculate_probabilities=True,
    verbose=True,
)

if __name__ == "__main__":
    df = pd.read_csv(INPUT_CSV)
    df = df.drop_duplicates(subset=[TEXT_COLUMN], keep="first").reset_index(drop=True)
    assert len(df) == 4234, f"Expected 4,234 articles after removing the duplicate; found {len(df)}"
    docs = df[TEXT_COLUMN].fillna("").astype(str).tolist()
    topics, probabilities = topic_model.fit_transform(docs)
    topic_model.get_topic_info().to_csv("topic_info_reproduced.csv", index=False)
    pd.DataFrame({"topic": topics}).to_csv("document_topics_reproduced.csv", index=False)
    topic_model.save("BERTopic_Model_reproduced", serialization="pickle")
