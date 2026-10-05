import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="E-commerce Sales Dashboard", page_icon="🛒", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce_sales.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

df = load_data()

st.title("🛒 E-commerce Sales Analysis Dashboard")
st.write("Interactive e-commerce sales analysis using Python, Pandas and Streamlit.")

# Sidebar filters
st.sidebar.header("🔎 Filters")

categories = ["All"] + sorted(df["Category"].unique().tolist())
selected_category = st.sidebar.selectbox("Category", categories)

states = ["All"] + sorted(df["State"].unique().tolist())
selected_state = st.sidebar.selectbox("State", states)

statuses = ["All"] + sorted(df["Order_Status"].unique().tolist())
selected_status = st.sidebar.selectbox("Order Status", statuses)

filtered = df.copy()

if selected_category != "All":
    filtered = filtered[filtered["Category"] == selected_category]

if selected_state != "All":
    filtered = filtered[filtered["State"] == selected_state]

if selected_status != "All":
    filtered = filtered[filtered["Order_Status"] == selected_status]

# KPIs
total_revenue = filtered["Revenue"].sum()
total_profit = filtered["Profit"].sum()
total_orders = filtered["Order_ID"].nunique()
total_quantity = filtered["Quantity"].sum()

c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
c2.metric("📈 Total Profit", f"₹{total_profit:,.0f}")
c3.metric("📦 Total Orders", f"{total_orders:,}")
c4.metric("🛍️ Total Quantity", f"{total_quantity:,}")

st.divider()

# Category analysis
st.subheader("📊 Revenue by Category")
category_sales = filtered.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
st.bar_chart(category_sales)

# Monthly trend
st.subheader("📈 Monthly Revenue Trend")
monthly_sales = (
    filtered.set_index("Order_Date")
    .resample("ME")["Revenue"]
    .sum()
)
monthly_sales.index = monthly_sales.index.strftime("%b %Y")
st.line_chart(monthly_sales)

# Two-column charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top Products")
    top_products = (
        filtered.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(top_products)

with col2:
    st.subheader("🗺️ Revenue by State")
    state_sales = (
        filtered.groupby("State")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(state_sales)

# Payment method
st.subheader("💳 Payment Method Analysis")
payment = filtered["Payment_Method"].value_counts()
st.bar_chart(payment)

# Order status
st.subheader("📦 Order Status")
status = filtered["Order_Status"].value_counts()
st.bar_chart(status)

# Data preview
with st.expander("👀 View Dataset"):
    st.dataframe(filtered, use_container_width=True)

st.success("Analysis completed successfully! 🎉")
