import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned dataset
df = pd.read_csv("furniture_cleaned.csv")

# Ensure order_date is datetime
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["year"] = df["order_date"].dt.year

# ===========================
# Streamlit Setup
# ===========================
st.set_page_config(page_title="Furniture Sales Dashboard", layout="wide")
st.title("🪑 Furniture Sales Dashboard")
st.markdown("Interactive dashboard to explore sales, customers, regions, profitability, and growth opportunities.")

# --- Compute Total Revenue ---
total_revenue = df["sales"].sum()
st.metric(label="💰 Total Revenue", value=f"${total_revenue:,.2f}")

# --- Revenue by Year ---
revenue_by_year = df.groupby("year")["sales"].sum().reset_index()
fig_revenue = px.line(revenue_by_year, x="year", y="sales", markers=True, title="Revenue by Year")
st.plotly_chart(fig_revenue, use_container_width=True)

# ===========================
# Dashboard Layout
# ===========================
# 1. Sales & Revenue Performance
# ===========================
st.header("📊 Sales & Revenue Performance")
top_category = pd.read_csv("top_category.csv")
top_product = pd.read_csv("top_product.csv")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Top Categories")
    st.dataframe(top_category)
with col2:
    st.subheader("Top Products")
    st.dataframe(top_product)

# ===========================
# 2. Customer Insights
# ===========================
top_customers = pd.read_csv("top_customers.csv")
repeat_purchases = pd.read_csv("repeat_purchases.csv")

st.header("👥 Customer Insights")
st.subheader("Top Customers by Revenue")
st.dataframe(top_customers)

st.subheader("Repeat Purchase Patterns")
fig_repeat = px.bar(repeat_purchases, x="customer_name", y="num_orders", title="Repeat Purchases")
st.plotly_chart(fig_repeat, use_container_width=True)

# ===========================
# 3. Regional / Store Performance
# ===========================
top_regions = pd.read_csv("top_regions.csv")
top_cities = pd.read_csv("top_cities.csv")
region_product_sales = pd.read_csv("region_product_sales.csv")
region_year_sales_growth = pd.read_csv("region_year_sales_growth.csv")

st.header("🌍 Regional / Store Performance")
st.subheader("Top Regions")
st.dataframe(top_regions)

st.subheader("Top Cities")
st.dataframe(top_cities)

st.subheader("Product Sales by Region")
top_products = (
    region_product_sales.groupby("product_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .index
)

top_region_product_sales = region_product_sales[region_product_sales["product_name"].isin(top_products)]

fig_region_product = px.bar(
    top_region_product_sales,
    x="region",
    y="sales",
    color="product_name",
    title="Top 10 Products Sold by Region"
)
st.plotly_chart(fig_region_product, use_container_width=True)

st.subheader("Year-over-Year Regional Growth")
fig_region_growth = px.line(region_year_sales_growth, x="year", y="sales_growth", color="region", markers=True, title="YoY Growth by Region")
st.plotly_chart(fig_region_growth, use_container_width=True)

# ===========================
# 4. Profitability & Costs
# ===========================
category_profit_margin = pd.read_csv("category_profit_margin.csv")
product_profit_margin = pd.read_csv("product_profit_margin.csv")
region_profit_margin = pd.read_csv("region_profit_margin.csv")
low_profit_products = pd.read_csv("low_profit_products.csv")

st.header("💰 Profitability & Costs")
st.subheader("Category Profit Margin")
st.dataframe(category_profit_margin)

st.subheader("Product Profit Margin")
st.dataframe(product_profit_margin)

st.subheader("Region Profit Margin")
st.dataframe(region_profit_margin)

st.subheader("Low Profit Products")
st.dataframe(low_profit_products)

# ===========================
# 5. Marketing & Promotions
# ===========================
discount_sales = pd.read_csv("discount_sales.csv")
segment_discount_sales = pd.read_csv("segment_discount_sales.csv")

st.header("📢 Marketing & Promotions")
st.subheader("Sales by Discount Level")
st.dataframe(discount_sales)

st.subheader("Segment Responsiveness to Promotions")
fig_segment_discount = px.bar(segment_discount_sales, x="segment", y="sales", color="discount_bin", title="Sales by Segment & Discount")
st.plotly_chart(fig_segment_discount, use_container_width=True)

# ===========================
# 6. Strategic Insights
# ===========================
cross_sell_opportunities = pd.read_csv("cross_sell_opportunities.csv")
growth_customers = pd.read_csv("growth_customers.csv")
growth_regions = pd.read_csv("growth_regions.csv")

st.header("🚀 Strategic Insights")
st.subheader("Cross-Selling Opportunities")
st.dataframe(cross_sell_opportunities)

st.subheader("High-Growth Customers")
st.dataframe(growth_customers)

st.subheader("High-Growth Regions")
st.dataframe(growth_regions)