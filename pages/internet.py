import streamlit as st
import plotly.express as px
import pandas as pd
from data import df
from filtros import aplicar_filtros

# --- Aplicar filtros globales ---
df_filtrado = aplicar_filtros(df)

# --- Estilos visuales ---
st.markdown("""
    <style>
    .stApp { background-color: #0a0e1a; }          /* Fondo oscuro */
    .int-titulo {
        border-left: 4px solid #4a9fd4;            /* Barra azul izquierda */
        padding-left: 12px;
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        font-family: sans-serif;
        margin-bottom: 4px;
    }
    .int-subtitulo {
        font-size: 12px;
        color: #667788;                            /* Gris suave */
        font-family: sans-serif;
        margin-bottom: 16px;
        padding-left: 16px;
    }
    .graf-label {
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 1.5px;
        color: #667788;
        text-transform: uppercase;
        margin-bottom: 8px;
        font-family: sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown('<div class="int-titulo">Acceso a internet — análisis profundo</div>', unsafe_allow_html=True)
st.markdown('<div class="int-subtitulo">Tipos de conexión · velocidad · correlación con variables socioeconómicas</div>', unsafe_allow_html=True)

# --- Preparar datos: solo cabecera y rural, sin total nacional ---
df_int = df_filtrado[
    (df_filtrado["departamento"] != "TOTAL NACIONAL") &
    (df_filtrado["zona"].isin(["CABECERA", "CENTROS POBLADOS Y RURAL DISPERSO"]))
].copy()

# Renombrar zonas para mejor lectura
df_int["zona"] = df_int["zona"].replace({
    "CABECERA": "Cabecera",
    "CENTROS POBLADOS Y RURAL DISPERSO": "Rural"
})

# Normalizar columnas si vienen en decimal
for col in ["internet_fijo_proporcion", "internet_movil_proporcion", "internet_proporcion", "computador_proporcion"]:
    if df_int[col].mean() < 2:
        df_int[col] = df_int[col] * 100

# --- Layout dos columnas ---
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="graf-label">Internet fijo vs móvil por zona y año</div>', unsafe_allow_html=True)

    # Agrupar por zona y año para promediar
    df_fijo = df_int.groupby(["zona", "año"])[["internet_fijo_proporcion", "internet_movil_proporcion"]].mean().reset_index()

    # Convertir a formato largo para graficar con color por tipo
    df_largo = df_fijo.melt(
        id_vars=["zona", "año"],
        value_vars=["internet_fijo_proporcion", "internet_movil_proporcion"],
        var_name="tipo",
        value_name="proporcion"
    )
    # Renombrar tipos para mejor lectura
    df_largo["tipo"] = df_largo["tipo"].replace({
        "internet_fijo_proporcion": "Fijo",
        "internet_movil_proporcion": "Móvil"
    })
    df_largo["año"] = df_largo["año"].astype(str)
    df_largo["zona_año"] = df_largo["zona"] + " · " + df_largo["año"]  # Combinar zona y año en eje X

    fig_barras = px.bar(
        df_largo,
        x="zona_año",
        y="proporcion",
        color="tipo",
        barmode="group",                                               # Barras lado a lado
        color_discrete_map={"Fijo": "#4a9fd4", "Móvil": "#f5a623"},  # Azul fijo, naranja móvil
        labels={"proporcion": "% Hogares", "zona_año": "", "tipo": "Tipo"}
    )
    fig_barras.update_layout(
        plot_bgcolor="#111827",
        paper_bgcolor="#111827",
        font_color="#aabbcc",
        height=400,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(bgcolor="#111827", font=dict(color="#aabbcc"), title_text=""),
        xaxis=dict(showgrid=False, color="#445566", tickangle=30),
        yaxis=dict(showgrid=True, gridcolor="#1e2d40", color="#445566")
    )
    st.plotly_chart(fig_barras, use_container_width=True, key="int_barras")

with col2:
    st.markdown('<div class="graf-label">Correlación internet vs computador por departamento</div>', unsafe_allow_html=True)

    # Promedio por departamento zona TOTAL
    df_scatter = df_filtrado[
        (df_filtrado["zona"] == "TOTAL") &
        (df_filtrado["departamento"] != "TOTAL NACIONAL")
    ].groupby("departamento")[["internet_proporcion", "computador_proporcion"]].mean().reset_index()

    # Normalizar si están en decimal
    for col in ["internet_proporcion", "computador_proporcion"]:
        if df_scatter[col].mean() < 2:
            df_scatter[col] = df_scatter[col] * 100

    fig_scatter = px.scatter(
        df_scatter,
        x="internet_proporcion",
        y="computador_proporcion",
        text="departamento",                                          # Nombre del departamento en cada punto
        color="internet_proporcion",
        color_continuous_scale="Blues",
        labels={
            "internet_proporcion": "% Internet",
            "computador_proporcion": "% Computador",
        }
    )
    fig_scatter.update_traces(
        textposition="top center",
        textfont=dict(size=8, color="#aabbcc"),
        marker=dict(size=8)
    )
    fig_scatter.update_layout(
        plot_bgcolor="#111827",
        paper_bgcolor="#111827",
        font_color="#aabbcc",
        height=400,
        margin=dict(l=10, r=10, t=10, b=10),
        coloraxis_showscale=False,
        xaxis=dict(showgrid=True, gridcolor="#1e2d40", color="#445566"),
        yaxis=dict(showgrid=True, gridcolor="#1e2d40", color="#445566")
    )
    st.plotly_chart(fig_scatter, use_container_width=True, key="int_scatter")