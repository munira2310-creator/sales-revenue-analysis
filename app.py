import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Sales Revenue Dashboard",
    page_icon="📊",
    layout="wide"
)

# ----------------------------
# Title
# ----------------------------
st.title("📊 Sales Revenue Analysis Dashboard")
st.markdown("Interactive dashboard for sales and profit insights")

# ----------------------------
# Load data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin1")
    return df

df = load_data()
st.dataframe(df.head())

# ----------------------------
# Sidebar filters
# ----------------------------
st.sidebar.header("🔎 Filter Data")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

# ----------------------------
# KPI Metrics
# ----------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("🧾 Total Orders", total_orders)

st.divider()

# ----------------------------
# Charts
# ----------------------------
st.subheader("📍 Profit by Region")

profit_by_region = (
    filtered_df.groupby("Region")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

fig1, ax1 = plt.subplots()
sns.barplot(
    x=profit_by_region.values,
    y=profit_by_region.index,
    ax=ax1
)
ax1.set_xlabel("Total Profit")
ax1.set_ylabel("Region")

st.pyplot(fig1)

# ----------------------------
st.subheader("📦 Sales by Category")

sales_by_category = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

fig2, ax2 = plt.subplots()
sns.barplot(
    x=sales_by_category.index,
    y=sales_by_category.values,
    ax=ax2
)
ax2.set_ylabel("Total Sales")
ax2.set_xlabel("Category")

st.pyplot(fig2)

# ----------------------------
# Data preview
# ----------------------------
st.subheader("📄 Data Preview")
st.dataframe(filtered_df.head(20))
