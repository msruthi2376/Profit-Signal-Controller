import streamlit as st
import pandas as pd
import plotly.express as px

# Set Page Config
st.set_page_config(page_title="AI Profit Control Agent", layout="wide")

# --- Title and Description ---
st.title("🤖 AI Profit Control Agent")
st.markdown("""
This agent monitors sales data, identifies low-margin transactions, 
and provides strategic pricing recommendations.
""")

# --- Data Loading Logic ---
@st.cache_data
def load_and_process_data(file_path):
    # Load data with appropriate encoding
    df = pd.read_csv(file_path, encoding='unicode_escape')
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
    
    # AI Logic: Calculate Estimated Profit (assuming Cost is 70% of MSRP)
    df['ESTIMATED_COST'] = df['MSRP'] * 0.70
    df['TOTAL_COST'] = df['QUANTITYORDERED'] * df['ESTIMATED_COST']
    df['PROFIT'] = df['SALES'] - df['TOTAL_COST']
    df['MARGIN_PERCENT'] = (df['PROFIT'] / df['SALES']) * 100
    
    return df

# Load the file
try:
    df = load_and_process_data('sales_data_sample.csv')
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# --- Sidebar Filters ---
st.sidebar.header("Filter Controls")
selected_country = st.sidebar.multiselect("Select Country", options=df['COUNTRY'].unique(), default=df['COUNTRY'].unique())
selected_product = st.sidebar.multiselect("Select Product Line", options=df['PRODUCTLINE'].unique(), default=df['PRODUCTLINE'].unique())

# Filter data
filtered_df = df[df['COUNTRY'].isin(selected_country) & df['PRODUCTLINE'].isin(selected_product)]

# --- KPI Dashboard ---
col1, col2, col3, col4 = st.columns(4)
total_sales = filtered_df['SALES'].sum()
total_profit = filtered_df['PROFIT'].sum()
avg_margin = filtered_df['MARGIN_PERCENT'].mean()
low_margin_count = len(filtered_df[filtered_df['MARGIN_PERCENT'] < 15])

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Estimated Profit", f"${total_profit:,.0f}", delta=f"{avg_margin:.1f}% Margin")
col3.metric("Avg Margin %", f"{avg_margin:.2f}%")
col4.metric("At-Risk Orders", low_margin_count, delta_color="inverse")

# --- Visualizations ---
st.subheader("Profit Analysis by Segment")
c1, c2 = st.columns(2)

with c1:
    fig_prod = px.bar(filtered_df.groupby('PRODUCTLINE')['PROFIT'].sum().reset_index(), 
                     x='PRODUCTLINE', y='PROFIT', title="Profit by Product Line",
                     color='PROFIT', color_continuous_scale='Viridis')
    st.plotly_chart(fig_prod, use_container_width=True)

with c2:
    fig_geo = px.choropleth(filtered_df.groupby('COUNTRY')['PROFIT'].sum().reset_index(),
                           locations="COUNTRY", locationmode='country names',
                           color="PROFIT", title="Global Profit Heatmap")
    st.plotly_chart(fig_geo, use_container_width=True)

# --- AI AGENT INSIGHTS ---
st.divider()
st.subheader("💡 AI Profit Agent Insights")

insights = []

# Logic 1: Identifying the worst performing product line
worst_line = filtered_df.groupby('PRODUCTLINE')['MARGIN_PERCENT'].mean().idxmin()
worst_val = filtered_df.groupby('PRODUCTLINE')['MARGIN_PERCENT'].mean().min()
insights.append(f"⚠️ **Profit Leak Detected:** The **{worst_line}** line has the lowest average margin ({worst_val:.1f}%). Consider reviewing its supply chain costs.")

# Logic 2: Pricing Efficiency
avg_efficiency = (filtered_df['PRICEEACH'] / filtered_df['MSRP']).mean() * 100
if avg_efficiency < 90:
    insights.append(f"📉 **Pricing Warning:** Items are selling at {avg_efficiency:.1f}% of MSRP on average. Discounts may be too aggressive.")
else:
    insights.append(f"✅ **Pricing Health:** Selling prices are maintained at {avg_efficiency:.1f}% of MSRP.")

# Logic 3: High Volume / Low Profit alert
for insight in insights:
    st.info(insight)

# --- Raw Data View ---
with st.expander("View Filtered Data"):
    st.dataframe(filtered_df)
