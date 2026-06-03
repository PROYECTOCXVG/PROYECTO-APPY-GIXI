import streamlit as st
import plotly.express as px
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import df
from filtros import aplicar_filtros

# --- Aplicar filtros globales ---
df_filtrado = aplicar_filtros(df)

# --- Estilos visuales ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    /* Fondo oscuro general */
    .stApp { background-color: #0a0e1a; font-family: 'Inter', sans-serif; 
}
            
/* Labels de controles (Variable, Año, 2019, 2022, 2023, Orden) — más visibles */
            
label[data-testid="stWidgetLabel"] p {
    font-size: 13px !important;      /* más grande */
    font-weight: 700 !important;     /* negrilla */
    color: #aabbcc !important;       /* más claro */
    }

/* Opciones de radio (Internet, Celular...) — más visibles */
            
div[data-testid="stRadio"] label p {
    font-size: 13px !important;
    color: #ccd6e0 !important;       /* aclaramos */
    }

/* Opciones del selectbox (años) — más visibles */
div[data-testid="stSelectbox"] div {
    font-size: 13px !important;
    color: #ccd6e0 !important;
    }
    /* Título con barra azul */
    .datos-titulo {
        border-left: 4px solid #4a9fd4;
        padding-left: 12px;
        font-size: 26px; font-weight: 700;   /* subimos de 18px */
        color: #ffffff; margin-bottom: 4px;
    }
    /* Subtítulo gris */
    .datos-subtitulo {
        font-size: 14px; color: #889aaa;     /* subimos de 12px, aclaramos */
        margin-bottom: 20px; padding-left: 16px;
    }
    /* Etiqueta de sección para gráficas */
    .graf-label {
        font-size: 12px; font-weight: 600;   /* subimos de 10px */
        letter-spacing: 1.5px; color: #0d1422;
        text-transform: uppercase; margin-bottom: 8px;
    }
    /* Franja de cierre */
    .franja-cierre {
        background-color: #0d1422;
        border: 1px solid #1e2d40;
        border-radius: 8px;
        padding: 14px 20px;
        margin-top: 16px;
        font-size: 13px; color: #778899;
    }
    </style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown('<div class="datos-titulo">Ranking departamentos</div>', unsafe_allow_html=True)
st.markdown('<div class="datos-subtitulo">Ordenable · selector de variable y año</div>', unsafe_allow_html=True)

# --- Variables disponibles para analizar ---
variables = {
    "Internet"  : "internet_proporcion",
    "Celular"   : "tel_celular_proporcion",
    "Computador": "computador_proporcion",
    "TV"        : "tv_proporcion"
}

# --- Controles en una fila ---
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([2, 1, 1])

with col_ctrl1:
    # Selector de variable como botones radio horizontal
    var_sel = st.radio("Variable", options=list(variables.keys()),
                       horizontal=True, key="datos_var")

with col_ctrl2:
    # Selector de año
    año_sel = st.selectbox("Año", options=sorted(df_filtrado["año"].unique()),
                           key="datos_año")

with col_ctrl3:
    # Orden de las barras
    orden = st.radio("Orden", options=["↓ Mayor a menor", "↑ Menor a mayor"],
                     key="datos_orden")

# --- Preparar datos: zona TOTAL, sin TOTAL NACIONAL ---
col_var = variables[var_sel]
df_rank = df_filtrado[
    (df_filtrado["año"] == año_sel) &
    (df_filtrado["zona"] == "TOTAL") &
    (df_filtrado["departamento"] != "TOTAL NACIONAL")
][["departamento", col_var]].dropna().copy()

# Ordenar según selección del usuario
ascendente = orden == "↑ Menor a mayor"
df_rank = df_rank.sort_values(col_var, ascending=ascendente)

# --- Layout dos columnas ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="graf-label">Barras horizontales · ordenable</div>', unsafe_allow_html=True)

    fig_rank = px.bar(
        df_rank,
        x=col_var, y="departamento",
        orientation="h",                          # barras horizontales
        color=col_var,
        color_continuous_scale="Blues",
        labels={col_var: f"% {var_sel}", "departamento": ""}
    )
    fig_rank.update_layout(
        plot_bgcolor="#111827", paper_bgcolor="#111827",
        font_color="#aabbcc", height=580,
        margin=dict(l=10, r=10, t=10, b=10),
        coloraxis_showscale=False,
        xaxis=dict(showgrid=True, gridcolor="#1e2d40",
                   color="#667788", tickfont=dict(size=11)),  # ejes más visibles
        yaxis=dict(showgrid=False,
                   color="#667788", tickfont=dict(size=11))   # etiquetas más grandes
    )
    st.plotly_chart(fig_rank, use_container_width=True, key="datos_rank")

with col2:
    st.markdown('<div class="graf-label">Dispersión · urbano vs rural</div>', unsafe_allow_html=True)

    # Cabecera por departamento
    df_cab = df_filtrado[
        (df_filtrado["año"] == año_sel) &
        (df_filtrado["zona"] == "CABECERA") &
        (df_filtrado["departamento"] != "TOTAL NACIONAL")
    ].set_index("departamento")[col_var].rename("Cabecera")

    # Rural por departamento
    df_rur = df_filtrado[
        (df_filtrado["año"] == año_sel) &
        (df_filtrado["zona"] == "CENTROS POBLADOS Y RURAL DISPERSO") &
        (df_filtrado["departamento"] != "TOTAL NACIONAL")
    ].set_index("departamento")[col_var].rename("Rural")

    df_scatter = pd.concat([df_cab, df_rur], axis=1).dropna().reset_index()
    df_scatter.columns = ["Departamento", "Cabecera", "Rural"]

    fig_scatter = px.scatter(
        df_scatter,
        x="Cabecera", y="Rural",
        hover_name="Departamento",               # nombre solo en tooltip, no en gráfica
        color="Cabecera",
        color_continuous_scale="Blues",
        labels={
            "Cabecera": f"% {var_sel} Cabecera",
            "Rural"   : f"% {var_sel} Rural"
        }
    )
    fig_scatter.update_traces(
        marker=dict(size=10),                    # puntos más grandes y visibles
        hovertemplate="<b>%{hovertext}</b><br>Cabecera: %{x:.1f}%<br>Rural: %{y:.1f}%"
    )
    fig_scatter.update_layout(
        plot_bgcolor="#111827", paper_bgcolor="#111827",
        font_color="#aabbcc", height=580,
        margin=dict(l=10, r=10, t=10, b=10),
        coloraxis_showscale=False,
        xaxis=dict(showgrid=True, gridcolor="#1e2d40",
                   color="#667788", tickfont=dict(size=11)),
        yaxis=dict(showgrid=True, gridcolor="#1e2d40",
                   color="#667788", tickfont=dict(size=11))
    )
    st.plotly_chart(fig_scatter, use_container_width=True, key="datos_scatter")

# --- Franja de cierre dinámica ---
st.markdown(f"""
<div class="franja-cierre">
    📊 &nbsp; Mostrando <strong style="color:#99aabb;">{var_sel}</strong> ·
    Año <strong style="color:#99aabb;">{año_sel}</strong> ·
    Zona <strong style="color:#99aabb;">Total nacional</strong>
</div>
""", unsafe_allow_html=True)

