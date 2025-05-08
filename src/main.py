import re
import difflib
from utils.data_utils import load_data, clean_data
from utils.ai_utils import generate_ai_explanation
from models.forecast import train_and_forecast
from config.config import INPUT_FILE, ITALIAN_TO_ENGLISH_REGION, POLLUTANTS

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
