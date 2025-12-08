import pandas as pd
import os

def get_data():
    # Percorso al file generato dal notebook
    path = os.path.join('data', 'processed_risk_data.csv')
    
    try:
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        print(f"Errore: Non trovo {path}. Assicurati di aver eseguito il notebook!")
        return pd.DataFrame()