"""Row-level validation and cleaning for sales data."""

import pandas as pd

# Known incoming date formats, tried in order. Explicit formats are used
# instead of pandas's format inference (e.g. `format="mixed"`) because that
# inference is not stable across pandas versions — it has been observed to
# mis-parse even unambiguous ISO dates depending on the installed version.
_DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%b %d %Y")


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise ``order_date`` into real datetimes.

    Input dates arrive in several formats (``2026-01-05``, ``05/01/2026``,
    ``Jan 6 2026``). Each known format is tried in turn against whatever
    hasn't parsed yet, so mixing formats within one column works. Rows
    whose date still can't be parsed by any known format are dropped.
    """
    df = df.copy()
    raw = df["order_date"].astype(str)
    parsed = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns]")

    for fmt in _DATE_FORMATS:
        unparsed = parsed.isna()
        attempt = pd.to_datetime(raw[unparsed], format=fmt, errors="coerce")
        parsed.loc[attempt.index] = attempt

    df["order_date"] = parsed
    return df.dropna(subset=["order_date"])


def clean_amounts(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce ``amount`` to numeric and drop null/negative rows.

    Strips common formatting noise first — surrounding whitespace and
    thousands-separator commas (e.g. ``"1,234.50"``) — so values exported
    from spreadsheets coerce cleanly instead of being dropped as invalid.
    """
    df = df.copy()
    cleaned = df["amount"].astype(str).str.strip().str.replace(",", "", regex=False)
    df["amount"] = pd.to_numeric(cleaned, errors="coerce")
    df = df.dropna(subset=["amount"])
    return df[df["amount"] >= 0]


def normalise_region(df: pd.DataFrame) -> pd.DataFrame:
    """Title-case ``region`` so casing variants collapse into one group."""
    df = df.copy()
    df["region"] = df["region"].str.strip().str.title()
    return df


def validate(df: pd.DataFrame) -> pd.DataFrame:
    """Run date parsing, amount cleaning, and region normalisation."""
    df = parse_dates(df)
    df = clean_amounts(df)
    df = normalise_region(df)
    return df
