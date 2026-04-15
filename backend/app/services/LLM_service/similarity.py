import numpy as np
from .embeddings import deserialize_embedding

SIMILARITY_THRESHOLD = 0.85
LOOKBACK_LIMIT = 50


def cosine_similarity(a: list, b: list) -> float:
    a = np.array(a)
    b = np.array(b)
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def find_similar(new_embedding: list, db) -> object | None:
    from app.models import Objection  # avoid circular import

    records = (
        db.query(Objection)
        .order_by(Objection.created_at.desc())
        .limit(LOOKBACK_LIMIT)
        .all()
    )

    for record in records:
        if record.embedding is None:
            continue
        stored_emb = deserialize_embedding(record.embedding)
        sim = cosine_similarity(new_embedding, stored_emb)
        if sim >= SIMILARITY_THRESHOLD:
            return record

    return None
