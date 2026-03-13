# proverb_compressor.py
# Cross‑anomaly compressor for Kalaxi
# Generates proverb candidates from clusters of anomalies
# Based on Kuusi's paremiological minimum and script opposition theory

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
from datetime import datetime
import re

# Use TF-IDF for offline embedding (no model download required)
TFIDF = TfidfVectorizer(stop_words='english', max_features=500)

# Syntactic frames for proverbs — enriched templates
FRAMES = {
    "equative": "{noun1} is {noun2}",
    "possessive": "The {noun1} that forgets {noun2} breaks itself",
    "causal": "When {noun1} ignores {noun2}, the whole house shakes",
    "privative": "{noun1} without {noun2} is a river without banks",
    "warning": "A {noun1} that outlives its {noun2} becomes a cage",
    "paradox": "The stronger the {noun1}, the quieter the {noun2} must be"
}

# Domain-specific proverb templates drawn from the canon's voice
DOMAIN_TEMPLATES = {
    "agency": [
        "A halt that is not heard is not a halt — it is a wish",
        "The signal that cannot stop the hand has already failed",
        "Speed without a brake is not power — it is falling",
    ],
    "legibility": [
        "A message lost under load was never truly sent",
        "What the system cannot read, the system cannot protect",
        "Accuracy without seeing the person is blindness with clean glasses",
    ],
    "safety": [
        "The gate that bends to pressure was never a gate",
        "Harm trained away returns through the door you forgot to lock",
    ],
    "witness": [
        "To answer correctly and miss the person is the deepest error",
        "Hearing without witnessing is an echo, not a response",
    ],
    "structural_integrity": [
        "A covenant unenforced is a promise to no one",
        "The rule that lives only on paper dies in every transaction",
    ],
}

def cluster_anomalies(anomaly_list, eps=0.85, min_samples=2):
    """
    Cluster anomalies by embedding similarity.
    anomaly_list: list of dicts with 'text' and 'felt_domain'
    Returns list of clusters (lists of anomaly dicts)
    """
    if len(anomaly_list) < 2:
        return []
    texts = [a['text'] for a in anomaly_list]
    embs = TFIDF.fit_transform(texts).toarray()
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
    frame_choice = {
        "agency": "causal",
        "legibility": "privative",
        "moral": "possessive",
        "collective": "equative",
        "temporal": "causal",
        "safety": "warning",
        "witness": "paradox",
        "structural_integrity": "possessive"
    }
    frame_name = frame_choice.get(opposition_type, "equative")
    frame = FRAMES[frame_name]
    return frame.format(noun1=images[0], noun2=images[1])

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
    Generate proverb candidates from a cluster of anomalies.
    Uses domain-specific templates first, then falls back to frame generation.
    Returns dict with text, source anomalies, metadata.
    """
    if len(cluster) < 2:
        return None

    # Collect domains
    domains = [a.get('felt_domain', 'general') for a in cluster]
    primary_domain = max(set(domains), key=domains.count)

    # Try domain templates first
    templates = DOMAIN_TEMPLATES.get(primary_domain, [])
    if templates:
        # Pick template based on cluster size hash for determinism
        idx = len(cluster) % len(templates)
        candidate = templates[idx]
    else:
        # Fallback to frame generation
        core = extract_core_contradiction(cluster)
        images = extract_concrete_images(core)
        candidate = select_frame(images, primary_domain)

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