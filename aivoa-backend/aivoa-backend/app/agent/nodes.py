from app.agent.state import ComplaintGraphState
from app.services.groq_client import call_json, call_text

FIELD_LIST = [
    "complaintSource", "customerName", "productName", "productStrengthGrade",
    "batchLotNumber", "manufacturingDate", "expiryDate", "quantityAffected",
    "complaintType", "complaintDate", "complaintDescription",
    "initialSeverity", "priority",
]


def extract_fields(state: ComplaintGraphState) -> ComplaintGraphState:
    """Pull the structured fields out of raw complaint text/email/PDF text."""
    system = (
        "You extract structured pharmaceutical complaint data from free text. "
        "Return ONLY a JSON object with these exact keys: "
        f"{FIELD_LIST}. Use empty string for any field you cannot find. "
        "Dates must be YYYY-MM-DD."
    )
    result = call_json(prompt=state["raw_text"], system=system)
    fields = {k: result.get(k, "") for k in FIELD_LIST}
    return {"fields": fields}


def check_completeness(state: ComplaintGraphState) -> ComplaintGraphState:
    """Bonus feature: Complaint Completeness Checker."""
    fields = state["fields"]
    missing = [k for k, v in fields.items() if not v]
    score = round(100 * (len(fields) - len(missing)) / len(fields))
    return {"completeness": {"score": score, "missing_fields": missing}}


def classify_risk(state: ComplaintGraphState) -> ComplaintGraphState:
    """Bonus feature: AI Risk Classification."""
    system = (
        "You are a pharmaceutical quality assurance risk classifier. "
        "Given complaint details, return ONLY a JSON object: "
        '{"level": "Low"|"Medium"|"High"|"Critical", "rationale": "one sentence"}. '
        "Base severity on patient safety impact, not just wording."
    )
    result = call_json(prompt=str(state["fields"]), system=system)
    return {"risk": result}


def detect_duplicates(state: ComplaintGraphState) -> ComplaintGraphState:
    """Bonus feature: Duplicate Complaint Detection. Compares against a
    supplied list of existing complaint descriptions (e.g. from Postgres)."""
    existing = state.get("existing_complaints") or []
    if not existing:
        return {"duplicate_check": {"is_duplicate": False, "matches": []}}

    system = (
        "You check if a new complaint duplicates any existing complaint. "
        'Return ONLY JSON: {"is_duplicate": bool, "matches": [indices]}. '
        "Match on same product + batch + same underlying issue, not just similar wording."
    )
    prompt = (
        f"New complaint: {state['fields'].get('complaintDescription', '')}\n\n"
        f"Existing complaints (indexed): {list(enumerate(existing))}"
    )
    result = call_json(prompt=prompt, system=system)
    return {"duplicate_check": result}


def recommend_root_cause(state: ComplaintGraphState) -> ComplaintGraphState:
    """Bonus feature: Root Cause Recommendation."""
    system = (
        "You are a pharma QA investigator. Suggest the most likely root cause "
        "category (e.g. manufacturing deviation, packaging defect, cold-chain "
        "excursion, labeling error, counterfeit risk) in 1-2 sentences."
    )
    text = call_text(prompt=str(state["fields"]), system=system)
    return {"root_cause_suggestion": text}


def recommend_capa(state: ComplaintGraphState) -> ComplaintGraphState:
    """Bonus feature: CAPA Recommendation (Corrective and Preventive Action)."""
    system = (
        "You are a pharma QA investigator. Given the complaint and its likely "
        "root cause, suggest a brief CAPA (Corrective and Preventive Action) "
        "in 2-3 sentences."
    )
    prompt = f"Complaint: {state['fields']}\nRoot cause: {state.get('root_cause_suggestion', '')}"
    text = call_text(prompt=prompt, system=system)
    return {"capa_suggestion": text}


def summarize_complaint(state: ComplaintGraphState) -> ComplaintGraphState:
    """Bonus feature: Complaint Summary — short human-readable recap."""
    system = "Summarize this pharmaceutical complaint in 2 sentences for a QA reviewer."
    text = call_text(prompt=str(state["fields"]), system=system)
    return {"summary": text}
