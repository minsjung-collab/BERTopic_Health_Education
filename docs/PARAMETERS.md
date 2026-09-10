# Verified BERTopic configuration from the serialized May 2026 model

These values were read directly from the serialized BERTopic object supplied from the May 2026 analysis folder. They are not reconstructed from package defaults.

## BERTopic-level settings
- embedding model: `sentence-transformers/all-MiniLM-L6-v2`
- top_n_words: `10`
- min_topic_size: `10`
- nr_topics: `None`
- calculate_probabilities: `True`
- verbose: `True`

## UMAP
- n_neighbors: `10`
- n_components: `5`
- min_dist: `0.0`
- metric: `cosine`
- output_metric: `euclidean`
- init: `spectral`
- random_state: `42`
- transform_seed: `42`
- n_jobs: `1`
- negative_sample_rate: `5`
- spread: `1.0`
- learning_rate: `1.0`
- repulsion_strength: `1.0`

## HDBSCAN
- min_cluster_size: `15`
- min_samples: `5`
- metric: `euclidean`
- alpha: `1.0`
- cluster_selection_method: `eom`
- prediction_data: `True`
- algorithm: `best`
- approx_min_span_tree: `True`
- gen_min_span_tree: `False`
- core_dist_n_jobs: `4`
- cluster_selection_epsilon: `0.0`
- allow_single_cluster: `False`

## CountVectorizer
- analyzer: `word`
- lowercase: `True`
- ngram_range: `(1, 2)`
- min_df: `5`
- max_df: `0.9`
- max_features: `None`
- binary: `False`
- token_pattern: `(?u)\\b\\w\\w+\\b`
- stop words: English stop-word list stored in the fitted vectorizer

## c-TF-IDF
- bm25_weighting: `False`
- reduce_frequent_words: `False`
- seed_words: `None`
- seed_multiplier: `2`

## Random seeds in PubMed preprocessing script
- Python `random.seed(42)`
- NumPy `np.random.seed(42)`
