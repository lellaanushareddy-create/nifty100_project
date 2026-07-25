import streamlit as st
from utils import db

st.set_page_config(page_title="Reports", page_icon="📄", layout="wide")

st.title("📄 Reports")

# Load company list
companies = db.get_company_list()

if companies.empty:
    st.warning("No company data available.")
    st.stop()

st.subheader("Company Report")

search = st.text_input("Search Company")

if search:
    companies = companies[
        companies["company_name"].str.contains(search, case=False, na=False)
    ]

st.dataframe(companies, use_container_width=True)

csv = companies.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Report (CSV)",
    data=csv,
    file_name="company_report.csv",
    mime="text/csv",
)

st.markdown("---")

st.subheader("Summary")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Companies", len(companies))

with col2:
    st.metric("Database Status", "Loaded")
