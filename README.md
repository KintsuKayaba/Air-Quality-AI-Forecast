# MPA-Project

MPA-Project è uno strumento basato su Python per analizzare le tendenze dell'inquinamento atmosferico e prevedere i livelli futuri di inquinanti utilizzando dati storici. Utilizza modelli di machine learning (Prophet) e spiegazioni generate da AI per fornire approfondimenti sulla qualità dell'aria in diverse regioni.

## Funzionalità

- **Pulizia dei Dati**: Pulisce e pre-elabora automaticamente il dataset per l'analisi.
- **Previsioni**: Utilizza la libreria Prophet per prevedere i livelli di inquinanti per i prossimi 10 anni.
- **Visualizzazione**: Genera grafici che mostrano dati storici e previsioni future.
- **Spiegazioni AI**: Fornisce spiegazioni in linguaggio naturale delle tendenze utilizzando un'API AI.
- **Chat Interattiva**: Permette agli utenti di interagire con lo strumento tramite un'interfaccia chat.

## Requisiti

Il progetto richiede le seguenti librerie Python, elencate in `requirements.txt`:

- `pandas`
- `matplotlib`
- `requests`
- `prophet`
- `scikit-learn`

Installa le dipendenze con:

```bash
pip install -r requirements.txt
```

## Utilizzo

1. **Prepara il Dataset**: Posiziona il file del dataset nella directory del progetto e chiamalo `Dataset.xlsx`. Assicurati che contenga colonne per `WHO Region`, `Measurement Year` e i livelli di inquinanti (es. PM2.5, PM10, NO2).

2. **Esegui lo Script**: Avvia la chat interattiva eseguendo:

   ```bash
   python progetto.py
   ```

3. **Interagisci con la Chat**: Fai domande come:

   - "Come sarà l'aria in Europe?"
   - "Analizza African Region."

4. **Visualizza i Risultati**: Lo strumento genererà:

   - Grafici delle previsioni salvati nella cartella `Results/`.
   - Spiegazioni generate dall'AI mostrate nella chat.

5. **Esci**: Digita `esci`, `exit` o `quit` per chiudere la chat.

## Output

- **Grafici**: I grafici delle previsioni sono salvati nella cartella `Results/`.
- **Spiegazioni**: Le spiegazioni generate dall'AI sono mostrate nella chat.

## Configurazione

Puoi personalizzare le seguenti impostazioni in `progetto.py`:

- `INPUT_FILE`: Nome del file del dataset di input (predefinito: `Dataset.xlsx`).
- `OUTPUT_FOLDER`: Cartella in cui salvare i risultati (predefinito: `Results`).
- `FORECAST_YEARS`: Numero di anni da prevedere (predefinito: 10).
- `POLLUTANTS`: Dizionario che mappa le chiavi degli inquinanti ai nomi delle colonne nel dataset.

## Note

- Il progetto utilizza l'API Groq per le spiegazioni generate dall'AI. Sostituisci la chiave `GROQ_API_KEY` in `progetto.py` con la tua chiave API.
- Assicurati che il tuo dataset contenga dati sufficienti per previsioni accurate.
