import sqlite3
from pathlib import Path

import pandas as pd
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
CLEAN_CSV = PROCESSED_DIR / "superstore_clean.csv"
DB_PATH = PROCESSED_DIR / "ecommerce.db"


@pytest.fixture(scope="module")
def clean_df():
    """Carga el CSV limpio generado por clean_data.py."""
    assert (
        CLEAN_CSV.exists()
    ), f"No se encontró {CLEAN_CSV}. Ejecuta clean_data.py primero."
    return pd.read_csv(CLEAN_CSV)


@pytest.fixture(scope="module")
def db_conn():
    """Conexión a la base de datos SQLite."""
    assert DB_PATH.exists(), f"No se encontró {DB_PATH}. Ejecuta clean_data.py primero."
    conn = sqlite3.connect(DB_PATH)
    yield conn
    conn.close()


def test_clean_csv_exists():
    assert CLEAN_CSV.exists(), "El CSV limpio no fue generado."


def test_database_exists():
    assert DB_PATH.exists(), "La base de datos SQLite no fue generada."


def test_no_duplicate_rows(clean_df):
    duplicados = clean_df.duplicated().sum()
    assert duplicados == 0, f"Se encontraron {duplicados} filas duplicadas."


def test_required_columns_exist(clean_df):
    columnas_requeridas = [
        "order_id",
        "order_date",
        "ship_date",
        "sales",
        "profit",
        "shipping_days",
        "profit_margin",
    ]
    for col in columnas_requeridas:
        assert col in clean_df.columns, f"Falta la columna '{col}'."


def test_dates_are_datetime(clean_df):
    order_dates = pd.to_datetime(clean_df["order_date"])
    ship_dates = pd.to_datetime(clean_df["ship_date"])
    assert pd.api.types.is_datetime64_any_dtype(order_dates)
    assert pd.api.types.is_datetime64_any_dtype(ship_dates)


def test_profit_margin_calculated(clean_df):
    assert "profit_margin" in clean_df.columns
    assert clean_df["profit_margin"].notna().all()


def test_table_exists_in_db(db_conn):
    cursor = db_conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='orders'"
    )
    resultado = cursor.fetchone()
    assert resultado is not None, "La tabla 'orders' no existe en la base de datos."


def test_orders_table_not_empty(db_conn):
    df = pd.read_sql_query("SELECT COUNT(*) AS total FROM orders", db_conn)
    assert df["total"].iloc[0] > 0, "La tabla 'orders' está vacía."
