from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
)

def generate_embedding(text: str) -> list:
    response = client.embeddings.create(
        model="openai/text-embedding-3-small",  # via OpenRouter
        input=text
    )
    return response.data[0].embedding

def serialize_embedding(embedding: list) -> str:
    return json.dumps(embedding)

def deserialize_embedding(embedding_str: str) -> list:
    return json.loads(embedding_str)
