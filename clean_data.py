"""
clean_data.py -- PharmEasy Regional Pulse: cleaning pipeline (Task 1.2)
                  + schema validation (Task 1.3)

Full annotated version: includes every inspection step, not just the
working logic, so this file also works as a learning reference.
"""
import pandas as pd

# ---------- load raw data ----------
df = pd.read_csv('pharmeasy_orders_raw.csv')

# df -> shows the actual table (in Colab this displays it directly)
print("First 3 raw rows:\n", df.head(3))

# df.shape -> (rows, columns)
print("Raw shape:", df.shape)

# len(df) -> just the row count
print("Raw row count:", len(df))

# ---------- Task 1.2, Step 1: remove exact duplicates ----------

# df.duplicated().sum() -> counts rows that are exact copies of an earlier row
print("Duplicate rows found:", df.duplicated().sum())

# df.duplicated(keep='first') -> True/False per row
# keep='first' = first occurrence is NOT a duplicate (False),
#                every repeat after it IS a duplicate (True)

# dupe -> the actual duplicate rows themselves (excluding the originals)
dupe = df[df.duplicated(keep='first')]
print("Sample of duplicate rows:\n", dupe.head(3))
print("Count of duplicate rows:", len(dupe))

# drop_duplicates() removes those duplicate rows, keeps the first occurrence of each
remove_dupe = df.drop_duplicates().copy()
print("Rows after removing duplicates:", len(remove_dupe))
print("Type of remove_dupe:", type(remove_dupe))

# ---------- Task 1.2, Step 2: normalize region spelling ----------

# .unique() -> lists every DISTINCT spelling currently in the region column
print("Region spellings before fix:", remove_dupe['region'].unique())

# .nunique() -> counts how many distinct spellings exist
print("Distinct region spellings before fix:", remove_dupe['region'].nunique())

# strip() removes extra leading/trailing spaces
# title() fixes casing, e.g. 'HYDERABAD ' -> 'Hyderabad'
remove_dupe['region'] = remove_dupe['region'].str.strip().str.title()

print("Distinct regions after fix:", remove_dupe['region'].nunique())

# ---------- Task 1.2, Step 3: impute missing category ----------

# see the actual rows with blank category, before fixing anything
print("Sample rows with missing category:\n", remove_dupe[remove_dupe['category'].isna()].head(3))
print("Missing category before fix:", remove_dupe['category'].isna().sum())

# see the actual rows with blank profit too, while we're here
print("Sample rows with missing profit:\n", remove_dupe[remove_dupe['profit_inr'].isna()].head(3))
print("Missing profit before fix:", remove_dupe['profit_inr'].isna().sum())

# notna() = opposite of isna() -> True where category HAS a value
# filtering with it keeps only the rows we can trust to build a lookup from
has_category = remove_dupe[remove_dupe['category'].notna()]
print("Rows with category filled in:", len(has_category))

# drop_duplicates('product') keeps just 1 row per product
# (a lookup only needs 1 example per product, not every repeat)
unique_products = has_category.drop_duplicates('product')
print("Unique products found:", len(unique_products))

# zip pairs up product with its category, one by one
# dict() turns those pairs into a lookup: {product: category}
lookup = dict(zip(unique_products['product'], unique_products['category']))
print("Sample of the lookup dictionary:", dict(list(lookup.items())[:3]))

# fillna() only fills the BLANK cells, using the lookup based on product name
# existing (non-blank) values are left untouched
remove_dupe['category'] = remove_dupe['category'].fillna(remove_dupe['product'].map(lookup))

print("Missing category after fix:", remove_dupe['category'].isna().sum())
print("All categories now:", remove_dupe['category'].unique())

# ---------- Task 1.2, Step 4: impute missing profit_inr ----------

# keep only rows where profit is filled in -> use these to learn typical margins
has_profit = remove_dupe[remove_dupe['profit_inr'].notna()].copy()
print("Rows with profit filled in:", len(has_profit))

# margin = what fraction of sales became profit (e.g. 0.15 = 15%)
has_profit['margin'] = has_profit['profit_inr'] / has_profit['sales_inr']

# groupby('category') splits rows into 6 groups (one per category)
# .mean() gives the average margin within each group -> this IS our lookup
avg_margin = has_profit.groupby('category')['margin'].mean()
print("Average margin per category:\n", avg_margin)

# map each row's category to its average margin (like using a lookup table)
category_margin = remove_dupe['category'].map(avg_margin)
print("Sample of mapped margins:\n", category_margin.head(3))

# fillna() fills blank profit_inr cells as: sales_inr * that row's category margin
# existing (non-blank) profit values are left untouched
remove_dupe['profit_inr'] = remove_dupe['profit_inr'].fillna(remove_dupe['sales_inr'] * category_margin)

print("Missing profit after fix:", remove_dupe['profit_inr'].isna().sum())

# ---------- Task 1.2, Step 5: save cleaned data ----------
print("Final row count:", len(remove_dupe))
print("Final region count:", remove_dupe['region'].nunique())
print("Final missing-value check (all columns):\n", remove_dupe.isna().sum())

remove_dupe.to_csv('orders_clean.csv', index=False)
print("Saved orders_clean.csv, total rows:", len(remove_dupe))

# ---------- Task 1.3: schema validation ----------
def validate_schema(df, required_columns):
    # check which required columns are NOT present
    missing = [column for column in required_columns if column not in df.columns]
    # if nothing's missing -> validated. if something's missing -> blocked
    status = "blocked_schema" if missing else "validated"
    return {"status": status, "row_count": len(df), "missing_columns": missing}

REQUIRED_COLUMNS = [
    "order_id", "order_date", "region", "category", "product",
    "quantity", "sales_inr", "profit_inr",
]

# test 1: valid data -> should say "validated"
print("validate_schema (clean data):",
      validate_schema(remove_dupe, REQUIRED_COLUMNS))

# test 2: broken data (missing column) -> should say "blocked_schema"
broken = remove_dupe.drop(columns=['profit_inr'])
print("validate_schema (broken copy, profit_inr dropped):",
      validate_schema(broken, REQUIRED_COLUMNS))
