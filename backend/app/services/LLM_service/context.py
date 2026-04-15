PRODUCT_CONTEXT = "AI-driven B2B SaaS platform improving sales efficiency and business outcomes."

KEYWORD_CONTEXT = {
    "price":      "Our platform delivers strong ROI — most clients recover costs within 90 days.",
    "expensive":  "Our platform delivers strong ROI — most clients recover costs within 90 days.",
    "cost":       "Our platform delivers strong ROI — most clients recover costs within 90 days.",
    "competitor": "We offer deeper integrations and dedicated onboarding unlike most alternatives.",
    "switch":     "Migration is handled fully by our team with zero downtime guaranteed.",
    "tool":       "Migration is handled fully by our team with zero downtime guaranteed.",
    "trust":      "We serve enterprise clients with SOC2 compliance and proven track records.",
    "security":   "We serve enterprise clients with SOC2 compliance and proven track records.",
    "time":       "Setup takes under a week — our onboarding team handles everything end-to-end.",
    "busy":       "Setup takes under a week — our onboarding team handles everything end-to-end.",
    "later":      "Early adopters get priority support and locked-in pricing — timing matters.",
}


def get_context(objection: str) -> str:
    objection_lower = objection.lower()
    for keyword, context in KEYWORD_CONTEXT.items():
        if keyword in objection_lower:
            return context
    return PRODUCT_CONTEXT
