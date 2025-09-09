"""
data_api.py
Modulo para cargar, limpiar, filtrar y analizar datos del suelo.
"""

import pandas as pd

# Columnas de interés del archivo .xlsx
SOIL_COLUMNS = {
    "pH": "pH agua:suelo 2,5:1,0",
    "Phosphorus": "Fósforo (P) Bray II mg/kg",
    "Potassium": "Potasio (K) intercambiable cmol(+)/kg",
    "Aluminum": "Aluminio (Al) intercambiable cmol(+)/kg",
    "Calcium": "Calcio (Ca) intercambiable cmol(+)/kg",
    "Sodium": "Sodio (Na) intercambiable cmol(+)/kg",
    "Zinc": "Zinc (Zn) disponible Olsen mg/kg",
}


def clean_column(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Clean a numeric soil variable column by removing text, replacing commas, and filtering outliers.
    """
    series = df[column].astype(str)

    # Remplaza "ND" con NaN
    series = series.replace("ND", None)

    # Remueve '<' signs
    series = series.str.replace("<", "", regex=False)

    # Remplaza comas con puntos
    series = series.str.replace(",", ".", regex=False)

    # Convertir a numerico, valores no validos -> NaN
    series = pd.to_numeric(series, errors="coerce")

    # Filtrar valores atipicos (> 10000)
    series = series.where(series < 10000, None)

    return series


def load_data(excel_path: str) -> pd.DataFrame:
    
    # Cargar datos del suelo desde Excel y limpiar columnas numericas.
    try:
        df = pd.read_excel(excel_path)

        # Limpia las variables de suelo
        for col in SOIL_COLUMNS.values():
            if col in df.columns:
                df[col] = clean_column(df, col)

        return df

    except FileNotFoundError:
        print("Error: Excel file not found.")
        return pd.DataFrame()


def filter_data(df: pd.DataFrame, department: str,
                municipality: str, crop: str,
                n_records: int) -> pd.DataFrame:
    
    # Filtra los datos por departamento, municipio, cultivo y numero de registros.
    filtered = df[
        (df["Departamento"].str.lower() == department.lower()) &
        (df["Municipio"].str.lower() == municipality.lower()) &
        (df["Cultivo"].str.lower() == crop.lower())
    ]

    return filtered.head(n_records)


def compute_median(df: pd.DataFrame) -> dict:
    
    # Calcular los valores medianos para las variables del suelo.
    if df.empty:
        return {}

    results = {}
    for name, column in SOIL_COLUMNS.items():
        if column in df.columns:
            if df[column].dropna().empty:
                results[name] = "No data"
            else:
                results[name] = round(df[column].median(skipna=True), 2)

    return results
