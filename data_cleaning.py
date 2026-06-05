import os
import re
import pandas as pd
import numpy as np

def clean_data():
    raw_dir = "data/raw"
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)
    
    print("--- Starting Day 2 Data Cleaning Pipeline ---")
    
    # Task 1: Clean nav_history.csv -> clean_nav.csv
    nav_path = os.path.join(raw_dir, "02_nav_history.csv")
    if os.path.exists(nav_path):
        df_nav = pd.read_csv(nav_path)
        df_nav['date'] = pd.to_datetime(df_nav['date'])
        
        # Sort by code and date, then remove exact duplicates
        df_nav = df_nav.sort_values(by=['amfi_code', 'date']).reset_index(drop=True)
        df_nav = df_nav.drop_duplicates(subset=['amfi_code', 'date'])
        
        # Validate NAV > 0
        df_nav = df_nav[df_nav['nav'] > 0]
        
        # Forward-fill missing NAV for holidays/weekends within each fund group
        df_nav['nav'] = df_nav.groupby('amfi_code')['nav'].ffill()
        
        df_nav.to_csv(os.path.join(processed_dir, "clean_nav.csv"), index=False)
        print("✔ Task 1 Complete: Created clean_nav.csv")

    # Task 2: Clean investor_transactions.csv -> clean_transactions.csv
    tx_path = os.path.join(raw_dir, "08_investor_transactions.csv")
    if os.path.exists(tx_path):
        df_tx = pd.read_csv(tx_path)
        
        # FIX: Strip invisible spaces from column names (e.g., ' amount ' -> 'amount')
        df_tx.columns = df_tx.columns.str.strip()
        
        # FIX: Dynamically find the right column if it's named slightly differently
        amt_col = [col for col in df_tx.columns if 'amount' in col.lower() or col.lower() == 'amt']
        amt_col = amt_col[0] if amt_col else 'amount' 
        
        date_col = [col for col in df_tx.columns if 'date' in col.lower()][0]
        
        # Parse dates using the dynamically found column name
        df_tx[date_col] = pd.to_datetime(df_tx[date_col])
        
        # Filter where amount > 0 using the correct column name
        if amt_col in df_tx.columns:
            df_tx = df_tx[df_tx[amt_col] > 0]
        
        # Regex standardisation function using the 're' module
        def standardize_tx_type(val):
            val = str(val).strip()
            if re.search(r'(?i)sip', val): return 'SIP'
            if re.search(r'(?i)lump', val): return 'Lumpsum'
            if re.search(r'(?i)red', val): return 'Redemption'
            return 'Lumpsum'
            
        if 'transaction_type' in df_tx.columns:
            df_tx['transaction_type'] = df_tx['transaction_type'].apply(standardize_tx_type)
            
        if 'kyc_status' in df_tx.columns:
            df_tx['kyc_status'] = df_tx['kyc_status'].str.upper().fillna('N')
            
        # Rename the amount column to exactly 'amount' for the database mapping
        if amt_col != 'amount':
            df_tx = df_tx.rename(columns={amt_col: 'amount'})
            
        df_tx.to_csv(os.path.join(processed_dir, "clean_transactions.csv"), index=False)
        print("✔ Task 2 Complete: Created clean_transactions.csv")

    # Task 3: Clean scheme_performance.csv -> clean_performance.csv
    perf_path = os.path.join(raw_dir, "07_scheme_performance.csv")
    if os.path.exists(perf_path):
        df_perf = pd.read_csv(perf_path)
        
        # Ensure return columns are numeric
        return_cols = [col for col in df_perf.columns if 'return' in col.lower()]
        for col in return_cols:
            df_perf[col] = pd.to_numeric(df_perf[col], errors='coerce').fillna(0)
            
        # Check expense ratio range (0.1% to 2.5%)
        if 'expense_ratio' in df_perf.columns:
            df_perf['expense_ratio'] = pd.to_numeric(df_perf['expense_ratio'], errors='coerce')
            
        # Flag negative Sharpe ratios
        if 'sharpe_ratio' in df_perf.columns:
            df_perf['sharpe_ratio'] = pd.to_numeric(df_perf['sharpe_ratio'], errors='coerce').fillna(0)
            df_perf['negative_sharpe_flag'] = np.where(df_perf['sharpe_ratio'] < 0, 1, 0)
            
        df_perf.to_csv(os.path.join(processed_dir, "clean_performance.csv"), index=False)
        print("✔ Task 3 Complete: Created clean_performance.csv")

    # Sync remaining files to processed folder to ensure clean loading later
    remaps = {
        "01_fund_master.csv": "clean_fund_master.csv",
        "03_aum_by_fund_house.csv": "clean_aum.csv"
    }
    for old, new in remaps.items():
        if os.path.exists(os.path.join(raw_dir, old)):
            pd.read_csv(os.path.join(raw_dir, old)).to_csv(os.path.join(processed_dir, new), index=False)

if __name__ == "__main__":
    clean_data()