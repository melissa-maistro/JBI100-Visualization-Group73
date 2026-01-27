import os
import numpy as np
import pandas as pd


def _parse_numeric(series: pd.Series) -> pd.Series:
    cleaned = series.astype(str).str.replace(r"[^\d\.]", "", regex=True)
    return pd.to_numeric(cleaned, errors="coerce")


def _minmax(series: pd.Series) -> pd.Series:
    min_val = series.min()
    max_val = series.max()
    if pd.isna(min_val) or pd.isna(max_val) or max_val == min_val:
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - min_val) / (max_val - min_val)

def get_data():
    # Percorso al file generato dal notebook
    path = os.path.join('data', 'processed_risk_data.csv')

    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print(f"Errore: Non trovo {path}. Assicurati di aver eseguito il notebook!")
        return pd.DataFrame()

    # --- Transport constraint index (Task 3.1.4) ---
    try:
        transport_df = pd.read_csv(os.path.join('data', 'transportation_data.csv'))
        demo_df = pd.read_csv(os.path.join('data', 'demographics_data.csv'))
        geo_df = pd.read_csv(os.path.join('data', 'geography_data.csv'))

        demo_df["Total_Population"] = _parse_numeric(demo_df["Total_Population"])
        geo_df["Land_Area"] = _parse_numeric(geo_df["Land_Area"])

        transport_cols = [
            "airports_paved_runways_count",
            "airports_unpaved_runways_count",
            "roadways_km",
            "railways_km",
            "waterways_km",
        ]
        for col in transport_cols:
            transport_df[col] = pd.to_numeric(transport_df[col], errors="coerce")

        df = df.merge(transport_df, on="Country", how="left")
        df = df.merge(demo_df[["Country", "Total_Population"]], on="Country", how="left")
        df = df.merge(geo_df[["Country", "Land_Area"]], on="Country", how="left")

        pop = df["Total_Population"]
        area = df["Land_Area"]

        def _per_unit(values: pd.Series) -> pd.Series:
            per_pop = values / pop * 1_000_000
            per_area = values / area * 1_000
            return per_pop.where(pop.notna() & (pop > 0), per_area)

        runways_total = df["airports_paved_runways_count"].fillna(0) + df["airports_unpaved_runways_count"].fillna(0)

        metrics = pd.DataFrame(
            {
                "runways_density": _per_unit(runways_total),
                "roadways_density": _per_unit(df["roadways_km"]),
                "railways_density": _per_unit(df["railways_km"]),
                "waterways_density": _per_unit(df["waterways_km"]),
            }
        )

        # Neutral imputation for missing values + log scaling to reduce skew
        metrics = metrics.apply(lambda s: s.fillna(s.median()), axis=0)
        metrics = metrics.clip(lower=0)
        metrics_log = metrics.apply(np.log1p)
        metrics_norm = metrics_log.apply(_minmax, axis=0)

        transport_supply = metrics_norm.mean(axis=1)
        df["Transport Constraint"] = 1 - transport_supply
        df["Transport Supply"] = transport_supply
    except Exception as exc:
        print(f"Warning: Transport data merge failed: {exc}")
        # Return base dataframe if transport pipeline fails
        return df

    return df
