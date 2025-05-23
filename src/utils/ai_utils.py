import requests
from config.config import GROQ_API_KEY

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

def generate_ai_chat_response(message_type, region=None, pollutant=None, user_message=None):
    """Generate AI-like chat responses using the Groq API."""
    prompts = {
        "greeting": (
            "Saluta l'utente e spiega che puoi fornire previsioni sulla qualità dell'aria "
            "solo per le regioni OMS disponibili nel dataset (ad esempio: European Region, African Region, ecc.) "
            "e solo per gli inquinanti PM2.5, PM10 e NO2. "
            "Invita l'utente a chiedere informazioni su una di queste regioni."
        ),
        "region_found": f"Conferma che hai trovato la regione {region} e che stai procedendo con l'analisi.",
        "region_not_found": "Informa l'utente che non hai trovato una regione nella sua frase e suggerisci di riprovare.",
        "processing_pollutant": f"Sto elaborando i dati per {pollutant}. Attendi qualche secondo mentre preparo la previsione.",
        "goodbye": "Saluta l'utente e ringrazialo per aver usato il servizio.",
        "exit_intent": (
            "Rispondi solo con 'SI' o 'NO'. "
            "La seguente frase dell'utente indica che vuole terminare o uscire dalla conversazione? "
            f"Frase: \"{user_message}\""
        ) if user_message else ""
    }
    prompt = prompts.get(message_type, "")
    if not prompt:
        return ""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0 if message_type == "exit_intent" else 0.7
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        try:
            content = response.json()['choices'][0]['message']['content'].strip()
            if message_type == "exit_intent":
                return content.lower().startswith("si")
            return content
        except Exception:
            return "Errore nella generazione della risposta"
    else:
        return f"[ERRORE AI] {response.text}"
