from pathlib import Path
import sqlite3
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

base_dir = Path(__file__).resolve().parent
db_path = base_dir / "data" / "processed" / "ecommerce.db"
sql_path = base_dir / "sql" / "02_business_queries.sql"

if not db_path.exists():
    raise FileNotFoundError(f"No se encontró {db_path}. Ejecuta primero clean_data.py")

if not sql_path.exists():
    raise FileNotFoundError(f"No se encontró {sql_path}.")

with open(sql_path, "r", encoding="utf-8") as f:
    raw_sql = f.read()

# Separar consultas por ';' y limpiar comentarios iniciales de cada bloque
blocks = [b.strip() for b in raw_sql.split(";") if b.strip()]

conn = sqlite3.connect(db_path)

try:
    for idx, block in enumerate(blocks, start=1):
        lines = block.splitlines()
        comment_lines = [
            line.lstrip("- ").strip() for line in lines if line.strip().startswith("--")
        ]
        title = comment_lines[-1] if comment_lines else f"Consulta {idx}"

        # Quitar líneas que sean solo comentarios para quedarse con el SQL ejecutable
        sql_query = "\n".join(
            line for line in lines if not line.strip().startswith("--")
        ).strip()

        if not sql_query:
            continue

        print("\n" + "=" * 75)
        print(f"RESULTADO {idx}: {title}")
        print("=" * 75)

        df_res = pd.read_sql_query(sql_query, conn)
        print(df_res.head(15))
finally:
    conn.close()
