"""
Step 1: Data Cleaning and Exploratory Data Analysis (Python)
Project: End-to-End Business Performance Case Study
"""

import csv
import datetime
from collections import defaultdict

input_file = "business_sales_data.csv"
output_file = "cleaned_sales_data.csv"

def parse_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

def main():
    print("=" * 60)
    print("STEP 1: DATA CLEANING & EXPLORATION")
    print("=" * 60)

    rows = []
    missing_count = 0
    duplicate_ids = set()
    seen_ids = set()

    with open(input_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check for duplicates
            oid = row["Order_ID"]
            if oid in seen_ids:
                duplicate_ids.add(oid)
            seen_ids.add(oid)

            # Check for nulls / missing fields
            if any(val is None or str(val).strip() == "" for val in row.values()):
                missing_count += 1
                continue

            # Data type parsing & validation
            try:
                o_date = parse_date(row["Order_Date"])
                s_date = parse_date(row["Ship_Date"])
                sales = float(row["Sales"])
                qty = int(row["Quantity"])
                discount = float(row["Discount"])
                profit = float(row["Profit"])
            except ValueError as e:
                print(f"Skipping malformed row {oid}: {e}")
                continue

            # Feature Engineering:
            # 1. Shipping lead time in days
            ship_days = (s_date - o_date).days
            
            # 2. Profit margin percentage
            profit_margin = round((profit / sales) * 100, 2) if sales > 0 else 0.0
            
            # 3. Discount Band
            if discount == 0:
                discount_band = "0% None"
            elif discount <= 0.10:
                discount_band = "1% - 10% Low"
            elif discount <= 0.20:
                discount_band = "11% - 20% Medium"
            else:
                discount_band = "> 20% High"

            # 4. Profitability Status
            profit_status = "Profitable" if profit >= 0 else "Loss-making"

            # 5. Order Year and Month
            order_year = o_date.year
            order_month = o_date.strftime("%Y-%m")

            row_cleaned = {
                "Order_ID": oid,
                "Order_Date": row["Order_Date"],
                "Ship_Date": row["Ship_Date"],
                "Order_Year": order_year,
                "Order_Month": order_month,
                "Ship_Days": ship_days,
                "Ship_Mode": row["Ship_Mode"],
                "Customer_ID": row["Customer_ID"],
                "Customer_Name": row["Customer_Name"],
                "Segment": row["Segment"],
                "Country": row["Country"],
                "City": row["City"],
                "Region": row["Region"],
                "Product_ID": row["Product_ID"],
                "Category": row["Category"],
                "Sub_Category": row["Sub_Category"],
                "Sales": sales,
                "Quantity": qty,
                "Discount": discount,
                "Discount_Band": discount_band,
                "Profit": profit,
                "Profit_Margin_Pct": profit_margin,
                "Profit_Status": profit_status
            }
            rows.append(row_cleaned)

    print(f"Total Raw Rows Processed: {len(rows)}")
    print(f"Missing/Null Values Dropped: {missing_count}")
    print(f"Duplicate Order IDs Detected: {len(duplicate_ids)}")

    # Write cleaned CSV
    fieldnames = list(rows[0].keys())
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Cleaned dataset successfully exported to: {output_file}\n")

    # High-level EDA Summary
    total_sales = sum(r["Sales"] for r in rows)
    total_profit = sum(r["Profit"] for r in rows)
    overall_margin = (total_profit / total_sales) * 100
    loss_count = sum(1 for r in rows if r["Profit"] < 0)

    print("-" * 60)
    print("EXPLORATORY DATA ANALYSIS (EDA) HIGHLIGHTS:")
    print("-" * 60)
    print(f"Total Revenue:         ${total_sales:,.2f}")
    print(f"Total Profit:          ${total_profit:,.2f}")
    print(f"Overall Profit Margin: {overall_margin:.2f}%")
    print(f"Total Orders:          {len(rows):,}")
    print(f"Loss-making Orders:    {loss_count} ({loss_count/len(rows)*100:.1f}%)")

    # Segment Performance
    print("\n--- Sales & Profit by Customer Segment ---")
    seg_stats = defaultdict(lambda: {"sales": 0.0, "profit": 0.0, "count": 0})
    for r in rows:
        seg_stats[r["Segment"]]["sales"] += r["Sales"]
        seg_stats[r["Segment"]]["profit"] += r["Profit"]
        seg_stats[r["Segment"]]["count"] += 1

    for seg, data in sorted(seg_stats.items(), key=lambda x: x[1]["sales"], reverse=True):
        margin = (data["profit"] / data["sales"]) * 100
        aov = data["sales"] / data["count"]
        print(f"{seg:<15}: Sales = ${data['sales']:>10,.2f} | Profit = ${data['profit']:>9,.2f} | Margin = {margin:>5.1f}% | AOV = ${aov:>6.2f}")

    # Category Performance
    print("\n--- Sales & Profit by Category ---")
    cat_stats = defaultdict(lambda: {"sales": 0.0, "profit": 0.0})
    for r in rows:
        cat_stats[r["Category"]]["sales"] += r["Sales"]
        cat_stats[r["Category"]]["profit"] += r["Profit"]

    for cat, data in sorted(cat_stats.items(), key=lambda x: x[1]["sales"], reverse=True):
        margin = (data["profit"] / data["sales"]) * 100
        print(f"{cat:<16}: Sales = ${data['sales']:>10,.2f} | Profit = ${data['profit']:>9,.2f} | Margin = {margin:>5.1f}%")

    # Discount Impact
    print("\n--- Profit Margin by Discount Band ---")
    disc_stats = defaultdict(lambda: {"sales": 0.0, "profit": 0.0, "count": 0})
    for r in rows:
        disc_stats[r["Discount_Band"]]["sales"] += r["Sales"]
        disc_stats[r["Discount_Band"]]["profit"] += r["Profit"]
        disc_stats[r["Discount_Band"]]["count"] += 1

    for band in sorted(disc_stats.keys()):
        data = disc_stats[band]
        margin = (data["profit"] / data["sales"]) * 100
        print(f"{band:<18}: Orders = {data['count']:>4} | Sales = ${data['sales']:>10,.2f} | Profit = ${data['profit']:>9,.2f} | Margin = {margin:>6.1f}%")

if __name__ == "__main__":
    main()

