# Plan — `csv-sales-analyzer`

Source spec: [`PROJECT_B_csv-sales-analyzer.md`](./PROJECT_B_csv-sales-analyzer.md)

This file is the working checklist for building the project. Work through the
steps **in order, one at a time**. After each step is finished and verified,
I will give you the exact `git add` / `git commit` command(s) to run — you run
them yourself. I will not run `git add`, `git commit`, or `git push` at any
point in this project.

---

## 0. Ground rules

- **Order matters.** Build in the exact commit sequence in §2 below — it's
  designed to produce a realistic red→green CI history, not just working code.
- **Push failing commits as failing.** Steps marked `FAIL` are *meant* to
  break CI when pushed. Don't "fix it while I'm at it" — the fix is its own
  later commit.
- **One commit = one step.** Don't bundle two rows of the table into one
  commit, and don't split one row across two commits.
- **You control git.** I will prepare/edit files for a step and tell you it's
  ready. You review, then run the `git add` / `git commit` line I give you
  (plain commands, no `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` — see note in
  §3). I never commit or push on my own.
- **README stays professional throughout.** After each step, the README is
  kept up to date and polished — badges, clear usage, project structure —
  the way a real company project would maintain it, not left as a stub.
- **No network calls anywhere in the code.** All data is local, in
  `sample_data/`.
- **Pure Python 3.11+, pandas, click, pytest, ruff** — no other frameworks.
- **Spread commits across ~6 days** per the schedule in §3, using backdated
  `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE` if building in one sitting.
- **Repo must end up public** on GitHub (your action, when you're ready).
- **Definition of done** (final state, see §6) must hold at the last commit:
  `pytest -q` and `ruff check .` both pass, and running the CLI produces
  `reports/report.md` and `reports/report.json`.

---

## 1. Final file structure

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

## 2. Step-by-step build order (20 commits)

Each row = one step = one commit. `Intended CI result` is what the push
**should** show — don't chase green on the `FAIL` rows, that's the point.

| # | Step | Commit message | Intended CI result |
|---|------|-----------------|---------------------|
| 1 | Create dirs, `__init__.py` files, README stub, `.gitignore` (ignore `reports/`, `__pycache__`, `.venv`) | `chore: project skeleton and README` | *(no CI yet)* |
| 2 | Add the messy `sample_data/messy_sales.csv` (see §4) | `data: add messy sample sales CSV` | *(no CI yet)* |
| 3 | Write `reader.py` with encoding fallback (utf-8 → latin-1); add `requirements.txt` (pandas, click, pytest, ruff) | `feat: robust CSV reader` | *(no CI yet)* |
| 4 | Add `.github/workflows/ci.yml` (runs ruff + pytest) — no tests exist yet | `chore: add GitHub Actions CI` | **FAIL** |
| 5 | Write `test_validator.py` against `validator.py` functions that don't exist yet | `test: validator tests` | **FAIL** (import error) |
| 6 | Implement `parse_dates` but only handle ISO (`YYYY-MM-DD`) dates — the `05/01/2026` / `Jan 6 2026` rows fail | `feat: date parsing in validator` | **FAIL** |
| 7 | Fix `parse_dates` with a tolerant parser (`pd.to_datetime(..., errors="coerce")` + format fallback) | `fix: handle mixed date formats` | **PASS** — 1st red→green cycle |
| 8 | Implement `clean_amounts` + tests | `feat: amount cleaning` | **PASS** |
| 9 | Implement `aggregator.revenue_by_product` + test | `feat: revenue by product` | **PASS** |
| 10 | Implement `revenue_by_month`, but group by the *full* `order_date` instead of year-month (wrong grain — one row per day) | `feat: revenue by month` | **FAIL** |
| 11 | Fix: group by year-month, not full date | `fix: group by year-month not full date` | **PASS** — 2nd cycle |
| 12 | Implement `revenue_by_region`, but forget to normalise region first (`north`/`North`/`NORTH` counted separately) | `feat: revenue by region` | **FAIL** |
| 13 | Fix: call `normalise_region` before grouping | `fix: normalise region before grouping` | **PASS** — 3rd cycle |
| 14 | Implement `reporter.py` (`to_markdown`, `to_json`, `write_report`) + test | `feat: markdown + json reporter` | **PASS** |
| 15 | Implement `cli.py` (click command wiring reader → validator → aggregator → reporter); CLI smoke test crashes on an empty-group / division-by-zero case | `feat: click CLI` | **FAIL** |
| 16 | Fix: guard empty groups in reporter | `fix: guard empty groups in reporter` | **PASS** — 4th cycle |
| 17 | Add a test that loads a latin-1-encoded row; reader still hardcodes utf-8 → `UnicodeDecodeError` | `test: encoding edge case` | **FAIL** |
| 18 | Fix: proper encoding fallback in `reader.py` | `fix: encoding fallback in reader` | **PASS** — 5th cycle |
| 19 | Add type hints and docstrings across all modules (no behavior change) | `refactor: type hints and docstrings` | **PASS** |
| 20 | Pin exact versions in `requirements.txt`, tidy up README | `chore: pin dependencies and tidy README` | **PASS** — final green |

Result: ~5–6 red commits, each immediately followed by a green fix. Five
distinct bug *types*, one per cycle: date-format parsing, groupby grain,
normalisation ordering, empty-group crash, encoding fallback.

---

## 3. Commit spacing (do not skip)

Spread the 20 commits across **~6 days**. The original idea was to backdate
with `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE` when building in one sitting —
**that's no longer how commands are given here.** Per your instruction, I now
give plain `git add` / `git commit` lines with no date env vars. If you still
want the backdated/spread-out history described below, add the env vars
yourself when you run the commit; otherwise commits will simply land on
today's actual date.

```bash
# optional, if you want to backdate it yourself:
GIT_AUTHOR_DATE="2026-08-06T14:00:00" GIT_COMMITTER_DATE="2026-08-06T14:00:00" \
  git commit -m "chore: project skeleton and README"
```

Use a date window distinct from (but may overlap) Project A's — e.g. Project A
ran Aug 4–9, so run this one **Aug 6–12**.

| Steps | Day |
|---|---|
| 1–3 | Day 1 (2026-08-06) |
| 4–7 | Day 2 (2026-08-07) |
| 8–11 | Day 3 (2026-08-08) |
| 12–14 | Day 4 (2026-08-09) |
| 15–17 | Day 5 (2026-08-10) |
| 18–20 | Day 6 (2026-08-11 or -12) |

Push per day (or per commit) so each push produces its own CI run.

---

## 4. Sample data rules (`sample_data/messy_sales.csv`)

Columns: `order_id, order_date, product, region, amount`

Must include, deliberately:
- mixed date formats: `2026-01-05`, `05/01/2026`, `Jan 6 2026`
- a couple of rows with empty `amount`
- one row with a negative `amount`
- inconsistent region casing: `North`, `north`, `NORTH`
- a non-UTF-8 character somewhere (e.g. an accented name) to force an
  encoding decision

Target ~25–30 rows total so aggregation produces non-trivial groups.

---

## 5. Module responsibilities

**`analyzer/reader.py`**
- `read_sales(path: str) -> pd.DataFrame` — read CSV, try `utf-8` then fall
  back to `latin-1`. Return the raw DataFrame, no cleaning.

**`analyzer/validator.py`**
- `parse_dates(df) -> pd.DataFrame` — normalise mixed `order_date` formats to
  real datetimes; drop or flag unparseable ones.
- `clean_amounts(df) -> pd.DataFrame` — coerce `amount` to numeric, drop rows
  with null or negative amounts.
- `normalise_region(df) -> pd.DataFrame` — title-case region so
  `north`/`NORTH` collapse to `North`.
- `validate(df) -> pd.DataFrame` — run all three, return the clean frame.

**`analyzer/aggregator.py`**
- `revenue_by_product(df) -> pd.DataFrame`
- `revenue_by_month(df) -> pd.DataFrame` — group by year-month of
  `order_date`.
- `revenue_by_region(df) -> pd.DataFrame`
- Each returns a tidy summary with a `total` column.

**`analyzer/reporter.py`**
- `to_markdown(summaries: dict) -> str`
- `to_json(summaries: dict) -> str`
- `write_report(summaries, out_dir)` — writes both files.

**`cli.py`**
- click command: `analyze --input sample_data/messy_sales.csv --out reports/`
- wires reader → validator → aggregator → reporter, prints a one-line
  summary.

---

## 6. `ci.yml` reference

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

## 7. Definition of done

- [ ] 20 commits, in the order in §2, spread across ~6 days.
- [ ] GitHub Actions history shows the intended red/green pattern.
- [ ] Final `HEAD` is green: `pytest -q` and `ruff check .` both pass.
- [ ] `python cli.py analyze --input sample_data/messy_sales.csv --out reports/`
      produces `reports/report.md` and `reports/report.json`.
- [ ] Repo is public.

---

## 7b. Unplanned hotfixes (deviations from the 20-step plan)

Real bugs that surfaced from actually running CI, on top of the intentionally
staged red/green cycles in §2. These are genuine mistakes, not scripted ones,
so they get their own honest commit rather than being folded silently into a
planned step.

- **At step 14** (`feat: markdown + json reporter`): the spec's file-structure
  list (§1) only names `test_reader.py`/`test_validator.py`/`test_aggregator.py`,
  but the commit table explicitly calls for reporter tests. Added
  `tests/test_reporter.py` rather than skip coverage to match the listing
  literally — real test coverage takes priority over an exact file list.
- **After step 7** (`fix: handle mixed date formats`): that commit passed
  locally but **failed in real CI**. Root cause: `requirements.txt` is
  unpinned, and CI installed pandas 3.0.5 (vs. 2.2.3 cached locally); pandas
  3.0's `format="mixed"` + `dayfirst=True` inference changed behavior and
  started mis-parsing even the unambiguous ISO date. Fixed by parsing each
  known date format explicitly in turn instead of relying on pandas's format
  inference — deterministic across pandas versions. Verified locally against
  both pandas 2.2.3 and 3.0.5 before committing.

## 8. Progress tracker

Check off as each step is completed and committed (by you).

- [x] 1. chore: project skeleton and README
- [x] 2. data: add messy sample sales CSV
- [x] 3. feat: robust CSV reader
- [x] 4. chore: add GitHub Actions CI
- [x] 5. test: validator tests
- [x] 6. feat: date parsing in validator
- [x] 7. fix: handle mixed date formats
- [x] 8. feat: amount cleaning
- [x] 9. feat: revenue by product
- [x] 10. feat: revenue by month
- [x] 11. fix: group by year-month not full date
- [x] 12. feat: revenue by region
- [x] 13. fix: normalise region before grouping
- [x] 14. feat: markdown + json reporter
- [x] 15. feat: click CLI
- [x] 16. fix: guard empty groups in reporter
- [ ] 17. test: encoding edge case
- [ ] 18. fix: encoding fallback in reader
- [ ] 19. refactor: type hints and docstrings
- [ ] 20. chore: pin dependencies and tidy README

---

## 9. Honesty note

This is real, self-generated build telemetry — not a fabricated "observed
student." The red/green pattern above is intentional and disclosed, not
staged to deceive; frame any write-up of this repo accordingly.
