"""Utilities for parsing raw report text into structured data."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

ITEM_PATTERN = re.compile(r"^\s*([\w\u4e00-\u9fa5()（）]+)[:：]\s*([\w.+\-/%]+)")
DATE_PATTERN = re.compile(r"(20\d{2}[年\-/\.](?:1[0-2]|0?[1-9])[月\-/\.](?:[12][0-9]|3[01]|0?[1-9])日?)")


@dataclass(slots=True)
class ReportRecord:
    person_id: str
    collected_at: Optional[datetime]
    metrics: Dict[str, float]
    source_path: Path
    raw_text: str = field(repr=False)


def _parse_person_and_date(stem: str) -> Tuple[str, Optional[datetime]]:
    parts = stem.split("_", 1)
    person_id = parts[0]
    collected_at: Optional[datetime] = None

    if len(parts) == 2:
        for fmt in ("%Y%m%d", "%Y-%m-%d", "%Y.%m.%d", "%Y%m", "%Y-%m", "%Y.%m"):
            try:
                collected_at = datetime.strptime(parts[1], fmt)
                break
            except ValueError:
                continue

    return person_id, collected_at


def _parse_metrics(text: str) -> Dict[str, float]:
    metrics: Dict[str, float] = {}
    for line in text.splitlines():
        match = ITEM_PATTERN.search(line)
        if not match:
            continue
        key, value = match.groups()
        try:
            metrics[key] = float(value)
        except ValueError:
            continue
    return metrics


def parse_report(stem: str, text: str, *, source_path: Path) -> ReportRecord:
    """Parse a raw text report into a :class:`ReportRecord`."""

    person_id, collected_at = _parse_person_and_date(stem)
    if collected_at is None:
        match = DATE_PATTERN.search(text)
        if match:
            cleaned = (
                match.group(1)
                .replace("年", "-")
                .replace("月", "-")
                .replace("日", "")
                .replace(".", "-")
                .replace("/", "-")
            )
            try:
                collected_at = datetime.strptime(cleaned, "%Y-%m-%d")
            except ValueError:
                pass

    metrics = _parse_metrics(text)

    return ReportRecord(
        person_id=person_id,
        collected_at=collected_at,
        metrics=metrics,
        source_path=source_path,
        raw_text=text,
    )
