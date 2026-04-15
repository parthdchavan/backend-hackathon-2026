def classify_objection(objection: str) -> dict:
    from .llm_client import call_llm_json

    prompt = f"""
Classify this sales objection.

Return JSON only:
{{"category":"Price|Competition|Trust|Timing|Other","severity":"Low|Medium|High"}}

Objection: {objection}
"""

    try:
        result = call_llm_json(prompt)
        # Validate keys exist
        if "category" not in result or "severity" not in result:
            raise ValueError("Missing keys")
        return result
    except Exception:
        return {"category": "Other", "severity": "Medium"}
