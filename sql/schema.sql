-- DDL Script for Mutual Fund Analytics Star Schema

-- ==========================================
-- 1. DIMENSION TABLES
-- ==========================================

-- Dimension Table: Fund Master Metadata
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code TEXT PRIMARY KEY,
    fund_house TEXT,
    scheme_name TEXT NOT NULL,
    category TEXT,
    sub_category TEXT,
    risk_grade TEXT
);

-- Dimension Table: Calendar Time Dimension
CREATE TABLE IF NOT EXISTS dim_date (
    date_id TEXT PRIMARY KEY, -- Expected format: YYYY-MM-DD
    calendar_year INTEGER NOT NULL,
    calendar_month INTEGER NOT NULL,
    month_name TEXT NOT NULL,
    calendar_quarter INTEGER NOT NULL,
    day_of_week TEXT NOT NULL
);


-- ==========================================
-- 2. FACT TABLES
-- ==========================================

-- Fact Table: Historical NAV Log Metrics
CREATE TABLE IF NOT EXISTS fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code TEXT,
    nav_date TEXT, -- Maps to dim_date(date_id)
    nav REAL NOT NULL,
    daily_return REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (nav_date) REFERENCES dim_date(date_id)
);

-- Fact Table: Investor Capital Transaction Flows
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id INTEGER PRIMARY KEY,
    amfi_code TEXT,
    investor_id TEXT,
    transaction_date TEXT, -- Maps to dim_date(date_id)
    transaction_type TEXT, -- SIP, Lumpsum, Redemption
    amount REAL NOT NULL,
    units REAL,
    kyc_status TEXT,
    state TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (transaction_date) REFERENCES dim_date(date_id)
);

-- Fact Table: Portfolio Risk & Return Performance
CREATE TABLE IF NOT EXISTS fact_performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code TEXT,
    return_1yr REAL,
    return_3yr REAL,
    return_5yr REAL,
    sharpe_ratio REAL,
    negative_sharpe_flag INTEGER DEFAULT 0,
    expense_ratio REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact Table: Assets Under Management Snapshot Logs
CREATE TABLE IF NOT EXISTS fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code TEXT,
    aum_amount REAL NOT NULL,
    recorded_date TEXT, -- Maps to dim_date(date_id)
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (recorded_date) REFERENCES dim_date(date_id)
);