import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils import db

st.set_page_config(page_title="Company Profile | Nifty 100 Analytics", layout="wide")
st.title("🔎 Company Profile")

# ---------------- Search box with autocomplete ----------------
query = st.text_input("Search by company name or ticker", value="")

selected_ticker = None

if query:
    matches = db.search_companies(query)
    if matches:
        labels = [f"{name} ({ticker})" for ticker, name in matches]
        choice = st.selectbox("Matching companies", options=labels)
        selected_ticker = matches[labels.index(choice)][0]
    else:
        st.warning("Ticker not found — please try another.")

if not selected_ticker:
    st.stop()

# ---------------- Company card ----------------
card = db.get_company_card(selected_ticker)

if card is None:
    st.warning("Ticker not found — please try another.")
    st.stop()

st.subheader(card["company_name"])
c1, c2, c3 = st.columns(3)
c1.markdown(f"**Sector:** {card['sector']}")
c2.markdown(f"**Sub-Sector:** {card['sub_sector']}")
c3.markdown(f"**NSE Ticker:** {card['nse_ticker']}")
st.markdown(card["about"] or "_No description available._")

st.divider()

# ---------------- KPI tiles ----------------
kpis = db.get_company_latest_kpis(selected_ticker)

if kpis is None:
    st.info("No financial ratio data available for this company.")
else:
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("ROE", f"{kpis['roe']:.2f}%" if kpis["roe"] is not None else "—")
    k2.metric("ROCE", f"{kpis['roce']:.2f}%" if kpis["roce"] is not None else "—")
    k3.metric("Net Profit Margin", f"{kpis['net_margin']:.2f}%" if kpis["net_margin"] is not None else "—")
    k4.metric("D/E", f"{kpis['de']:.2f}" if kpis["de"] is not None else "—")
    k5.metric("Revenue CAGR (5yr)", f"{kpis['rev_cagr_5yr']:.2f}%" if kpis["rev_cagr_5yr"] is not None else "—")
    k6.metric("FCF (₹ Cr)", f"{kpis['fcf']:.2f}" if kpis["fcf"] is not None else "—")

st.divider()

# ---------------- 10-year Revenue & Net Profit bar chart ----------------
st.subheader("Revenue & Net Profit (10-Year)")
fin_df = db.get_company_financials_10yr(selected_ticker)

if fin_df.empty:
    st.info("No 10-year financial history available.")
else:
    fig_bar = px.bar(
        fin_df,
        x="year",
        y=["revenue", "net_profit"],
        barmode="group",
        labels={"value": "₹ Cr", "year": "Year", "variable": "Metric"},
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ---------------- ROE / ROCE dual-axis line chart ----------------
st.subheader("ROE & ROCE (10-Year)")
ratio_df = db.get_company_roe_roce_10yr(selected_ticker)

if ratio_df.empty:
    st.info("No 10-year ROE/ROCE history available.")
else:
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=ratio_df["year"], y=ratio_df["roe"], name="ROE (%)", yaxis="y1"))
    fig_line.add_trace(go.Scatter(x=ratio_df["year"], y=ratio_df["roce"], name="ROCE (%)", yaxis="y2"))
    fig_line.update_layout(
        yaxis=dict(title="ROE (%)"),
        yaxis2=dict(title="ROCE (%)", overlaying="y", side="right"),
        legend=dict(orientation="h"),
    )
    st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# ---------------- Pros and Cons ----------------
st.subheader("Pros & Cons")
pros, cons = db.get_pros_cons(selected_ticker)

pc1, pc2 = st.columns(2)
with pc1:
    st.markdown("**Pros**")
    if pros:
        for p in pros:
            st.markdown(f"✅ {p}")
    else:
        st.caption("No pros listed.")

with pc2:
    st.markdown("**Cons**")
    if cons:
        for c in cons:
            st.markdown(f"❌ {c}")
    else:
        st.caption("No cons listed.")