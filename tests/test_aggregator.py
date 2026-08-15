"""Tests for analyzer.aggregator."""

import pandas as pd

from analyzer.aggregator import revenue_by_product


def test_revenue_by_product_sums_and_sorts():
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
