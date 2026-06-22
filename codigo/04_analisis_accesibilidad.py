"""
Análisis de accesibilidad: distancia y tiempo de traslado al hospital.

Este archivo debe ejecutarse después de 01 y 02, ya que utiliza df_pacientes.

Analiza:
- Distancia al hospital (km).
- Tiempo de traslado (minutos).
- Comparación entre pacientes urbanos y rurales.
"""

import os
import matplotlib.pyplot as plt
import pandas as pd

# =========================
# CARPETA DE SALIDA
# =========================
carpeta_salida = "imagenes_resultados"
os.makedirs(carpeta_salida, exist_ok=True)

# =========================
# LIMPIEZA DE DATOS
# =========================
df_accesibilidad = df_pacientes.copy()

# Aseguramos que las columnas existan y sean numéricas
df_accesibilidad["km"] = pd.to_numeric(
    df_accesibilidad["km"], errors="coerce"
)
df_accesibilidad["tiempo (minutos)"] = pd.to_numeric(
    df_accesibilidad["tiempo (minutos)"], errors="coerce"
)

# Eliminar filas sin datos de km o tiempo
df_accesibilidad = df_accesibilidad.dropna(subset=["km", "tiempo (minutos)"])

# =========================
# HISTOGRAMA: DISTANCIA
# =========================
plt.figure(figsize=(8, 5))
plt.hist(
    df_accesibilidad["km"], bins=15, color=AZUL_MEDIO, edgecolor=AZUL_OSCURO
)
plt.title("Distribución de distancia al hospital (km)")
plt.xlabel("Distancia al hospital (km)")
plt.ylabel("Número de pacientes")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(f"{carpeta_salida}/distancia_hospital.png", dpi=300)
plt.close()

# =========================
# HISTOGRAMA: TIEMPO
# =========================
plt.figure(figsize=(8, 5))
plt.hist(
    df_accesibilidad["tiempo (minutos)"], bins=15, color=AZUL_MEDIO, edgecolor=AZUL_OSCURO
)
plt.title("Distribución del tiempo de traslado (minutos)")
plt.xlabel("Tiempo de traslado (minutos)")
plt.ylabel("Número de pacientes")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(f"{carpeta_salida}/tiempo_traslado.png", dpi=300)
plt.close()

# =========================
# COMPARACIÓN URBANO/RURAL: TIEMPO PROMEDIO
# =========================
if "clas_final" in df_pacientes.columns:
    promedio_tiempo = (
        df_accesibilidad.groupby("clas_final")["tiempo (minutos)"]
        .mean()
        .round(2)
    )
    
    plt.figure(figsize=(6, 5))
    promedio_tiempo.plot(
        kind="bar", color=[AZUL_MEDIO, AZUL_CLARO], edgecolor=AZUL_OSCURO
    )
    plt.title("Tiempo promedio de traslado según zona")
    plt.xlabel("Clasificación territorial")
    plt.ylabel("Promedio de tiempo (minutos)")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{carpeta_salida}/tiempo_promedio_zona.png", dpi=300)
    plt.close()

    print("\nTiempo promedio (minutos) por zona:")
    print(promedio_tiempo)
