# Data Dictionary - Mutual Fund Schema v1.1

## Table: dim_fund (Dimension)
| Column Name | Data Type | Key Type | Business Context / Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- |
| amfi_code | TEXT | PK | Unique tracking ID assigned by the Association of Mutual Funds in India | clean_fund_master.csv |
| fund_house | TEXT | - | Parent Asset Management Company (AMC) umbrella (e.g., HDFC Mutual Fund) | clean_fund_master.csv |
| scheme_name | TEXT | - | Full legal retail name of the mutual fund asset portfolio | clean_fund_master.csv |
| category | TEXT | - | Macro asset class allocation grouping (e.g., Equity, Debt, Hybrid) | clean_fund_master.csv |
| sub_category| TEXT | - | Micro sector investment strategy focus alignment (e.g., Large Cap) | clean_fund_master.csv |
| risk_grade | TEXT | - | Portfolio variance and risk rating evaluation grade | clean_fund_master.csv |

## Table: dim_date (Dimension)
| Column Name | Data Type | Key Type | Business Context / Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- |
| date_id | TEXT | PK | Primary date string key used to join tracking timelines (Format: YYYY-MM-DD) | Generated Dimension |
| calendar_year | INTEGER | - | Numerical calendar year of the record | Generated Dimension |
| calendar_month | INTEGER | - | Numerical calendar month of the record (1 to 12) | Generated Dimension |
| month_name | TEXT | - | Full alphabetical name of the month (e.g., January) | Generated Dimension |
| calendar_quarter | INTEGER | - | Calendar quarter numerical indicator (1 to 4) | Generated Dimension |
| day_of_week | TEXT | - | Name of the day of the week (e.g., Monday, Sunday) | Generated Dimension |

## Table: fact_nav (Fact)
| Column Name | Data Type | Key Type | Business Context / Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- |
| nav_id | INTEGER | PK | Auto-incrementing internal surrogate primary key | Internal Database |
| amfi_code | TEXT | FK | Target fund entity code connection parameter linking to dim_fund | clean_nav.csv |
| nav_date | TEXT | FK | Date of closing NAV price record linking to dim_date | clean_nav.csv |
| nav | REAL | - | Net Asset Value (closing unit price). Value is forward-filled for holidays | clean_nav.csv |
| daily_return | REAL | - | Calculated daily percentage price movement variant from the prior day | clean_nav.csv |

## Table: fact_transactions (Fact)
| Column Name | Data Type | Key Type | Business Context / Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- |
| transaction_id| INTEGER | PK | Unique operational audit sequence identifier for order processing | clean_transactions.csv |
| amfi_code | TEXT | FK | Target fund entity code connection parameter linking to dim_fund | clean_transactions.csv |
| investor_id | TEXT | - | Masked alphanumeric token string representing a unique investor account | clean_transactions.csv |
| transaction_date| TEXT | FK | Execution date of the trade order transaction linking to dim_date | clean_transactions.csv |
| transaction_type| TEXT | - | Mapped method of distribution capital vehicle (SIP / Lumpsum / Redemption) | clean_transactions.csv |
| amount | REAL | - | Total cash currency value processed for the financial order | clean_transactions.csv |
| units | REAL | - | Total fractional asset allocation volume credited or debited to account | clean_transactions.csv |
| kyc_status | TEXT | - | Regulatory identity validation confirmation field status (Y/N) | clean_transactions.csv |
| state | TEXT | - | Geographic regional state of origin data point for distribution metrics | clean_transactions.csv |

## Table: fact_performance (Fact)
| Column Name | Data Type | Key Type | Business Context / Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- |
| performance_id| INTEGER | PK | Auto-incrementing internal surrogate primary key | Internal Database |
| amfi_code | TEXT | FK | Target fund entity code connection parameter linking to dim_fund | clean_performance.csv |
| return_1yr | REAL | - | 1-Year trailing compound annualized return percentage value | clean_performance.csv |
| return_3yr | REAL | - | 3-Year trailing compound annualized return percentage value | clean_performance.csv |
| return_5yr | REAL | - | 5-Year trailing compound annualized return percentage value | clean_performance.csv |
| sharpe_ratio | REAL | - | Risk-adjusted return structural efficiency evaluation metric | clean_performance.csv |
| negative_sharpe_flag| INTEGER| - | Binary status flag (1 if sharpe_ratio is less than 0, else 0) | clean_performance.csv |
| expense_ratio | REAL | - | Annualized cost percentage fees charged by AMC (Valid range: 0.1% to 2.5%) | clean_performance.csv |

## Table: fact_aum (Fact)
| Column Name | Data Type | Key Type | Business Context / Definition | Source Reference |
| :--- | :--- | :--- | :--- | :--- |
| aum_id | INTEGER | PK | Auto-incrementing internal surrogate primary key | Internal Database |
| amfi_code | TEXT | FK | Target fund entity code connection parameter linking to dim_fund | clean_aum.csv |
| aum_amount | REAL | - | Total valuation value of Assets Under Management held by the fund | clean_aum.csv |
| recorded_date| TEXT | FK | Log capture date of the snapshot data entry linking to dim_date | clean_aum.csv |