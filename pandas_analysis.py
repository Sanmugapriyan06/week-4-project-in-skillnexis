"""
Step 2 (Alternative): Data Analysis using Python Pandas
Project: End-to-End Business Performance Case Study

Note: Run this in Jupyter Notebook, Google Colab, or any Python environment with pandas installed.
"""

# import pandas as pd

def run_pandas_analysis():
    print("""
======================================================================
PANDAS ANALYSIS CODE SCRIPT
======================================================================
# 1. Load Cleaned Dataset
import pandas as pd
df = pd.read_csv('cleaned_sales_data.csv')

# 2. Key Metrics (KPIs)
total_revenue = df['Sales'].sum()
total_profit = df['Profit'].sum()
overall_margin = (total_profit / total_revenue) * 100
total_orders = df['Order_ID'].nunique()
total_customers = df['Customer_ID'].nunique()
avg_order_value = df['Sales'].mean()

print(f"Total Revenue:         ${total_revenue:,.2f}")
print(f"Total Profit:          ${total_profit:,.2f}")
print(f"Overall Profit Margin: {overall_margin:.2f}%")
print(f"Average Order Value:   ${avg_order_value:.2f}")

# 3. Category & Sub-Category Performance
cat_summary = df.groupby(['Category', 'Sub_Category']).agg(
    Order_Count=('Order_ID', 'count'),
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum')
).reset_index()
cat_summary['Profit_Margin_%'] = (cat_summary['Total_Profit'] / cat_summary['Total_Sales']) * 100
cat_summary = cat_summary.sort_values(by='Total_Profit', ascending=True)
print("\\n--- Sub-Category Profitability ---")
print(cat_summary.to_string(index=False))

# 4. Discount Impact Analysis
discount_analysis = df.groupby('Discount_Band').agg(
    Order_Count=('Order_ID', 'count'),
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Loss_Orders=('Profit', lambda x: (x < 0).sum())
).reset_index()
discount_analysis['Profit_Margin_%'] = (discount_analysis['Total_Profit'] / discount_analysis['Total_Sales']) * 100
print("\\n--- Discount Band Analysis ---")
print(discount_analysis.to_string(index=False))

# 5. Customer Segment Breakdown
segment_summary = df.groupby('Segment').agg(
    Orders=('Order_ID', 'count'),
    Revenue=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    AOV=('Sales', 'mean')
).reset_index()
segment_summary['Margin_%'] = (segment_summary['Profit'] / segment_summary['Revenue']) * 100
print("\\n--- Customer Segment Performance ---")
print(segment_summary.to_string(index=False))

# 6. Monthly Revenue Trend
monthly_trend = df.groupby('Order_Month').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Profit', 'sum')
).reset_index()
print("\\n--- Monthly Sales & Profit Trend (Head) ---")
print(monthly_trend.head(10).to_string(index=False))
""")

if __name__ == "__main__":
    run_pandas_analysis()

