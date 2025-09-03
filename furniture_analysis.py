import pandas as pd
from collections import Counter
from itertools import combinations

# ===========================
# 1. Load cleaned dataset
# ===========================
df = pd.read_csv("furniture_cleaned.csv")

# -- Have to convert to date time again, because it reads as a string once csv was saved --
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")

# Drop rows that still failed to convert
df = df.dropna(subset=["order_date"])


# Extract year, month, and quarter for grouping
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["quarter"] = df["order_date"].dt.quarter

"""
# ===========================
# 2. Sales & Revenue Performance
# ===========================
# ---- Total revenue over entire dataset ----
total_revenue = df["sales"].sum()
print("Total Revenue (All Time):", f"${total_revenue:,.2f}", "\n")

# ---- Total revenue over a specific time period ----
# Example: revenue in 2017
start_date = "2017-01-01"
end_date = "2017-12-31"

mask = (df["order_date"] >= start_date) & (df["order_date"] <= end_date)
total_revenue = df.loc[mask, "sales"].sum()
print(f"Total Revenue from {start_date} to {end_date}: ${total_revenue:,.2f}")


# ---- Product that generates the highest sales ----
top_product = (
    df.groupby("product_name")["sales"]
    .sum()
    .reset_index()
    .sort_values(by="sales", ascending=False)
    .head(1)
)
print("Top Product by Sales:\n", top_product, "\n")

# ---- Product categories that are most profitable ----
top_category = (
    df.groupby("category")["profit"]
    .sum()
    .reset_index()
    .sort_values(by="profit", ascending=False)
    .head(1)
)
print("Most Profitable Category:\n", top_category, "\n")

# Export results to CSV for dashboard
top_product.to_csv("top_product.csv", index=False)
top_category.to_csv("top_category.csv", index=False)

# ===========================
# 3. Customer Insights
# ===========================
# Top customers by total revenue
top_customers = (
    df.groupby(["customer_id", "customer_name"])["sales"]
    .sum()
    .reset_index()
    .sort_values(by="sales", ascending=False)
)

print("Top Customers by Revenue:")
print(top_customers.head(10))  # top 10 customers

# export for dashboard
top_customers.to_csv("top_customers.csv", index=False)

# Count of purchases per customer per month
repeat_purchases = (
    df.groupby(["customer_id", "customer_name", "year", "month"])["order_id"]
    .nunique()  # number of unique orders
    .reset_index(name="num_orders")
)

print("Repeat Purchase Patterns (Sample):")
print(repeat_purchases.head(10))

# export for dashboard
repeat_purchases.to_csv("repeat_purchases.csv", index=False)

# ================================
# 4. Regional & Store Performance
# ================================
# Top regions by total sales
top_regions = df.groupby("region")["sales"].sum().reset_index()
top_regions = top_regions.sort_values(by="sales", ascending=False)
print("Top Regions by Sales:")
print(top_regions)

# Top cities by total sales
top_cities = df.groupby("city")["sales"].sum().reset_index()
top_cities = top_cities.sort_values(by="sales", ascending=False)
print("\n Top Cities by Sales:")
print(top_cities)

# Export for dashboard
top_regions.to_csv("top_regions.csv", index=False)
top_cities.to_csv("top_cities.csv", index=False)

# Sales per region per year
region_year_sales = df.groupby(["region", "year"])["sales"].sum().reset_index()

# Calculate year-over-year growth per region
region_year_sales["sales_growth"] = region_year_sales.groupby("region")["sales"].pct_change() * 100

print("\n Region Sales Growth (YoY %):")
print(region_year_sales)

# Export for dashboard
region_year_sales.to_csv("region_year_sales_growth.csv", index=False)

# Sales by region and product
region_product_sales = df.groupby(["region", "product_name"])["sales"].sum().reset_index()
region_product_sales = region_product_sales.sort_values(["region", "sales"], ascending=[True, False])

print("\n Regional Product Preferences (Top 5 per region):")
for region in region_product_sales["region"].unique():
    top_products = region_product_sales[region_product_sales["region"] == region].head(5)
    print(f"\nRegion: {region}")
    print(top_products)

# Export for dashboard
region_product_sales.to_csv("region_product_sales.csv", index=False)

# ===============================================
# 5. Profitability & Cost/Inventory & Operations
# ===============================================
# Group by region
region_profit_margin = df.groupby("region").agg({"sales": "sum", "profit": "sum"}).reset_index()
region_profit_margin["profit_margin_pct"] = (region_profit_margin["profit"] / region_profit_margin["sales"]) * 100

print("Profit Margin by Region:")
print(region_profit_margin)

# Export for dashboard
region_profit_margin.to_csv("region_profit_margin.csv", index=False)

# Group by product
product_profit_margin = df.groupby("product_name").agg({"sales": "sum", "profit": "sum"}).reset_index()
product_profit_margin["profit_margin_pct"] = (product_profit_margin["profit"] / product_profit_margin["sales"]) * 100

print("\n Profit Margin by Product:")
print(product_profit_margin.sort_values("profit_margin_pct", ascending=False).head(10))

# Export for dashboard
product_profit_margin.to_csv("product_profit_margin.csv", index=False)

# Group by category
category_profit_margin = df.groupby("category").agg({"sales": "sum", "profit": "sum"}).reset_index()
category_profit_margin["profit_margin_pct"] = (category_profit_margin["profit"] / category_profit_margin["sales"]) * 100

print("\n Profit Margin by Category:")
print(category_profit_margin.sort_values("profit_margin_pct", ascending=False))

# Export for dashboard
category_profit_margin.to_csv("category_profit_margin.csv", index=False)

# Low profit products
# Products with negative or very low profit margin (e.g., less than 5%)
low_profit_products = product_profit_margin[product_profit_margin["profit_margin_pct"] < 5].sort_values("profit_margin_pct")

print("\n Products Not Making Much Profit:")
print(low_profit_products)

# Export for dashboard
low_profit_products.to_csv("low_profit_products.csv", index=False)

# ==========================
# 6. Marketing & Promotions
# ==========================
# Create discount bins
df["discount_bin"] = pd.cut(df["discount"],
                            bins=[-0.01, 0, 0.1, 0.25, 0.5, 1],
                            labels=["0%", "0-10%", "10-25%", "25-50%", "50%+"])

# Group sales by discount bin
discount_sales = df.groupby("discount_bin", observed=True)["sales"].sum().reset_index().sort_values(by="sales", ascending=False)

print("Sales by Discount Level:")
print(discount_sales)

# Export for dashboard
discount_sales.to_csv("discount_sales.csv", index=False)

# Sales by customer segment and discount bin
segment_discount_sales = df.groupby(
    ["segment", "discount_bin"], observed=True
)["sales"].sum().reset_index()

print("\nSegment Responsiveness to Promotions:")
print(segment_discount_sales)

# Export for dashboard
segment_discount_sales.to_csv("segment_discount_sales.csv", index=False)

"""
# ==========================
# 7. Strategic Insights
# ==========================
# Potential for cross-selling
# Create a "basket" per order
basket = df.groupby("order_id")["product_name"].apply(list)

# Count product co-occurrences
co_occurrence = Counter()
for products in basket:
    # Count every pair of products bought together
    co_occurrence.update(combinations(sorted(products), 2))

# Convert to DataFrame
cross_sell_df = pd.DataFrame(
    [(k[0], k[1], v) for k, v in co_occurrence.items()],
    columns=["Product_A", "Product_B", "Co_Purchase_Count"]
).sort_values(by="Co_Purchase_Count", ascending=False)

print("Top Product Pairs for Cross-Selling:")
print(cross_sell_df.head(10))

# Export for dashboard
cross_sell_df.to_csv("cross_sell_opportunities.csv", index=False)

# High growth regions
# Load pre-calculated region growth
region_year_sales = pd.read_csv("region_year_sales_growth.csv")

latest_year = region_year_sales["year"].max()
growth_regions = region_year_sales[region_year_sales["year"] == latest_year].sort_values("sales_growth", ascending=False)

print(f"\n Regions with Highest Growth in {latest_year}:")
print(growth_regions)

# Save to CSV for dashboard
growth_regions.to_csv("growth_regions.csv", index=False)

# Customers growth opportunities 
# Load repeat purchase data
repeat_purchases = pd.read_csv("repeat_purchases.csv")

latest_year = repeat_purchases["year"].max()
growth_customers = repeat_purchases[repeat_purchases["year"] == latest_year].sort_values("num_orders", ascending=False)

print(f"\n Customers with Highest Purchase Growth in {latest_year}:")
print(growth_customers.head(10))

# Save to CSV for dashboard
growth_customers.to_csv("growth_customers.csv", index=False)
