"""Robust CSV loading for messy sales data."""

import pandas as pd


def read_sales(path: str) -> pd.DataFrame:
    """Read the sales CSV at ``path`` into a DataFrame.

    Handles encoding explicitly: tries UTF-8 first, and falls back to
    Latin-1 if the file contains bytes that aren't valid UTF-8. Returns
    the raw DataFrame as-is — no cleaning or validation happens here.
    """
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1")
