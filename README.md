# Task-2
## 📊 E-Commerce Dataset — Analysis Insights

### Dataset Overview
| Property | Value |
|---|---|
| Total Orders | 1,200 |
| Date Range | Jan 2023 – Jun 2025 |
| Columns | 14 (after cleaning: 15) |
| Products | 7 categories |

---

### 🔢 Key Statistics

| Metric | Value |
|---|---|
| Total Revenue | $1,264,762 |
| Mean Order Value | $1,054 |
| Median Order Value | $824 |
| Avg Quantity per Order | 2.95 units |
| Avg Unit Price | $356 |

> The gap between mean ($1,054) and median ($824) confirms a **right-skewed** distribution — a small number of high-value orders pull the average up.

---

### 📦 Product Performance

| Product | Revenue | Avg Order Value |
|---|---|---|
| Chair | $195,620 | $1,099 |
| Printer | $195,613 | $1,081 |
| Laptop | $192,127 | $1,111 ← highest AOV |
| Tablet | $186,569 | $1,042 |
| Monitor | $175,651 | $1,078 |
| Desk | $167,460 | $985 |
| Phone | $151,722 | $973 ← lowest AOV |

Revenue is **evenly distributed** across all 7 categories (12–15.5% each), indicating no single product dependency.

---

### ⚠️ Critical Finding — Fulfilment Rate

| Status | Count | Share |
|---|---|---|
| Cancelled | 250 | 20.8% |
| Returned | 247 | 20.6% |
| Pending | 237 | 19.8% |
| Shipped | 235 | 19.6% |
| Delivered | 231 | 19.3% |

**Only 19.3% of orders are delivered.** Cancel + return rate combined is **41.4%** — well above the healthy e-commerce benchmark of <10%. This is the most significant operational flag in the dataset.

---

### 📉 Year-over-Year Trend

| Year | Orders | Revenue | Avg Order Value |
|---|---|---|---|
| 2023 | 510 | $552,643 | $1,084 |
| 2024 | 459 | $480,236 | $1,046 |
| 2025* | 231 | $231,883 | $1,004 |

*2025 is a partial year (Jan–Jun only)*

Both order volume and average order value are **declining year-over-year**, suggesting either shrinking demand or increasing competition.

---

### 🛒 Cart Size → Spend Correlation

Cart size is the strongest predictor of order value:

| Cart Size | Avg Order Value |
|---|---|
| 1 | $369 |
| 3 | $722 |
| 5 | $1,056 |
| 8 | $1,488 |
| 10 | $1,743 |

Customers with a cart size of 10 spend **4.7× more** than those with a cart size of 1. Upsell and cross-sell strategies targeting active browsers represent the clearest revenue opportunity.

---

### 📣 Referral Source Performance

| Source | Avg Order Value |
|---|---|
| Facebook | $1,098 ← best |
| Instagram | $1,063 |
| Email | $1,047 |
| Google | $1,039 |
| Referral | $1,022 ← lowest |

Social channels (Facebook + Instagram) consistently drive higher-value orders than search or peer referrals.

---

### 🔍 Outliers

Only **8 orders** qualify as statistical outliers (IQR method) — all are max-quantity (Qty = 5) purchases of high-priced items, with order totals between **$3,334 and $3,456**. These are legitimate high-value transactions, not data errors.

---

### 🧹 Data Cleaning Applied

| Issue | Fix Applied |
|---|---|
| 309 null `CouponCode` values | Filled with `"No Coupon"` |
| `ItemsInCart` ≠ `Quantity` (1,000 rows) | Renamed to `CartSize` to reflect true meaning |
| Incomplete `ShippingAddress` (street only) | Flagged with `ShippingAddress_Complete = False` |
| Tracking numbers on Cancelled/Pending orders | Set to `null` for 487 affected rows |

---

### 🛠️ Tools & Libraries
`Python` · `pandas` · `numpy` · `matplotlib` · `seaborn` · `openpyxl`
