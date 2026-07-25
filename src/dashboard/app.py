import streamlit as st

st.set_page_config(
    page_title="Nifty100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("Nifty100 Analytics")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🏢 Company Profile",
        "📊 Screener",
        "👥 Peers",
        "📈 Trends",
        "🏭 Sectors",
        "💰 Capital",
        "📄 Reports",
    ],
)

st.title(page)
st.write("Welcome to the Nifty100 Analytics Dashboard!")
