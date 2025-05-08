import os
import re
import matplotlib.pyplot as plt
import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, r2_score
from utils.ai_utils import generate_ai_explanation
from config.config import OUTPUT_FOLDER, FORECAST_YEARS

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
