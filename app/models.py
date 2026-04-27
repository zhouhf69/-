from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal


SourceType = Literal["his", "paste", "ocr", "document", "manual"]
LevelType = Literal["info", "warning", "high"]


@dataclass
class PatientFact:
    key: str
    value: Any
    source: SourceType = "manual"
    timestamp: datetime | None = None


@dataclass
class CaseInput:
    patient_id: str
    encounter_id: str | None = None
    department: str | None = None
    facts: list[PatientFact] = field(default_factory=list)
    raw_text: str | None = None


@dataclass
class TriggeredItem:
    id: str
    title: str
    level: LevelType
    rationale: str
    recommendation: str
    evidence: list[str] = field(default_factory=list)


@dataclass
class EvaluationResponse:
    patient_id: str
    encounter_id: str | None = None
    summary: str = ""
    triggered: list[TriggeredItem] = field(default_factory=list)
    scores: dict[str, float] = field(default_factory=dict)
