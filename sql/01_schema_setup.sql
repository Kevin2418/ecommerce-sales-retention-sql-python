import pandas as pd
import sqlite3

# 1. Cargar dataset (encoding 'latin1' evita errores de caracteres especiales en Superstore)
df = pd.read_csv('data/raw/superstore_raw.csv', encoding='latin1')

# 2. Estandarizar nombres de columnas (minúsculas y guiones bajos para SQL)
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(' ', '_')
    .str.replace('-', '_')
)

# 3. Revisar y eliminar duplicados exactos
print(f"Filas iniciales: {len(df)}")
df = df.drop_duplicates()

# 4. Convertir fechas al formato estándar YYYY-MM-DD
df['order_date'] = pd.to_datetime(df['order_date'])
df['ship_date'] = pd.to_datetime(df['ship_date'])

# 5. Crear métricas derivadas útiles para negocio
df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days
df['profit_margin'] = (df['profit'] / df['sales']).round(4)

# 6. Guardar CSV limpio en data/processed/
df.to_csv('data/processed/superstore_clean.csv', index=False)

# 7. Exportar a base de datos SQLite para ejecutar consultas SQL
conn = sqlite3.connect('data/processed/ecommerce.db')
df.to_sql('orders', conn, if_exists='replace', index=False)
conn.close()

print("¡Limpieza completada y tabla 'orders' cargada en SQLite!")
