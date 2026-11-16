# SkillNexis Week 4 Project: End-to-End Business Performance & Retail Analytics

A complete end-to-end data analytics and business intelligence project converting raw transactional retail records into executive strategic decisions.

---

## 🌟 Project Overview & Architecture

This repository fulfills all criteria of the **SkillNexis Week 4 Capstone Case Study**:
1. **Data Cleaning & Exploration**: Automated Python pipeline handling missing values, type validation, date parsing, and feature engineering.
2. **Deep-Dive Analysis**: SQL diagnostic queries (SQLite) and Python Pandas scripts uncovering key profitability drivers and margin leaks.
3. **Interactive BI Dashboard**: Full-fledged web-based BI dashboard (`index.html`) ready for GitHub Pages hosting, complete with multi-criteria filters, KPI metric cards, SVG trend charts, and a live searchable department breakdown table.
4. **BI Tool Fundamentals (Power BI & Tableau)**: Full DAX formula library, Tableau calculated fields, chart selection matrix, and visual hierarchy blueprint.
5. **Stakeholder Executive Report**: Structured insights and strategic recommendations using the SCQA (Situation, Complication, Question, Answer) framework.

```
       +---------------------------------------------+
       |   Raw Transactional Data (2,500 records)     |
       +---------------------------------------------+
                              |
                              v  (clean_and_explore.py)
       +---------------------------------------------+
       |   Cleaned & Enriched Dataset (CSV)          |
       +---------------------------------------------+
                     /                  \
                    v                    v
+-----------------------------+  +-----------------------------+
|   SQL Database Analysis     |  |   Pandas Exploration        |
|   (sales_analysis.db)       |  |   (pandas_analysis.py)      |
+-----------------------------+  +-----------------------------+
                    \                    /
                     v                  v
       +---------------------------------------------+
       |   Interactive BI Dashboard (index.html)     |
       |   & Power BI / Tableau Implementation       |
       +---------------------------------------------+
                              |
                              v
       +---------------------------------------------+
       |   Executive Stakeholder Presentation & Deck |
       +---------------------------------------------+
```

---

## 📁 Repository Structure

```text
├── index.html                  # Interactive web-based BI dashboard (GitHub Pages ready)
├── clean_and_explore.py        # Python data cleaning, validation, and automated EDA
├── sql_analysis.py             # SQLite database loader and diagnostic SQL business queries
├── pandas_analysis.py          # Python Pandas script for Jupyter / Colab analysis
├── generate_dataset.py         # Reproducible multi-year retail transaction dataset generator
├── business_sales_data.csv     # Raw input transaction records (2,500 orders)
├── cleaned_sales_data.csv      # Cleaned and feature-engineered analytical dataset
├── sales_analysis.db           # SQLite database with structured orders table
├── End_to_End_Analysis_Report.md # Full analytical findings and stakeholder presentation
└── README.md                   # Project documentation and guide
```

---

## 📊 Key Executive Findings

1. **Overall Business Health**:
   - **Total Revenue**: \$1,739,237.54
   - **Total Net Profit**: \$415,944.97
   - **Overall Net Margin**: **23.92%**
   - **Average Order Value (AOV)**: \$695.70

2. **The "Discount Cliff" (Critical Risk Finding)**:
   - Full-price transactions (`0% Discount`) yielded an average **32.39% profit margin**.
   - Moderate discounts (`1% - 10%`) maintained a healthy **27.36% profit margin**.
   - Heavy promotional discounts (`> 20%`) generated a net loss of **\$-10,836.30** across 198 loss-making orders (**-4.98% margin**).

3. **Category Profitability Divergence**:
   - **Office Supplies**: Top margin producer at **43.6%** net margin (\$66.4K profit).
   - **Technology**: Core revenue and profit engine at **32.0%** net margin (\$303.8K profit).
   - **Furniture**: Volume trap — generated \$636.3K in gross sales (36.6% company share) but yielded only **7.2%** net profit, heavily dragged down by **Tables** (5.8% margin) and **Bookcases** (7.2% margin).

---

## 🛠️ Step-by-Step Technical Execution

### 1. Data Cleaning & Feature Engineering (`clean_and_explore.py`)
Run the automated cleaning pipeline:
```bash
python clean_and_explore.py
```
- Validates data types and checks for duplicate Order IDs.
- Calculates order fulfillment velocity: `Ship_Days = Ship_Date - Order_Date`.
- Formulates `Profit_Margin_Pct = (Profit / Sales) * 100`.
- Categorizes discount bands (`0% None`, `1-10% Low`, `11-20% Medium`, `>20% High`).
- Exports `cleaned_sales_data.csv`.

### 2. SQL Analysis (`sql_analysis.py`)
Run the diagnostic SQL queries on SQLite:
```bash
python sql_analysis.py
```
Key SQL Queries included:
- **Executive KPI Summary**: Aggregate revenue, profit, distinct orders, and distinct customer counts.
- **Sub-Category Profitability**: Identifies loss leaders and margin diluters.
- **Discount Band Analysis**: Measures exact financial impact across discount tiers.
- **Regional Performance**: Compares revenue, profit margin, and delivery cycle times across geographic regions.
- **Monthly Performance Trend**: Tracks seasonality and monthly growth rates.

### 3. Interactive Web Dashboard (`index.html`)
The dashboard is built with modern HTML5, Tailwind CSS, and pure SVG visualizations:
- **Interactive Multi-Criteria Filtering**: Filter dynamically by Year (2012–2015), Market, and Category.
- **Live Search**: Instant client-side filtering on the Department Performance Table.
- **Export Utility**: One-click download of cleaned CSV data directly from the UI.
- **GitHub Pages Ready**: Can be deployed instantly via repository settings.

---

## 📈 Power BI & Tableau Implementation Guide

### Power BI DAX Formulas
```dax
-- Total Revenue
Total Sales = SUM(cleaned_sales_data[Sales])

-- Total Profit
Total Profit = SUM(cleaned_sales_data[Profit])

-- Profit Margin %
Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0)

-- Average Order Value (AOV)
AOV = DIVIDE([Total Sales], DISTINCTCOUNT(cleaned_sales_data[Order_ID]), 0)

-- Unprofitable Orders Count
Loss Orders = CALCULATE(COUNTROWS(cleaned_sales_data), cleaned_sales_data[Profit] < 0)
```

### Tableau Calculated Fields
```tableau
// Profit Margin %
SUM([Profit]) / SUM([Sales])

// Fulfillment Days
DATEDIFF('day', [Order Date], [Ship Date])

// Profitability Status
IF SUM([Profit]) > 0 THEN "Profitable" 
ELSEIF SUM([Profit]) = 0 THEN "Breakeven" 
ELSE "Loss" END
```

---

## 💡 Strategic Recommendations for Stakeholders

1. **Enforce Hard Discount Guardrails**:
   - Cap discretionary sales discounts at **15%**.
   - Require senior leadership approval for discounts exceeding 15%.
   - Immediately terminate discounts `>20%` on Furniture to stop the \$10.8K margin leak.

2. **Revamp Furniture Pricing & Shipping Surcharges**:
   - Introduce freight surcharges on bulky Furniture items (Tables, Bookcases).
   - Bundle low-margin Furniture with high-margin Accessories and Office Supplies.

3. **Align Sales Incentives with Net Profit Contribution**:
   - Transition sales commission models from gross booking volume to gross margin dollars to eliminate unprofitable discounted deals.

---

## 👤 Author
- **GitHub**: [@Sanmugapriyan06](https://github.com/Sanmugapriyan06)
- **Project**: SkillNexis Week 4 Analytics Project
