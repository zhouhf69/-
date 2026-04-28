from __future__ import annotations

from collections import defaultdict

from app.knowledge_base import CLINICAL_RULES, KNOWLEDGE_BASE_VERSION, compare
from app.models import CaseInput, EvaluationResponse, TriggeredItem


def _to_fact_map(case: CaseInput) -> dict[str, list]:
    facts = defaultdict(list)
    for f in case.facts:
        facts[f.key].append(f.value)
    return dict(facts)


def _compute_basic_scores(fact_map: dict[str, list]) -> dict[str, float]:
    scores: dict[str, float] = {}
    if "age" in fact_map and "systolic_bp" in fact_map:
        age = float(fact_map["age"][-1])
        sbp = float(fact_map["systolic_bp"][-1])
        scores["simple_cv_risk_index"] = round((age / 10) + (sbp / 60), 2)
    return scores


def evaluate_case(case: CaseInput) -> EvaluationResponse:
    fact_map = _to_fact_map(case)
    triggered: list[TriggeredItem] = []

    for rule in CLINICAL_RULES:
        values = fact_map.get(rule.fact_key, [])
        if not values:
            continue
        latest = values[-1]
        if compare(latest, rule.operator, rule.threshold):
            triggered.append(
                TriggeredItem(
                    id=rule.id,
                    title=rule.title,
                    level=rule.level,  # type: ignore[arg-type]
                    rationale=rule.rationale,
                    recommendation=rule.recommendation,
                    evidence=rule.evidence
                )
            )

    scores = _compute_basic_scores(fact_map)
    summary = (
        f"已基于知识库 v{KNOWLEDGE_BASE_VERSION} 完成评估，"
        f"触发 {len(triggered)} 条提醒，"
        f"计算 {len(scores)} 项评分。"
    )

    return EvaluationResponse(
        patient_id=case.patient_id,
        encounter_id=case.encounter_id,
        summary=summary,
        triggered=triggered,
        scores=scores,
    )
