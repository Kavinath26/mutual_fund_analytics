import os
import requests
import pandas as pd
from datetime import datetime

# AMFI Codes assigned for Day 1
SCHEMES = {
    "125497": "HDFC_Top_100_Direct",
    "119551": "SBI_Bluechip",
    "120503": "ICICI_Bluechip",
    "118632": "Nippon_Large_Cap",
    "119092": "Axis_Bluechip",
    "120841": "Kotak_Bluechip"
}

def fetch_live_nav(scheme_code, scheme_name):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"Fetching data for {scheme_name} ({scheme_code})...")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            meta = data.get('meta', {})
            nav_list = data.get('data', [])
            if not nav_list:
                return None
            df = pd.DataFrame(nav_list)
            df['scheme_code'] = scheme_code
            df['scheme_name'] = meta.get('scheme_name', scheme_name)
            df['fund_house'] = meta.get('fund_house', 'Unknown')
            df['fetched_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return df[['scheme_code', 'scheme_name', 'fund_house', 'date', 'nav', 'fetched_at']]
    except Exception as e:
        print(f"Error fetching {scheme_code}: {str(e)}")
        return None

def main():
    os.makedirs("data/raw", exist_ok=True)
    all_data = []
    for code, name in SCHEMES.items():
        df = fetch_live_nav(code, name)
        if df is not None:
            all_data.append(df)
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df.to_csv("data/raw/live_nav_data.csv", index=False)
        print("\nSuccess! Raw NAV data successfully saved to data/raw/live_nav_data.csv")

if __name__ == "__main__":
    main()