"""Group-by revenue summaries."""

import pandas as pd


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
