"""Integration with large language models for narrative sections."""
from __future__ import annotations

import json
import os
import textwrap
from dataclasses import dataclass
from typing import Dict, Optional, Protocol

import requests

from .aggregator import PersonAnalysis

SECTION_KEYS = {
    "data_sources": "数据来源",
    "risk_assessment": "风险评估",
    "health_interpretation": "健康解读",
    "intervention": "干预建议",
    "follow_up": "随访计划",
    "evidence": "依据说明",
    "hotline": "24小时热线电话",
    "consult_line": "健康咨询电话",
    "disclaimer": "免责声明",
}


class LLMClient(Protocol):
    def generate_sections(self, person: PersonAnalysis) -> Dict[str, str]:
        ...


@dataclass(slots=True)
class DashScopeClient:
    """Simple client for the Aliyun DashScope (通义千问) API."""

    api_key: str
    model: str = "qwen-plus"

    def generate_sections(self, person: PersonAnalysis) -> Dict[str, str]:
        prompt = _build_prompt(person)
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一名资深健康管理师，需要基于结构化检测数据生成中文健康报告。",
                },
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_object"},
        }
        response = requests.post(
            "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=120,
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        return {
            key: parsed.get(key) or parsed.get(SECTION_KEYS[key], "")
            for key in SECTION_KEYS
        }


@dataclass(slots=True)
class FallbackClient:
    """Rule-based fallback used when no API key is provided."""

    hotline: str
    consult_line: str

    def generate_sections(self, person: PersonAnalysis) -> Dict[str, str]:
        metric_lines = []
        for name, trend in person.metric_trends.items():
            metric_lines.append(
                f"{name}: 最新值 {trend.latest_value if trend.latest_value is not None else '未知'},"
                f" 趋势 {trend.direction}"
            )
        joined_metrics = "\n".join(metric_lines) or "暂无结构化指标"

        return {
            "data_sources": "、".join(
                sorted({record.source_path.name for record in person.records})
            ),
            "risk_assessment": "基于已解析指标进行了初步风险评估，建议结合医生意见。",
            "health_interpretation": f"关键指标概览:\n{joined_metrics}",
            "intervention": "保持健康生活方式，均衡饮食、适度运动，并根据医生建议服药。",
            "follow_up": "建议定期复查，若指标持续异常请联系专业医生。",
            "evidence": "分析依据为历史体检数据及通用健康管理原则。",
            "hotline": self.hotline,
            "consult_line": self.consult_line,
            "disclaimer": "此报告为自动生成，仅供参考，不能替代专业医疗诊断。",
        }


def build_client(*, provider: Optional[str], model: Optional[str], hotline: str, consult_line: str) -> LLMClient:
    provider = (provider or "").lower()
    if provider in {"dashscope", "qwen"}:
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            raise RuntimeError("DASHSCOPE_API_KEY environment variable is required for DashScope integration.")
        return DashScopeClient(api_key=api_key, model=model or "qwen-plus")

    # Future providers can be added here (e.g. ZhiPuAI)
    return FallbackClient(hotline=hotline, consult_line=consult_line)


def _build_prompt(person: PersonAnalysis) -> str:
    metric_descriptions = []
    for trend in person.metric_trends.values():
        history_lines = []
        for collected_at, value in trend.history:
            history_lines.append(f"- {collected_at or '未知日期'}: {value}")
        metric_descriptions.append(
            textwrap.dedent(
                f"""
                指标名称: {trend.name}
                最新值: {trend.latest_value}
                与上一期差值: {trend.change}
                趋势判断: {trend.direction}
                历史数据:\n{os.linesep.join(history_lines)}
                """
            ).strip()
        )

    history_summary = "\n\n".join(metric_descriptions) or "暂无结构化指标"
    raw_concat = "\n\n".join(record.raw_text for record in person.records)

    instructions = textwrap.dedent(
        """
        请根据提供的体检指标趋势和原始文本，总结一份面向普通人的健康分析报告。
        输出 JSON 对象，字段需包含：
        - data_sources
        - risk_assessment
        - health_interpretation
        - intervention
        - follow_up
        - evidence
        - hotline
        - consult_line
        - disclaimer
        hotline 字段应使用输入中给出的热线电话，consult_line 字段应使用健康咨询电话。
        其余字段请返回中文长文本，兼顾科学性与可读性。
        """
    ).strip()

    return (
        f"{instructions}\n\n"
        f"【体检指标趋势】\n{history_summary}\n\n"
        f"【原始体检文本】\n{raw_concat}"
    )
