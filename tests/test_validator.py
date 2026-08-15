"""Tests for analyzer.validator."""

import pandas as pd

from analyzer.validator import clean_amounts, normalise_region, parse_dates, validate


def test_parse_dates_handles_mixed_formats():
    df = pd.DataFrame({"order_date": ["2026-01-05", "05/01/2026", "Jan 6 2026"]})

    result = parse_dates(df)

    assert pd.api.types.is_datetime64_any_dtype(result["order_date"])
    assert result["order_date"].notna().all()
    assert list(result["order_date"].dt.month) == [1, 1, 1]
    assert list(result["order_date"].dt.day) == [5, 5, 6]


def test_clean_amounts_drops_null_and_negative():
    df = pd.DataFrame({"amount": ["120.50", "", "-50.00", "89.99"]})

    result = clean_amounts(df)

    assert len(result) == 2
    assert set(result["amount"]) == {120.50, 89.99}
    assert (result["amount"] >= 0).all()


def test_clean_amounts_handles_formatting_noise():
    df = pd.DataFrame({"amount": ["1,234.50", "  99.99  ", "2,000"]})

    result = clean_amounts(df)

    assert list(result["amount"]) == [1234.50, 99.99, 2000.0]


def test_normalise_region_collapses_casing():
    df = pd.DataFrame({"region": ["North", "north", "NORTH", "south"]})

    result = normalise_region(df)

    assert set(result["region"]) == {"North", "South"}


def test_validate_returns_clean_frame():
    df = pd.DataFrame(
        {
            "order_id": ["ORD001", "ORD002", "ORD003"],
            "order_date": ["2026-01-05", "05/01/2026", "Jan 6 2026"],
            "product": ["Widget A", "Widget B", "Gadget Pro"],
            "region": ["North", "north", "SOUTH"],
            "amount": ["120.50", "-10.00", "89.99"],
        }
    )

    result = validate(df)

    assert len(result) == 2  # the negative-amount row is dropped
    assert pd.api.types.is_datetime64_any_dtype(result["order_date"])
    assert set(result["region"]) == {"North", "South"}
