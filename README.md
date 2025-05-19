# Previsione della Qualità dell'Aria con l'IA

Air Quality AI Forecast è uno strumento basato su Python per analizzare le tendenze dell'inquinamento atmosferico e prevedere i livelli futuri di inquinanti utilizzando dati storici. Sfrutta modelli di machine learning (Prophet) e spiegazioni generate dall'IA per fornire approfondimenti sulla qualità dell'aria in diverse regioni.

## Funzionalità

- **Pulizia dei Dati**: Pulisce e pre-elabora automaticamente il dataset per l'analisi.
- **Previsioni**: Utilizza la libreria Prophet per prevedere i livelli degli inquinanti per i prossimi 10 anni.
- **Visualizzazione**: Genera grafici che mostrano dati storici e previsioni future.
- **Spiegazioni AI**: Fornisce spiegazioni in linguaggio naturale sulle tendenze tramite un'API AI.
- **Chat Interattiva**: Permette agli utenti di interagire con lo strumento tramite un'interfaccia chat.
- **Risposte AI Dinamiche**: L'interfaccia chat utilizza l'API Groq per generare risposte conversazionali e dinamiche, rendendo l'interazione più coinvolgente.

## Requisiti

Il progetto richiede le seguenti librerie Python, elencate in `requirements.txt`:

- `pandas`
- `matplotlib`
- `requests`
- `prophet`
- `scikit-learn`
- `python-dotenv`

Installa le dipendenze con:

```bash
pip install -r requirements.txt
```

## Utilizzo

1. **Avvia lo Script**: Avvia la chat interattiva eseguendo:

   ```bash
   python src/main.py
   ```

2. **Interagisci con la Chat**: Fai domande come:

   - "Come sarà la qualità dell'aria in Europa?"
   - "Analizza la Regione Africana."

   L'interfaccia chat fornirà risposte dinamiche generate dall'IA, rendendo l'interazione più conversazionale.

3. **Visualizza i Risultati**: Lo strumento genererà:

   - Grafici delle previsioni salvati nella cartella `results/`.
   - Spiegazioni generate dall'IA mostrate nella chat.

4. **Esci**: Per terminare la sessione della chat, digita qualsiasi comando relativo all'uscita (ad esempio "esci", "exit" o "quit").

## Output

- **Grafici**: I grafici delle previsioni sono salvati nella cartella `results/`.
- **Spiegazioni**: Le spiegazioni generate dall'IA sono mostrate nella chat.
- **Risposte Dinamiche**: L'interfaccia chat utilizza l'API Groq per generare risposte personalizzate e contestuali.

## Configurazione

Puoi personalizzare le seguenti impostazioni in `src/config.py`:

- `INPUT_FILE`: Nome del file di input del dataset (default: `data/dataset.xlsx`).
- `OUTPUT_FOLDER`: Cartella dove salvare i risultati (default: `results/`).
- `FORECAST_YEARS`: Numero di anni da prevedere (default: 10).
- `POLLUTANTS`: Dizionario che mappa le chiavi degli inquinanti ai nomi delle colonne del dataset.

## Progettazione Tecnica e Logica del Progetto

### Dataset e Preparazione dei Dati

Il progetto si basa su un dataset contenente misurazioni storiche della qualità dell'aria per diverse regioni OMS. Le colonne principali di interesse sono:

- `WHO Region`: La regione geografica.
- `Measurement Year`: L'anno della misurazione.
- `PM2.5 (μg/m3)`, `PM10 (μg/m3)`, `NO2 (μg/m3)`: Le concentrazioni medie annuali dei principali inquinanti.

**Pulizia dei Dati**:  
Lo script carica il dataset e seleziona solo le colonne rilevanti. Rimuove le righe in cui tutti i valori degli inquinanti sono mancanti, assicurando che vengano utilizzati solo dati significativi per l'analisi.

### Logica delle Previsioni

Per ogni regione e inquinante:

1. **Selezione dei Dati**: Lo strumento filtra il dataset per la regione e l'inquinante selezionati.
2. **Pre-elaborazione**: Rinomina le colonne per adattarle ai requisiti di Prophet (`ds` per la data, `y` per il valore) e converte gli anni in oggetti datetime.
3. **Aggregazione**: Se esistono più misurazioni per lo stesso anno, viene calcolata la media.
4. **Addestramento del Modello**:
   - Viene utilizzata la libreria [Prophet](https://facebook.github.io/prophet/) per la previsione delle serie temporali.
   - Prophet è scelto per la sua robustezza con dati mancanti, outlier e la capacità di modellare la stagionalità annuale.
   - Il modello viene addestrato sui dati storici per ogni inquinante nella regione.
5. **Generazione delle Previsioni**:
   - Il modello prevede i livelli degli inquinanti per i prossimi N anni (default: 10).
   - La previsione include il valore previsto (`yhat`) e un intervallo di confidenza (`yhat_lower`, `yhat_upper`).
6. **Valutazione delle Prestazioni**:
   - L'accuratezza del modello viene valutata sui dati storici utilizzando l'Errore Assoluto Medio (MAE) e il punteggio R².
7. **Visualizzazione**:
   - Viene generato un grafico che mostra dati storici, valori previsti e intervalli di confidenza.
   - Il grafico viene salvato nella cartella `results/`.

### Generazione della Spiegazione AI

Dopo la previsione, lo strumento genera una spiegazione in linguaggio naturale della tendenza:

- **Costruzione del Prompt**:
  - Il prompt riassume la tendenza (aumento/diminuzione, variazione percentuale, anni, valori).
  - Se il valore previsto è molto basso, il prompt avverte sulla plausibilità di risultati così ottimistici.
- **Modello AI**:
  - Il prompt viene inviato all'[API Groq](https://console.groq.com/keys), che utilizza il modello `llama3-70b-8192`.
  - L'IA genera un testo in italiano, discutendo l'impatto sulla salute e sull'ambiente, e le possibili cause della tendenza, basandosi solo sui dati e sul grafico.
- **Integrazione**:
  - La spiegazione viene mostrata nella chat insieme al grafico.

### Logica della Chat Interattiva

- L'utente interagisce tramite un'interfaccia chat.
- Lo strumento riconosce i nomi delle regioni (in italiano o inglese) utilizzando fuzzy matching e un dizionario di traduzione.
- Per ogni query valida, lo strumento:
  1. Conferma la regione.
  2. Elabora tutti gli inquinanti disponibili per quella regione.
  3. Mostra il grafico delle previsioni e la spiegazione AI.
- La chat utilizza l'API Groq per generare risposte dinamiche e contestuali per saluti, conferme ed errori, rendendo l'interazione più naturale.

### Riepilogo della Pipeline

1. **Input Utente**: L'utente chiede informazioni sulla qualità dell'aria in una regione.
2. **Rilevamento Regione**: Lo strumento identifica la regione dalla query.
3. **Estrazione Dati**: I dati rilevanti vengono filtrati e puliti.
4. **Previsione**: Prophet prevede i livelli futuri degli inquinanti.
5. **Generazione Grafico**: Viene creata e salvata una visualizzazione.
6. **Spiegazione AI**: La tendenza viene spiegata tramite un LLM via API.
7. **Output Chat**: L'utente riceve grafico, spiegazione e risposte dinamiche.

### Perché Prophet e LLM?

- **Prophet**:
  - Gestisce bene dati mancanti e outlier.
  - Modella la stagionalità annuale, tipica dei dati ambientali.
  - Richiede una minima ottimizzazione dei parametri.
- **LLM (Groq API)**:
  - Fornisce spiegazioni umane e contestuali.
  - Migliora il coinvolgimento e la comprensione dell'utente.
  - Può generare risposte dinamiche in chat, rendendo lo strumento più interattivo.

### Estendibilità

- L'architettura consente di aggiungere facilmente nuovi inquinanti o regioni.
- Il prompt AI può essere adattato per diverse lingue o stili di spiegazione.
- L'orizzonte di previsione e i parametri del modello sono configurabili.

## Note

- Il progetto utilizza l'API Groq per spiegazioni e risposte in chat generate dall'IA. Per utilizzare questo progetto, devi:
  1. Ottenere la tua chiave API registrandoti sul [sito Groq API](https://console.groq.com/keys).
  2. Creare un file `.env` nella directory principale del progetto.
  3. Aggiungere la seguente riga al file `.env`, sostituendo `your_api_key` con la tua chiave API reale:
     ```
     GROQ_API_KEY=your_api_key
     ```
- Assicurati che il tuo dataset contenga dati sufficienti per previsioni accurate.
