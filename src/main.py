import re
import difflib
import random
from utils.data_utils import load_data, clean_data
from utils.ai_utils import generate_ai_explanation, generate_ai_chat_response
from models.forecast import train_and_forecast
from config.config import INPUT_FILE, ITALIAN_TO_ENGLISH_REGION, POLLUTANTS

def generate_ai_response(message_type, region=None, pollutant=None):
    """Generate dynamic AI-like responses for the chat."""
    responses = {
        "greeting": [
            "Ciao! Sono qui per aiutarti con le previsioni sulla qualità dell'aria. 😊",
            "Benvenuto! Scrivimi qualcosa e ti mostrerò le previsioni sull'aria. 🌍",
        ],
        "region_found": [
            f"Ho trovato la regione {region}. Procedo con l'analisi! 🔍",
            f"Perfetto, analizziamo la regione {region}. 🚀",
        ],
        "region_not_found": [
            "Non riesco a trovare una regione nella tua frase. Prova a essere più specifico. 🤔",
            "Mi dispiace, non ho capito la regione. Puoi riprovare? 🧐",
        ],
        "processing_pollutant": [
            f"Sto elaborando i dati per {pollutant}. Un attimo... ⏳",
            f"Analizzo {pollutant}. Ti mostro i risultati tra poco! 📊",
        ],
        "goodbye": [
            "Grazie per avermi usato! Alla prossima! 👋",
            "È stato un piacere aiutarti. A presto! 😊",
        ],
    }
    return random.choice(responses.get(message_type, [""]))

def process_region(df, region_name):
    """Process a specific region and generate forecasts and explanations."""
    df_region = df[df['WHO Region'] == region_name]
    for key, col_name in POLLUTANTS.items():
        if col_name in df_region.columns:
            print(generate_ai_response("processing_pollutant", pollutant=col_name))
            path, explanation = train_and_forecast(df_region, col_name, col_name, region_name)
            if path:
                print(f"[✓] Grafico salvato in: {path}")
                print(f"\n📄 Spiegazione AI per {col_name}:\n{explanation}\n")
            else:
                print(f"[⚠️] Dati insufficienti per {col_name}")

def find_region(query, df):
    """Find the region based on the user's query."""
    query_lower = query.lower()
    # Check for Italian-to-English translation
    for ita, eng in ITALIAN_TO_ENGLISH_REGION.items():
        if ita in query_lower:
            return eng, "traduzione italiana"
    # Match regions directly or using similar words
    avaible_regions = df['WHO Region'].unique()
    words = re.findall(r'\b\w+\b', query_lower)
    matches = [region for region in avaible_regions if isinstance(region, str) and any(
        word in region.lower() or region.lower() in word for word in words)]
    matches = list(dict.fromkeys(matches))  # Remove duplicates
    if len(matches) == 1:
        return matches[0], "match diretto"
    elif len(matches) > 1:
        print("❗ La tua frase corrisponde a più regioni. Sii più specifico.")
    return None, None

def chat_loop():
    print(generate_ai_chat_response("greeting"))

    df = load_data(INPUT_FILE)
    if df is None:
        print("Errore nel caricamento del file.")
        return

    df = clean_data(df)

    while True:
        query = input("🗣️ Tu: ").strip()
        if query.lower() in ["esci", "exit", "quit", "stop"]:
            print(generate_ai_chat_response("goodbye"))
            break

        matched_region, match_type = find_region(query, df)
        if matched_region:
            print(generate_ai_chat_response("region_found", region=matched_region))
            process_region(df, matched_region)
        else:
            print(generate_ai_chat_response("region_not_found"))
            print(f"Regioni disponibili: {', '.join(df['WHO Region'].unique())}")

if __name__ == "__main__":
    chat_loop()
