import os
import pandas as pd
from sqlalchemy import create_engine

def database_migration():
    processed_dir = "data/processed"
    db_file = "bluestock_mf.db"
    engine = create_engine(f"sqlite:///{db_file}")
    
    # Precise map alignment
    target_tables = {
        "clean_fund_master.csv": "dim_fund",
        "clean_nav.csv": "fact_nav",
        "clean_transactions.csv": "fact_transactions",
        "clean_performance.csv": "fact_performance"
    }
    
    print("\n--- Loading Datasets into bluestock_mf.db ---")
    for csv_name, sql_table in target_tables.items():
        path = os.path.join(processed_dir, csv_name)
        if os.path.exists(path):
            df = pd.read_csv(path)
            
            # Enforce clean string rendering for text primary keys
            if 'amfi_code' in df.columns:
                df['amfi_code'] = df['amfi_code'].astype(str)
                
            df.to_sql(sql_table, con=engine, if_exists='replace', index=False)
            
            # Verification Row Count Metrics
            db_count = pd.read_sql(f"SELECT COUNT(*) FROM {sql_table}", con=engine).iloc[0, 0]
            print(f"✔ Transferred {sql_table}: {db_count} rows successfully mapped.")

if __name__ == "__main__":
    database_migration()