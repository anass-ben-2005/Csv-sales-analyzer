# Project B — `csv-sales-analyzer`

> **Build spec for an AI coding agent.** Self-contained. Build the project exactly
> as described, committing in the specified order so the git history and CI run
> history carry realistic learning telemetry (commit spacing, break→fix cycles,
> recurring error types). The commit/CI *history* is a first-class deliverable.
>
> This is the second of two projects. It is deliberately a **different domain and
> different bug set** from Project A (`weather-etl-pipeline`) so the two resulting
> learner profiles don't look copy-pasted. Same *rhythm* (~7 red / green-fix
> cycles), different *errors*.

---

## 1. Purpose

A command-line tool that ingests **messy sales CSV files**, validates rows,
aggregates them into summaries (revenue per product, per month, per region), and
writes a report as Markdown and JSON. Pure Python, no external services.

The messy-CSV angle gives natural, realistic bugs (bad dates, wrong group grain,
empty-group division, encoding issues) — which is exactly the kind of error
recurrence the telemetry pipeline reads.

---

## 2. Tech stack

| Concern | Choice | Notes |
|---|---|---|
| Language | Python 3.11+ | |
| Data | `pandas` | |
| CLI | `click` | different from Project A's argparse, on purpose |
| Tests | `pytest` | |
| Lint | `ruff` | |
| CI | GitHub Actions | must actually run on push |
| Input | local CSV in `sample_data/` | no network at all |

---

## 3. Final file structure

```
csv-sales-analyzer/
├── .github/
│   └── workflows/
│       └── ci.yml
├── analyzer/
│   ├── __init__.py
│   ├── reader.py       # robust CSV loading
│   ├── validator.py    # row-level validation + cleaning
│   ├── aggregator.py   # group-by summaries
│   └── reporter.py     # Markdown + JSON output
├── tests/
│   ├── __init__.py
│   ├── test_reader.py
│   ├── test_validator.py
│   └── test_aggregator.py
├── sample_data/
│   └── messy_sales.csv
├── cli.py              # click entry point
├── requirements.txt
├── ruff.toml
├── .gitignore
└── README.md
```

---

## 4. The sample data (`sample_data/messy_sales.csv`)

Deliberately messy so validation has real work to do. Include:
- mixed date formats (`2026-01-05`, `05/01/2026`, `Jan 6 2026`)
- a couple of rows with empty `amount`
- one row with a negative `amount`
- inconsistent region casing (`North`, `north`, `NORTH`)
- a non-UTF-8 character somewhere (e.g. an accented name) to force an encoding
  decision

Columns: `order_id, order_date, product, region, amount`

Aim for ~25–30 rows so aggregation produces non-trivial groups.

---

## 5. What each module does

**`analyzer/reader.py`**
- `read_sales(path: str) -> pd.DataFrame` — read the CSV. Handle encoding
  explicitly (try `utf-8`, fall back to `latin-1`). Return raw DataFrame, no
  cleaning yet.

**`analyzer/validator.py`**
- `parse_dates(df) -> pd.DataFrame` — normalise the mixed `order_date` formats to
  real datetimes; drop or flag unparseable ones.
- `clean_amounts(df) -> pd.DataFrame` — coerce `amount` to numeric, drop rows with
  null or negative amounts.
- `normalise_region(df) -> pd.DataFrame` — title-case region so `north`/`NORTH`
  collapse to `North`.
- `validate(df) -> pd.DataFrame` — run all three, return the clean frame.

**`analyzer/aggregator.py`**
- `revenue_by_product(df) -> pd.DataFrame`
- `revenue_by_month(df) -> pd.DataFrame` — group by year-month of `order_date`.
- `revenue_by_region(df) -> pd.DataFrame`
- Each returns a tidy summary with a `total` column.

**`analyzer/reporter.py`**
- `to_markdown(summaries: dict) -> str`
- `to_json(summaries: dict) -> str`
- `write_report(summaries, out_dir)` — write both files.

**`cli.py`**
- `click` command: `analyze --input sample_data/messy_sales.csv --out reports/`.
- Wire reader → validator → aggregator → reporter. Print a one-line summary.

---

## 6. The commit sequence — build in THIS order

Same principle as Project A: **push failing commits as failing.** Different bugs,
so this learner's V5/V6 error signature differs from Project A's.

| # | Commit message | Intended CI result | What to actually do |
|---|---|---|---|
| 1 | `chore: project skeleton and README` | *(no CI yet)* | dirs, `__init__.py`, README stub, `.gitignore` (ignore `reports/`, `__pycache__`, `.venv`) |
| 2 | `data: add messy sample sales CSV` | *(no CI yet)* | the `sample_data/messy_sales.csv` described in §4 |
| 3 | `feat: robust CSV reader` | *(no CI yet)* | `reader.py` with encoding fallback; `requirements.txt` (pandas, click, pytest, ruff) |
| 4 | `chore: add GitHub Actions CI` | **FAIL** | `ci.yml` runs pytest — no tests yet → red |
| 5 | `test: validator tests` | **FAIL** | `test_validator.py` against functions that don't exist yet → import error |
| 6 | `feat: date parsing in validator` | **FAIL** | write `parse_dates` but it only handles ISO dates; the `05/01/2026` and `Jan 6 2026` rows fail the test |
| 7 | `fix: handle mixed date formats` | **PASS** | use a tolerant parser (e.g. `pd.to_datetime(..., errors="coerce")` + format fallback) → **first cycle** |
| 8 | `feat: amount cleaning` | **PASS** | `clean_amounts` + tests |
| 9 | `feat: revenue by product` | **PASS** | `aggregator.revenue_by_product` + test |
| 10 | `feat: revenue by month` | **FAIL** | group by full `order_date` instead of year-month → wrong grain, one row per day → test expecting monthly totals fails (deliberate grain bug — echoes the benchmark's `subtly_wrong.py`) |
| 11 | `fix: group by year-month not full date` | **PASS** | second cycle |
| 12 | `feat: revenue by region` | **FAIL** | forget to normalise region first → `north` and `North` counted separately → test fails |
| 13 | `fix: normalise region before grouping` | **PASS** | third cycle |
| 14 | `feat: markdown + json reporter` | **PASS** | `reporter.py` + test |
| 15 | `feat: click CLI` | **FAIL** | division-by-zero / empty-group crash when a filter yields no rows → CLI smoke test fails |
| 16 | `fix: guard empty groups in reporter` | **PASS** | fourth cycle |
| 17 | `test: encoding edge case` | **FAIL** | test loads a latin-1 row; reader still hardcodes utf-8 → `UnicodeDecodeError` |
| 18 | `fix: encoding fallback in reader` | **PASS** | fifth cycle |
| 19 | `refactor: type hints and docstrings` | **PASS** | annotations/docs only |
| 20 | `chore: pin dependencies and tidy README` | **PASS** | pin versions; final green |

Result: ~6–7 red commits each followed by a green fix. Distinct error *types* from
Project A — a date-format bug, a groupby-grain bug, a normalisation-order bug, an
empty-group crash, an encoding bug — so the two profiles read as two different
learners.

---

## 7. Spacing the commits (do NOT skip)

Spread across **~6 days**, a few per day. Backdate if committing in one sitting:
```bash
GIT_AUTHOR_DATE="2026-08-04T14:00:00" GIT_COMMITTER_DATE="2026-08-04T14:00:00" \
  git commit -m "chore: project skeleton and README"
```
Use a **different date window from Project A** (e.g. if A ran Aug 4–9, run B Aug
6–12, overlapping is fine) so the two learners have distinct but realistic
timelines.

| Commits | Day |
|---|---|
| 1–3 | Day 1 |
| 4–7 | Day 2 |
| 8–11 | Day 3 |
| 12–14 | Day 4 |
| 15–17 | Day 5 |
| 18–20 | Day 6 |

Push per day (or per commit) so each push is its own CI run.

---

## 8. `ci.yml` (reference)

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: ruff check .
      - run: pytest -q
```

---

## 9. Definition of done

- 20 commits, in the order above, spread across ~6 days.
- GitHub Actions history shows the intended red/green pattern.
- Final `HEAD` is green: `pytest -q` and `ruff check .` both pass.
- Running `python cli.py analyze --input sample_data/messy_sales.csv --out reports/`
  produces `reports/report.md` and `reports/report.json`.
- Repo is public.

---

## 10. One honesty note

Same as Project A: this is real self-generated telemetry, not a fabricated
observed student. Frame any write-up accordingly — the pipeline is demonstrated on
genuine data you produced, which is a legitimate demo.
