
"""
Clasificación territorial urbano-rural de pacientes con pie diabético.

Este archivo utiliza las coordenadas de residencia de los pacientes y el archivo
geoespacial de áreas pobladas para clasificar cada paciente como:

- Urbano: si su coordenada cae dentro de un área poblada.
- Rural: si su coordenada no cae dentro de un área poblada.

IMPORTANTE:
Este archivo debe ejecutarse después de haber cargado los datos en
01_configuracion_y_carga.py, ya que utiliza el DataFrame df_pacientes_geo.
"""

# =========================
# LIBRERÍAS
# =========================

import pandas as pd
import geopandas as gpd


# =========================
# ARCHIVO GEOESPACIAL
# =========================
# En este repositorio sí se incluye el archivo geoespacial de áreas pobladas,
# ya que no contiene información clínica sensible.
#
# El archivo esta guardado en:
# datos/Areas_Pobladas.zip

ruta_datos = "datos/"
archivo_areas_pobladas = "Areas_Pobladas.zip"


# =========================
# PREPARACIÓN DE PACIENTES CON COORDENADAS
# =========================
# Se utiliza df_pacientes_geo, creado previamente en 01_configuracion_y_carga.py.
#
# df_pacientes_geo corresponde a la base de pacientes únicos con coordenadas válidas.
# Esta base se usa para evitar duplicar pacientes que tuvieron más de una hospitalización.

df_pacientes_geo = df_pacientes_geo.dropna(subset=["lat", "lon"]).copy()


# =========================
# CONVERSIÓN A GEODATAFRAME
# =========================
# Se transforman las coordenadas lat/lon en puntos geográficos.
#
# lon = longitud
# lat = latitud
#
# El sistema de coordenadas utilizado es EPSG:4326,
# que corresponde a coordenadas geográficas en latitud y longitud.

gdf_pacientes = gpd.GeoDataFrame(
    df_pacientes_geo,
    geometry=gpd.points_from_xy(
        df_pacientes_geo["lon"],
        df_pacientes_geo["lat"]
    ),
    crs="EPSG:4326"
)


# =========================
# CARGA DE ÁREAS POBLADAS
# =========================
# Se carga el archivo geoespacial que contiene los polígonos de áreas pobladas.

gdf_areas = gpd.read_file(ruta_datos + archivo_areas_pobladas)


# =========================
# HOMOLOGACIÓN DEL SISTEMA DE COORDENADAS
# =========================
# Para realizar el cruce espacial, ambos GeoDataFrames deben tener
# el mismo sistema de coordenadas.

gdf_areas = gdf_areas.to_crs("EPSG:4326")
gdf_pacientes = gdf_pacientes.to_crs("EPSG:4326")


# =========================
# CRUCE ESPACIAL
# =========================
# Se identifica si cada paciente cae dentro de un polígono de área poblada.
#
# Si el paciente cae dentro de un área poblada, se genera coincidencia espacial.
# Si no cae dentro de ningún polígono, queda sin coincidencia.

gdf_clasificado = gpd.sjoin(
    gdf_pacientes,
    gdf_areas,
    how="left",
    predicate="within"
)


# =========================
# CLASIFICACIÓN URBANO / RURAL
# =========================
# La columna index_right indica si hubo coincidencia con un área poblada.
#
# - Si index_right tiene valor: el paciente se clasifica como Urbano.
# - Si index_right está vacío: el paciente se clasifica como Rural.

gdf_clasificado["clas_final"] = gdf_clasificado["index_right"].apply(
    lambda x: "Urbano" if pd.notna(x) else "Rural"
)


# =========================
# LIMPIEZA DEL RESULTADO
# =========================

if "index_right" in gdf_clasificado.columns:
    gdf_clasificado = gdf_clasificado.drop(columns=["index_right"])


# =========================
# BASE FINAL CLASIFICADA
# =========================
# Se elimina la geometría para volver a trabajar con un DataFrame normal.
# La columna clas_final queda disponible para los análisis posteriores.

df_pacientes_clasificado = pd.DataFrame(
    gdf_clasificado.drop(columns="geometry")
)


# =========================
# RESUMEN DE RESULTADOS
# =========================

print("Clasificación territorial de pacientes:")
print(df_pacientes_clasificado["clas_final"].value_counts())

print("\nPorcentaje de pacientes por clasificación territorial:")
print(
    df_pacientes_clasificado["clas_final"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)


# =========================
# GUARDAR RESULTADO OPCIONAL
# =========================
# Si deseas guardar la base clasificada localmente, puedes descomentar
# la siguiente línea.
#
# IMPORTANTE:
# No se recomienda subir este archivo resultante a GitHub si contiene
# información sensible o identificadores de pacientes.

# df_pacientes_clasificado.to_excel(
#     "datos/df_pacientes_clasificado.xlsx",
#     index=False
# )
