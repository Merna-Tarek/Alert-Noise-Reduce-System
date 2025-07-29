
# Alert Noise Reducer

A Python AI project for classifying, predicting, and reducing noisy alerts in SIEM and security log data. It uses machine learning models to predict whether an alert is noisy or valid. Includes both a Tkinter GUI and a Streamlit dashboard for interactive use.

## What does it do?
- Predicts if a security alert is noisy (false positive) or valid (true positive) using a trained AI model.
- Supports batch prediction from files and single alert prediction.
- Helps security teams focus on real threats by filtering out noise.

## How does it work?
- Uses a machine learning classifier (trained on labeled alert data) and a text vectorizer.
- The model is loaded from `models/noise_classifier.pkl` and the vectorizer from `models/vectorizer.pkl`.
- You can use the Streamlit dashboard for interactive exploration, or the Tkinter GUI for a classic desktop experience.

## Features
- Batch alert noise prediction from .txt or .csv files
- Predicts noisy vs. valid alerts using AI/ML
- Interactive dashboard with Streamlit
- Classic desktop GUI with Tkinter
- Export and filter results
- Model and vectorizer loading from `models/`


## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/your-username/alert_noise_reducer.git
cd alert_noise_reducer
```

### 2. Set up a virtual environment (recommended)
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit dashboard
```bash
.venv\Scripts\python.exe -m streamlit run src/dashboard.py
```

### 5. Run the Tkinter GUI
```bash
.venv\Scripts\python.exe src/gui.py
```

## File Structure
- `src/` - Source code (dashboard, GUI, prediction logic)
- `models/` - Trained model and vectorizer files
- `data/` - Example and generated log data
- `requirements.txt` - Python dependencies

## Notes
- The Streamlit dashboard expects a CSV with an `alert` column for predictions.
- The Tkinter GUI expects a CSV with an `alert_description` column.
- Model files (`.pkl`) and sample data are included for demonstration.

## License
MIT
