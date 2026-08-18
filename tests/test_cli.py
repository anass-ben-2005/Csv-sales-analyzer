"""Smoke tests for the CLI."""

from click.testing import CliRunner

from cli import analyze


def test_analyze_writes_report(tmp_path):
    input_csv = tmp_path / "sales.csv"
    input_csv.write_text(
        "order_id,order_date,product,region,amount\n"
        "ORD001,2026-01-05,Widget A,North,100.00\n"
        "ORD002,2026-01-10,Widget B,South,50.00\n",
        encoding="utf-8",
    )
    out_dir = tmp_path / "reports"

    runner = CliRunner()
    result = runner.invoke(analyze, ["--input", str(input_csv), "--out", str(out_dir)])

    assert result.exit_code == 0
    assert (out_dir / "report.md").exists()
    assert (out_dir / "report.json").exists()


def test_analyze_handles_all_rows_filtered_out(tmp_path):
    """Every row is invalid (bad date, negative amount) — nothing survives
    validation, so every aggregate group is empty. The CLI should still
    finish cleanly rather than crash.
    """
    input_csv = tmp_path / "all_invalid.csv"
    input_csv.write_text(
        "order_id,order_date,product,region,amount\n"
        "ORD001,not-a-date,Widget A,North,-10.00\n",
        encoding="utf-8",
    )
    out_dir = tmp_path / "reports"

    runner = CliRunner()
    result = runner.invoke(analyze, ["--input", str(input_csv), "--out", str(out_dir)])

    assert result.exit_code == 0
    assert (out_dir / "report.md").exists()
