# Presentation Storyline - Guntur April-May Sales Swing

## For an Executive (Situation-Complication-Resolution)

**Situation:** PharmEasy Regional Pulse tracks nine active regions monthly. Total sales across all regions were healthy this quarter, and most regions moved within a normal range month to month.

**Complication:** Guntur is the exception. Its sales more than doubled from April to May, +122.19%, the largest swing of any region this quarter, then partially pulled back -28.11% in May-June. A jump this large either signals a real opportunity or a data issue, and the aggregate number alone can't tell us which.

**Resolution:** Before adjusting Guntur's targets or budget based on this number, we recommend a manual spot-check of Guntur's May order-level detail to confirm the spike is broad-based, not one large order. This is a short check, not a delay to the rest of the review, since every other region's numbers are already verified.

## For a Regional Manager (Overview-Category-Detail)

**Overview:** Guntur's sales jumped from about Rs 62,442 to about Rs 138,739 between April and May, a 122% increase, the biggest single-region move this quarter.

**Category:** This isn't isolated to one product line based on the current region-level view. The dashboard's category breakdown for Guntur should be checked against April's mix to see whether the spike is concentrated in one category or spread across all six.

**Detail:** April total: Rs 62,442.27. May total: Rs 138,738.93. Both are SQL-verified sums from pharmeasy.db's orders_clean table, computed the same way for every region, so Guntur's figures are directly comparable to any other region on the dashboard.

## Anticipated Pushback Q&A

**Q1: Why should I believe this number?**
Acknowledgement: Fair question, a 122% jump in one month is exactly the kind of number that should be checked before anyone acts on it.
Verified vs not verified: The Rs 62,442.27 and Rs 138,738.93 totals are verified, they come from a SUM(sales_inr) GROUP BY region, month query against the cleaned, deduplicated dataset, and the duplicate-key and null-count checks confirm there's no double-counting or join error behind the number. What is not verified is why the number moved.
Resolution: A manual spot-check of a sample of May's Guntur order rows would confirm the spike is broad-based. This can be done within a day.

**Q2: What if an alternative explanation is driving this?**
Acknowledgement: Reasonable, a spike this size could come from real demand, a single large bulk order, or a promotional push not visible in this dataset.
Verified vs not verified: The duplicate-key check confirms the total is not driven by literal duplicate order_ids. The distribution of individual order sizes within Guntur's May data has not yet been checked.
Resolution: Pulling Guntur's May order list sorted by sales_inr descending would show whether a handful of unusually large orders are driving the total. This is the same spot-check named in Q1.
