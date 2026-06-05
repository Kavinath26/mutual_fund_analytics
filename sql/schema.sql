-- DDL Schema reflecting requirements in Task 4

-- Dimension: Fund Master
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code TEXT PRIMARY KEY,
    fund_house TEXT,
    scheme_name TEXT NOT NULL,
    category TEXT,
    sub_category TEXT,
    risk_grade TEXT
);

-- Fact: NAV Operational Timeline
CREATE TABLE IF NOT EXISTS fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code TEXT,
    nav_date DATE,
    nav REAL,
    daily_return REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact: Investor Capital Flows
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id INTEGER PRIMARY KEY,
    amfi_code TEXT,
    investor_id TEXT,
    transaction_date DATE,
    transaction_type TEXT,
    amount REAL,
    units REAL,
    kyc_status TEXT,
    state TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact: Performance Evaluation Metrics
CREATE TABLE IF NOT EXISTS fact_performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code TEXT,
    return_1yr REAL,
    return_3yr REAL,
    return_5yr REAL,
    sharpe_ratio REAL,
    negative_sharpe_flag INTEGER,
    expense_ratio REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);