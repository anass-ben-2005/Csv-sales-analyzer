"""Tests for analyzer.reporter."""

import json

import pandas as pd

from analyzer.reporter import to_json, to_markdown, write_report


def _sample_summaries():
    return {
        "revenue_by_product": pd.DataFrame(
            {"product": ["Widget A", "Widget B"], "total": [125.0, 110.0]}
        )
    }


def test_to_markdown_includes_headers_and_rows():
    markdown = to_markdown(_sample_summaries())

    assert "# Sales Report" in markdown
    assert "Revenue By Product" in markdown
    assert "| product | total |" in markdown
    assert "Widget A" in markdown


def test_to_json_round_trips_data():
    payload = json.loads(to_json(_sample_summaries()))

    assert payload["revenue_by_product"][0]["product"] == "Widget A"
    assert payload["revenue_by_product"][0]["total"] == 125.0


def test_write_report_creates_both_files(tmp_path):
    write_report(_sample_summaries(), str(tmp_path))

    assert (tmp_path / "report.md").exists()
    assert (tmp_path / "report.json").exists()
    assert "Widget A" in (tmp_path / "report.md").read_text(encoding="utf-8")
