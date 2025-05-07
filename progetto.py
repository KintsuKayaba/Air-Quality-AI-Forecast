import pandas as pd
import os
import matplotlib.pyplot as plt
import requests
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, r2_score
import re
import warnings
import difflib

warnings.filterwarnings("ignore", category=UserWarning)

# ======== CONFIGURAZIONI ========
INPUT_FILE = 'Dataset.xlsx'
OUTPUT_FOLDER = 'Results'
FORECAST_YEARS = 10  # Anni da prevedere
GROQ_API_KEY = "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"

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
# ================================

def load_data(file_path):
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"[ERRORE] {e}")
        return None

def clean_data(df):
    print(df.shape)
    cols_needed = ['WHO Region', 'Measurement Year'] + list(POLLUTANTS.values())
    df_clean = df[[col for col in cols_needed if col in df.columns]].dropna(how='all')
    
    print(df_clean.shape)
    return df_clean

def generate_ai_explanation(region, pollutant_name, first_year, first_value, last_year, last_value):
    region_clean = region.replace("Region", "").strip()
    trend = "diminuito" if last_value < first_value else "aumentato"
    percent = 0 if first_value == 0 else abs((last_value - first_value) / first_value) * 100

    plausibility = ""
    if last_value < 5:
        plausibility = ("Tuttavia, questo valore molto basso nel futuro potrebbe essere "
                        "ottimistico: raggiungerlo richiederebbe politiche molto rigorose e durature.")

    prompt = (
        f"Nella regione {region_clean}, l'inquinante {pollutant_name} è {trend} dal {first_year} "
        f"({first_value:.2f} μg/m³) al {last_year} ({last_value:.2f} μg/m³), con un cambiamento "
        f"del {percent:.1f}%. {plausibility} Scrivi un testo su questo andamento in italiano, "
        "parlando dell'impatto sulla salute, sull'ambiente e su cosa potrebbe causare questa evoluzione. "
        "Basandoti solo sui dati forniti dal dataset e da ciò che vedi sul grafico."
    )

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        try:
            return response.json()['choices'][0]['message']['content'].strip()
        except Exception:
            return "Errore nella generazione della risposta"
    else:
        return f"[ERRORE AI] {response.text}"

def train_and_forecast(df_region, pollutant, pollutant_name, region_name):
    # === Preprocessing dei dati ===
    df_model = df_region[['Measurement Year', pollutant]].dropna()
    df_model.columns = ['ds', 'y']
    df_model['ds'] = pd.to_datetime(df_model['ds'].astype(str), format='%Y')
    
    # Calcola la media per ogni anno
    mean_model = df_model.groupby('ds').mean().reset_index()

    # === Impostazione e training del modello Prophet ===
    model = Prophet(yearly_seasonality=True, seasonality_mode='additive')
    model.fit(df_model)

    # Utilizza frequenza annuale per mantenere la coerenza con i dati
    future = model.make_future_dataframe(periods=FORECAST_YEARS, freq='YE')
    forecast = model.predict(future)

    # Filtro per mostrare solo le previsioni dopo l'ultimo dato storico
    last_date = df_model['ds'].max()
    forecast_future = forecast[forecast['ds'] >= last_date]

    # === Calcolo delle prestazioni su dati storici ===
    merged = pd.merge(df_model, forecast[['ds', 'yhat']], on='ds')
    mae = mean_absolute_error(merged['y'], merged['yhat'])
    r2 = r2_score(merged['y'], merged['yhat'])

    # === Creazione del grafico ===
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(mean_model['ds'], mean_model['y'], label='Dati storici', linewidth=2)
    ax.plot(forecast_future['ds'], forecast_future['yhat'], label='Previsione', color='red', linestyle='--')
    ax.fill_between(forecast_future['ds'], forecast_future['yhat_lower'], forecast_future['yhat_upper'], 
                    color='pink', alpha=0.3, label='Intervallo confidenza')

    ax.set_title(f"{pollutant_name} Forecast for {region_name} - MAE: {mae:.2f}, R²: {r2:.2f}", fontsize=14)
    ax.set_xlabel('Anno')
    ax.set_ylabel(pollutant_name)
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    safe_name = re.sub(r'[^\w\-_\.]', '_', pollutant_name)
    filename = f"{region_name}_{safe_name}_forecast_prophet.png"
    path = os.path.join(OUTPUT_FOLDER, filename)
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)

    # === Generazione della spiegazione AI ===
    first_year = forecast_future['ds'].dt.year.min()
    first_value = forecast_future[forecast_future['ds'].dt.year == first_year]['yhat'].mean()
    last_year = forecast_future['ds'].dt.year.max()
    last_value = forecast_future[forecast_future['ds'].dt.year == last_year]['yhat'].mean()

    explanation = generate_ai_explanation(region_name, pollutant_name, first_year, first_value, last_year, last_value)
    return path, explanation

def chat_loop():
    print("🤖 Ciao! Scrivimi in linguaggio naturale e ti mostro le previsioni.")
    print("Puoi chiedere qualcosa come: 'Come sarà l'aria in Europe?' o 'Analizza African Region'.")

    df = load_data(INPUT_FILE)
    if df is None:
        print("Errore nel caricamento del file.")
        return

    df = clean_data(df)

    while True:
        query = input("🗣️ Tu: ").strip()
        if query.lower() in ["esci", "exit", "quit", "stop"]:
            print("👋 A presto!")
            break
        
        avaible_regions = df['WHO Region'].unique()

        matched_region = None
        query_lower = query.lower()
        region_found = False  # Variabile per evitare duplicati

        # Controlla se la frase contiene nomi italiani e traduce
        for ita, eng in ITALIAN_TO_ENGLISH_REGION.items():
            if ita in query_lower and not region_found:
                matched_region = eng
                print(f"🔍 Regione trovata (da traduzione italiana): {matched_region}")
                df_region = df[df['WHO Region'] == matched_region]

                for key, col_name in POLLUTANTS.items():
                    if col_name in df_region.columns:
                        print(f"📊 Elaborazione: {col_name}")
                        path, explanation = train_and_forecast(df_region, col_name, col_name, matched_region)
                        if path:
                            print(f"[✓] Grafico salvato in: {path}")
                            print(f"\n📄 Spiegazione AI per {col_name}:\n{explanation}\n")
                        else:
                            print(f"[⚠️] Dati insufficienti per {col_name}")
                region_found = True  # Impostiamo che la regione è stata trovata tramite traduzione
                break  # Esci dal ciclo di traduzione per evitare duplicati

        if not region_found:
            # Estrai solo parole "importanti" (regioni) dalla frase 
            words = re.findall(r'\b\w+\b', query_lower)

            # Lista di match per le regioni
            matches = []

            for region in avaible_regions:
                if not isinstance(region, str):
                    continue
                region_lower = region.lower()
                for word in words:
                    # Verifica se le parole dell'utente corrispondono (parzialmente o completamente) al nome della regione
                    if word in region_lower or region_lower in word:
                        matches.append(region)
                        break
                else:
                    # Se nessuna parola matcha, proviamo con parole simili
                    # Utilizziamo difflib per trovare parole simili
                    if difflib.get_close_matches(region_lower, words, n=1, cutoff=0.8):
                        matches.append(region)

            # Eliminiamo i duplicati (es. stessa regione trovata da più parole)
            matches = list(dict.fromkeys(matches))

            if len(matches) == 1:
                matched_region = matches[0]
            elif len(matches) > 1:
                print("❗ La tua frase corrisponde a più regioni.")
                print("Per favore, sii più specifico, puoi visualizzare le previsioni di una regione alla volta.")
                continue

            if not matched_region:
                print("❌ Non ho trovato una regione nella tua frase. Riprova.")
                print(f"Regioni disponibili: {', '.join(avaible_regions)}")
                continue

            print(f"🔍 Regione trovata: {matched_region}")
            df_region = df[df['WHO Region'] == matched_region]

            for key, col_name in POLLUTANTS.items():
                if col_name in df_region.columns:
                    print(f"📊 Elaborazione: {col_name}")
                    path, explanation = train_and_forecast(df_region, col_name, col_name, matched_region)
                    if path:
                        print(f"[✓] Grafico salvato in: {path}")
                        print(f"\n📄 Spiegazione AI per {col_name}:\n{explanation}\n")
                    else:
                        print(f"[⚠️] Dati insufficienti per {col_name}")

if __name__ == "__main__":
    chat_loop()
