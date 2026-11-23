from pathlib import Path
import sqlite3
import pandas as pd

# Ruta base del proyecto (asumiendo que clean_data.py está en la raíz)
base_dir = Path(__file__).resolve().parent
raw_path = base_dir / "data" / "raw" / "superstore_raw.csv"
processed_dir = base_dir / "data" / "processed"
processed_dir.mkdir(parents=True, exist_ok=True)

# 1. Cargar dataset
df = pd.read_csv(raw_path, encoding="latin1")

# 2. Estandarizar nombres de columnas
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
    .str.replace("-", "_", regex=False)
)

# 3. Eliminar duplicados exactos
print(f"Filas iniciales: {len(df)}")
df = df.drop_duplicates()
print(f"Filas después de quitar duplicados: {len(df)}")

# 4. Convertir fechas
df["order_date"] = pd.to_datetime(df["order_date"])
df["ship_date"] = pd.to_datetime(df["ship_date"])

# 5. Crear métricas derivadas
df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days
df["profit_margin"] = (df["profit"] / df["sales"]).round(4)

# 6. Guardar CSV limpio
clean_csv_path = processed_dir / "superstore_clean.csv"
df.to_csv(clean_csv_path, index=False)

# 7. Exportar a SQLite
db_path = processed_dir / "ecommerce.db"
conn = sqlite3.connect(db_path)
df.to_sql("orders", conn, if_exists="replace", index=False)
conn.close()

print("¡Listo! Se generaron superstore_clean.csv y ecommerce.db en data/processed/")
