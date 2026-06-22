"""
Análisis de trayectorias diagnósticas (CIE-10).

Debe ejecutarse tras la carga de df_hosp. Analiza transiciones entre diagnósticos consecutivos (diag1 → diag2, etc.) y trayectorias más frecuentes.

Requiere columnas 'diag1_codigo', 'diag2_codigo', ... en df_hosp.
"""

import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

# =========================
# COLUMNAS DE DIAGNÓSTICO
# =========================
columnas_diag = ["diag1_codigo", "diag2_codigo", "diag3_codigo", "diag4_codigo", "diag5_codigo"]

# Aseguramos que las columnas sean string y limpias
for col in columnas_diag:
    df_hosp[col] = df_hosp[col].astype(str).str.strip().str.upper().replace(["", "NAN"], pd.NA)

# =========================
# TRANSICIONES ENTRE DIAGNÓSTICOS
# =========================
def calcular_transiciones(df, columnas):
    transiciones = []
    for _, row in df.iterrows():
        secuencia = [row[col] for col in columnas if pd.notna(row[col])]
        for i in range(len(secuencia) - 1):
            transiciones.append((secuencia[i], secuencia[i + 1]))

    conteo = Counter(transiciones)
    df_trans = pd.DataFrame(conteo.items(), columns=["origen", "destino", "frecuencia"])
    df_trans = df_trans.sort_values(by="frecuencia", ascending=False)
    return df_trans

transiciones_completas = calcular_transiciones(df_hosp, columnas_diag)

# Guardar o mostrar las principales transiciones
transiciones_completas.to_csv(f"{carpeta_salida}/transiciones_diagnosticos.csv", index=False)
print("Principales transiciones:")
print(transiciones_completas.head(10))

# =========================
# TRAYECTORIAS COMPLETAS (MULTI-DIAGNÓSTICO)
# =========================
def calcular_trayectorias(df, columnas):
    trayectorias = df[columnas].dropna().apply(tuple, axis=1)
    conteo = trayectorias.value_counts().reset_index()
    conteo.columns = ["trayectoria", "frecuencia"]
    conteo["trayectoria"] = conteo["trayectoria"].apply(lambda x: " → ".join(x))
    return conteo

trayectorias_completas = calcular_trayectorias(df_hosp, columnas_diag)

# Guardar o mostrar las trayectorias
trayectorias_completas.to_csv(f"{carpeta_salida}/trayectorias_diagnosticas.csv", index=False)
print("Principales trayectorias:")
print(trayectorias_completas.head(10))
