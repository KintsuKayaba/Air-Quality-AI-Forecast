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
