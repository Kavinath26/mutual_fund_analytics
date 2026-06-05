-- 1. Top 5 Funds by Transaction Capital Volume Inflow
SELECT amfi_code, SUM(amount) as total_capital_volume
FROM fact_transactions
GROUP BY amfi_code
ORDER BY total_capital_volume DESC
LIMIT 5;

-- 2. Average Net Asset Value (NAV) Per Month
SELECT amfi_code, strftime('%Y-%m', nav_date) as monthly_period, AVG(nav) as average_nav_value
FROM fact_nav
GROUP BY amfi_code, monthly_period;

-- 3. SIP Inflow Volume Performance Tracking
SELECT strftime('%Y', transaction_date) as calendar_year, SUM(amount) as periodic_sip_inflow
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY calendar_year;

-- 4. Regional Distribution Metrics by State
SELECT state, COUNT(transaction_id) as processing_count, SUM(amount) as raw_inflow_total
FROM fact_transactions
GROUP BY state
ORDER BY raw_inflow_total DESC;

-- 5. Cost Filter: Funds with Expense Ratios < 1%
SELECT amfi_code, expense_ratio
FROM fact_performance
WHERE expense_ratio < 1.0;

-- 6. Strategic Compliance Check: Negative Sharpe Ratio Targets
SELECT amfi_code, sharpe_ratio
FROM fact_performance
WHERE negative_sharpe_flag = 1;

-- 7. High-Yield Performance Filtering (Returns > 12%)
SELECT amfi_code, return_3yr, return_5yr
FROM fact_performance
WHERE return_3yr > 12.0;

-- 8. Capital Asset Distribution Mix by Transaction Profile
SELECT transaction_type, COUNT(*) as dynamic_volume, AVG(amount) as mean_transaction_value
FROM fact_transactions
GROUP BY transaction_type;

-- 9. KYC Audit Screening
SELECT kyc_status, COUNT(*) as registration_volume, SUM(amount) as value_at_risk
FROM fact_transactions
GROUP BY kyc_status;

-- 10. Core Portfolio Size Summary Mapping
SELECT COUNT(DISTINCT amfi_code) as registered_operational_funds FROM dim_fund;