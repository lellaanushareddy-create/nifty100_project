import streamlit as st
import plotly.express as px

from utils import db

st.set_page_config(page_title="Home | Nifty 100 Analytics", layout="wide")
st.title("🏠 Home")

# ---------------- Sidebar: year selector ----------------
# Temporary fix
try:
    available_years = db.get_available_years()
except Exception as e:
    st.error(f"Database Error: {e}")
    available_years = [2024, 2023, 2022, 2021, 2020, 2019]

selected_year = st.sidebar.selectbox(
    "Select Year",
    available_years,
    index=0
)

# ---------------- KPI tiles ----------------
try:
    kpis = db.get_home_kpis(selected_year)
except Exception as e:
    st.error(f"KPI Error: {e}")
    kpis = {
        "avg_roe": None,
        "median_pe": None,
        "median_de": None,
        "total_companies": 0,
        "median_rev_cagr": None,
        "debt_free_count": 0,
    }

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Average ROE", f"{kpis['avg_roe']:.2f}%" if kpis["avg_roe"] is not None else "-")
col2.metric("Median P/E", f"{kpis['median_pe']:.2f}" if kpis["median_pe"] is not None else "-")
col3.metric("Median D/E", f"{kpis['median_de']:.2f}" if kpis["median_de"] is not None else "-")
col4.metric("Total Companies", kpis["total_companies"])
col5.metric(
    "Median Revenue CAGR (5Y)",
    f"{kpis['median_rev_cagr']:.2f}%" if kpis["median_rev_cagr"] is not None else "-"
)
col6.metric("Debt-Free Companies", kpis["debt_free_count"])



# ---------------- Sector breakdown donut chart ----------------
st.divider()
st.subheader("Sector Breakdown")
sector_df = db.get_sector_breakdown()

if sector_df.empty:
    st.info("No sector data available.")
else:
    fig = px.pie(
        sector_df,
        names="sector",
        values="company_count",
        hole=0.5,
        title="Companies by Sector",
    )
    fig.update_traces(textinfo="label+value")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------- Top-5 companies by composite quality score ----------------
st.subheader("Top 5 Companies by Composite Quality Score")
top5_df = db.get_top5_quality_companies(selected_year)

if top5_df.empty:
    st.info("No data available for the selected year.")
else:
    top5_df = top5_df.copy()
    top5_df["quality_score"] = top5_df["quality_score"].round(2)
    st.dataframe(
        top5_df.rename(columns={
            "company_name": "Company",
            "sector": "Sector",
            "quality_score": "Quality Score",
        }),
        use_container_width=True,
        hide_index=True,
    )