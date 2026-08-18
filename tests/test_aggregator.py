"""Tests for analyzer.aggregator."""

import pandas as pd

from analyzer.aggregator import revenue_by_month, revenue_by_product, revenue_by_region


def test_revenue_by_product_sums_and_sorts() -> None:
    df = pd.DataFrame(
        {
            "product": ["Widget A", "Widget B", "Widget A", "Widget B", "Widget B"],
            "amount": [100.0, 50.0, 25.0, 50.0, 10.0],
        }
    )

    result = revenue_by_product(df)

    assert list(result.columns) == ["product", "total"]
    assert list(result["product"]) == ["Widget A", "Widget B"]
    assert list(result["total"]) == [125.0, 110.0]


def test_revenue_by_month_groups_by_calendar_month() -> None:
    df = pd.DataFrame(
        {
            "order_date": pd.to_datetime(
                ["2026-01-05", "2026-01-15", "2026-02-01", "2026-02-20"]
            ),
            "amount": [100.0, 50.0, 75.0, 25.0],
        }
    )

    result = revenue_by_month(df)

    assert list(result.columns) == ["month", "total"]
    assert list(result["month"]) == ["2026-01", "2026-02"]
    assert list(result["total"]) == [150.0, 100.0]


def test_revenue_by_region_collapses_casing() -> None:
    df = pd.DataFrame(
        {
            "region": ["North", "north", "NORTH", "South"],
            "amount": [100.0, 50.0, 25.0, 40.0],
        }
    )

    result = revenue_by_region(df)

    assert list(result.columns) == ["region", "total"]
    assert set(result["region"]) == {"North", "South"}
    assert float(result.loc[result["region"] == "North", "total"].iloc[0]) == 175.0
