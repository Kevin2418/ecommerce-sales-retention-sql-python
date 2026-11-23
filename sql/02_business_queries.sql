-- 1. Ventas, ganancia y margen promedio por categoría y subcategoría
SELECT
    category,
    sub_category,
    COUNT(*) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(profit_margin) * 100, 2) AS avg_profit_margin_pct
FROM orders
GROUP BY category, sub_category
ORDER BY total_sales DESC;

-- 2. Tiempos de envío promedio y ganancia según modo de envío
SELECT
    ship_mode,
    COUNT(*) AS total_orders,
    ROUND(AVG(shipping_days), 2) AS avg_shipping_days,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM orders
GROUP BY ship_mode
ORDER BY avg_shipping_days ASC;

-- 3. Top 10 clientes por ingresos generados (con recurrencia de pedidos)
SELECT
    customer_id,
    customer_name,
    segment,
    COUNT(DISTINCT order_id) AS distinct_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM orders
GROUP BY customer_id, customer_name, segment
ORDER BY total_sales DESC
LIMIT 10;

-- 4. Crecimiento mensual de ventas usando CTE y función de ventana LAG()
WITH monthly_sales AS (
    SELECT
        strftime('%Y-%m', order_date) AS year_month,
        ROUND(SUM(sales), 2) AS monthly_revenue
    FROM orders
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT
    year_month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (ORDER BY year_month) AS prev_month_revenue,
    ROUND(
        ((monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY year_month))
         / NULLIF(LAG(monthly_revenue) OVER (ORDER BY year_month), 0)) * 100,
        2
    ) AS mom_growth_pct
FROM monthly_sales
ORDER BY year_month;
