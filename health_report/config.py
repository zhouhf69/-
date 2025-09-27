"""Configuration helpers for the health report workflow."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


def _expand(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


@dataclass(slots=True)
class AppConfig:
    """Holds runtime configuration for the report generator."""

    data_dir: Path
    template_path: Path
    output_dir: Path
    hotline: str
    consult_line: str
    ai_provider: Optional[str] = None
    ai_model: Optional[str] = None

    @classmethod
    def from_args(
        cls,
        *,
        data_dir: str | Path,
        template_path: str | Path,
        output_dir: str | Path,
        hotline: str,
        consult_line: str,
        ai_provider: Optional[str] = None,
        ai_model: Optional[str] = None,
    ) -> "AppConfig":
        return cls(
            data_dir=_expand(data_dir),
            template_path=_expand(template_path),
            output_dir=_expand(output_dir),
            hotline=hotline,
            consult_line=consult_line,
            ai_provider=ai_provider,
            ai_model=ai_model,
        )

    def ensure_directories(self) -> None:
        """Create the output directory if it does not already exist."""

        self.output_dir.mkdir(parents=True, exist_ok=True)

    def iter_report_files(self, suffixes: Iterable[str] | None = None) -> Iterable[Path]:
        """Yield files in :pyattr:`data_dir` that match the provided suffixes."""

        suffixes = {s.lower() for s in suffixes} if suffixes else None
        for item in sorted(self.data_dir.iterdir()):
            if not item.is_file():
                continue
            if suffixes is None or item.suffix.lower() in suffixes:
                yield item
