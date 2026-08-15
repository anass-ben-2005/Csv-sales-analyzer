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
