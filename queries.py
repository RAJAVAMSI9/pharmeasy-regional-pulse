import sqlite3
import pandas as pd

conn = sqlite3.connect('pharmeasy.db')

#LEFT JOIN uploaded csvs
print(pd.read_sql("""
SELECT COUNT(*) FROM regions_master r
LEFT JOIN orders_clean o ON r.region = o.region
""", conn))

#INNER JOIN
print(pd.read_sql("""
SELECT COUNT(*) FROM regions_master r
INNER JOIN orders_clean o ON r.region = o.region
""", conn))

#Duplicate order_id check
print(pd.read_sql("""
SELECT order_id, COUNT(*) as n
FROM orders_clean
GROUP BY order_id
HAVING COUNT(*) > 1
""", conn))

#NULL CHECK
print(pd.read_sql("""
SELECT r.region,
       COUNT(*) as count_star,
       COUNT(o.order_id) as count_fk
FROM regions_master r
LEFT JOIN orders_clean o ON r.region = o.region
GROUP BY r.region
""", conn))

#PER REGION QUERY
print(pd.read_sql("""
SELECT r.region, COUNT(o.order_id) as order_count
FROM regions_master r
LEFT JOIN orders_clean o ON r.region = o.region
GROUP BY r.region
ORDER BY order_count ASC
""", conn))

#TASK 2.3 REGION x MONTH METRICS
result = pd.read_sql("""
SELECT region, substr(order_date, 1, 7) as month, SUM(sales_inr) as total_sales
FROM orders_clean
GROUP BY region, month
ORDER BY region, month
""", conn)
print(result)
