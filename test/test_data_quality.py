from pathlib import Path

import pandas as pd
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_CSV = BASE_DIR / "data" / "processed" / "superstore_clean.csv"


@pytest.fixture(scope="module")
def df():
    assert CLEAN_CSV.exists(), f"No se encontró {CLEAN_CSV}."
    return pd.read_csv(CLEAN_CSV)


def test_no_null_order_id(df):
    assert "order_id" in df.columns
    assert df["order_id"].notna().all()


def test_no_null_sales(df):
    assert "sales" in df.columns
    assert df["sales"].notna().all()


def test_sales_positive(df):
    assert "sales" in df.columns
    assert (df["sales"] >= 0).all()


def test_ship_date_after_order_date(df):
    assert "order_date" in df.columns
    assert "ship_date" in df.columns
    order_dates = pd.to_datetime(df["order_date"])
    ship_dates = pd.to_datetime(df["ship_date"])
    assert (
        ship_dates >= order_dates
    ).all(), "Hay fechas de envío anteriores a la fecha de orden."
