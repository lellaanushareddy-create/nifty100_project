import streamlit as st
from utils import db

st.set_page_config(page_title="Peer Comparison", layout="wide")

st.title("🤝 Peer Comparison")

# -------------------------------
# Select Year
# -------------------------------
years = db.get_available_years()
selected_year = st.sidebar.selectbox("Select Year", years)

# -------------------------------
# Select Peer Group
# -------------------------------
groups = db.get_peer_groups()

if not groups:
    st.warning("No peer groups available.")
    st.stop()

selected_group = st.selectbox(
    "Select Peer Group",
    groups
)

# -------------------------------
# Load Data
# -------------------------------
try:
    df = db.get_peer_metrics(
        selected_group,
        selected_year
    )
except Exception as e:
    st.error(f"Error loading peer data: {e}")
    st.stop()

if df.empty:
    st.warning("No data available.")
    st.stop()

# -------------------------------
# Display Table
# -------------------------------
st.subheader(f"Peer Group: {selected_group}")

st.dataframe(
    df,
    use_container_width=True
)

# -------------------------------
# Download CSV
# -------------------------------
csv = df.to_csv(index=False)

st.download_button(
    label="⬇ Download CSV",
    data=csv,
    file_name="peer_comparison.csv",
    mime="text/csv"
)