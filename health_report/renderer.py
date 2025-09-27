"""HTML rendering helpers."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .aggregator import PersonAnalysis


def _format_history(history):
    return [
        {
            "date": collected_at or "未提供",
            "value": value if value is not None else "-",
        }
        for collected_at, value in history
    ]


def _build_environment(template_path: Path) -> Environment:
    loader = FileSystemLoader(template_path.parent)
    return Environment(loader=loader, autoescape=select_autoescape(["html", "xml"]))


def render_html(person: PersonAnalysis, sections: Dict[str, str], *, template_path: Path) -> str:
    env = _build_environment(template_path)
    template = env.get_template(template_path.name)

    metric_rows = []
    for name, trend in person.metric_trends.items():
        metric_rows.append(
            {
                "name": name,
                "latest_value": trend.latest_value,
                "change": trend.change,
                "direction": trend.direction,
                "history": _format_history(trend.history),
            }
        )

    return template.render(
        person_id=person.person_id,
        metric_rows=metric_rows,
        sections=sections,
    )


def write_html(output_dir: Path, filename: str, content: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / filename
    target.write_text(content, encoding="utf-8")
    return target
