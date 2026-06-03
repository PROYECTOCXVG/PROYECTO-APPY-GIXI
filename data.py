import pandas as pd
import os

# Ruta absoluta para evitar errores según desde dónde se ejecute
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "Data")

# --- Cargar C1 con su año ---
c1_2019 = pd.read_excel(os.path.join(DATA_PATH, "c1_2019.xlsx")); c1_2019["año"] = 2019
c1_2022 = pd.read_excel(os.path.join(DATA_PATH, "c1_2022.xlsx")); c1_2022["año"] = 2022
c1_2023 = pd.read_excel(os.path.join(DATA_PATH, "c1_ 2023.xlsx")); c1_2023["año"] = 2023

# --- Cargar C2 con su año ---
c2_2019 = pd.read_excel(os.path.join(DATA_PATH, "c2_2019.xlsx")); c2_2019["año"] = 2019
c2_2022 = pd.read_excel(os.path.join(DATA_PATH, "c2_2022.xlsx")); c2_2022["año"] = 2022
c2_2023 = pd.read_excel(os.path.join(DATA_PATH, "c2_2023.xlsx")); c2_2023["año"] = 2023

# --- Normalizar columnas de proporción a porcentaje en 2019 y 2022 ---
cols_normalizar = [
    "internet_proporcion", "tel_celular_proporcion",
    "computador_proporcion", "tv_proporcion", "smartphone_proporcion",
    "internet_fijo_proporcion", "internet_movil_proporcion",
    "internet_fijo_movil_proporcion", "tv_conv_proporcion",
    "tv_lcd_proporcion", "streaming_proporcion", "tableta_proporcion",
    "comp_escr_proporcion", "comp_port_proporcion"
]

for df_temp in [c1_2019, c1_2022]:
    for col in cols_normalizar:
        if col in df_temp.columns and df_temp[col].mean() < 2:
            df_temp[col] = df_temp[col] * 100

# --- Unir todos los C1 y todos los C2 ---
df_c1 = pd.concat([c1_2019, c1_2022, c1_2023], ignore_index=True)

# --- Normalizar columnas de proporción a porcentaje en 2019 y 2022 ---
cols_normalizar_c2 = [
    "tel_celular_proporcion", "smartphone_proporcion",
    "tel_fijo_proporcion_c2", "personas_celular_proporcion"
]
for df_temp in [c2_2019, c2_2022]:
    for col in cols_normalizar_c2:
        if col in df_temp.columns and df_temp[col].mean() < 2:
            df_temp[col] = df_temp[col] * 100

df_c2 = pd.concat([c2_2019, c2_2022, c2_2023], ignore_index=True)

# --- Fusionar C1 y C2 en un solo df ---
columnas_comunes = ["departamento_zona", "departamento", "zona", "año"]
df = pd.merge(df_c1, df_c2, on=columnas_comunes, how="outer", suffixes=("_c1", "_c2"))

print(df["zona"].unique())