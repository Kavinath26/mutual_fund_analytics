import os
import pandas as pd

def inspect_dataset(file_path):
    print(f"\n{'='*50}\nInspecting: {os.path.basename(file_path)}\n{'='*50}")
    try:
        df = pd.read_csv(file_path)
        print(f"Shape: {df.shape}")
        print("\nData Types:")
        print(df.dtypes)
        print("\nFirst 3 rows:")
        print(df.head(3))
        return df
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def main():
    raw_data_dir = "data/raw"
    if not os.path.exists(raw_data_dir):
        print(f"Directory {raw_data_dir} does not exist.")
        return
        
    csv_files = [f for f in os.listdir(raw_data_dir) if f.endswith('.csv') and f != 'live_nav_data.csv']
    if not csv_files:
        print("No provided CSV datasets found in data/raw/ yet. Please place the 10 assignment CSVs there.")
        return
        
    for file in csv_files:
        inspect_dataset(os.path.join(raw_data_dir, file))

if __name__ == "__main__":
    main()