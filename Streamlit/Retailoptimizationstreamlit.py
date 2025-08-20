import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import ast
import logging

# ------------- Streamlit Config ---------------
st.set_page_config(layout="wide", page_title="Retail Promotions Dashboard")
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                    format='%(asctime)s %(levelname)s:%(message)s')

# ------------- Load Data -------------------
logging.info('---- Loading data from csv file ---- ')

try:
        df = pd.read_csv('retail_promo.csv')
        df['sales'] = df['total_cost'] * df['total_items']
        df['profit'] = df['sales'] - df['total_cost']
        df['profit_margin'] = df['profit'] / df['sales'] * 100
        df['promotion'] = df['promotion'].fillna('None')
        df['Year'] = pd.to_datetime(df['date']).dt.year
        df['product'] = df['product'].apply(ast.literal_eval)
        df_exploded = df.explode('product')
        # Category mapping
        product_categories = {
            'Groceries': ['Ketchup', 'Milk', 'Bread', 'Potatoes', 'Spinach', 'Chicken', 'Honey', 'BBQ Sauce', 'Soda', 'Cheese', 'Jam', 'Rice'],
            'Personal Care': ['Toothpaste', 'Soap', 'Shampoo', 'Shaving Cream', 'Deodorant', 'Diapers'],
            'Household Goods': ['Iron', 'Toilet Paper', 'Laundry Detergent', 'Sponges'],
            'Home & Garden': ['Garden Hose', 'Extension Cords', 'Lawn Mower']
        }
        product_mapping = {product: cat for cat, plist in product_categories.items() for product in plist}
        df_exploded['product_category'] = df_exploded['product'].map(product_mapping)
        df_exploded['season'] = pd.to_datetime(df_exploded['date']).dt.month % 12 // 3 + 1
        season_map = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
        df_exploded['season'] = df_exploded['season'].map(season_map)
        
except Exception as e:
    logging.error(f'error loading Data : {e}')
    st.error(f'Data loading Failed {e}')
else:
        logging.info('-- Data loaded Successfully-- ')
        st.info('-- Data loaded -- ')


# ------------- App Title -------------------
st.title("📊 Optimizing Retail Promotions & Product Mix")
st.markdown("Analyze and optimize retail promotion strategies, products, store performance, and customer targeting.")

st.sidebar.header("🔎 Filter Data")
available_years = sorted(df['Year'].unique())
selected_year = st.sidebar.selectbox("Select Year", available_years)

filtered_df = df[df['Year'] == selected_year]

st.markdown(f"## 📊 Key Business Metrics for {selected_year}")

# Compute KPIs from filtered data
total_sales = filtered_df['sales'].sum()
total_profit = filtered_df['profit'].sum()
avg_profit_margin = filtered_df['profit_margin'].mean()
top_promotion = filtered_df[filtered_df['promotion'] != 'None'].groupby('promotion')['sales'].sum().idxmax()
top_promo_sales = filtered_df[filtered_df['promotion'] == top_promotion]['sales'].sum()

# Format numbers
def format_currency(value):
    return f"${value/1_000_000:.2f}M" if value >= 1_000_000 else f"${value/1_000:.1f}K"

# Display KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🛒 Total Sales", format_currency(total_sales))

with col2:
    st.metric("💰 Total Profit", format_currency(total_profit))

with col3:
    st.metric("📈 Avg Profit Margin", f"{avg_profit_margin:.2f}%")

with col4:
    st.metric("🏷️ Top Promotion", top_promotion, delta=format_currency(top_promo_sales))


# ------------- Promotion Uplift Analysis -------------------
st.header("🚀 Promotion Uplift Analysis")

def promotion_uplift():
    category_store_perf = df.groupby(['customer_category', 'store_type', 'promotion'])['sales'].sum().reset_index()
    baseline_df = category_store_perf[category_store_perf['promotion'] == 'None']
    baseline_df = baseline_df.rename(columns={'sales': 'baseline_sales'})[['customer_category', 'store_type', 'baseline_sales']]
    merged = category_store_perf.merge(baseline_df, on=['customer_category', 'store_type'], how='left')
    merged['Uplift_%'] = ((merged['sales'] - merged['baseline_sales']) / merged['baseline_sales']) * 100
    top_uplift = merged[(merged['Uplift_%'] > 0) & (merged['promotion'] != 'None')]
    top_uplift = top_uplift.groupby('promotion').apply(lambda x: x.nlargest(3, 'Uplift_%')).reset_index(drop=True)

    fig = px.bar(top_uplift, x='customer_category', y='Uplift_%', color='promotion', text_auto=True)
    fig.update_layout(title="Top Promotion Uplifts by Customer Category", xaxis_title="Customer Category", yaxis_title="Uplift (%)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### **Key Insights**")
    st.markdown(''' 
* **Best Performing Promotion:**
    * "Discount on Selected Items" for Professionals in Warehouse Club: +5.12% uplift.
    * Strong alignment between product mix, bulk buying, and targeted discounts.
* **BOGO for Teenagers:**
    * BOGO in Convenience Stores has +4.04% uplift.
    * Highly effective for impulse-buy behavior.
* **Moderate Impact Promotions:**
    * Middle-aged in Specialty Stores (BOGO): +2.31%
    * Homemakers in Discount Stores (Selected Items): +2.92%
* **Insight:**
    * Targeted promotions outperform blanket campaigns.
''')

promotion_uplift()

# ------------- Product Profitability -------------------
st.header("🛒 Product Profitability by Season")

def format_number(val):
    if pd.isna(val):
        return "N/A"
    if abs(val) >= 1_000_000:
        return f"{val / 1_000_000:.2f}M"
    elif abs(val) >= 1_000:
        return f"{val / 1_000:.2f}K"
    return f"{val:.2f}"

def product_by_season():
    season_perf = df_exploded.groupby(['season', 'product']).agg({'sales': 'sum', 'profit': 'sum'})
    top_perf = season_perf.groupby(level=0, group_keys=False).apply(lambda x: x.nlargest(3, 'profit'))
    top_perf['sales'] = top_perf['sales'].apply(format_number)
    top_perf['profit'] = top_perf['profit'].apply(format_number)
    st.dataframe(top_perf)

product_by_season()

st.markdown('''### **Product and Category Profitability Analysis**

* **Toothpaste** is the highest performing product across all seasons with profits around $4.3M.
* **Seasonal Trends:**
    * **Fall:** Ironing Boards, Air Fresheners follow.
    * **Spring:** Soap and Yogurt are next best.
    * **Summer:** Extension Cords and Ice Cream rise in popularity.
    * **Winter:** Insect Repellent and Oranges gain importance.
''')

# ------------- Category Heatmap -------------------
st.header("📦 Product Category Heatmap")

def category_heatmap():
    season_perf = df_exploded.groupby(['season', 'product_category']).agg({'profit': 'sum'}).reset_index()
    pivot = season_perf.pivot(index='season', columns='product_category', values='profit')
    fig = px.imshow(pivot, text_auto=True, color_continuous_scale='Viridis', aspect='auto')
    st.plotly_chart(fig, use_container_width=True)

category_heatmap()

st.markdown('''
### **Product Category Insights 📈**

* **Groceries** are the most profitable: ~ $90M consistently across all seasons.
* **Household Goods** and **Personal Care** trail behind at ~$40M and ~$32M respectively.
* **Profitability is stable across all seasons**, showing consistent demand.
''')

# ------------- Customer Category Response -------------------
st.header("👥 Customer Response to Promotions")

def customer_response():
    promo_perf = df.groupby(['promotion', 'customer_category', 'store_type'])['sales'].sum().reset_index()
    baseline = promo_perf[promo_perf['promotion'] == 'None'][['customer_category', 'sales']]
    baseline = baseline.rename(columns={'sales': 'baseline_sales'})
    merged = promo_perf.merge(baseline, on='customer_category', how='left')
    merged['Uplift_%'] = ((merged['sales'] - merged['baseline_sales']) / merged['baseline_sales']) * 100
    uplift = merged[(merged['promotion'] != 'None') & (merged['Uplift_%'] > 0)]
    top_customers = uplift.groupby('customer_category').apply(lambda x: x.nlargest(1, 'Uplift_%')).reset_index(drop=True)

    fig = px.bar(top_customers, x='customer_category', y='Uplift_%', color='promotion', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

customer_response()

st.markdown('''
### **Customer Response to Promotions**

* **BOGO is highly effective**:
    * Teenagers and Professionals show strong uplift (~4%) in Convenience Stores and Pharmacies.
* **Discounts depend on context**:
    * “Selected Items” has highest uplift (+5.15%) for Professionals in Pharmacies.
''')

# ------------- Store & Payment Profit -------------------
st.header("🏬 Store & Payment Method Profitability (by Profit)")

def store_payment_analysis():
    store_perf = df_exploded.groupby('store_type').agg({'profit': 'sum'}).reset_index()
    fig1 = px.bar(store_perf, x='store_type', y='profit', title="Profit by Store Type", text_auto=True)
    fig1.update_layout(xaxis_title="Store Type", yaxis_title="Profit")
    st.plotly_chart(fig1, use_container_width=True)

    pay_perf = df_exploded.groupby('payment_method').agg({'profit': 'sum'}).reset_index()
    fig2 = px.bar(pay_perf, x='payment_method', y='profit', title="Profit by Payment Method", text_auto=True)
    fig2.update_layout(xaxis_title="Payment Method", yaxis_title="Profit")
    st.plotly_chart(fig2, use_container_width=True)

store_payment_analysis()

st.markdown('''
### **Store Type and Payment Method Performance Analysis**

* **All store types and payment methods perform consistently** in terms of total profit.
* No single store or method dominates, suggesting **balanced operations** across channels.
''')

# ------------- Recommendations -------------------
st.markdown('''
# ✅ **Final Recommendations**

---

### **1. Promotion Strategy**

* Focus on **targeted promotions** for customer+store combinations instead of general campaigns.
* **Top-performing promotions:**
    * "Discount on Selected Items" — Professionals in Warehouse/Pharmacy (+5.12%, +5.15%)
    * BOGO — Teenagers in Convenience Stores (~+4%)

---

### **2. Product Optimization**

* **Toothpaste** consistently performs best (~$4.3M profit)
* **Seasonal Focus**:
    * Fall: Ironing Boards, Air Fresheners
    * Spring: Soap, Yogurt
    * Summer: Extension Cords, Ice Cream
    * Winter: Oranges, Insect Repellent

---

### **3. Store and Payment Channels**

* Profits are **evenly distributed** across store types and payment methods.
* No urgent need to shift store or payment strategies—focus on promotions and products instead.
''')
# ------------- Footer -------------------
st.markdown("---")
st.markdown("© 2025 Retail Optimization | Streamlit App created by Harshit kharka")