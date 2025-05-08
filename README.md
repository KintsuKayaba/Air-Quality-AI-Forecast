# Air Quality AI Forecast

Air Quality AI Forecast is a Python-based tool for analyzing air pollution trends and forecasting future pollutant levels using historical data. It leverages machine learning models (Prophet) and AI-generated explanations to provide insights into air quality across different regions.

## Features

- **Data Cleaning**: Automatically cleans and preprocesses the dataset for analysis.
- **Forecasting**: Uses the Prophet library to predict pollutant levels for the next 10 years.
- **Visualization**: Generates charts showing historical data and future forecasts.
- **AI Explanations**: Provides natural language explanations of trends using an AI API.
- **Interactive Chat**: Allows users to interact with the tool via a chat interface.

## Requirements

The project requires the following Python libraries, listed in `requirements.txt`:

- `pandas`
- `matplotlib`
- `requests`
- `prophet`
- `scikit-learn`
- `python-dotenv`

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

1. **Prepare the Dataset**: Place the dataset file in the `data/` directory and name it `dataset.xlsx`. Ensure it contains columns for `WHO Region`, `Measurement Year`, and pollutant levels (e.g., PM2.5, PM10, NO2).

2. **Run the Script**: Start the interactive chat by running:

   ```bash
   python src/main.py
   ```

3. **Interact with the Chat**: Ask questions like:

   - "What will the air quality be like in Europe?"
   - "Analyze African Region."

4. **View Results**: The tool will generate:

   - Forecast charts saved in the `results/` folder.
   - AI-generated explanations displayed in the chat.

5. **Exit**: Type `exit`, `quit`, or `q` to close the chat.

## Output

- **Charts**: Forecast charts are saved in the `results/` folder.
- **Explanations**: AI-generated explanations are displayed in the chat.

## Configuration

You can customize the following settings in `src/config.py`:

- `INPUT_FILE`: Name of the input dataset file (default: `data/dataset.xlsx`).
- `OUTPUT_FOLDER`: Folder to save results (default: `results/`).
- `FORECAST_YEARS`: Number of years to forecast (default: 10).
- `POLLUTANTS`: Dictionary mapping pollutant keys to dataset column names.

## Notes

- The project uses the Groq API for AI-generated explanations. To use this project, you must:
  1. Obtain your API key by registering on the [Groq API website](https://console.groq.com/keys).
  2. Create a `.env` file in the root directory of the project.
  3. Add the following line to the `.env` file, replacing `your_api_key` with your actual API key:
     ```
     GROQ_API_KEY=your_api_key
     ```
- Ensure your dataset contains sufficient data for accurate forecasts.
