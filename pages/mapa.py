import streamlit as st
import plotly.express as px
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import df
from filtros import aplicar_filtros

# --- Aplicar filtros globales ---
df_filtrado = aplicar_filtros(df)

# --- Cargar GeoJSON ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
geojson_path = os.path.join(os.path.dirname(BASE_DIR), "img", "Mapa Colombia.json")
with open(geojson_path, encoding="utf-8") as f:
    geojson = json.load(f)

# --- Estilos visuales ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    .stApp { background-color: #0a0e1a; font-family: 'Inter', sans-serif; }

    /* Título con barra azul */
    .mapa-titulo {
        border-left: 4px solid #4a9fd4;
        padding-left: 12px;
        font-size: 22px; font-weight: 700;
        color: #ffffff; margin-bottom: 4px;
    }
    .mapa-subtitulo {
        font-size: 12px; color: #667788;
        margin-bottom: 20px; padding-left: 16px;
    }

    /* Etiqueta de sección ranking */
    .rank-label {
        font-size: 10px; font-weight: 600;
        letter-spacing: 1.5px; color: #667788;
        text-transform: uppercase; margin-bottom: 8px;
    }

    /* Fila del ranking con posición, nombre y valor */
    .rank-item {
        background-color: #111827;
        border: 1px solid #1e2d40;
        border-radius: 8px;
        padding: 8px 14px;
        margin-bottom: 6px;
        font-size: 12px; color: #aabbcc;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    /* Número de posición en el ranking */
    .rank-pos {
        font-size: 10px; font-weight: 700;
        color: #445566; width: 18px;
        flex-shrink: 0; text-align: center;
    }
    /* Nombre del departamento */
    .rank-nombre { flex: 1; }

    /* Franja de cierre */
    .franja-cierre {
        background-color: #0d1422;
        border: 1px solid #1e2d40;
        border-radius: 8px;
        padding: 12px 20px;
        margin-top: 16px;
        font-size: 11px; color: #445566;
    }
    </style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown('<div class="mapa-titulo">Mapa coroplético interactivo</div>', unsafe_allow_html=True)
st.markdown('<div class="mapa-subtitulo">Distribución territorial del acceso digital · tooltips por departamento</div>', unsafe_allow_html=True)

# --- Controles: Año y Variable con mejor estilo ---
col_ctrl1, col_ctrl2, col_vacio = st.columns([1.5, 1.5, 3])
with col_ctrl1:
    año_sel = st.radio("📅 Año", options=sorted(df["año"].unique()),
                       horizontal=True, key="mapa_año")
with col_ctrl2:
    variable_sel = st.radio("📡 Variable", options=["Internet", "Celular"],
                            horizontal=True, key="mapa_var")

# --- Mapear variable seleccionada a columna del df ---
col_variable = "internet_proporcion" if variable_sel == "Internet" else "tel_celular_proporcion"

# --- Filtrar por año y zona TOTAL ---
df_mapa = df_filtrado[
    (df_filtrado["año"] == año_sel) &
    (df_filtrado["zona"] == "TOTAL")
].copy()

# --- Normalizar celular si viene en decimal ---
if col_variable == "tel_celular_proporcion":
    if df_mapa[col_variable].mean() < 2:
        df_mapa[col_variable] = df_mapa[col_variable] * 100

# --- Limpiar df: quitar TOTAL NACIONAL ---
df_mapa = df_mapa[df_mapa["departamento"] != "TOTAL NACIONAL"].copy()

# --- Normalizar nombres a Title Case para que coincidan con el GeoJSON ---
df_mapa["departamento"] = df_mapa["departamento"].str.title()

# Correcciones manuales de nombres que str.title() no resuelve bien
df_mapa["departamento"] = df_mapa["departamento"].replace({
    "Bogotá D.C."              : "Bogotá D.C.",
    "Valle Del Cauca"          : "Valle del Cauca",
    "Norte De Santander"       : "Norte de Santander",
    "La Guajira"               : "La Guajira",
    "San Andrés"               : "San Andrés",
    "Nariño"                   : "Nariño",
    "Chocó"                    : "Chocó",
    "Córdoba"                  : "Córdoba",
    "Bolívar"                  : "Bolívar",
    "Atlántico"                : "Atlántico",
})

# --- Verificar qué propiedad usa el GeoJSON para nombres ---
primer_feature = geojson["features"][0]
props = primer_feature["properties"]

# Imprime las propiedades disponibles para diagnóstico (solo en desarrollo)
# st.write(props)  # descomenta si el mapa sigue en blanco para ver los nombres del GeoJSON

# Detecta automáticamente la clave de nombre en el GeoJSON
if "NOMBRE_DPT" in props:
    prop_key = "NOMBRE_DPT"
elif "name" in props:
    prop_key = "name"
else:
    prop_key = list(props.keys())[0]   # usa la primera propiedad disponible

# --- Construir mapa coroplético ---
fig = px.choropleth(
    df_mapa,
    geojson=geojson,
    locations="departamento",
    featureidkey=f"properties.{prop_key}",   # clave dinámica según GeoJSON
    color=col_variable,
    color_continuous_scale="Blues",
    hover_name="departamento",
    hover_data={col_variable: ":.1f"},
    labels={col_variable: f"% {variable_sel}"}
)

fig.update_geos(
    fitbounds="locations",
    visible=False,
    bgcolor="#0a0e1a"
)
fig.update_layout(
    height=520,
    geo_bgcolor="#0a0e1a",
    plot_bgcolor="#0a0e1a",
    paper_bgcolor="#0a0e1a",
    font_color="#aabbcc",
    margin=dict(l=0, r=0, t=0, b=0),
    coloraxis_colorbar=dict(
        title=f"% {variable_sel}",
        tickfont=dict(color="#aabbcc"),
        title_font=dict(color="#aabbcc"),
    )
)

# --- Layout: mapa izquierda + rankings derecha ---
col_mapa, col_rank = st.columns([2.5, 1])

with col_mapa:
    st.plotly_chart(fig, use_container_width=True)

with col_rank:
    # --- Top 5 mayor acceso ---
    st.markdown('<div class="rank-label">🏆 Top 5 · Mayor acceso</div>', unsafe_allow_html=True)
    top5 = df_mapa.nlargest(5, col_variable)[["departamento", col_variable]].reset_index(drop=True)
    for i, row in top5.iterrows():
        st.markdown(f"""
        <div class="rank-item">
            <span class="rank-pos">{i+1}°</span>
            <span class="rank-nombre">{row["departamento"]}</span>
            <span style="color:#4a9fd4; font-weight:700;">{row[col_variable]:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Top 5 mayor rezago ---
    st.markdown('<div class="rank-label">⚠️ Top 5 · Mayor rezago</div>', unsafe_allow_html=True)
    bot5 = df_mapa.nsmallest(5, col_variable)[["departamento", col_variable]].reset_index(drop=True)
    for i, row in bot5.iterrows():
        st.markdown(f"""
        <div class="rank-item">
            <span class="rank-pos">{i+1}°</span>
            <span class="rank-nombre">{row["departamento"]}</span>
            <span style="color:#e05252; font-weight:700;">{row[col_variable]:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)

# --- Franja de cierre ---
st.markdown(f"""
<div class="franja-cierre">
    🗺️ &nbsp; Mostrando <strong style="color:#667788;">{variable_sel}</strong> ·
    Año <strong style="color:#667788;">{año_sel}</strong> ·
    Zona <strong style="color:#667788;">Total nacional</strong>
</div>
""", unsafe_allow_html=True)
