import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# =========================================================
# CONFIGURACION GENERAL MATPLOTLIB
# =========================================================

plt.ion()

# =========================================================
# FUNCION TABLA DE FRECUENCIA
# =========================================================

def tabla_frecuencia(datos):

    frecuencia = datos.value_counts().sort_index()

    tabla = pd.DataFrame()

    # Frecuencia absoluta
    tabla["fi"] = frecuencia

    # Frecuencia acumulada
    tabla["Fi"] = tabla["fi"].cumsum()

    # Frecuencia relativa
    tabla["hi"] = tabla["fi"] / tabla["fi"].sum()

    # Frecuencia porcentual
    tabla["hip"] = tabla["hi"] * 100

    # Frecuencia relativa acumulada
    tabla["Hi"] = tabla["hi"].cumsum()

    # Frecuencia porcentual acumulada
    tabla["Hip"] = tabla["Hi"] * 100

    return tabla


# =========================================================
# FUNCION TABLA AGRUPADA STURGES
# =========================================================

def tabla_agrupada(datos):

    n = len(datos)

    # Valor maximo
    maximo = datos.max()

    # Valor minimo
    minimo = datos.min()

    # Rango
    rango = maximo - minimo

    # Formula de Sturges
    k = int(1 + 3.322 * np.log10(n))

    # Amplitud
    amplitud = rango / k

    # Crear intervalos
    intervalos = pd.cut(
        datos,
        bins=k
    )

    frecuencia = (
        intervalos
        .value_counts()
        .sort_index()
    )

    tabla = pd.DataFrame()

    tabla["fi"] = frecuencia

    tabla["Fi"] = tabla["fi"].cumsum()

    tabla["hi"] = (
        tabla["fi"]
        / tabla["fi"].sum()
    )

    tabla["hip"] = (
        tabla["hi"] * 100
    )

    tabla["Hi"] = (
        tabla["hi"].cumsum()
    )

    tabla["Hip"] = (
        tabla["Hi"] * 100
    )

    # Convertir intervalos a texto limpio

    tabla.index = [

    f"{intervalo.left:.0f} - {intervalo.right:.0f}"

    for intervalo in tabla.index

]

# Marca de clase

    tabla["Marca"] = [

    round((i.left + i.right) / 2, 2)

    for i in intervalos.cat.categories

]

    return tabla, n, maximo, minimo, rango, k, amplitud


# =========================================================
# FUNCION MEDIDAS ESTADISTICAS
# =========================================================

def medidas_estadisticas(datos):

    media = datos.mean()

    mediana = datos.median()

    moda = datos.mode()[0]

    varianza = datos.var()

    desviacion = datos.std()

    maximo = datos.max()

    minimo = datos.min()

    rango = maximo - minimo

    tabla = pd.DataFrame({

        "Medida": [

            "Media",
            "Mediana",
            "Moda",
            "Varianza",
            "Desviacion Estandar",
            "Maximo",
            "Minimo",
            "Rango"

        ],

        "Valor": [

            media,
            mediana,
            moda,
            varianza,
            desviacion,
            maximo,
            minimo,
            rango

        ]

    })

    return tabla


# =========================================================
# MODO TERMINAL
# =========================================================

def ejecutar_terminal():

    print("\n" + "=" * 60)
    print(" ESTADISTICA DESCRIPTIVA CON PYTHON ")
    print("=" * 60)

    # =====================================================
    # LEER ARCHIVO CSV
    # =====================================================

    df = pd.read_csv("datos.csv")

    print("\nBASE DE DATOS\n")

    print(df)

    print("\nTOTAL DE REGISTROS:",
          len(df))

    # =====================================================
    # VARIABLE CUALITATIVA
    # =====================================================

    print("\n" + "=" * 60)
    print(" VARIABLE CUALITATIVA ")
    print("=" * 60)

    tabla_cualitativa = tabla_frecuencia(
        df["Carrera"]
    )

    print("\nTABLA DE FRECUENCIA CUALITATIVA\n")

    print(tabla_cualitativa)

    # -----------------------------------------------------
    # GRAFICO DE BARRAS
    # -----------------------------------------------------

    plt.figure(figsize=(8, 5))

    barras = plt.bar(
        tabla_cualitativa.index.astype(str),
        tabla_cualitativa["fi"]
    )

    # Etiquetas sobre barras

    for barra in barras:

        altura = barra.get_height()

        plt.text(

            barra.get_x()
            + barra.get_width() / 2,

            altura,

            str(int(altura)),

            ha='center'

        )

    plt.title("Grafico de Barras")
    plt.xlabel("Carrera")
    plt.ylabel("Frecuencia")

    plt.grid(True)

    plt.tight_layout()

    plt.show(block=True)

    # -----------------------------------------------------
    # GRAFICO DE TORTA
    # -----------------------------------------------------

    plt.figure(figsize=(7, 7))

    plt.pie(

        tabla_cualitativa["fi"],

        labels=tabla_cualitativa.index.astype(str),

        autopct="%1.1f%%"

    )

    plt.title("Grafico de Torta")

    plt.tight_layout()

    plt.show(block=True)

    # =====================================================
    # VARIABLE CUANTITATIVA DISCRETA
    # =====================================================

    print("\n" + "=" * 60)
    print(" VARIABLE CUANTITATIVA DISCRETA ")
    print("=" * 60)

    tabla_discreta = tabla_frecuencia(
        df["Aprobadas"]
    )

    print("\nTABLA DE FRECUENCIA DISCRETA\n")

    print(tabla_discreta)

    # -----------------------------------------------------
    # MEDIDAS ESTADISTICAS
    # -----------------------------------------------------

    medidas = medidas_estadisticas(
        df["Aprobadas"]
    )

    print("\nMEDIDAS ESTADISTICAS\n")

    print(medidas)

    # -----------------------------------------------------
    # GRAFICO DE BASTON
    # -----------------------------------------------------

    plt.figure(figsize=(8, 5))

    plt.stem(

        tabla_discreta.index,

        tabla_discreta["fi"]

    )

    plt.title("Grafico de Baston")

    plt.xlabel("Aprobadas")

    plt.ylabel("Frecuencia")

    plt.grid(True)

    plt.tight_layout()

    plt.show(block=True)

    # =====================================================
    # VARIABLE CUANTITATIVA CONTINUA
    # =====================================================

    print("\n" + "=" * 60)
    print(" VARIABLE CUANTITATIVA CONTINUA ")
    print("=" * 60)

    (
        tabla_continua,
        n,
        maximo,
        minimo,
        rango,
        k,
        amplitud

    ) = tabla_agrupada(df["Edad"])

    print("\nNUMERO DE DATOS:", n)

    print("MAXIMO:", maximo)

    print("MINIMO:", minimo)

    print("RANGO:", rango)

    print("NUMERO DE CLASES:", k)

    print("AMPLITUD:", amplitud)

    print("\nTABLA AGRUPADA\n")

    print(tabla_continua)

    # -----------------------------------------------------
    # HISTOGRAMA
    # -----------------------------------------------------

    plt.figure(figsize=(8, 5))

    plt.hist(

        df["Edad"],

        bins=k

    )

    plt.title("Histograma")

    plt.xlabel("Edad")

    plt.ylabel("Frecuencia")

    plt.grid(True)

    plt.tight_layout()

    plt.show(block=True)

    # -----------------------------------------------------
    # POLIGONO DE FRECUENCIA
    # -----------------------------------------------------

    plt.figure(figsize=(8, 5))

    plt.plot(

        tabla_continua["Marca"],

        tabla_continua["fi"],

        marker="o"

    )

    plt.title("Poligono de Frecuencia")

    plt.xlabel("Marca de Clase")

    plt.ylabel("Frecuencia")

    plt.grid(True)

    plt.tight_layout()

    plt.show(block=True)

    # -----------------------------------------------------
    # HISTOGRAMA + POLIGONO
    # -----------------------------------------------------

    plt.figure(figsize=(8, 5))

    plt.hist(

        df["Edad"],

        bins=k,

        alpha=0.7

    )

    plt.plot(

        tabla_continua["Marca"],

        tabla_continua["fi"],

        marker="o"

    )

    plt.title("Histograma y Poligono")

    plt.grid(True)

    plt.tight_layout()

    plt.show(block=True)

    # -----------------------------------------------------
    # OJIVA
    # -----------------------------------------------------

    plt.figure(figsize=(8, 5))

    plt.plot(

        tabla_continua["Marca"],

        tabla_continua["Fi"],

        marker="o"

    )

    plt.title("Ojiva")

    plt.xlabel("Marca de Clase")

    plt.ylabel("Frecuencia Acumulada")

    plt.grid(True)

    plt.tight_layout()

    plt.show(block=True)

    print("\n" + "=" * 60)

    print(" PROGRAMA EJECUTADO CORRECTAMENTE ")

    print("=" * 60)


# =========================================================
# MODO STREAMLIT
# =========================================================

def ejecutar_streamlit():

    st.set_page_config(

        page_title="Estadistica Descriptiva",

        layout="wide"

    )

    st.title("📊 ESTADISTICA DESCRIPTIVA")

    st.success(
        "Sistema iniciado correctamente"
    )

    # =====================================================
    # LEER CSV
    # =====================================================

    df = pd.read_csv("datos.csv")

    st.header("📋 BASE DE DATOS")

    st.dataframe(df)

    st.write(
        "Total de registros:",
        len(df)
    )

    # =====================================================
    # VARIABLE CUALITATIVA
    # =====================================================

    st.header("📊 VARIABLE CUALITATIVA")

    tabla_cualitativa = tabla_frecuencia(
        df["Carrera"]
    )

    st.subheader(
        "Tabla de Frecuencia"
    )

    st.dataframe(tabla_cualitativa)

    # GRAFICO BARRAS

    fig1, ax1 = plt.subplots(
        figsize=(8, 5)
    )

    barras = ax1.bar(

        tabla_cualitativa.index.astype(str),

        tabla_cualitativa["fi"]

    )

    for barra in barras:

        altura = barra.get_height()

        ax1.text(

            barra.get_x()
            + barra.get_width() / 2,

            altura,

            str(int(altura)),

            ha='center'

        )

    ax1.set_title(
        "Grafico de Barras"
    )

    ax1.grid(True)

    st.pyplot(fig1)

    # GRAFICO TORTA

    fig2, ax2 = plt.subplots(
        figsize=(7, 7)
    )

    ax2.pie(

        tabla_cualitativa["fi"],

        labels=tabla_cualitativa.index.astype(str),

        autopct="%1.1f%%"

    )

    ax2.set_title(
        "Grafico de Torta"
    )

    st.pyplot(fig2)

    # =====================================================
    # VARIABLE DISCRETA
    # =====================================================

    st.header(
        "📈 VARIABLE CUANTITATIVA DISCRETA"
    )

    tabla_discreta = tabla_frecuencia(
        df["Aprobadas"]
    )

    st.subheader(
        "Tabla Discreta"
    )

    st.dataframe(tabla_discreta)

    # MEDIDAS

    medidas = medidas_estadisticas(
        df["Aprobadas"]
    )

    st.subheader(
        "Medidas Estadisticas"
    )

    st.dataframe(medidas)

    # GRAFICO BASTON

    fig3, ax3 = plt.subplots(
        figsize=(8, 5)
    )

    ax3.stem(

        tabla_discreta.index,

        tabla_discreta["fi"]

    )

    ax3.set_title(
        "Grafico de Baston"
    )

    ax3.grid(True)

    st.pyplot(fig3)

    # =====================================================
    # VARIABLE CONTINUA
    # =====================================================

    st.header(
        "📉 VARIABLE CUANTITATIVA CONTINUA"
    )

    (
        tabla_continua,
        n,
        maximo,
        minimo,
        rango,
        k,
        amplitud

    ) = tabla_agrupada(df["Edad"])

    st.write("Numero de datos:", n)

    st.write("Maximo:", maximo)

    st.write("Minimo:", minimo)

    st.write("Rango:", rango)

    st.write("Numero de clases:", k)

    st.write("Amplitud:", amplitud)

    st.latex(
        r'k = 1 + 3.322 \log_{10}(n)'
    )

    st.subheader(
        "Tabla Agrupada"
    )

    st.dataframe(tabla_continua)

    # HISTOGRAMA

    fig4, ax4 = plt.subplots(
        figsize=(8, 5)
    )

    ax4.hist(
        df["Edad"],
        bins=k
    )

    ax4.set_title(
        "Histograma"
    )

    ax4.grid(True)

    st.pyplot(fig4)

    # POLIGONO

    fig5, ax5 = plt.subplots(
        figsize=(8, 5)
    )

    ax5.plot(

        tabla_continua["Marca"],

        tabla_continua["fi"],

        marker="o"

    )

    ax5.set_title(
        "Poligono de Frecuencia"
    )

    ax5.grid(True)

    st.pyplot(fig5)

    # HISTOGRAMA + POLIGONO

    fig6, ax6 = plt.subplots(
        figsize=(8, 5)
    )

    ax6.hist(

        df["Edad"],

        bins=k,

        alpha=0.7

    )

    ax6.plot(

        tabla_continua["Marca"],

        tabla_continua["fi"],

        marker="o"

    )

    ax6.set_title(
        "Histograma y Poligono"
    )

    ax6.grid(True)

    st.pyplot(fig6)

    # OJIVA

    fig7, ax7 = plt.subplots(
        figsize=(8, 5)
    )

    ax7.plot(

        tabla_continua["Marca"],

        tabla_continua["Fi"],

        marker="o"

    )

    ax7.set_title(
        "Ojiva"
    )

    ax7.grid(True)

    st.pyplot(fig7)

    st.success(
        "Programa ejecutado correctamente"
    )


# =========================================================
# DETECTAR MODO DE EJECUCION
# =========================================================

if __name__ == "__main__":

    try:

        from streamlit.runtime.scriptrunner import get_script_run_ctx

        if get_script_run_ctx() is not None:

            ejecutar_streamlit()

        else:

            ejecutar_terminal()

    except:

        ejecutar_terminal()