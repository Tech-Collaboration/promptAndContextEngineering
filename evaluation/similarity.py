from sentence_transformers import SentenceTransformer
import numpy as np

_model = SentenceTransformer("all-MiniLM-L6-v2")

def cosine_sim(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def semantic_similarity(a: str, b: str) -> float:
    va = _model.encode(a, normalize_embeddings=True)
    vb = _model.encode(b, normalize_embeddings=True)
    return cosine_sim(va, vb)
