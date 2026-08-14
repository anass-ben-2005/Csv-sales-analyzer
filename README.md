# csv-sales-analyzer

A command-line tool that ingests messy sales CSV files, validates and cleans
the rows, aggregates them into revenue summaries (by product, by month, by
region), and writes a report as Markdown and JSON. Pure Python, no external
services.

## Status

🚧 Work in progress — see [plan.md](./plan.md) for the build plan.

## Usage

```bash
pip install -r requirements.txt
python cli.py analyze --input sample_data/messy_sales.csv --out reports/
```

This produces `reports/report.md` and `reports/report.json`.

## Project layout

```
csv-sales-analyzer/
├── analyzer/
│   ├── reader.py       # robust CSV loading
│   ├── validator.py    # row-level validation + cleaning
│   ├── aggregator.py   # group-by summaries
│   └── reporter.py     # Markdown + JSON output
├── tests/
├── sample_data/
│   └── messy_sales.csv
├── cli.py              # click entry point
└── requirements.txt
```
