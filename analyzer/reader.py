"""Robust CSV loading for messy sales data."""

import pandas as pd


def read_sales(path: str) -> pd.DataFrame:
    """Read the sales CSV at ``path`` into a DataFrame.

    Handles encoding explicitly, trying each in turn:

    1. UTF-8 — the expected default.
    2. Windows-1252 (cp1252) — what most Windows/Excel exports actually use;
       a plain Latin-1 fallback would silently mangle its curly quotes and
       em-dashes (0x80-0x9F byte range) instead of raising, so it has to be
       tried explicitly rather than treated as equivalent to Latin-1.
    3. Latin-1 — the final fallback. Unlike cp1252 (which has a handful of
       undefined byte values), Latin-1 maps every possible byte to a
       character, so this step never raises.

    Returns the raw DataFrame as-is — no cleaning or validation happens
    here.
    """
    for encoding in ("utf-8", "cp1252"):
        try:
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(path, encoding="latin-1")
