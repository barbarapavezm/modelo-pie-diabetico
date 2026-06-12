"""
Análisis descriptivo de pacientes y hospitalizaciones asociadas al estudio:
"Modelo multietapa de progresión clínica del pie diabético".

Este archivo contiene conteos y gráficos descriptivos relacionados con:

- pacientes por comuna,
- clasificación urbano-rural,
- reincidencia hospitalaria,
- número de hospitalizaciones por paciente,
- distribución por sexo,
- distribución según previsión/FONASA.

IMPORTANTE:
Este archivo debe ejecutarse después de:

01_configuracion_y_carga.py
02_clasificacion_territorial.py

ya que utiliza los DataFrames:

- df_hosp
- df_pacientes
- df_pacientes_clasificado
"""

# =========================
# CARPETA DE SALIDA
# =========================
# Las imágenes generadas se guardan en la carpeta imagenes_resultados/.

carpeta_salida = "imagenes_resultados"

if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)


# =========================
# FUNCIÓN AUXILIAR
# =========================

def buscar_columna(df, posibles_nombres):
    """
    Busca una columna dentro de un DataFrame considerando varias opciones
    posibles de nombre.

    Esto permite que el código sea más flexible si los nombres de columnas
    cambian levemente entre archivos.

    Parámetros:
    df: DataFrame.
    posibles_nombres: lista de nombres posibles.

    Retorna:
    El nombre real de la columna encontrada.
    """
    for nombre in posibles_nombres:
        if nombre in df.columns:
            return nombre

    raise ValueError(
        "No se encontró ninguna de estas columnas: "
        + ", ".join(posibles_nombres)
    )


# =========================
# 1. PACIENTES POR COMUNA
# =========================

col_comuna = buscar_columna(
    df_pacientes,
    [
        "Comuna de residencia ( Desc )",
        "Comuna de residencia (Desc)",
        "Comuna residencia",
        "Comuna"
    ]
)

conteo_comuna = (
    df_pacientes[col_comuna]
    .value_counts()
    .sort_values(ascending=True)
)

plt.figure(figsize=(10, 8))
conteo_comuna.plot(kind="barh")
plt.title("Distribución de pacientes por comuna")
plt.xlabel("Número de pacientes")
plt.ylabel("Comuna")
plt.tight_layout()
plt.savefig(f"{carpeta_salida}/pacientes_por_comuna.png", dpi=300)
plt.close()

print("Pacientes por comuna:")
print(conteo_comuna.sort_values(ascending=False))


# =========================
# 2. CLASIFICACIÓN URBANO-RURAL
# =========================
# Se utiliza df_pacientes_clasificado, generado en el archivo 02.

conteo_zona = (
    df_pacientes_clasificado["clas_final"]
    .value_counts()
)

plt.figure(figsize=(7, 5))
conteo_zona.plot(kind="bar")
plt.title("Clasificación territorial de pacientes")
plt.xlabel("Clasificación")
plt.ylabel("Número de pacientes")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{carpeta_salida}/clasificacion_urbano_rural.png", dpi=300)
plt.close()

print("\nClasificación urbano-rural:")
print(conteo_zona)


# =========================
# 3. NÚMERO DE HOSPITALIZACIONES POR PACIENTE
# =========================
# df_hosp contiene todas las hospitalizaciones.
# Por eso, un mismo paciente puede aparecer más de una vez.

col_codigo = buscar_columna(
    df_hosp,
    [
        "Codigo",
        "Código",
        "ID paciente",
        "ID"
    ]
)

hospitalizaciones_por_paciente = (
    df_hosp[col_codigo]
    .value_counts()
    .sort_index()
)

distribucion_hospitalizaciones = (
    hospitalizaciones_por_paciente
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(8, 5))
distribucion_hospitalizaciones.plot(kind="bar")
plt.title("Distribución del número de hospitalizaciones por paciente")
plt.xlabel("Número de hospitalizaciones")
plt.ylabel("Número de pacientes")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{carpeta_salida}/hospitalizaciones_por_paciente.png", dpi=300)
plt.close()

print("\nDistribución del número de hospitalizaciones por paciente:")
print(distribucion_hospitalizaciones)


# =========================
# 4. REINCIDENCIA HOSPITALARIA
# =========================
# Se considera reincidente a un paciente con más de una hospitalización.

df_reincidencia = hospitalizaciones_por_paciente.reset_index()
df_reincidencia.columns = ["Codigo", "n_hospitalizaciones"]

df_reincidencia["reincidente"] = df_reincidencia["n_hospitalizaciones"].apply(
    lambda x: "Sí" if x > 1 else "No"
)

conteo_reincidencia = (
    df_reincidencia["reincidente"]
    .value_counts()
)

plt.figure(figsize=(6, 5))
conteo_reincidencia.plot(kind="bar")
plt.title("Reincidencia hospitalaria")
plt.xlabel("Reincidente")
plt.ylabel("Número de pacientes")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{carpeta_salida}/reincidencia_hospitalaria.png", dpi=300)
plt.close()

print("\nReincidencia hospitalaria:")
print(conteo_reincidencia)


# =========================
# 5. REINCIDENCIA SEGÚN CLASIFICACIÓN TERRITORIAL
# =========================
# Se cruza la clasificación urbano-rural con la condición de reincidencia.

if "Codigo" in df_pacientes_clasificado.columns:
    df_reincidencia_zona = df_pacientes_clasificado.merge(
        df_reincidencia,
        on="Codigo",
        how="left"
    )

    tabla_reincidencia_zona = pd.crosstab(
        df_reincidencia_zona["clas_final"],
        df_reincidencia_zona["reincidente"],
        normalize="index"
    ) * 100

    tabla_reincidencia_zona.plot(kind="bar", figsize=(8, 5))
    plt.title("Reincidencia hospitalaria según clasificación territorial")
    plt.xlabel("Clasificación territorial")
    plt.ylabel("Porcentaje")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{carpeta_salida}/reincidencia_por_zona.png", dpi=300)
    plt.close()

    print("\nReincidencia por zona (%):")
    print(tabla_reincidencia_zona.round(2))


# =========================
# 6. DISTRIBUCIÓN POR SEXO
# =========================

col_sexo = buscar_columna(
    df_pacientes,
    [
        "Sexo (Desc)",
        "Sexo",
        "sexo"
    ]
)

conteo_sexo = (
    df_pacientes[col_sexo]
    .value_counts()
)

plt.figure(figsize=(6, 5))
conteo_sexo.plot(kind="bar")
plt.title("Distribución de pacientes por sexo")
plt.xlabel("Sexo")
plt.ylabel("Número de pacientes")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{carpeta_salida}/distribucion_barras_por_sexo.png", dpi=300)
plt.close()

print("\nDistribución por sexo:")
print(conteo_sexo)


# =========================
# 7. DISTRIBUCIÓN SEGÚN PREVISIÓN / FONASA
# =========================

col_prevision = buscar_columna(
    df_pacientes,
    [
        "Prevision (Desc)",
        "Previsión (Desc)",
        "Prevision",
        "Previsión"
    ]
)

def clasificar_fonasa(valor):
    """
    Clasifica el tramo FONASA o previsión en categorías socioeconómicas simples.
    """
    valor = str(valor).upper()

    if "FONASA A" in valor or "TRAMO A" in valor:
        return "Muy bajo"
    elif "FONASA B" in valor or "TRAMO B" in valor:
        return "Bajo"
    elif "FONASA C" in valor or "TRAMO C" in valor:
        return "Medio"
    elif "FONASA D" in valor or "TRAMO D" in valor:
        return "Medio-alto"
    elif "FONASA" in valor:
        return "Fonasa sin tramo"
    elif "NAN" in valor or valor == "":
        return "Sin información"
    else:
        return "No Fonasa / Otro"

df_pacientes["tramo_fonasa"] = df_pacientes[col_prevision].apply(clasificar_fonasa)

conteo_fonasa = (
    df_pacientes["tramo_fonasa"]
    .value_counts()
    .sort_values(ascending=True)
)

plt.figure(figsize=(9, 5))
conteo_fonasa.plot(kind="barh")
plt.title("Distribución de pacientes según tramo FONASA")
plt.xlabel("Número de pacientes")
plt.ylabel("Categoría")
plt.tight_layout()
plt.savefig(f"{carpeta_salida}/fonasa_tramos.png", dpi=300)
plt.close()

print("\nDistribución según FONASA:")
print(conteo_fonasa.sort_values(ascending=False))


# =========================
# 8. RESUMEN GENERAL
# =========================

print("\nResumen general:")
print("Total de hospitalizaciones:", df_hosp.shape[0])
print("Total de pacientes únicos:", df_pacientes.shape[0])
print("Pacientes reincidentes:", conteo_reincidencia.get("Sí", 0))
print("Pacientes no reincidentes:", conteo_reincidencia.get("No", 0))
