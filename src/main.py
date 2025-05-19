from utils.data_utils import load_data, clean_data
from utils.ai_utils import generate_ai_chat_response
from models.forecast import train_and_forecast
from config.config import INPUT_FILE, POLLUTANTS

def process_region(df, region_name):
    
    if not region_name:
        print("❗ Non sono riuscito a trovare la regione.")
        return
    
    """Process a specific region and generate forecasts and explanations."""
    df_region = df[df['WHO Region'] == region_name]
    
    for _, col_name in POLLUTANTS.items():
        if col_name in df_region.columns:
            print(generate_ai_chat_response("processing_pollutant", pollutant=col_name))
            path, explanation = train_and_forecast(df_region, col_name, col_name, region_name)
            if path:
                print(f"[✓] Grafico salvato in: {path}")
                print(f"\n📄 Spiegazione AI per {col_name}:\n{explanation}\n")
            else:
                print(f"[⚠️] Dati insufficienti per {col_name}")

def find_region(query, df):
    """Find the region based on the user's query."""
    query_lower = query.lower()
    # Match regions directly or using similar words
    avaible_regions = df['WHO Region'].unique()
    words = query_lower.split()
    matches = [region for region in avaible_regions if isinstance(region, str) and any(
        word in region.lower() or region.lower() in word for word in words)]
    matches = list(dict.fromkeys(matches))  # Remove duplicates
    
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        print("❗ La tua frase corrisponde a più regioni. Sii più specifico.")
        
    return None

def chat_loop():
    print(generate_ai_chat_response("greeting"))

    df = load_data(INPUT_FILE)
    if df is None:
        print("Errore nel caricamento del file.")
        return

    df = clean_data(df)

    while True:
        query = input("🗣️ Tu: ").strip()
        if generate_ai_chat_response("exit_intent", user_message=query):
            print(generate_ai_chat_response("goodbye"))
            break

        matched_region = find_region(query, df)
        if matched_region:
            print(generate_ai_chat_response("region_found", region=matched_region))
            process_region(df, matched_region)
        else:
            print(generate_ai_chat_response("region_not_found"))
            print(f"Regioni disponibili: {', '.join(df['WHO Region'].unique())}")

if __name__ == "__main__":
    chat_loop()
