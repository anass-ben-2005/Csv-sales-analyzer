"""Tests for analyzer.reader."""

from analyzer.reader import read_sales

_HEADER = "order_id,order_date,product,region,amount\n"


def test_read_sales_handles_windows1252_smart_quotes(tmp_path):
    """Windows-exported CSVs are commonly Windows-1252 (cp1252), not plain
    Latin-1 — cp1252 uses the 0x80-0x9F byte range for printable characters
    such as curly quotes and em-dashes, where Latin-1 maps that same range
    to control codes. A naive Latin-1-only fallback silently mangles those
    characters instead of raising, so this has to be checked by content,
    not by exception.
    """
    csv_path = tmp_path / "windows1252_sales.csv"
    row = "ORD001,2026-01-05,O’Brien Goods,North,50.00\n"
    csv_path.write_bytes((_HEADER + row).encode("cp1252"))

    df = read_sales(str(csv_path))

    assert df.loc[0, "product"] == "O’Brien Goods"
