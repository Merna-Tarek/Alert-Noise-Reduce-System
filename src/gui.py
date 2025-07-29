import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import joblib
import os

# Load trained model and vectorizer
VECTORIZER_PATH = "models/vectorizer.pkl"
CLASSIFIER_PATH = "models/noise_classifier.pkl"
DEFAULT_LOG_PATH = "data/generated_siem_logs.csv"

vectorizer = joblib.load(VECTORIZER_PATH)
classifier = joblib.load(CLASSIFIER_PATH)

class AlertNoiseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Alert Noise Classifier GUI")
        self.df = pd.DataFrame()

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Load button
        tk.Button(frame, text="Load Alerts File", command=self.load_file).grid(row=0, column=0, sticky="w")

        # Predict button
        tk.Button(frame, text="Predict Noise", command=self.predict_noise).grid(row=0, column=1, padx=10)

        # Filter options
        tk.Label(frame, text="Filter:").grid(row=0, column=2)
        self.filter_var = tk.StringVar(value="All")
        filter_menu = ttk.Combobox(frame, textvariable=self.filter_var, values=["All", "VALID", "NOISY"])
        filter_menu.grid(row=0, column=3)
        filter_menu.bind("<<ComboboxSelected>>", self.update_table)

        # Export button
        tk.Button(frame, text="Export CSV", command=self.export_csv).grid(row=0, column=4, padx=10)

        # Table
        self.tree = ttk.Treeview(frame, columns=("Timestamp", "Source IP", "Alert", "Label"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.grid(row=1, column=0, columnspan=5, pady=10, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=5, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if path:
            self.load_and_display(path)

    def load_and_display(self, path):
        try:
            self.df = pd.read_csv(path)
            if "alert_description" not in self.df.columns:
                raise ValueError("Missing required column: alert_description")
            self.df["label"] = "Not Predicted"
            self.update_table()
        except Exception as e:
            messagebox.showerror("Load Error", str(e))

    def predict_noise(self):
        try:
            alerts = self.df["alert_description"].astype(str)
            X = vectorizer.transform(alerts)
            preds = classifier.predict(X)
            self.df["prediction"] = preds
            self.df["label"] = self.df["prediction"].apply(lambda x: "NOISY" if x == 1 else "VALID")
            self.update_table()
        except Exception as e:
            messagebox.showerror("Prediction Error", str(e))

    def update_table(self, event=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        if self.df.empty:
            return

        filt = self.filter_var.get()
        if filt == "VALID":
            rows = self.df[self.df["label"] == "VALID"]
        elif filt == "NOISY":
            rows = self.df[self.df["label"] == "NOISY"]
        else:
            rows = self.df

        for _, row in rows.iterrows():
            self.tree.insert("", "end", values=(row.get("timestamp", "-"), row.get("source_ip", "-"), row.get("alert_description", "-"), row.get("label", "-")))

    def export_csv(self):
        if self.df.empty or "label" not in self.df.columns:
            messagebox.showinfo("Export", "Nothing to export. Run prediction first.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if path:
            self.df.to_csv(path, index=False)
            messagebox.showinfo("Export", f"Results exported to {path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AlertNoiseGUI(root)
    app.load_and_display(DEFAULT_LOG_PATH)  # Auto-load SIEM logs
    root.mainloop()