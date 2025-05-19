import pandas as pd

POLLUTANTS = {
    "pm2.5": "PM2.5 (μg/m3)",
    "pm10": "PM10 (μg/m3)",
    "no2": "NO2 (μg/m3)"
}

def load_data(file_path):
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"[ERRORE] {e}")
        return None

def clean_data(df):
    cols_needed = ['WHO Region', 'Measurement Year'] + list(POLLUTANTS.values())
    df_clean = df[[col for col in cols_needed if col in df.columns]].dropna(how='all')
    
    return df_clean
