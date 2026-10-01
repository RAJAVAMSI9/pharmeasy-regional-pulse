import sqlite3
import pandas as pd
import json

conn = sqlite3.connect('pharmeasy.db')

result = pd.read_sql("""
SELECT region, substr(order_date, 1, 7) as month, SUM(sales_inr) as total_sales
FROM orders_clean
GROUP BY region, month
ORDER BY region, month
""", conn)

sales_dict = {}

for index, row in result.iterrows():
    region = row['region']
    month = row['month']
    sales = row['total_sales']

    if region not in sales_dict:
        sales_dict[region] = {}

    sales_dict[region][month] = sales

def compute_percentage_change_v1(current, previous):
    if previous == 0:
        return 0
    return (current - previous) / previous * 100

apr_may = {}
may_jun = {}

for region in sales_dict:
    apr = sales_dict[region].get('2026-04', 0)
    may = sales_dict[region].get('2026-05', 0)
    jun = sales_dict[region].get('2026-06', 0)

    apr_may[region] = round(compute_percentage_change_v1(may, apr), 2)
    may_jun[region] = round(compute_percentage_change_v1(jun, may), 2)

print(apr_may)
print(may_jun)

print(apr_may['Guntur'])
print(apr_may['Nellore'])

#TASK 2.4 FLAG SIGNIFICANT REGIONS
def flag_significant_regions_v1(changes, threshold=8):
    flagged = []
    for region in changes:
        if abs(changes[region]) > threshold:
            flagged.append(region)
    return flagged

flagged_apr_may = flag_significant_regions_v1(apr_may)
flagged_may_jun = flag_significant_regions_v1(may_jun)

print(flagged_apr_may)
print(flagged_may_jun)

def save_state_v1(month_summary, path):
    with open(path, 'w') as f:
        json.dump(month_summary, f)

def load_previous_state_v1(path):
    with open(path) as f:
        return json.load(f)

april_summary = {region: sales_dict[region].get('2026-04', 0) for region in sales_dict}

save_state_v1(april_summary, 'april_summary.json')

reloaded = load_previous_state_v1('april_summary.json')

print(reloaded == april_summary)
