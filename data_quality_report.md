# Data Quality Report

1. Removing duplicates -> Uniqueness
The same order was accidentally counted twice. Uniqueness means each real thing should appear only once in the data.

2. Fixing region spelling -> Consistency
"Hyderabad", " hyderabad", "HYDERABAD " all mean the same place but were written differently. Consistency means the same thing should always be written the same way.

3. Filling missing category -> Completeness
Some rows had blank category cells. Completeness means the data should have no missing values.

4. Filling missing profit -> Completeness and Accuracy
This also fixes missing data (Completeness). But since the value is estimated using each category's real average margin, it also relates to Accuracy, since the estimate should be close to the true value.

Other dimensions:
- Timeliness: not relevant here, since this is a one-time monthly file, not live streaming data.
- Validity: partly touched by the region fix, since only 9 official region names are considered valid.
- Relevance: partly touched, since missing values were filled in instead of deleted, keeping more usable data instead of throwing rows away.
