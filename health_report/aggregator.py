"""Aggregate multiple records into longitudinal trend information."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from .parser import ReportRecord


@dataclass(slots=True)
class MetricTrend:
    name: str
    latest_value: Optional[float]
    change: Optional[float]
    direction: str
    history: List[Tuple[Optional[str], Optional[float]]]


@dataclass(slots=True)
class PersonAnalysis:
    person_id: str
    metric_trends: Dict[str, MetricTrend]
    records: Sequence[ReportRecord]


def _sort_records(records: Sequence[ReportRecord]) -> List[ReportRecord]:
    return sorted(
        records,
        key=lambda r: (r.collected_at or r.source_path.stat().st_mtime, r.source_path.name),
    )


def _format_date(record: ReportRecord) -> Optional[str]:
    if record.collected_at:
        return record.collected_at.strftime("%Y-%m-%d")
    return None


def analyze_person(records: Sequence[ReportRecord]) -> PersonAnalysis:
    if not records:
        raise ValueError("No records provided for analysis")

    sorted_records = _sort_records(records)
    person_id = sorted_records[0].person_id

    metric_history: Dict[str, List[Tuple[Optional[str], Optional[float]]]] = {}

    for record in sorted_records:
        date_str = _format_date(record)
        for metric, value in record.metrics.items():
            metric_history.setdefault(metric, []).append((date_str, value))

    metric_trends: Dict[str, MetricTrend] = {}
    for metric, history in metric_history.items():
        latest_value = history[-1][1]
        prev_value = history[-2][1] if len(history) > 1 else None
        change = None
        direction = "无变化"
        if latest_value is not None and prev_value is not None:
            change = latest_value - prev_value
            if change > 0:
                direction = "上升"
            elif change < 0:
                direction = "下降"
            else:
                direction = "持平"

        metric_trends[metric] = MetricTrend(
            name=metric,
            latest_value=latest_value,
            change=change,
            direction=direction,
            history=history,
        )

    return PersonAnalysis(
        person_id=person_id,
        metric_trends=metric_trends,
        records=sorted_records,
    )
