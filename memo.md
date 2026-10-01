# Guntur's +122.19% April-May Sales Swing
## Context
PharmEasy Regional Pulse tracks nine active regions monthly. [LOW] In April 2026, Guntur recorded total sales of Rs 62442.27. [HIGH]
## Key Insight
Guntur's sales rose to Rs 138738.93 in May 2026, a Month-on-Month increase of +122.19%, the largest swing of any region in either transition this quarter. [HIGH]
## Evidence
- April 2026 Guntur sales: Rs 62442.27, computed via SUM(sales_inr) GROUP BY region, month against pharmeasy.db. [HIGH]
- May 2026 Guntur sales: Rs 138738.93, same query. [HIGH]
- compute_percentage_change_v1(138738.93, 62442.27) = +122.19%. [HIGH]
- flag_significant_regions_v1() with threshold=8 flags Guntur in April-May, alongside 6 other regions (7 of 9 that month). [HIGH]
- Guntur's swing partially reverses in May-June (-28.11%), consistent with a spike-then-pullback pattern. [HIGH]
## Recommendation
Before treating May's number as the new normal for Guntur, manually spot-check a sample of Guntur's May order rows to confirm the spike is broad-based, not one large anomalous order. [MEDIUM]
## Next Check
Re-run this pipeline against Guntur's July data once available. [LOW] If sales settle back toward the April baseline (around Rs 60000-70000), that supports a temporary spike rather than a lasting shift. [MEDIUM]
## Assumptions
This memo does not know why Guntur spiked in May. [LOW] No external context (promotions, festivals, competitor activity) is available in this dataset. [LOW] The unverified assumption: the spike reflects genuine demand, not a data artifact such as one large bulk order. [MEDIUM]
