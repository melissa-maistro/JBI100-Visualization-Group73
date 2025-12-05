import pandas as pd
import numpy as np
import os

def get_data():
    # Percorso relativo alla cartella data
    # Usa processed_risk_data.csv generato dal notebook
    path = os.path.join('data', 'processed_risk_data.csv')
    
    try:
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        print(f"Errore: Non trovo {path}. Esegui prima il notebook di preprocessing!")
        return pd.DataFrame()