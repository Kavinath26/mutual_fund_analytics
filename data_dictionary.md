# Data Dictionary — Mutual Fund Analytics Schema (v1.1)

This documentation outlines the relational schema, structural datatypes, constraints, and source file mappings for the **`bluestock_mf.db`** SQLite database.

---

## 1. Dimension Tables

### Table: `dim_fund`
* **Business Context:** Contains master metadata for all registered mutual fund schemes.
* **Granularity:** One row per unique AMFI scheme code.

| Column Name | Data Type | Constraints | Business Definition / Rules | Source Reference |
| :--- | :--- | :--- | :--- | :--- |
| `amfi_code` | TEXT | PRIMARY KEY | Unique identification code assigned by the Association of Mutual Funds in India. | `clean_fund_master.csv` |
| `fund_house` | TEXT | None | The Asset Management Company (AMC) managing the fund (e.g., HDFC Mutual Fund). | `clean_fund_master.csv` |
| `scheme_name` | TEXT | NOT NULL | The official market-facing portfolio name of the fund. | `clean_fund_master.csv` |
| `category` | TEXT | None | High-level asset class designation (e.g., Equity, Debt, Hybrid). | `clean_fund_master.csv` |
| `sub_category` | TEXT | None | Specific investment strategy alignment (e.g., Large Cap, Flexi Cap, Section 80C). | `clean_fund_master.csv` |
| `risk_grade` | TEXT | None | Risk rating evaluation assigned to the portfolio (e.g., Low, High, Very High). | `clean_fund_master.csv` |

---

## 2. Fact Tables

### Table: `fact_nav`
* **Business Context:** Tracks the daily Net Asset Value (NAV) pricing history for funds over time.
* **Granularity:** One row per unique combination of `amfi_code` and `nav_date`.

| Column Name | Data Type | Constraints | Business Definition / Rules | Source Reference |
| :--- | :--- | :--- | :--- | :--- |
| `nav_id` | INTEGER | PRIMARY KEY AUTOINCREMENT | System-generated surrogate primary key for unique row identification. | Internal Database |
| `amfi_code` | TEXT | FOREIGN KEY | References `dim_fund(amfi_code)` to connect tracking logs to the master fund profile. | `clean_nav.csv` |
| `nav_date` | DATE | None | The trading calendar date of the record. (Format: YYYY-MM-DD). | `clean_nav.csv` |
| `nav` | REAL | Check `nav > 0` | The closing price per unit of the fund. Values are forward-filled for holidays/weekends. | `clean_nav.csv` |
| `daily_return` | REAL | None | The calculated percentage price movement relative to the prior trading day's closing NAV. | `clean_nav.csv` |

---

### Table: `fact_transactions`
* **Business Context:** Captures capital flow volumes, investor transaction methods, and compliance registration data.
* **Granularity:** One row per distinct financial order entry execution.

| Column Name | Data Type | Constraints | Business Definition / Rules | Source Reference |
| :--- | :--- | :--- | :--- | :--- |
| `transaction_id`| INTEGER | PRIMARY KEY | Unique operational audit identifier parsed directly from order logs. | `clean_transactions.csv` |
| `amfi_code` | TEXT | FOREIGN KEY | References `dim_fund(amfi_code)` to link capital flow tracking metrics to specific funds. | `clean_transactions.csv` |
| `investor_id` | TEXT | None | Masked alphanumeric tracking token representing an individual investor profile. | `clean_transactions.csv` |
| `transaction_date`| DATE | None | Execution date of the payment processing structure. (Format: YYYY-MM-DD). | `clean_transactions.csv` |
| `transaction_type`| TEXT | None | Standardized investment vehicle path. Explicitly mapped via regex to: `SIP`, `Lumpsum`, or `Redemption`. | `clean_transactions.csv` |
| `amount` | REAL | Check `amount > 0` | Total local currency capital valuation exchanged during the transaction. | `clean_transactions.csv` |
| `units` | REAL | None | Total fractional asset allocation volume credited or debited to the account. | `clean_transactions.csv` |
| `kyc_status` | TEXT | Enum | Know Your Customer validation string status flag. Standardized to uppercase: `Y` (Yes) or `N` (No). | `clean_transactions.csv` |
| `state` | TEXT | None | Regional geographic origin of the investor used to measure demographic market density. | `clean_transactions.csv` |

---

### Table: `fact_performance`
* **Business Context:** Houses annualized compounded return structures, management costs, and risk performance evaluation metrics.
* **Granularity:** One row per tracking fund instance.

| Column Name | Data Type | Constraints | Business Definition / Rules | Source Reference |
| :--- | :--- | :--- | :--- | :--- |
| `performance_id`| INTEGER | PRIMARY KEY AUTOINCREMENT | Internal system surrogate tracking key. | Internal Database |
| `amfi_code` | TEXT | FOREIGN KEY | References `dim_fund(amfi_code)` to tie investment return stats back to the entity. | `clean_performance.csv` |
| `return_1yr` | REAL | None | 1-Year trailing compound annualized return percentage value. | `clean_performance.csv` |
| `return_3yr` | REAL | None | 3-Year trailing compound annualized return percentage value. | `clean_performance.csv` |
| `return_5yr` | REAL | None | 5-Year trailing compound annualized return percentage value. | `clean_performance.csv` |
| `sharpe_ratio` | REAL | None | Risk-adjusted return structural metric representing portfolio reward per unit of volatility. | `clean_performance.csv` |
| `negative_sharpe_flag`| INTEGER| Binary (0 or 1) | Operational flag generated dynamically. Set to `1` if `sharpe_ratio < 0`, indicating poor asset efficiency. | `clean_performance.csv` |
| `expense_ratio` | REAL | Value: 0.1 – 2.5 | Annual operational fees charged by the asset house relative to assets under management. | `clean_performance.csv` |