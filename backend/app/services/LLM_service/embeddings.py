import json
from sentence_transformers import SentenceTransformer

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def generate_embedding(text: str) -> list:
    model = get_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()


def serialize_embedding(embedding: list) -> str:
    return json.dumps(embedding)


def deserialize_embedding(embedding_str: str) -> list:
    return json.loads(embedding_str)
