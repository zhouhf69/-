from __future__ import annotations

"""简化版临床知识库：作为触发器与建议的基础。

实际生产中可替换为：
1) 指南条款库（版本化）
2) 医院本地规范库
3) 药品禁忌/相互作用库
4) 模型服务注册中心
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    level: str
    fact_key: str
    operator: str
    threshold: Any
    recommendation: str
    rationale: str
    evidence: list[str]


KNOWLEDGE_BASE_VERSION = "0.1.0"

CLINICAL_RULES: list[Rule] = [
    Rule(
        id="renal_dose_check",
        title="肾功能减退用药审查",
        level="warning",
        fact_key="eGFR",
        operator="lt",
        threshold=30,
        recommendation="建议复核经肾排泄药物剂量，必要时调整或替代。",
        rationale="eGFR < 30 ml/min/1.73m² 时，多种药物需要减量或禁用。",
        evidence=["KDIGO CKD guideline", "医院药事管理规范"],
    ),
    Rule(
        id="hypoglycemia_risk",
        title="低血糖高风险提醒",
        level="high",
        fact_key="glucose",
        operator="lt",
        threshold=3.9,
        recommendation="建议立即复测血糖并评估降糖方案，必要时进行纠正。",
        rationale="血糖低于 3.9 mmol/L 需按低血糖流程处理。",
        evidence=["ADA Standards of Care"],
    ),
    Rule(
        id="hypertension_alert",
        title="血压控制不佳提醒",
        level="info",
        fact_key="systolic_bp",
        operator="ge",
        threshold=140,
        recommendation="建议结合并发症风险评估优化降压治疗和随访频率。",
        rationale="收缩压≥140 mmHg 提示血压控制未达标（视人群分层）。",
        evidence=["中国高血压防治指南"],
    ),
]


def compare(value: Any, operator: str, threshold: Any) -> bool:
    try:
        if operator == "lt":
            return float(value) < float(threshold)
        if operator == "le":
            return float(value) <= float(threshold)
        if operator == "gt":
            return float(value) > float(threshold)
        if operator == "ge":
            return float(value) >= float(threshold)
        if operator == "eq":
            return value == threshold
    except (ValueError, TypeError):
        return False
    return False
