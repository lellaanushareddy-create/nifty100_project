import streamlit as st
import plotly.express as px
from utils import db

st.set_page_config(
    page_title="Sector Analysis",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Sector Analysis")

# -----------------------------
# Load sectors
# -----------------------------
sector_df = db.get_sector_list()

sector = st.selectbox(
    "Select Sector",
    sector_df["broad_sector"].tolist()
)

# -----------------------------
# Load data
# -----------------------------
df = db.get_sector_data(sector)

if df.empty:
    st.warning("No data available.")
    st.stop()

# -----------------------------
# Bubble Chart
# -----------------------------
st.subheader("Sector Bubble Chart")

fig = px.scatter(
    df,
    x="Revenue",
    y="ROE",
    size="MarketCap",
    color="sub_sector",
    hover_name="company_name",
    text="company_name",
    size_max=60,
    template="plotly_white"
)

fig.update_traces(textposition="top center")

fig.update_layout(
    xaxis_title="Revenue (Cr)",
    yaxis_title="ROE (%)",
    height=650
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Sector Median KPIs
# -----------------------------
st.subheader("Sector Median KPIs")

median_df = (
    df[["Revenue", "ROE", "MarketCap"]]
    .median()
    .reset_index()
)

median_df.columns = ["Metric", "Median"]

bar = px.bar(
    median_df,
    x="Metric",
    y="Median",
    text="Median",
    template="plotly_white"
)

bar.update_traces(texttemplate="%{text:.2f}")

st.plotly_chart(bar, use_container_width=True)

# -----------------------------
# Company Data
# -----------------------------
st.subheader("Companies")

st.dataframe(
    df,
    use_container_width=True
)