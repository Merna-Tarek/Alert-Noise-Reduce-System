# Alert Noise Reducer

A Python project for classifying and reducing noisy alerts in SIEM and security log data. Includes both a Tkinter GUI and a Streamlit dashboard for interactive use.

## Features
- Batch alert noise prediction from .txt or .csv files
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
