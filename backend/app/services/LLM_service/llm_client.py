import os
import json
from openai import OpenAI

from .embeddings import generate_embedding, serialize_embedding
from .context import get_context
from .prompt_builder import build_prompt
from .classifier import classify_objection

from dotenv import load_dotenv

load_dotenv()

from .prompt_builder import SYSTEM_PROMPT, FEW_SHOT_EXAMPLES

client = OpenAI(
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL = os.getenv("MODEL")


def preprocess(text: str) -> str:
    return text.strip().lower()


def call_llm(prompt: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *FEW_SHOT_EXAMPLES,
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()


def call_llm_json(prompt: str) -> dict:
    messages = [
        {"role": "system", "content": "You are a JSON-only response generator. Respond with valid JSON only, no markdown or extra text."},
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=100,
    )
    raw = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def response(objection_text: str) -> dict:
    """Accept raw objection text and return LLM response metadata.

    This is the final entrypoint for POST /objectives routes.
    """
    cleaned = preprocess(objection_text)
    emb = generate_embedding(cleaned)
    context = get_context(cleaned)
    prompt = build_prompt(cleaned, context)
    response = call_llm(prompt)
    meta = classify_objection(cleaned)

    return {
        "response": response,
        "category": meta["category"],
        "severity": meta["severity"],
        "embedding": serialize_embedding(emb),
    }


if __name__ == "__main__":
    test_objection = "I don't think your product is worth the price."
    result = response(test_objection)
    print(json.dumps(result, indent=2))