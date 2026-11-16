import csv
import random
import datetime

# Set seed for reproducible results
random.seed(42)

start_date = datetime.date(2023, 1, 1)

categories = {
    'Technology': ['Phones', 'Accessories', 'Laptops', 'Printers'],
    'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
    'Office Supplies': ['Binders', 'Paper', 'Storage', 'Appliances', 'Art']
}

segments = ['Consumer', 'Corporate', 'Home Office']
regions = {
    'East': ['New York', 'Philadelphia', 'Boston'],
    'West': ['Los Angeles', 'San Francisco', 'Seattle'],
    'Central': ['Chicago', 'Detroit', 'Houston'],
    'South': ['Atlanta', 'Miami', 'Charlotte']
}
ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']

rows = []
for i in range(1, 2501):
    order_id = f"ORD-2023-{i:04d}"
    days_offset = random.randint(0, 720) # over 2 years of data
    o_date = start_date + datetime.timedelta(days=days_offset)
    lead_time = random.choices([1, 2, 3, 4, 5, 6, 7], weights=[0.1, 0.2, 0.3, 0.2, 0.1, 0.05, 0.05])[0]
    s_date = o_date + datetime.timedelta(days=lead_time)
    
    ship_mode = random.choices(ship_modes, weights=[0.6, 0.2, 0.15, 0.05])[0]
    cust_num = random.randint(101, 380)
    cust_id = f"CUST-{cust_num:03d}"
    cust_name = f"Client {cust_num}"
    seg = random.choices(segments, weights=[0.52, 0.30, 0.18])[0]
    
    reg = random.choice(list(regions.keys()))
    city = random.choice(regions[reg])
    cat = random.choice(list(categories.keys()))
    sub_cat = random.choice(categories[cat])
    prod_id = f"PROD-{cat[:3].upper()}-{random.randint(10, 99)}"
    
    qty = random.randint(1, 8)
    if cat == 'Technology':
        base_unit_price = random.uniform(80, 500)
        cogs_rate = random.uniform(0.55, 0.65)
    elif cat == 'Furniture':
        base_unit_price = random.uniform(50, 350)
        cogs_rate = random.uniform(0.75, 0.90)  # High cost of goods sold
    else: # Office Supplies
        base_unit_price = random.uniform(10, 80)
        cogs_rate = random.uniform(0.45, 0.55)

    disc = random.choices(
        [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50],
        weights=[0.35, 0.15, 0.15, 0.10, 0.10, 0.08, 0.04, 0.03]
    )[0]
    
    gross_sales = base_unit_price * qty
    sales = round(gross_sales * (1 - disc), 2)
    cost = round(gross_sales * cogs_rate, 2)
    profit = round(sales - cost, 2)
    
    rows.append([
        order_id,
        o_date.strftime('%Y-%m-%d'),
        s_date.strftime('%Y-%m-%d'),
        ship_mode,
        cust_id,
        cust_name,
        seg,
        'United States',
        city,
        reg,
        prod_id,
        cat,
        sub_cat,
        sales,
        qty,
        disc,
        profit
    ])

with open('business_sales_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Order_ID', 'Order_Date', 'Ship_Date', 'Ship_Mode',
        'Customer_ID', 'Customer_Name', 'Segment', 'Country', 'City', 'Region',
        'Product_ID', 'Category', 'Sub_Category', 'Sales', 'Quantity', 'Discount', 'Profit'
    ])
    writer.writerows(rows)

print(f"Dataset generated successfully: 2,500 rows written to business_sales_data.csv")

