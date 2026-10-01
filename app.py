import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="PharmEasy Regional Pulse", layout="wide")

conn = sqlite3.connect('pharmeasy.db')
orders = pd.read_sql("SELECT * FROM orders_clean", conn)
orders['month'] = orders['order_date'].str.slice(0, 7)

flagged_apr_may = ['Bengaluru', 'Guntur', 'Hyderabad', 'Karimnagar', 'Tirupati', 'Visakhapatnam', 'Warangal']
#REGION FILTER DROPDOWN
region_list = ["All regions"] + sorted(orders['region'].unique())
selected_region = st.selectbox("Filter by region", region_list)

if selected_region == "All regions":
    filtered = orders
else:
    filtered = orders[orders['region'] == selected_region]

#TASK 4.2 EXECUTIVE SUMMARY
st.title("PharmEasy Regional Pulse")

st.markdown(f"""
**Executive summary:** Across April–June 2026, the nine active regions generated a combined
**Rs {orders['sales_inr'].sum():,.2f}** in sales and **Rs {orders['profit_inr'].sum():,.2f}** in profit
across **{orders['order_id'].nunique():,}** distinct orders. Guntur's April→May sales jumped
**+122.19%**, the largest swing of any region this quarter, while **Medical Devices** remains the
top-selling category overall. 7 of 9 regions moved enough in April→May to clear the 8% review
threshold and warrant a closer look. See the charts and detail table below for the full breakdown.
""")
# 3 KPI CARDS
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales (INR)", f"Rs {filtered['sales_inr'].sum():,.2f}")
col2.metric("Total Profit (INR)", f"Rs {filtered['profit_inr'].sum():,.2f}")
col3.metric("Total Orders", filtered['order_id'].nunique())

#BAR CHART
st.subheader("Total sales by region")
bar_df = filtered.groupby('region')['sales_inr'].sum().reset_index().sort_values('sales_inr', ascending=False)
colors = ['#D62728' if r in flagged_apr_may else '#4C78A8' for r in bar_df['region']]
fig_bar = go.Figure(go.Bar(x=bar_df['region'], y=bar_df['sales_inr'], marker_color=colors))
fig_bar.update_layout(
    title='Which regions drive total sales? (red = flagged Apr→May)',
    xaxis_title='Region',
    yaxis_title='Total sales (INR)',
    yaxis=dict(rangemode='tozero')
)
st.plotly_chart(fig_bar, use_container_width=True)

#LINE CHART
st.subheader("Monthly sales trend by region")
detail = filtered.groupby(['region', 'month']).agg(
    total_sales=('sales_inr', 'sum'),
    total_profit=('profit_inr', 'sum'),
    order_count=('order_id', 'nunique')
).reset_index()

fig_line = go.Figure()
for region in sorted(detail['region'].unique()):
    sub = detail[detail['region'] == region]
    is_flagged = region in flagged_apr_may
    fig_line.add_trace(go.Scatter(
        x=sub['month'],
        y=sub['total_sales'],
        mode='lines+markers',
        name=region,
        line=dict(color='#D62728' if is_flagged else '#4C78A8')
    ))

fig_line.update_layout(
    title='Which regions moved most from April to June? (red = flagged Apr→May)',
    xaxis_title='Month',
    yaxis_title='Total sales (INR)',
    yaxis=dict(rangemode='tozero'),
    xaxis=dict(type='category')
)
st.plotly_chart(fig_line, use_container_width=True)

#PIE CHART
st.subheader("Sales share by category")
category_sales = filtered.groupby('category')['sales_inr'].sum().reset_index()
fig_pie = px.pie(
    category_sales,
    names='category',
    values='sales_inr',
    title='Which categories drive revenue?',
    hole=0.4
)
fig_pie.update_traces(textinfo='percent+label')
st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("Detail: region x month")
st.dataframe(detail)
