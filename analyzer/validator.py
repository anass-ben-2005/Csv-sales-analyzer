"""Row-level validation and cleaning for sales data."""

import pandas as pd


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise ``order_date`` into real datetimes.

    Rows whose date can't be parsed are dropped.
    """
    df = df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"], format="%Y-%m-%d", errors="coerce")
    return df.dropna(subset=["order_date"])


def clean_amounts(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce ``amount`` to numeric and drop null/negative rows."""
    df = df.copy()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
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
