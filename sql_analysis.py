"""
Step 2: Data Analysis using SQL (SQLite)
Project: End-to-End Business Performance Case Study
"""

import sqlite3
import csv

DB_FILE = "sales_analysis.db"
CSV_FILE = "cleaned_sales_data.csv"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    # Drop existing table if any
    cur.execute("DROP TABLE IF EXISTS orders;")
    
    cur.execute("""
    CREATE TABLE orders (
        order_id TEXT,
        order_date TEXT,
        ship_date TEXT,
        order_year INTEGER,
        order_month TEXT,
        ship_days INTEGER,
        ship_mode TEXT,
        customer_id TEXT,
        customer_name TEXT,
        segment TEXT,
        country TEXT,
        city TEXT,
        region TEXT,
        product_id TEXT,
        category TEXT,
        sub_category TEXT,
        sales REAL,
        quantity INTEGER,
        discount REAL,
        discount_band TEXT,
        profit REAL,
        profit_margin_pct REAL,
        profit_status TEXT
    );
    """)
    
    with open(CSV_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        to_insert = [
            (
                r["Order_ID"], r["Order_Date"], r["Ship_Date"], int(r["Order_Year"]),
                r["Order_Month"], int(r["Ship_Days"]), r["Ship_Mode"], r["Customer_ID"],
                r["Customer_Name"], r["Segment"], r["Country"], r["City"], r["Region"],
                r["Product_ID"], r["Category"], r["Sub_Category"], float(r["Sales"]),
                int(r["Quantity"]), float(r["Discount"]), r["Discount_Band"],
                float(r["Profit"]), float(r["Profit_Margin_Pct"]), r["Profit_Status"]
            )
            for r in reader
        ]
        
    cur.executemany("""
    INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, to_insert)
    
    conn.commit()
    print(f"Loaded {len(to_insert)} records into SQLite database '{DB_FILE}'.\n")
    return conn

def run_query(conn, title, sql_query):
    print("=" * 80)
    print(title)
    print("=" * 80)
    print("SQL Query:\n" + sql_query.strip() + "\n")
    cur = conn.cursor()
    cur.execute(sql_query)
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    
    # Print formatted table
    col_widths = [max(len(col), max((len(str(row[i])) for row in rows), default=0)) for i, col in enumerate(columns)]
    
    header = " | ".join(f"{col:<{col_widths[i]}}" for i, col in enumerate(columns))
    print(header)
    print("-" * len(header))
    for row in rows:
        print(" | ".join(f"{str(val):<{col_widths[i]}}" for i, val in enumerate(row)))
    print()

def main():
    conn = init_db()
    
    # Query 1: Executive KPI Summary
    q1 = """
    SELECT 
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(DISTINCT customer_id) AS total_customers,
        ROUND(SUM(sales), 2) AS total_revenue,
        ROUND(SUM(profit), 2) AS total_profit,
        ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
        ROUND(AVG(sales), 2) AS avg_order_value
    FROM orders;
    """
    run_query(conn, "QUERY 1: EXECUTIVE KPI SUMMARY", q1)

    # Query 2: Sub-Category Profitability (Identifying Loss Leaders)
    q2 = """
    SELECT 
        category,
        sub_category,
        COUNT(order_id) AS order_volume,
        ROUND(SUM(sales), 2) AS revenue,
        ROUND(SUM(profit), 2) AS profit,
        ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS margin_pct
    FROM orders
    GROUP BY category, sub_category
    ORDER BY profit ASC;
    """
    run_query(conn, "QUERY 2: SUB-CATEGORY PERFORMANCE & LOSS-MAKER DETECTION", q2)

    # Query 3: Discount Threshold Analysis (The Margin Destruction Effect)
    q3 = """
    SELECT 
        discount_band,
        COUNT(order_id) AS total_transactions,
        ROUND(SUM(sales), 2) AS total_revenue,
        ROUND(SUM(profit), 2) AS total_profit,
        ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
        SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) AS loss_making_orders
    FROM orders
    GROUP BY discount_band
    ORDER BY discount_band;
    """
    run_query(conn, "QUERY 3: IMPACT OF DISCOUNT BANDS ON PROFIT MARGINS", q3)

    # Query 4: Regional & Shipping Performance
    q4 = """
    SELECT 
        region,
        COUNT(order_id) AS orders,
        ROUND(SUM(sales), 2) AS revenue,
        ROUND(SUM(profit), 2) AS profit,
        ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS margin_pct,
        ROUND(AVG(ship_days), 1) AS avg_ship_days
    FROM orders
    GROUP BY region
    ORDER BY revenue DESC;
    """
    run_query(conn, "QUERY 4: REGIONAL REVENUE, MARGIN & AVERAGE SHIPPING TIME", q4)

    # Query 5: Monthly Sales and YoY Trend
    q5 = """
    SELECT 
        order_month,
        COUNT(order_id) AS orders_count,
        ROUND(SUM(sales), 2) AS monthly_revenue,
        ROUND(SUM(profit), 2) AS monthly_profit,
        ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS margin_pct
    FROM orders
    GROUP BY order_month
    ORDER BY order_month ASC
    LIMIT 12;
    """
    run_query(conn, "QUERY 5: MONTHLY PERFORMANCE TREND (FIRST 12 MONTHS)", q5)

    conn.close()

if __name__ == "__main__":
    main()

