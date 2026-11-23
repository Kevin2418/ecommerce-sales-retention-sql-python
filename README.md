## E-Commerce Sales, Shipping & Customer Analysis (Python + SQL)

## Business Problem
Analyze transactional retail order data (`Sample - Superstore`, 9,994 records) to evaluate revenue, profit margins, shipping performance by fulfillment mode, customer order frequency, and month-over-month sales trends.

##  Tech Stack
* **Python:** `pandas`, `sqlite3`, `pathlib`
* **Database:** SQLite (`data/processed/ecommerce.db`)
* **SQL:** Aggregations, `GROUP BY`, `CTEs` (`WITH`), `LAG()` window functions, `NULLIF`

##  Project Structure
```text
├── data/
│   ├── raw/
│   │   └── superstore_raw.csv
│   └── processed/
│       ├── superstore_clean.csv
│       └── ecommerce.db
├── notebooks/
├── reports/
├── sql/
│   ├── 01_schema_setup.sql
│   └── 02_business_queries.sql
├── clean_data.py
├── run_queries.py
├── requirements.txt
└── README.md