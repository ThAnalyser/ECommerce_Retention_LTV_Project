## Data Export

After all SQL transformations completed, four tables were exported to CSV 
for Python-based modeling:

- `cleaned_data.csv` — 397,880 transactions after removing blanks/cancellations
- `rfm_summary.csv` — 4,338 unique customers with recency/frequency/monetary
- `cohort_retention_matrix.csv` — monthly retention % by acquisition cohort
- `churn_modeling_data.csv` — 3,370 customers with leakage-free churn labels
  (1,921 stayed active, 1,449 churned — 57/43 split)