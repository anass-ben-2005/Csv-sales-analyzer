"""Group-by revenue summaries."""

import pandas as pd

from analyzer.validator import normalise_region


def revenue_by_product(df: pd.DataFrame) -> pd.DataFrame:
    """Total revenue per product, highest revenue first."""
    return (
        df.groupby("product", as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "total"})
        .sort_values("total", ascending=False)
        .reset_index(drop=True)
    )


def revenue_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Total revenue per calendar month, as ``YYYY-MM``.

    Groups by year-month, not the full date — multiple orders on different
    days of the same month must land in the same bucket.
    """
    df = df.copy()
    df["month"] = df["order_date"].dt.strftime("%Y-%m")
    return (
        df.groupby("month", as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "total"})
    )


def revenue_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Total revenue per region, highest revenue first.

    Region casing is normalised before grouping — otherwise casing variants
    like ``north`` and ``NORTH`` would be counted as separate regions.
    """
    df = normalise_region(df)
    return (
        df.groupby("region", as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "total"})
        .sort_values("total", ascending=False)
        .reset_index(drop=True)
    )
