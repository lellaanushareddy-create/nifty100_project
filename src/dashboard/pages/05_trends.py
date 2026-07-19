import streamlit as st
import plotly.express as px
from utils import db

st.set_page_config(
    page_title="Trend Analysis",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Trend Analysis")

# ---------------------------------------------------
# Load companies
# ---------------------------------------------------

companies = db.get_company_list()

company_name = st.selectbox(
    "Select Company",
    companies["company_name"].tolist()
)

company_id = companies.loc[
    companies["company_name"] == company_name,
    "id"
].iloc[0]

# ---------------------------------------------------
# Load trend data
# ---------------------------------------------------

df = db.get_company_trends(company_id)

if df.empty:
    st.warning("No trend data available.")
    st.stop()

# ---------------------------------------------------
# Metric Selection
# ---------------------------------------------------

metrics = [
    "Revenue",
    "Net Profit",
    "EPS",
    "ROE",
    "Net Margin",
    "Debt to Equity",
    "Free Cash Flow"
]

selected_metrics = st.multiselect(
    "Select Metrics (Max 3)",
    metrics,
    default=["Revenue"],
    max_selections=3
)

if len(selected_metrics) == 0:
    st.info("Please select at least one metric.")
    st.stop()

# ---------------------------------------------------
# Line Chart
# ---------------------------------------------------

fig = px.line(
    df,
    x="year",
    y=selected_metrics,
    markers=True,
    title="10-Year Financial Trend"
)

# ---------------------------------------------------
# Add YoY annotations
# ---------------------------------------------------

for metric in selected_metrics:

    values = df[metric].tolist()

    for i in range(1, len(values)):

        if values[i-1] in [0, None]:
            continue

        try:
            yoy = ((values[i] - values[i-1]) / values[i-1]) * 100

            fig.add_annotation(
                x=df.iloc[i]["year"],
                y=values[i],
                text=f"{yoy:.1f}%",
                showarrow=False,
                font=dict(size=9)
            )

        except Exception:
            pass

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Value",
    legend_title="Metrics",
    hovermode="x unified",
    template="plotly_white",
    height=650
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Data Table
# ---------------------------------------------------

st.subheader("Financial Data")

st.dataframe(
    df,
    use_container_width=True
)