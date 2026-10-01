import pandas as pd #upload orders_clean.csv & regions_master.csv begin
check = pd.read_csv('orders_clean.csv')
print(len(check))

regions = pd.read_csv('regions_master.csv')
print(len(regions))

import sqlite3

conn = sqlite3.connect('pharmeasy.db')

# to_sql() writes a pandas table into the database as a new SQL table
# 'orders_clean' -> name the table will have inside the database
# conn -> which database file to write into (pharmeasy.db)
# if_exists='replace' -> if this table already exists, overwrite it (avoids duplicate data on re-runs)
# index=False -> don't save pandas' internal row numbers as an extra column
check.to_sql('orders_clean', conn, if_exists='replace', index=False)
regions.to_sql('regions_master', conn, if_exists='replace', index=False)

print(pd.read_sql("SELECT COUNT(*) FROM orders_clean", conn))
print(pd.read_sql("SELECT COUNT(*) FROM regions_master", conn))
