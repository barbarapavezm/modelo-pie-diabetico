"""
Configuración inicial y carga de datos del proyecto:
"Modelo multietapa de progresión clínica del pie diabético".

Este archivo contiene la importación de librerías, configuración general,
definición de colores del proyecto y carga inicial de las bases utilizadas.

IMPORTANTE:
Las bases de datos originales no se incluyen en este repositorio porque
contienen información clínica y administrativa sensible de pacientes.

Para ejecutar este código, el usuario debe guardar sus archivos Excel dentro
de la carpeta "datos/" y modificar los nombres indicados en la sección
"CARGA DE DATOS".
"""

# =========================
# LIBRERÍAS PRINCIPALES
# =========================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from unidecode import unidecode

warnings.filterwarnings("ignore")

plt.rcParams["figure.figsize"] = (10, 4)
pd.set_option("display.max_columns", 100)


# =========================
# LIBRERÍAS GEOESPACIALES
# =========================

import geopandas as gpd
import folium
from folium.plugins import MarkerCluster, HeatMap


# =========================
# GRAFOS Y REDES
# =========================

import networkx as nx


# =========================
# PALETA DE COLORES DEL TRABAJO
# =========================

AZUL_OSCURO = "#1B3A57"
AZUL_MEDIO = "#1F77B4"
AZUL_CLARO = "#6BAED6"
CELESTE = "#A9D6E5"
GRIS_AZULADO = "#B0C4DE"
GRIS_SUAVE = "#ECEFF1"

PALETA_AZUL = [
    AZUL_OSCURO,
    AZUL_MEDIO,
    AZUL_CLARO,
    CELESTE,
    GRIS_AZULADO
]


# =========================
# FUNCIONES AUXILIARES
# =========================

def limpiar_columnas(df):
    """
    Limpia los nombres de columnas eliminando espacios al inicio/final,
    tildes y caracteres especiales.
    Retorna:
    DataFrame con nombres de columnas normalizados.
    """
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .map(unidecode)
    )
    return df

'''
=========================
CARGA DE DATOS
=========================
IMPORTANTE:
Las bases de datos originales no se incluyen en este repositorio
porque contienen información clínica y administrativa sensible.

Para ejecutar este código:
1. Crea una carpeta llamada "datos/".
2. Guarda dentro tus archivos Excel.
3. Cambia los nombres de archivo en las siguientes variables.

En este proyecto se trabaja con dos DataFrames principales:

- df_hosp:
  Corresponde a la base de hospitalizaciones.
  Contiene todos los egresos/hospitalizaciones registrados.
  Un mismo paciente puede aparecer más de una vez si tuvo múltiples ingresos.
  Se utiliza para analizar reingreso, número de hospitalizaciones,
  estancia hospitalaria, trayectorias diagnósticas y redes bayesianas.

- df_pacientes:
  Corresponde a la base de pacientes únicos.
  Contiene una sola fila por paciente, construida a partir del identificador "Codigo".
  Se utiliza para conteos descriptivos a nivel individual, distribución por comuna,
  sexo, clasificación territorial y accesibilidad geográfica.

Esta separación permite diferenciar los análisis a nivel de hospitalización
de los análisis a nivel de paciente.
'''

ruta_datos = "datos/"

archivo_hospitalizaciones = "AQUI_TU_ARCHIVO_DE_HOSPITALIZACIONES.xlsx"
archivo_pacientes = "AQUI_TU_ARCHIVO_DE_PACIENTES.xlsx"

df_hosp = pd.read_excel(ruta_datos + archivo_hospitalizaciones)
df_pacientes = pd.read_excel(ruta_datos + archivo_pacientes)

df_hosp = limpiar_columnas(df_hosp)
df_pacientes = limpiar_columnas(df_pacientes)

print("Base hospitalizaciones:", df_hosp.shape)
print("Base pacientes:", df_pacientes.shape)


# =========================
# LIMPIEZA BÁSICA DE FECHAS
# =========================

fechas = [
    "Fecha ingreso completa",
    "Fecha de egreso completa"
]

for col in fechas:
    if col in df_hosp.columns:
        df_hosp[col] = pd.to_datetime(df_hosp[col], errors="coerce")


# =========================
# LIMPIEZA BÁSICA DE COORDENADAS
# =========================

for base in [df_hosp, df_pacientes]:
    for col in ["lat", "lon"]:
        if col in base.columns:
            base[col] = pd.to_numeric(base[col], errors="coerce")


# =========================
# BASES CON COORDENADAS VÁLIDAS
# =========================

df_hosp_geo = df_hosp.dropna(subset=["lat", "lon"]).copy()
df_pacientes_geo = df_pacientes.dropna(subset=["lat", "lon"]).copy()

print("Hospitalizaciones con coordenadas:", df_hosp_geo.shape)
print("Pacientes con coordenadas:", df_pacientes_geo.shape)


# =========================
# VISUALIZACIÓN INICIAL
# =========================

print("\nColumnas hospitalizaciones:")
print(df_hosp.columns.tolist())

print("\nColumnas pacientes:")
print(df_pacientes.columns.tolist())

print("\nPrimeras filas hospitalizaciones:")
print(df_hosp.head())

print("\nPrimeras filas pacientes:")
print(df_pacientes.head())
