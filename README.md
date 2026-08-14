# csv-sales-analyzer

![CI](https://github.com/YOUR_GITHUB_USERNAME/csv-sales-analyzer/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)

A command-line tool for turning messy, real-world sales CSV exports into
clean revenue reports. It validates and normalizes inconsistent input data,
then aggregates it into summaries by **product**, **month**, and **region**,
exporting the result as both Markdown and JSON. Pure Python — no external
services, no network calls.

---

## Table of contents

- [Why this exists](#why-this-exists)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project structure](#project-structure)
- [How it works](#how-it-works)
- [Development](#development)
- [Testing](#testing)
- [Roadmap](#roadmap)

---

## Why this exists

Sales exports from CRMs, POS systems, and spreadsheets are rarely clean:
dates come in three different formats, amounts get typo'd or left blank,
region names are cased inconsistently, and encoding issues creep in from
copy-pasted names. `csv-sales-analyzer` handles that mess automatically so
you can go from a raw export to a trustworthy revenue report in one command.

## Features

- **Encoding-safe ingestion** — reads UTF-8 by default, falls back to
  Latin-1 automatically if the file isn't valid UTF-8.
- **Tolerant date parsing** — normalizes `2026-01-05`, `05/01/2026`, and
  `Jan 6 2026`-style dates into a single consistent format.
- **Amount cleaning** — coerces amounts to numeric and drops invalid rows
  (missing or negative values).
- **Region normalization** — collapses casing variants like `north`,
  `NORTH`, and `North` into one canonical group.
- **Multi-dimensional aggregation** — revenue totals by product, by
  calendar month, and by region.
- **Dual-format reporting** — writes both a human-readable Markdown report
  and a machine-readable JSON report.

## Installation

Requires Python 3.11+.

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/csv-sales-analyzer.git
cd csv-sales-analyzer
pip install -r requirements.txt
```

## Usage

```bash
python cli.py analyze --input sample_data/messy_sales.csv --out reports/
```

This reads the input CSV, validates and cleans it, aggregates revenue, and
writes:

- `reports/report.md` — a Markdown summary
- `reports/report.json` — the same summary as structured JSON

The CLI prints a one-line summary to the console when it finishes.

## Project structure

```
csv-sales-analyzer/
├── .github/workflows/ci.yml   # GitHub Actions: lint + test on every push
├── analyzer/
│   ├── reader.py               # robust CSV loading (encoding fallback)
│   ├── validator.py            # row-level validation + cleaning
│   ├── aggregator.py           # group-by revenue summaries
│   └── reporter.py             # Markdown + JSON report generation
├── tests/                      # pytest test suite
├── sample_data/
│   └── messy_sales.csv         # intentionally messy example input
├── cli.py                      # click-based CLI entry point
├── requirements.txt
├── ruff.toml
└── plan.md                     # build plan and commit-by-commit history
```

## How it works

The pipeline is a straightforward, composable flow:

```
CSV file → reader → validator → aggregator → reporter → reports/
```

1. **`reader.read_sales`** loads the raw CSV into a DataFrame, with no
   cleaning applied yet.
2. **`validator.validate`** runs date parsing, amount cleaning, and region
   normalization, returning a clean DataFrame.
3. **`aggregator`** produces three summary tables: revenue by product, by
   month, and by region.
4. **`reporter`** renders those summaries to Markdown and JSON and writes
   them to the output directory.

## Development

```bash
pip install -r requirements.txt
ruff check .        # lint
pytest -q           # run the test suite
```

CI runs both of these on every push and pull request via GitHub Actions.

## Testing

The test suite covers the reader, validator, and aggregator modules,
including edge cases drawn directly from the messy sample data: mixed date
formats, missing/negative amounts, inconsistent region casing, and
non-UTF-8 input.

```bash
pytest -q
```

## Roadmap

- [ ] Configurable output formats (CSV export)
- [ ] Support for multiple input files in one run
- [ ] Optional currency conversion
