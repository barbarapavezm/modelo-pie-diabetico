"""
Clasificación territorial urbano-rural de pacientes con pie diabético basada en la columna 'Entidad'.

Este archivo utiliza las coordenadas de residencia de los pacientes y el shapefile de áreas pobladas para clasificar la residencia como:

- Urbano: si la 'Entidad' es Ciudad, Pueblo o Villa.
- Rural: si la 'Entidad' es Aldea, Caserío, Villorrio o Localidad.
- Sin data: si no hay coincidencia con un área poblada.

Debe ejecutarse después de 01_configuracion_y_carga.py.
"""

import geopandas as gpd
import pandas as pd

# Ruta del shapefile (ya debería estar en la carpeta "datos/").
ruta_datos = "datos/"
archivo_areas_pobladas = "Areas_Pobladas.zip"

# Pacientes con coordenadas
df_pacientes_geo = df_pacientes_geo.dropna(subset=["lat", "lon"]).copy()

# Convertir a GeoDataFrame
gdf_pacientes = gpd.GeoDataFrame(
    df_pacientes_geo,
    geometry=gpd.points_from_xy(df_pacientes_geo["lon"], df_pacientes_geo["lat"]),
    crs="EPSG:4326"
)

# Cargar áreas pobladas y transformar CRS
gdf_areas = gpd.read_file(ruta_datos + archivo_areas_pobladas).to_crs("EPSG:4326")

# Cruce espacial
gdf_clasificado = gpd.sjoin(
    gdf_pacientes,
    gdf_areas[["Entidad", "geometry"]],
    how="left",
    predicate="within"
)

# Clasificación según 'Entidad'
def clasificar_territorio(entidad):
    if entidad in ["Ciudad", "Pueblo", "Villa"]:
        return "Urbano"
    elif entidad in ["Aldea", "Caserío", "Villorrio", "Localidad"]:
        return "Rural"
    else:
        return "Sin data"

gdf_clasificado["clas_final"] = gdf_clasificado["Entidad"].apply(clasificar_territorio)

# DataFrame final
df_pacientes_clasificado = pd.DataFrame(
    gdf_clasificado.drop(columns="geometry")
)

# Resumen de resultados
print("Clasificación territorial de pacientes:")
print(df_pacientes_clasificado["clas_final"].value_counts())
