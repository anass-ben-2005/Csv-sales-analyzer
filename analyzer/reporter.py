"""Markdown and JSON report generation."""

import json
from pathlib import Path

import pandas as pd


def _table_to_markdown(df: pd.DataFrame) -> str:
    """Render a DataFrame as a Markdown table without extra dependencies."""
    if df.empty:
        return "_(no data)_"
    headers = list(df.columns)
    rows = [
        "| " + " | ".join(str(value) for value in row) + " |"
        for row in df.itertuples(index=False)
    ]
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
            *rows,
        ]
    )


def to_markdown(summaries: dict[str, pd.DataFrame]) -> str:
    """Render all summary tables as a single Markdown report."""
    sections = ["# Sales Report"]
    for name, df in summaries.items():
        title = name.replace("_", " ").title()
        sections.append(f"## {title}\n\n{_table_to_markdown(df)}")
    return "\n\n".join(sections) + "\n"


def to_json(summaries: dict[str, pd.DataFrame]) -> str:
    """Render all summary tables as a single JSON document."""
    payload = {name: df.to_dict(orient="records") for name, df in summaries.items()}
    return json.dumps(payload, indent=2, default=str)


def write_report(summaries: dict[str, pd.DataFrame], out_dir: str) -> None:
    """Write both the Markdown and JSON report into ``out_dir``."""
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    (out_path / "report.md").write_text(to_markdown(summaries), encoding="utf-8")
    (out_path / "report.json").write_text(to_json(summaries), encoding="utf-8")
