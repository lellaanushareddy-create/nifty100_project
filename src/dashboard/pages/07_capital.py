import plotly.express as px
import streamlit as st
from utils import db

st.set_page_config(page_title="Capital Allocation", page_icon="💰", layout="wide")

st.title("💰 Capital Allocation Map")

df = db.get_capital_data()

if df.empty:
    st.warning("No capital allocation data found.")
    st.stop()

fig = px.treemap(
    df,
    path=["capital_pattern", "company_name"],
    color="broad_sector",
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Companies")

pattern = st.selectbox("Select Capital Pattern", sorted(df["capital_pattern"].unique()))

st.dataframe(df[df["capital_pattern"] == pattern], use_container_width=True)
