"""
E-Commerce Customer Retention & LTV Dashboard — Modern UI + Enhancements
Run with: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
from pathlib import Path
from datetime import datetime, timedelta

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Retention Analytics | E-Commerce",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS — Modern, Professional Look
# =========================================================
st.markdown("""
<style>
    /* ---------- Global ---------- */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #eef2f7 100%);
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* ---------- Header ---------- */
    .hero-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #8b5cf6 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(30, 58, 138, 0.25);
        position: relative;
        overflow: hidden;
    }
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-header h1 {
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        position: relative;
        z-index: 1;
        color: white !important;
    }
    .hero-header p {
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.92;
        position: relative;
        z-index: 1;
        color: white !important;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.75rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        position: relative;
        z-index: 1;
        color: white !important;
    }
    .hero-clock {
        position: absolute;
        top: 1.5rem;
        right: 2rem;
        font-size: 0.8rem;
        opacity: 0.9;
        font-weight: 500;
        z-index: 1;
        color: white !important;
    }
    
    /* ---------- KPI Cards ---------- */
    .kpi-card {
        background: white;
        padding: 1.25rem 1.5rem;
        border-radius: 14px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.25s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    .kpi-card:hover {
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .kpi-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
    }
    .kpi-card.blue::after   { background: linear-gradient(180deg, #3b82f6, #1e40af); }
    .kpi-card.green::after  { background: linear-gradient(180deg, #10b981, #047857); }
    .kpi-card.orange::after { background: linear-gradient(180deg, #f59e0b, #b45309); }
    .kpi-card.red::after    { background: linear-gradient(180deg, #ef4444, #b91c1c); }
    .kpi-card.purple::after { background: linear-gradient(180deg, #8b5cf6, #6d28d9); }
    
    .kpi-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.1;
        letter-spacing: -0.5px;
    }
    .kpi-delta {
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.35rem;
    }
    .kpi-delta.up   { color: #10b981; }
    .kpi-delta.down { color: #ef4444; }
    .kpi-icon {
        position: absolute;
        top: 1.1rem;
        right: 1.1rem;
        font-size: 1.5rem;
        opacity: 0.9;
    }
    
    /* ---------- Section Headers ---------- */
    .section-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1e293b;
        margin: 1.5rem 0 0.75rem 0;
        padding-left: 0.75rem;
        border-left: 4px solid #3b82f6;
    }
    
    /* ---------- Recommendation Cards ---------- */
    .rec-card {
        background: white;
        padding: 1.25rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 0.75rem;
        border-left: 5px solid;
        transition: all 0.2s;
    }
    .rec-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }
    .rec-card.champions { border-color: #10b981; }
    .rec-card.at-risk   { border-color: #f59e0b; }
    .rec-card.new       { border-color: #3b82f6; }
    .rec-card.lost      { border-color: #ef4444; }
    .rec-card h4 {
        margin: 0 0 0.4rem 0;
        font-size: 1rem;
        color: #0f172a;
        font-weight: 700;
    }
    .rec-card p {
        margin: 0;
        color: #64748b;
        font-size: 0.88rem;
        line-height: 1.5;
    }
    
    /* ---------- Predictor Result ---------- */
    .predictor-result {
        padding: 1.5rem 2rem;
        border-radius: 14px;
        text-align: center;
        margin-top: 1rem;
        animation: fadeIn 0.5s ease;
    }
    .predictor-result.high {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 2px solid #ef4444;
    }
    .predictor-result.low {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 2px solid #10b981;
    }
    .predictor-result h2 { margin: 0; font-size: 1.5rem; font-weight: 800; }
    .predictor-result.high h2 { color: #991b1b; }
    .predictor-result.low h2  { color: #065f46; }
    .predictor-result p { margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: 800; }
    .predictor-result.high p { color: #b91c1c; }
    .predictor-result.low p  { color: #047857; }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    
    /* ---------- Model Badge ---------- */
    .model-badge {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-left: 5px solid #0284c7;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }
    .model-badge-item {
        text-align: center;
        flex: 1;
        min-width: 100px;
    }
    .model-badge-label {
        font-size: 0.7rem;
        color: #0369a1;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .model-badge-value {
        font-size: 1.1rem;
        color: #0c4a6e;
        font-weight: 800;
        margin-top: 0.2rem;
    }
    
    /* ---------- Customer Result Card (DARK - matches sidebar) ---------- */
    .customer-result {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1.25rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        margin-top: 0.75rem;
        border-left: 4px solid #8b5cf6;
    }
    .customer-result h4 {
        margin: 0 0 0.75rem 0;
        color: #ffffff !important;
        font-size: 1rem;
        font-weight: 700;
    }
    .customer-result-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 0.5rem;
        font-size: 0.9rem;
    }
    .customer-result-grid > div {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.4rem 0;
        border-bottom: 1px solid rgba(148, 163, 184, 0.2);
        color: #cbd5e1 !important;
        font-weight: 500;
    }
    .customer-result-grid > div:last-child {
        border-bottom: none;
    }
    .customer-result-grid span {
        font-weight: 700 !important;
        color: #ffffff !important;
    }
    
    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 0.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        border-radius: 8px;
        padding: 0 1.25rem;
        font-weight: 600;
        color: #64748b;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        color: white !important;
    }
    
    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    section[data-testid="stSidebar"] * {
        color: #e2e8f0;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: white;
    }
    /* Ensure customer result card keeps dark styling */
    section[data-testid="stSidebar"] .customer-result * {
        color: #cbd5e1 !important;
    }
    section[data-testid="stSidebar"] .customer-result h4 {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] .customer-result-grid span {
        color: #ffffff !important;
    }
    
    /* ---------- Buttons ---------- */
    .stButton > button, .stDownloadButton > button {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 700;
        transition: all 0.2s;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(59, 130, 246, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================
BASE_DIR  = Path(__file__).parent.parent
DATA_DIR  = BASE_DIR / "Data" / "processed"
MODEL_DIR = BASE_DIR / "Data" / "models"

@st.cache_data
def load_data():
    cleaned = pd.read_csv(DATA_DIR / "cleaned_data.csv", parse_dates=["invoice_date"])
    rfm     = pd.read_csv(DATA_DIR / "rfm_summary.csv")
    cohort  = pd.read_csv(DATA_DIR / "cohort_retention_matrix.csv")
    churn   = pd.read_csv(DATA_DIR / "churn_modeling_data.csv")
    return cleaned, rfm, cohort, churn

@st.cache_resource
def load_model():
    return joblib.load(MODEL_DIR / "churn_model.pkl")

try:
    cleaned_data, rfm_summary, cohort_matrix, churn_data = load_data()
    model_bundle = load_model()
except FileNotFoundError as e:
    st.error(f"❌ Missing file: {e}")
    st.stop()

# =========================================================
# RFM SEGMENTATION
# =========================================================
rfm = rfm_summary.copy()
recency_median = rfm["recency"].median()
value_score = rfm["frequency"].rank(pct=True) * 0.5 + rfm["monetary"].rank(pct=True) * 0.5
value_median = value_score.median()

def assign_segment(row_recency, row_value_score):
    recent = row_recency <= recency_median
    high_value = row_value_score >= value_median
    if recent and high_value:
        return "Champions"
    elif not recent and high_value:
        return "At Risk"
    elif recent and not high_value:
        return "New / Casual"
    else:
        return "Lost"

rfm["segment"] = [assign_segment(r, v) for r, v in zip(rfm["recency"], value_score)]

SEGMENT_COLORS = {
    "Champions":    "#10b981",
    "At Risk":      "#f59e0b",
    "New / Casual": "#3b82f6",
    "Lost":         "#ef4444"
}

# =========================================================
# SIDEBAR WITH CUSTOMER SEARCH
# =========================================================
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    st.markdown("---")
    
    # Date range
    st.markdown("**📅 Date Range**")
    min_date = cleaned_data["invoice_date"].min().date()
    max_date = cleaned_data["invoice_date"].max().date()
    date_range = st.date_input(
        "Select range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )
    
    # Country
    st.markdown("**🌍 Country**")
    countries = ["All Countries"] + sorted(cleaned_data["country"].dropna().unique().tolist())
    selected_country = st.selectbox("Country", countries, label_visibility="collapsed")
    
    # Segment
    st.markdown("**👥 Segment**")
    segments = ["All Segments", "Champions", "At Risk", "New / Casual", "Lost"]
    selected_segment = st.selectbox("Segment", segments, label_visibility="collapsed")
    
    st.markdown("---")
    
    # CUSTOMER SEARCH
    st.markdown("### 🔍 Customer Lookup")
    st.caption("Search any customer by ID")
    
    customer_id_input = st.text_input(
        "Customer ID",
        placeholder="e.g., 13047",
        label_visibility="collapsed"
    )
    
    if customer_id_input:
        try:
            cid = int(customer_id_input.strip())
            match = rfm[rfm["customer_id"] == cid]
            if not match.empty:
                row = match.iloc[0]
                seg_color = SEGMENT_COLORS.get(row["segment"], "#64748b")
                st.markdown(f"""
                <div class="customer-result">
                    <h4>✅ Customer #{cid}</h4>
                    <div class="customer-result-grid">
                        <div>
                            <span style="color:#cbd5e1; font-weight:500;">Segment</span>
                            <span style="color:{seg_color}; font-weight:800;">{row['segment']}</span>
                        </div>
                        <div>
                            <span style="color:#cbd5e1; font-weight:500;">Recency</span>
                            <span style="color:#ffffff; font-weight:800;">{int(row['recency'])} days</span>
                        </div>
                        <div>
                            <span style="color:#cbd5e1; font-weight:500;">Frequency</span>
                            <span style="color:#ffffff; font-weight:800;">{int(row['frequency'])} orders</span>
                        </div>
                        <div>
                            <span style="color:#cbd5e1; font-weight:500;">Monetary</span>
                            <span style="color:#ffffff; font-weight:800;">£{row['monetary']:,.0f}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(f"No customer found with ID {cid}")
        except ValueError:
            st.error("Please enter a valid number")
    
    st.markdown("---")
    st.markdown("### 📌 About")
    st.caption(
        "E-Commerce Customer Retention & LTV dashboard. "
        "Built on the UCI Online Retail II dataset."
    )
    st.caption("Made with ❤️ using Streamlit + Plotly")

# =========================================================
# APPLY FILTERS
# =========================================================
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_data = cleaned_data[
        (cleaned_data["invoice_date"].dt.date >= start_date) &
        (cleaned_data["invoice_date"].dt.date <= end_date)
    ]
else:
    filtered_data = cleaned_data

if selected_country != "All Countries":
    filtered_data = filtered_data[filtered_data["country"] == selected_country]

rfm_filtered = rfm if selected_segment == "All Segments" else rfm[rfm["segment"] == selected_segment]

# =========================================================
# HERO HEADER WITH REAL-TIME CLOCK
# =========================================================
now_str = datetime.now().strftime("%A, %B %d, %Y · %H:%M:%S")

st.markdown(f"""
<div class="hero-header">
    <div class="hero-clock">🕐 {now_str}</div>
    <h1>📊 Customer Retention & Lifetime Value</h1>
    <p>Real-time retention intelligence and churn prediction for your e-commerce business</p>
    <span class="hero-badge">● Live Dashboard</span>
</div>
""", unsafe_allow_html=True)

# =========================================================
# KPI CARDS
# =========================================================
orders_per_customer = filtered_data.groupby("customer_id")["invoice"].nunique()
one_time_pct = (orders_per_customer == 1).mean() * 100
total_revenue = filtered_data["line_total"].sum()
overall_churn_rate = churn_data["is_churned"].mean() * 100
total_customers = filtered_data["customer_id"].nunique()
avg_order_value = filtered_data["line_total"].sum() / max(filtered_data["invoice"].nunique(), 1)

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""
    <div class="kpi-card blue">
        <div class="kpi-icon">👥</div>
        <div class="kpi-label">Total Customers</div>
        <div class="kpi-value">{total_customers:,}</div>
        <div class="kpi-delta up">↑ active base</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card green">
        <div class="kpi-icon">💰</div>
        <div class="kpi-label">Total Revenue</div>
        <div class="kpi-value">£{total_revenue/1000:.1f}K</div>
        <div class="kpi-delta up">↑ lifetime value</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    color = "down" if one_time_pct > 50 else "up"
    arrow = "↑" if one_time_pct > 50 else "↓"
    st.markdown(f"""
    <div class="kpi-card orange">
        <div class="kpi-icon">🔄</div>
        <div class="kpi-label">One-Time Buyers</div>
        <div class="kpi-value">{one_time_pct:.1f}%</div>
        <div class="kpi-delta {color}">{arrow} target &lt; 30%</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    color = "down" if overall_churn_rate > 40 else "up"
    st.markdown(f"""
    <div class="kpi-card red">
        <div class="kpi-icon">⚠️</div>
        <div class="kpi-label">Churn Rate (90d)</div>
        <div class="kpi-value">{overall_churn_rate:.1f}%</div>
        <div class="kpi-delta {color}">90-day window</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="kpi-card purple">
        <div class="kpi-icon">🛒</div>
        <div class="kpi-label">Avg Order Value</div>
        <div class="kpi-value">£{avg_order_value:.0f}</div>
        <div class="kpi-delta up">per transaction</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# EXPORT REPORT BUTTONS
# =========================================================
st.markdown("")
exp_col1, exp_col2, exp_col3 = st.columns([2, 1, 1])

with exp_col2:
    rfm_export = rfm_filtered.copy()
    csv_data = rfm_export.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Export RFM Report",
        data=csv_data,
        file_name=f"retention_report_{datetime.now():%Y%m%d_%H%M}.csv",
        mime="text/csv",
        use_container_width=True
    )

with exp_col3:
    summary_data = pd.DataFrame([{
        "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_customers": total_customers,
        "total_revenue": round(total_revenue, 2),
        "one_time_pct": round(one_time_pct, 2),
        "churn_rate": round(overall_churn_rate, 2),
        "avg_order_value": round(avg_order_value, 2),
    }])
    st.download_button(
        label="📊 Export KPI Summary",
        data=summary_data.to_csv(index=False).encode("utf-8"),
        file_name=f"kpi_summary_{datetime.now():%Y%m%d_%H%M}.csv",
        mime="text/csv",
        use_container_width=True
    )

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Overview",
    "👥 Segments",
    "🔁 Cohort Retention",
    "🤖 Churn Insights",
    "🔮 Predictor"
])

# =========================================================
# TAB 1 — OVERVIEW
# =========================================================
with tab1:
    st.markdown('<div class="section-header">Revenue Trend</div>', unsafe_allow_html=True)
    
    revenue_by_month = (
        filtered_data
        .set_index("invoice_date")
        .resample("ME")["line_total"]
        .sum()
        .reset_index()
    )
    
    fig_rev = px.area(
        revenue_by_month, x="invoice_date", y="line_total",
        template="plotly_white",
        labels={"invoice_date": "Month", "line_total": "Revenue (£)"}
    )
    fig_rev.update_traces(
        line=dict(color="#3b82f6", width=3),
        fillcolor="rgba(59, 130, 246, 0.15)"
    )
    fig_rev.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=20, b=0),
        hovermode="x unified",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9")
    )
    st.plotly_chart(fig_rev, use_container_width=True)
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown('<div class="section-header">Top 10 Products</div>', unsafe_allow_html=True)
        top_products = (
            filtered_data.groupby("description")["line_total"]
            .sum().nlargest(10).reset_index()
            .sort_values("line_total")
        )
        fig_prod = px.bar(
            top_products, x="line_total", y="description",
            orientation="h",
            template="plotly_white",
            color="line_total",
            color_continuous_scale=["#bfdbfe", "#3b82f6", "#1e40af"],
            labels={"line_total": "Revenue (£)", "description": ""}
        )
        fig_prod.update_layout(
            height=400, showlegend=False, coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_prod, use_container_width=True)
    
    with c2:
        st.markdown('<div class="section-header">Revenue by Country</div>', unsafe_allow_html=True)
        top_countries = (
            filtered_data.groupby("country")["line_total"]
            .sum().nlargest(10).reset_index()
        )
        fig_country = px.pie(
            top_countries, values="line_total", names="country",
            hole=0.55, template="plotly_white",
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig_country.update_traces(textinfo="percent+label", textposition="inside")
        fig_country.update_layout(
            height=400, showlegend=False,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_country, use_container_width=True)

# =========================================================
# TAB 2 — SEGMENTS
# =========================================================
with tab2:
    c1, c2 = st.columns([1, 1.3])
    
    with c1:
        st.markdown('<div class="section-header">Segment Distribution</div>', unsafe_allow_html=True)
        seg_counts = rfm["segment"].value_counts().reset_index()
        seg_counts.columns = ["segment", "count"]
        
        fig_seg = px.pie(
            seg_counts, names="segment", values="count", hole=0.6,
            color="segment",
            color_discrete_map=SEGMENT_COLORS,
            template="plotly_white"
        )
        fig_seg.update_traces(
            textinfo="percent+label",
            textfont_size=12,
            marker=dict(line=dict(color="white", width=2))
        )
        fig_seg.update_layout(
            height=420, showlegend=True,
            margin=dict(l=0, r=0, t=20, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1)
        )
        st.plotly_chart(fig_seg, use_container_width=True)
    
    with c2:
        st.markdown('<div class="section-header">Recency vs. Monetary</div>', unsafe_allow_html=True)
        fig_scatter = px.scatter(
            rfm_filtered, x="recency", y="monetary",
            color="segment", size="frequency",
            hover_data=["customer_id", "frequency"],
            color_discrete_map=SEGMENT_COLORS,
            template="plotly_white",
            labels={"recency": "Days since last purchase", "monetary": "Total spend (£)"},
            size_max=30
        )
        fig_scatter.update_layout(
            height=420,
            margin=dict(l=0, r=0, t=20, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown('<div class="section-header">Segment Insights</div>', unsafe_allow_html=True)
    seg_stats = rfm.groupby("segment").agg(
        Customers=("customer_id", "count"),
        Avg_Recency=("recency", "mean"),
        Avg_Frequency=("frequency", "mean"),
        Avg_Monetary=("monetary", "mean"),
        Total_Revenue=("monetary", "sum")
    ).round(1).reset_index()
    seg_stats["Total_Revenue"] = seg_stats["Total_Revenue"].apply(lambda x: f"£{x:,.0f}")
    seg_stats["Avg_Monetary"] = seg_stats["Avg_Monetary"].apply(lambda x: f"£{x:,.0f}")
    st.dataframe(seg_stats, use_container_width=True, hide_index=True)

# =========================================================
# TAB 3 — COHORT
# =========================================================
with tab3:
    st.markdown('<div class="section-header">Monthly Cohort Retention Heatmap</div>', unsafe_allow_html=True)
    st.caption("Each row is a cohort (grouped by first purchase month). Each cell shows the % still buying N months later.")
    
    pivot = cohort_matrix.pivot(index="cohort_month", columns="period_number", values="retention_pct")
    pivot = pivot.iloc[:20]
    
    fig_cohort = px.imshow(
        pivot,
        labels=dict(x="Months since first purchase", y="Acquisition cohort", color="Retention %"),
        color_continuous_scale="Blues",
        text_auto=".0f",
        aspect="auto",
        template="plotly_white"
    )
    fig_cohort.update_layout(height=600, margin=dict(l=0, r=0, t=20, b=0))
    st.plotly_chart(fig_cohort, use_container_width=True)
    
    st.markdown('<div class="section-header">Average Retention Decay</div>', unsafe_allow_html=True)
    avg_retention = cohort_matrix.groupby("period_number")["retention_pct"].mean().reset_index()
    avg_retention = avg_retention[avg_retention["period_number"] <= 11]
    
    fig_decay = px.line(
        avg_retention, x="period_number", y="retention_pct",
        markers=True, template="plotly_white",
        labels={"period_number": "Months since first purchase", "retention_pct": "Avg Retention %"}
    )
    fig_decay.update_traces(line=dict(color="#8b5cf6", width=3), marker=dict(size=10))
    fig_decay.update_layout(height=350, margin=dict(l=0, r=0, t=20, b=0))
    st.plotly_chart(fig_decay, use_container_width=True)

# =========================================================
# TAB 4 — CHURN INSIGHTS
# =========================================================
with tab4:
    st.markdown(f"""
    <div class="model-badge">
        <div class="model-badge-item">
            <div class="model-badge-label">🤖 Model</div>
            <div class="model-badge-value">Logistic Regression</div>
        </div>
        <div class="model-badge-item">
            <div class="model-badge-label">📈 ROC-AUC</div>
            <div class="model-badge-value">0.732</div>
        </div>
        <div class="model-badge-item">
            <div class="model-badge-label">🔢 Features</div>
            <div class="model-badge-value">5</div>
        </div>
        <div class="model-badge-item">
            <div class="model-badge-label">👥 Dataset</div>
            <div class="model-badge-value">{len(churn_data):,} customers</div>
        </div>
        <div class="model-badge-item">
            <div class="model-badge-label">🎯 Accuracy</div>
            <div class="model-badge-value">~73%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown('<div class="section-header">Churn Distribution</div>', unsafe_allow_html=True)
        churn_counts = churn_data["is_churned"].value_counts().reset_index()
        churn_counts.columns = ["status", "count"]
        churn_counts["status"] = churn_counts["status"].map({0: "Active", 1: "Churned"})
        
        fig_churn = px.pie(
            churn_counts, names="status", values="count", hole=0.6,
            color="status",
            color_discrete_map={"Active": "#10b981", "Churned": "#ef4444"},
            template="plotly_white"
        )
        fig_churn.update_traces(textinfo="percent+label")
        fig_churn.update_layout(height=350, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_churn, use_container_width=True)
    
    with c2:
        st.markdown('<div class="section-header">Feature Comparison</div>', unsafe_allow_html=True)
        feat_compare = churn_data.groupby("is_churned")[["recency", "frequency", "monetary"]].mean().round(1)
        feat_compare.index = ["Active", "Churned"]
        
        fig_compare = go.Figure()
        for col, color in zip(["recency", "frequency", "monetary"], ["#3b82f6", "#10b981", "#f59e0b"]):
            fig_compare.add_trace(go.Bar(
                name=col.title(),
                x=feat_compare.index,
                y=feat_compare[col],
                marker_color=color
            ))
        fig_compare.update_layout(
            barmode="group", height=350, template="plotly_white",
            margin=dict(l=0, r=0, t=20, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2)
        )
        st.plotly_chart(fig_compare, use_container_width=True)

# =========================================================
# TAB 5 — PREDICTOR
# =========================================================
with tab5:
    st.markdown('<div class="section-header">🔮 Churn Risk Predictor</div>', unsafe_allow_html=True)
    st.write("Enter a customer's behavioral metrics to estimate their churn probability using the trained Logistic Regression model.")
    
    st.markdown("")
    
    p1, p2, p3, p4, p5 = st.columns(5)
    with p1:
        in_recency = st.number_input("📅 Recency (days)", min_value=0, max_value=1000, value=60, help="Days since last purchase")
    with p2:
        in_frequency = st.number_input("🔄 Frequency (orders)", min_value=1, max_value=500, value=5, help="Total distinct orders")
    with p3:
        in_monetary = st.number_input("💰 Monetary (£)", min_value=0.0, max_value=200000.0, value=1000.0, step=50.0, help="Total lifetime spend")
    with p4:
        in_aov = st.number_input("🛒 Avg Order Value (£)", min_value=0.0, max_value=20000.0, value=200.0, step=10.0, help="Monetary ÷ Frequency")
    with p5:
        in_products = st.number_input("📦 Unique Products", min_value=1, max_value=2000, value=20, help="Distinct stock codes bought")
    
    st.markdown("")
    
    col_btn_center = st.columns([1, 1, 1])[1]
    with col_btn_center:
        predict_clicked = st.button("🚀 Predict Churn Risk", use_container_width=True)
    
    if predict_clicked:
        model        = model_bundle["model"]
        scaler       = model_bundle["scaler"]
        feature_cols = model_bundle["feature_cols"]
        input_df = pd.DataFrame(
            [[in_recency, in_frequency, in_monetary, in_aov, in_products]],
            columns=feature_cols
        )
        input_scaled = scaler.transform(input_df)
        proba = model.predict_proba(input_scaled)[0][1]
        
        if proba >= 0.5:
            st.markdown(f"""
            <div class="predictor-result high">
                <h2>⚠️ High Risk of Churn</h2>
                <p>{proba*100:.1f}%</p>
                <span style="color:#7f1d1d; font-weight:600;">Recommended action: Priority win-back campaign</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="predictor-result low">
                <h2>✅ Likely to Stay Active</h2>
                <p>{proba*100:.1f}%</p>
                <span style="color:#065f46; font-weight:600;">Recommended action: Nurture with loyalty perks</span>
            </div>
            """, unsafe_allow_html=True)
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=proba * 100,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Churn Probability (%)", "font": {"size": 16}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1},
                "bar": {"color": "#1e293b"},
                "steps": [
                    {"range": [0, 40],  "color": "#d1fae5"},
                    {"range": [40, 70], "color": "#fef3c7"},
                    {"range": [70, 100],"color": "#fecaca"}
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 50
                }
            }
        ))
        fig_gauge.update_layout(height=350, template="plotly_white", margin=dict(l=20, r=20, t=60, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

st.markdown("---")

# =========================================================
# RECOMMENDATIONS
# =========================================================
st.markdown('<div class="section-header">📌 Retention Strategy Recommendations</div>', unsafe_allow_html=True)

rec1, rec2 = st.columns(2)
with rec1:
    st.markdown(f"""
    <div class="rec-card champions">
        <h4>🟢 Champions — {(rfm['segment']=='Champions').sum()} customers</h4>
        <p>Reward with early access, VIP perks, and exclusive offers. These customers drive the bulk of revenue — protect them aggressively.</p>
    </div>
    <div class="rec-card at-risk">
        <h4>🟠 At Risk — {(rfm['segment']=='At Risk').sum()} customers</h4>
        <p>Previously high-value but now lapsing. Prioritize win-back campaigns and personalized discount codes before they fully churn.</p>
    </div>
    """, unsafe_allow_html=True)

with rec2:
    st.markdown(f"""
    <div class="rec-card new">
        <h4>🔵 New / Casual — {(rfm['segment']=='New / Casual').sum()} customers</h4>
        <p>Recently acquired but low value so far. Trigger a second-purchase incentive within 30 days to convert them into repeat buyers.</p>
    </div>
    <div class="rec-card lost">
        <h4>🔴 Lost — {(rfm['segment']=='Lost').sum()} customers</h4>
        <p>Low historical value and inactive. Deprioritize retention spend here and reallocate the budget to the three segments above.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.markdown("---")
st.caption("📊 E-Commerce Customer Retention & LTV Optimization · Built with Streamlit & Plotly · UCI Online Retail II dataset")