# Reliability Checklist - Guntur Memo

## 1. Safety check
No personally identifiable customer data appears anywhere in the memo or the dashboard - only region-level aggregates (SUM of sales_inr per region/month) are used.

## 2. Validation
Every number tagged [HIGH] in memo.md was cross-checked by re-running the SQL queries against pharmeasy.db and confirming the printed output matches the memo exactly (Rs 62442.27, Rs 138738.93, +122.19%).

## 3. Critique / refine
An early draft implied Guntur's spike was caused by a promotion, but this was not something the data actually showed, so it was moved into the Assumptions section and clearly labeled as a guess, not a fact.

## 4. Human sign-off
The memo was passed through review_gate_v1 with an approve decision and a reviewer note, and logged in audit_log.jsonl before being treated as ready to use.
