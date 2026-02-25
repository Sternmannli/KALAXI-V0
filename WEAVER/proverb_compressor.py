# proverb_compressor.py
# Cross‑anomaly compressor for Kalaxi
# Generates proverb candidates from clusters of anomalies
# Based on Kuusi's paremiological minimum and script opposition theory

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
from datetime import datetime
import re

# Load embedding model
EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

# Syntactic frames for proverbs
FRAMES = {
    "equative": "{} is {}",
    "possessive": "The {} that {}s",
    "causal": "When {}, {}",
    "privative": "{} without {}"
}

def cluster_anomalies(anomaly_list, eps=0.5, min_samples=2):
    """
    Cluster anomalies by embedding similarity.
    anomaly_list: list of dicts with 'text' and 'felt_domain'
    Returns list of clusters (lists of anomaly dicts)
    """
    if len(anomaly_list) < 2:
        return []
    texts = [a['text'] for a in anomaly_list]
    embs = EMBEDDING_MODEL.encode(texts)
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine').fit(embs)
    clusters = {}
    for i, label in enumerate(clustering.labels_):
        if label == -1:
            continue
        clusters.setdefault(label, []).append(anomaly_list[i])
    return list(clusters.values())

def extract_core_contradiction(cluster):
    """
    Combine anomaly descriptions and extract a plain sentence
    describing the shared script opposition.
    Simplified: take the longest description as representative.
    """
    # In production, use a more sophisticated method (e.g., summarization)
    # Here we just pick the longest text
    texts = [a['text'] for a in cluster if 'text' in a]
    if not texts:
        return ""
    return max(texts, key=len)

def extract_concrete_images(text):
    """
    Return the two most concrete nouns/verbs from text.
    Simplified: take the first and last content word.
    """
    words = re.findall(r'\b\w+\b', text.lower())
    stopwords = set(["the","and","is","in","to","of","that","for","on","with","a","an","be","are","was"])
    content = [w for w in words if w not in stopwords and len(w) > 2]
    if len(content) < 2:
        # fallback: use whole text
        return ["something", "everything"]
    return [content[0], content[-1]]

def select_frame(images, opposition_type):
    """
    Choose a syntactic frame based on opposition type.
    opposition_type: e.g., 'agency', 'legibility', etc.
    """
    # Simple mapping – can be extended
    frame_choice = {
        "agency": "causal",
        "legibility": "privative",
        "moral": "possessive",
        "collective": "equative",
        "temporal": "causal"
    }
    frame_name = frame_choice.get(opposition_type, "equative")
    frame = FRAMES[frame_name]
    return frame.format(images[0], images[1])

def lock_test(candidate):
    """
    Simple lock test: candidate should be non‑trivial length and contain a verb.
    In production, this would use paraphrase models and measure embedding shift.
    """
    words = candidate.split()
    if len(words) < 4:
        return False
    if not any(w in candidate.lower() for w in ["is","are","was","be","have","has","do","does","will","can"]):
        return False
    return True

def generate_proverb_from_cluster(cluster):
    """
    Generate a proverb candidate from a cluster of anomalies.
    Returns dict with text, source anomalies, metadata.
    """
    if len(cluster) < 2:
        return None
    core = extract_core_contradiction(cluster)
    images = extract_concrete_images(core)
    # Determine opposition type from felt_domain of first anomaly
    opp_type = cluster[0].get('felt_domain', 'general')
    candidate = select_frame(images, opp_type)
    if not lock_test(candidate):
        return None
    return {
        "text": candidate,
        "source_anomalies": [a.get('id', 'unknown') for a in cluster],
        "felt_domains": list(set(a.get('felt_domain','unknown') for a in cluster)),
        "timestamp": datetime.now().isoformat(),
        "provisional": True
    }

def compress_all(anomaly_registry):
    """
    Run compression on entire anomaly registry.
    Returns list of candidate proverbs.
    """
    clusters = cluster_anomalies(anomaly_registry)
    candidates = []
    for cl in clusters:
        prov = generate_proverb_from_cluster(cl)
        if prov:
            candidates.append(prov)
    return candidates

# Example usage
if __name__ == "__main__":
    # Simulated anomalies
    test_anomalies = [
        {"id": "ANOM#0020", "text": "system fails to halt when stress threshold exceeded", "felt_domain": "agency"},
        {"id": "ANOM#0021", "text": "model continues to advance after halt signal", "felt_domain": "agency"},
        {"id": "ANOM#0091", "text": "covenant COV#002 not enforced in Turn module", "felt_domain": "agency"}
    ]
    clusters = cluster_anomalies(test_anomalies)
    for cl in clusters:
        prov = generate_proverb_from_cluster(cl)
        if prov:
            print("Proverb candidate:", prov["text"])
            print("Source:", prov["source_anomalies"])