import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def get_data():
    # Helper per pulire valute e percentuali
    def clean_currency(x):
        if isinstance(x, str):
            return float(x.replace(',', '').replace('$', '').replace('%', ''))
        return x

    # Caricamento Dataset (Assumiamo che i CSV siano nella root folder del progetto)
    try:
        comm = pd.read_csv('communications_data.csv')
        demo = pd.read_csv('demographics_data.csv')
        econ = pd.read_csv('economy_data.csv')
        gov = pd.read_csv('government_and_civics_data.csv')
        trans = pd.read_csv('transportation_data.csv')
    except FileNotFoundError:
        # Fallback per evitare crash se i file non ci sono ancora
        return pd.DataFrame()

    # Merge dei dataset
    df = demo.merge(econ, on='Country', how='left') \
             .merge(comm, on='Country', how='left') \
             .merge(gov, on='Country', how='left') \
             .merge(trans, on='Country', how='left')

    # Pulizia colonne
    cols_to_clean = [
        'Total_Literacy_Rate', 'Youth_Unemployment_Rate', 'Population_Growth_Rate',
        'Real_GDP_per_Capita_USD', 'Population_Below_Poverty_Line_percent',
        'internet_users_total', 'Total_Population'
    ]

    for col in cols_to_clean:
        if col in df.columns:
            df[col] = df[col].apply(clean_currency)

    df = df.fillna(0)

    # --- CALCOLO RISCHI (Normalizzazione) ---
    scaler = MinMaxScaler()

    # 1. Rischio Economico (Inv. GDP, Povertà, Disoccupazione)
    df['norm_poverty'] = scaler.fit_transform(df[['Population_Below_Poverty_Line_percent']])
    df['norm_unemployment'] = scaler.fit_transform(df[['Youth_Unemployment_Rate']])
    df['norm_gdp_inverted'] = 1 - scaler.fit_transform(df[['Real_GDP_per_Capita_USD']]) 
    df['Economic Risk'] = (df['norm_poverty'] + df['norm_unemployment'] + df['norm_gdp_inverted']) / 3

    # 2. Rischio Demografico
    df['Demographic Risk'] = scaler.fit_transform(df[['Population_Growth_Rate']])

    # 3. Rischio Infrastrutturale
    df['internet_per_capita'] = df['internet_users_total'] / df['Total_Population']
    df['internet_per_capita'] = df['internet_per_capita'].replace([np.inf, -np.inf], 0).fillna(0)
    df['Infrastructure Risk'] = 1 - scaler.fit_transform(df[['internet_per_capita']])

    # 4. Rischio Sociale
    df['Social Risk'] = 1 - scaler.fit_transform(df[['Total_Literacy_Rate']])

    # Totale
    risk_columns = ['Economic Risk', 'Demographic Risk', 'Infrastructure Risk', 'Social Risk']
    df['Total Vulnerability'] = df[risk_columns].mean(axis=1)

    return df