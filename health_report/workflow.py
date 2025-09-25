"""High level orchestration for the health report workflow."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from . import aggregator, ingestion, llm, parser, renderer
from .config import AppConfig


class Workflow:
    def __init__(self, config: AppConfig):
        self.config = config
        self.client = llm.build_client(
            provider=config.ai_provider,
            model=config.ai_model,
            hotline=config.hotline,
            consult_line=config.consult_line,
        )

    def run(self) -> Dict[str, Path]:
        self.config.ensure_directories()

        report_files = list(self.config.iter_report_files(ingestion.SUPPORTED_SUFFIXES))
        loaded = ingestion.load_many(report_files)

        grouped: Dict[str, List[parser.ReportRecord]] = defaultdict(list)
        for stem, (text, source_path) in loaded.items():
            record = parser.parse_report(stem, text, source_path=source_path)
            grouped[record.person_id].append(record)

        outputs: Dict[str, Path] = {}
        for person_id, records in grouped.items():
            person_analysis = aggregator.analyze_person(records)
            sections = self.client.generate_sections(person_analysis)
            sections.setdefault("hotline", self.config.hotline)
            sections.setdefault("consult_line", self.config.consult_line)
            html = renderer.render_html(
                person_analysis,
                sections,
                template_path=self.config.template_path,
            )
            filename = f"{person_id}_analysis.html"
            target = renderer.write_html(self.config.output_dir, filename, html)
            outputs[person_id] = target

        return outputs
