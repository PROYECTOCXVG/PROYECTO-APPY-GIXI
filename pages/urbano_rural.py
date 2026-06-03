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
    .stApp { background-color: #0a0e1a; }
    .ur-titulo {
        border-left: 4px solid #4a9fd4;
        padding-left: 12px;
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        font-family: sans-serif;
        margin-bottom: 4px;
    }
    .ur-subtitulo {
        font-size: 12px;
        color: #667788;
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
st.markdown('<div class="ur-titulo">Brecha urbano / rural</div>', unsafe_allow_html=True)
st.markdown('<div class="ur-subtitulo">Comparación por departamento entre zonas cabecera y rural disperso</div>', unsafe_allow_html=True)

# --- Preparar datos: solo cabecera y rural, sin total nacional ni San Andrés ---
df_ur = df_filtrado[
    (df_filtrado["departamento"] != "TOTAL NACIONAL") &
    (df_filtrado["departamento"] != "SAN ANDRÉS") &
    (df_filtrado["zona"].isin(["CABECERA", "CENTROS POBLADOS Y RURAL DISPERSO"]))
].copy()

# Renombrar zonas para mejor lectura
df_ur["zona"] = df_ur["zona"].replace({
    "CABECERA": "Urbano",
    "CENTROS POBLADOS Y RURAL DISPERSO": "Rural"
})

# --- Layout dos columnas ---
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="graf-label">Barras agrupadas cabecera vs rural</div>', unsafe_allow_html=True)

    # Promedio por departamento y zona
    df_barras = df_ur.groupby(["departamento", "zona"])["internet_proporcion"].mean().reset_index()
    df_barras = df_barras.sort_values("internet_proporcion", ascending=True)

    fig_barras = px.bar(
        df_barras,
        x="internet_proporcion",
        y="departamento",
        color="zona",
        orientation="h",
        barmode="group",
        color_discrete_map={"Urbano": "#4a9fd4", "Rural": "#f5a623"},
        labels={"internet_proporcion": "% Internet", "departamento": "", "zona": "Zona"}
    )
    fig_barras.update_layout(
        plot_bgcolor="#111827",
        paper_bgcolor="#111827",
        font_color="#aabbcc",
        height=500,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(bgcolor="#111827", font=dict(color="#aabbcc"), title_text=""),
        xaxis=dict(showgrid=True, gridcolor="#1e2d40", color="#445566"),
        yaxis=dict(showgrid=False, color="#445566", tickfont=dict(size=9))
    )
    st.plotly_chart(fig_barras, use_container_width=True, key="ur_barras")

with col2:
    st.markdown('<div class="graf-label">Mapa de calor · brecha por año</div>', unsafe_allow_html=True)

    # Calcular diferencia pp entre cabecera y rural
    df_cab = df_ur[df_ur["zona"] == "Urbano"].groupby(
        ["departamento", "año"])["internet_proporcion"].mean()
    df_rur = df_ur[df_ur["zona"] == "Rural"].groupby(
        ["departamento", "año"])["internet_proporcion"].mean()

    df_brecha = (df_cab - df_rur).reset_index()
    df_brecha.columns = ["departamento", "año", "brecha_pp"]
    df_brecha = df_brecha.dropna(subset=["brecha_pp"])
    df_brecha["año"] = df_brecha["año"].astype(str)

    # Pivot para heatmap
    df_pivot = df_brecha.pivot(index="departamento", columns="año", values="brecha_pp")

    # Solo años reales
    cols_validas = [c for c in ["2019", "2022", "2023"] if c in df_pivot.columns]
    df_pivot = df_pivot[cols_validas]

    fig_heat = px.imshow(
        df_pivot,
        color_continuous_scale="RdBu_r",
        aspect="auto",
        labels={"color": "Brecha pp", "x": "Año", "y": "Departamento"},
    )
    fig_heat.update_layout(
        plot_bgcolor="#111827",
        paper_bgcolor="#111827",
        font_color="#aabbcc",
        height=500,
        margin=dict(l=10, r=10, t=10, b=10),
        coloraxis_colorbar=dict(
            title="pp",
            tickfont=dict(color="#aabbcc"),
        ),
        xaxis=dict(
            color="#445566",
            tickmode="array",
            tickvals=cols_validas,
            ticktext=cols_validas,
            tickfont=dict(size=11)
        ),
        yaxis=dict(color="#445566", tickfont=dict(size=9))
    )
    st.plotly_chart(fig_heat, use_container_width=True, key="ur_heatmap")