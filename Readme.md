# E-Commerce Customer Retention & LTV Optimization

**Internship Project — End-to-End Analytics Pipeline**

## 🎯 Business Problem
- Customer Acquisition Cost (CAC): **+22%** over past 3 quarters
- 90-day repeat purchase rate: **-14%** over the same period
- Goal: Identify churn drivers, predict at-risk customers, and deliver an actionable dashboard.

## 📁 Project Structure
| Folder | Contents |
|---|---|
| `1_SQL/` | Cleaning, RFM, cohort retention, leakage-free churn labels |
| `2_Notebooks/` | EDA, feature engineering, model comparison |
| `3_Data/` | Raw and processed CSVs, trained model |
| `4_Dashboard/` | Streamlit app |
| `5_Reports/` | Executive summary |
| `6_Docs/` | Methodology, data dictionary, limitations |

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the pipeline (SQL files assume MySQL; or run the notebook for Python-only)
jupyter notebook 2_Notebooks/churn_analysis.ipynb

# 3. Launch the dashboard
cd 4_Dashboard
streamlit run app.py