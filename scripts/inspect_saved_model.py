"""Print key settings from a trusted BERTopic pickle.
Only unpickle files you trust; Python pickle can execute code during loading.
"""
from bertopic import BERTopic

MODEL_PATH = "model/BERTopic_Model.pkl"
model = BERTopic.load(MODEL_PATH)

u = model.umap_model
h = model.hdbscan_model
v = model.vectorizer_model

print("Embedding model:", getattr(getattr(model, "embedding_model", None), "embedding_model", None))
print("BERTopic min_topic_size:", model.min_topic_size)
print("BERTopic top_n_words:", model.top_n_words)
print("BERTopic nr_topics:", model.nr_topics)
print("UMAP:", {k: getattr(u, k, None) for k in ["n_neighbors","n_components","min_dist","metric","output_metric","init","random_state","transform_seed","n_jobs"]})
print("HDBSCAN:", {k: getattr(h, k, None) for k in ["min_cluster_size","min_samples","metric","alpha","cluster_selection_method","prediction_data","algorithm","core_dist_n_jobs"]})
print("Vectorizer:", {k: getattr(v, k, None) for k in ["ngram_range","min_df","max_df","max_features","lowercase"]})
