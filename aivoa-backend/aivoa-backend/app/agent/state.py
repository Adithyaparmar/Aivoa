from typing import TypedDict, Optional


class ComplaintGraphState(TypedDict, total=False):
    # Input
    raw_text: str

    # Node: extract_fields
    fields: dict

    # Node: check_completeness
    completeness: dict  # { score: int, missing_fields: [str] }

    # Node: classify_risk
    risk: dict  # { level: str, rationale: str }

    # Bonus branches — only populated if those nodes run
    duplicate_check: Optional[dict]
    root_cause_suggestion: Optional[str]
    capa_suggestion: Optional[str]
    summary: Optional[str]

    # Existing complaints text corpus, used only by duplicate-detection node
    existing_complaints: Optional[list]
