from dotenv import load_dotenv
import os

load_dotenv()

INPUT_FILE = 'data/Dataset.xlsx'
OUTPUT_FOLDER = 'results'
FORECAST_YEARS = 10
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise ValueError("La chiave API 'GROQ_API_KEY' non è stata trovata. Assicurati che sia attiva.")

POLLUTANTS = {
    "pm2.5": "PM2.5 (μg/m3)",
    "pm10": "PM10 (μg/m3)",
    "no2": "NO2 (μg/m3)"
}

ITALIAN_TO_ENGLISH_REGION = {
    "africa": "African Region",
    "europa": "European Region",
    "america": "Region of the Americas",
    "pacifico": "Western Pacific Region",
    "asia": "South East Asia Region",
    "mediterraneo": "Eastern Mediterranean Region",
}
