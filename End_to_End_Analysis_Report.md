# End-to-End Business Performance Analysis Case Study
*From Raw Data to Executive Decision-Making*

---

## 1. Project Architecture & Workflow

This project fulfills all requirements of the **End-to-End Analysis Case Study**, covering data ingestion, automated cleaning, deep exploratory analysis, BI dashboard implementation, and executive storytelling.

```
Raw Data (CSV / Sheets)  -->  Python Cleaning & EDA  -->  Cleaned Dataset
                                                               |
                     +-----------------------------------------+
                     |                                         |
                     v                                         v
            SQL Relational Analysis                  Pandas Exploratory Pipeline
                     \                                         /
                      +---------------------------------------+
                                          |
                                          v
                              Interactive BI Dashboard
                           (Power BI / Tableau / Web)
                                          |
                                          v
                            Executive Stakeholder Report
```

---

## 2. Step 1: Python Data Cleaning & Feature Engineering

### 2.1 Cleaning Pipeline
1. **Null & Anomaly Handling**: Verified complete record integrity; rows with negative quantities or invalid dates are flagged and parsed.
2. **Date Parsing & Lead Time**: Converted string dates to ISO timestamps and computed fulfillment velocity:
   $$\text{Ship\_Days} = \text{Ship\_Date} - \text{Order\_Date}$$
3. **Feature Engineering**:
   - **Profit Margin %**: `(Profit / Sales) * 100`
   - **Discount Band**: Stratified into `0% None`, `1% - 10% Low`, `11% - 20% Medium`, and `> 20% High`.
   - **Profit Status**: Categorized as `Profitable` vs `Loss-making`.

### 2.2 Key Exploratory Data Analysis (EDA) Findings
- **Total Revenue**: \$1,739,237.54 across 2,500 orders
- **Total Net Profit**: \$415,944.97 (Overall Margin: **23.92%**)
- **Loss-making Transactions**: 267 orders (**10.7%** of all orders) generated negative profit.
- **Top Margin Category**: Office Supplies (**43.6%** margin), followed by Technology (**32.0%**).
- **Vulnerability**: Furniture delivers large gross volume (\$636,342.71) but a dangerously low net margin of only **7.2%**.

---

## 3. Step 2: SQL & Pandas Deep-Dive Analysis

### Query 1: Executive KPI Baseline
```sql
SELECT 
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(sales), 2) AS avg_order_value
FROM orders;
```
*Result:* 2,500 Orders | 280 Customers | \$1,739,237.54 Revenue | \$415,944.97 Profit | 23.92% Margin | \$695.70 AOV.

---

### Query 2: Sub-Category Profitability & Loss Leaders
```sql
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
```

| Category | Sub-Category | Orders | Revenue | Net Profit | Profit Margin % | Business Diagnosis |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Furniture** | Tables | 194 | \$152,738.62 | \$8,902.42 | **5.83%** | Margin drain: High shipping/COGS |
| **Furniture** | Bookcases | 187 | \$145,252.18 | \$10,523.76 | **7.25%** | Margin drain: High discount sensitivity |
| **Furniture** | Furnishings | 216 | \$166,964.98 | \$12,027.44 | **7.20%** | Low margin despite high volume |
| **Technology** | Accessories | 230 | \$267,292.10 | \$84,131.88 | **31.48%** | Star performer: Core profit driver |
| **Technology** | Phones | 209 | \$248,852.04 | \$77,772.88 | **31.25%** | Star performer: High revenue & margin |
| **Office Supplies** | Appliances | 179 | \$33,075.07 | \$14,686.63 | **44.40%** | Highest margin percentage |

---

### Query 3: Discount Threshold Analysis (The Margin Cliff)
```sql
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
```

| Discount Band | Orders | Total Revenue | Net Profit | Margin % | Loss-Making Orders |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **0% (Full Price)** | 869 | \$673,350.15 | \$218,124.27 | **32.39%** | 0 |
| **1% - 10% Low** | 728 | \$536,090.13 | \$146,655.14 | **27.36%** | 0 |
| **11% - 20% Medium** | 506 | \$312,273.94 | \$62,001.86 | **19.85%** | 69 |
| **> 20% High** | 397 | \$217,523.32 | **\$-10,836.30** | **-4.98%** | **198** |

---

## 4. Step 3: BI Dashboard Implementation (Power BI & Tableau)

### 4.1 Calculated Fields & DAX Measures Guide

#### Power BI (DAX Formulas)
```dax
-- 1. Total Sales
Total Sales = SUM(cleaned_sales_data[Sales])

-- 2. Total Profit
Total Profit = SUM(cleaned_sales_data[Profit])

-- 3. Profit Margin %
Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0)

-- 4. Average Order Value (AOV)
AOV = DIVIDE([Total Sales], DISTINCTCOUNT(cleaned_sales_data[Order_ID]), 0)

-- 5. Loss-making Order Count
Unprofitable Orders = CALCULATE(COUNTROWS(cleaned_sales_data), cleaned_sales_data[Profit] < 0)

-- 6. High Discount Sales Share
High Discount Sales = CALCULATE([Total Sales], cleaned_sales_data[Discount] > 0.20)
```

#### Tableau (Calculated Fields)
```tableau
// 1. Profit Margin %
SUM([Profit]) / SUM([Sales])

// 2. Shipping Lead Time (Days)
DATEDIFF('day', [Order Date], [Ship Date])

// 3. Profitability Indicator (Color encoding)
IF SUM([Profit]) > 0 THEN "Profitable" 
ELSEIF SUM([Profit]) = 0 THEN "Breakeven" 
ELSE "Loss" END

// 4. Discount Category
IF [Discount] = 0 THEN "No Discount"
ELSEIF [Discount] <= 0.10 THEN "Low (1-10%)"
ELSEIF [Discount] <= 0.20 THEN "Medium (11-20%)"
ELSE "High (>20%)" END
```

---

## 5. Step 4: Final Executive Presentation & Stakeholder Report

### Executive Summary
Across 2,500 transactions, the business achieved **\$1.74M in revenue** and **\$415.9K in net profit**, reflecting a healthy overall profit margin of **23.9%**. However, underlying operational inefficiencies and uncalibrated promotional discounting are eroding bottom-line margins.

### Key Insights (The "So What?")
1. **The Promotional Discount Trap**:
   - Orders with zero discount achieved a **32.4% profit margin**.
   - Orders discounted at >20% resulted in **\$-10,836 net losses** across 198 transactions.
2. **Category Imbalance (Furniture Dilemma)**:
   - Furniture generated **\$636K in sales** (36.6% of company revenue) but only delivered **\$45.8K in net profit (7.2% margin)**.
   - Specifically, **Tables (5.8%)** and **Bookcases (7.2%)** suffer from heavy freight costs and aggressive price cuts.
3. **High-Margin Growth Engines**:
   - **Technology (Accessories & Phones)** generated over **\$161K in net profit** with strong 31%+ margins.
   - **Office Supplies** boasts an outstanding **43.6% profit margin**, providing steady, highly profitable cash flow.
