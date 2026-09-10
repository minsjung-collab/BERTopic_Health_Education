"""Reconstruct the BERTopic configuration verified from the saved May 2026 model.

Expected input: a CSV containing the exact analytical corpus used in the paper.
By default, this script looks for `data/final_df.csv` and a text column named
`Combined_Text`. Change TEXT_COLUMN only if the archived corpus uses another name.

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

INPUT_CSV = "data/final_df.csv"
TEXT_COLUMN = "Combined_Text"

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
    docs = df[TEXT_COLUMN].fillna("").astype(str).tolist()
    topics, probabilities = topic_model.fit_transform(docs)
    topic_model.get_topic_info().to_csv("topic_info_reproduced.csv", index=False)
    pd.DataFrame({"topic": topics}).to_csv("document_topics_reproduced.csv", index=False)
    topic_model.save("BERTopic_Model_reproduced", serialization="pickle")
