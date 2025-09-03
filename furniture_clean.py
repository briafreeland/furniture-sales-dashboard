import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pymysql

"""
# ===========================
# 1. Load Dataset
# ===========================
file_path = "/Users/briafreeland/Desktop/SQL Projects Beginner/Furniture Sales Project/furniture_sales.csv"
df = pd.read_csv(file_path, encoding='latin1')

print("First 5 rows of data:")
print(df.head(), "\n")
# ===========================
# 2. Inspection
# ===========================
print("Dataset shape:", df.shape)
print("\nColumn info:") 
print(df.info(), "\n") 
print("Null values per column:")
print(df.isnull().sum(), "\n")

print("Duplicate rows:", df.duplicated().sum(), "\n")
# ===========================
# 3. Cleaning
# ===========================

# Drop duplicate rows
df.drop_duplicates(inplace=True)

# Standardize column names to snake_case
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Convert Order/Ship Date to datetime
if "order_date" in df.columns:
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
if "ship_date" in df.columns:
    df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")

# Handle text columns (strip spaces, title case)
text_cols = [
    "order_id", "ship_mode", "customer_id", "customer_name", 
    "segment", "country", "city", "state", "region", 
    "product_id", "category", "sub_category", "product_name"
]

for col in text_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title()

# Columns that should stay as floats
float_cols = ["sales", "discount", "profit"]

# Columns that should be integers
int_cols = ["row_id", "quantity", "postal_code"]

for col in float_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(",", "").str.replace("-", "0")
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(float)

for col in int_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(",", "").str.replace("-", "0")
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

# Check for duplicate column names
duplicates = df.columns[df.columns.duplicated()].tolist()
if duplicates:
    print("Duplicate columns found:", duplicates)
else:
    print("No duplicate columns found")
# ===========================
# 4. Final check
# ===========================
print("\nCleaned dataset info:")
print(df.info())
print("\nPreview of cleaned data:")
print(df.head())
# ===========================
# 5. Save cleaned data
# ===========================
df.to_csv("furniture_cleaned.csv", index=False)
print("\n Cleaned dataset saved as 'furniture_cleaned.csv'")

"""

# ===========================
# 6. Push to MySQL
# ===========================
# Load cleaned CSV
df = pd.read_csv("/Users/briafreeland/Desktop/SQL Projects Beginner/Furniture Sales Project/furniture_cleaned.csv")

# Update these credentials
username = "root"
password = quote_plus("BFree2013!")
host = "localhost"
database = "furniture_sales_project"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")

df.to_sql("furniture_sales", con=engine, if_exists="replace", index=False)

print("Data cleaned and loaded into MySQL (table: furniture_sales)")