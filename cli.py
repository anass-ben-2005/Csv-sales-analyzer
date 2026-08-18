"""Command-line entry point for csv-sales-analyzer."""

import click

from analyzer.aggregator import revenue_by_month, revenue_by_product, revenue_by_region
from analyzer.reader import read_sales
from analyzer.reporter import summary_line, write_report
from analyzer.validator import validate


@click.group()
def main() -> None:
    """csv-sales-analyzer command-line tool."""


@main.command()
@click.option(
    "--input",
    "input_path",
    required=True,
    type=click.Path(exists=True),
    help="Path to the input sales CSV.",
)
@click.option(
    "--out",
    "out_dir",
    required=True,
    type=click.Path(),
    help="Directory to write the report into.",
)
def analyze(input_path: str, out_dir: str) -> None:
    """Analyze a messy sales CSV and write a Markdown + JSON revenue report."""
    df = read_sales(input_path)
    df = validate(df)

    summaries = {
        "revenue_by_product": revenue_by_product(df),
        "revenue_by_month": revenue_by_month(df),
        "revenue_by_region": revenue_by_region(df),
    }

    write_report(summaries, out_dir)
    click.echo(summary_line(summaries))


if __name__ == "__main__":
    main()
