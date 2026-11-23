from pathlib import Path

import pandas as pd
import pytest
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "processed" / "ecommerce.db"
SQL_PATH = BASE_DIR / "sql" / "02_business_queries.sql"


@pytest.fixture(scope="module")
def db_conn():
    assert DB_PATH.exists(), f"No se encontró {DB_PATH}. Ejecuta clean_data.py primero."
    conn = sqlite3.connect(DB_PATH)
    yield conn
    conn.close()


def test_sql_file_exists():
    assert SQL_PATH.exists(), f"No se encontró {SQL_PATH}."


def test_queries_execute_without_error(db_conn):
    """Ejecuta cada bloque SQL del archivo y verifica que no fallen."""
    with open(SQL_PATH, "r", encoding="utf-8") as f:
        raw_sql = f.read()

    bloques = [b.strip() for b in raw_sql.split(";") if b.strip()]

    for idx, block in enumerate(bloques, start=1):
        # Quitar líneas de comentario para ejecutar solo SQL
        sql_query = "\n".join(
            line for line in block.splitlines() if not line.strip().startswith("--")
        ).strip()

        if not sql_query:
            continue

        df_result = pd.read_sql_query(sql_query, db_conn)
        assert df_result is not None, f"La consulta {idx} retornó None."
        assert len(df_result) > 0, f"La consulta {idx} no retornó filas."
