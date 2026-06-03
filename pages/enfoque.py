import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import df           # Importa el dataframe
from filtros import aplicar_filtros

df_filtrado = aplicar_filtros(df)

# --- Estilos visuales ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    /* Fondo oscuro general */
    .stApp { background-color: #0a0e1a; font-family: 'Inter', sans-serif; }

    /* Título principal de la página */
.enfoque-titulo {
    border-left: 4px solid #4a9fd4;
    padding-left: 12px;
    font-size: 26px; font-weight: 700;   /* subimos de 22px a 26px */
    color: #ffffff; margin-bottom: 4px;
}
    /* Subtítulo gris */
    .enfoque-subtitulo {
    font-size: 14px; color: #889aaa;     /* subimos de 12px, aclaramos color */
    margin-bottom: 24px; padding-left: 16px;
}

    /* Tarjeta base */
    .card-enfoque {
        background-color: #111827;
        border: 1px solid #1e2d40;
        border-radius: 10px;
        padding: 20px 20px;
        font-family: 'Inter', sans-serif;
        height: 100%;
    }
    /* Variantes de borde izquierdo por color */
    .card-blue  { border-left: 4px solid #4a9fd4; }  /* azul */
    .card-green { border-left: 4px solid #4ade80; }  /* verde */
    .card-amber { border-left: 4px solid #f59e0b; }  /* amarillo */
    .card-purple{ border-left: 4px solid #a78bfa; }  /* morado */

    /* Ícono arriba del título de tarjeta */
    .card-icon  { font-size: 24px; margin-bottom: 8px; }  /* subimos de 20px */

    /* Título de tarjeta */
   .card-title {
        font-size: 15px; font-weight: 700;   /* subimos de 13px a 15px */
        color: #e0eaf0; margin-bottom: 8px;  /* aclaramos color */
}
    /* Texto de tarjeta */
    .card-text  { font-size: 14px; color: #99aabb; line-height: 1.8; }  /* subimos de 12px, aclaramos */

    /* Separador de sección */
   .section-label {
        font-size: 12px; letter-spacing: 2px;   /* subimos de 10px a 12px */
        color: #667788; text-transform: uppercase;
        margin-top: 28px; margin-bottom: 12px;
}
    </style>
""", unsafe_allow_html=True)

# --- Encabezado --- (sin st.title para evitar título duplicado)
st.markdown('<div class="enfoque-titulo">Marco Conceptual</div>', unsafe_allow_html=True)
st.markdown('<div class="enfoque-subtitulo">Marco conceptual que sitúa la problemática de la brecha digital en Colombia</div>', unsafe_allow_html=True)

# --- Fila 1: dos tarjetas principales ---
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown("""
    <div class="card-enfoque card-blue">
        <div class="card-icon">🌐</div>
        <div class="card-title">¿Qué es la brecha digital?</div>
        <div class="card-text">La brecha digital es la desigualdad en el acceso, uso y aprovechamiento
        de las tecnologías de la información y comunicación (TIC). Va más allá de la conectividad:
        incluye habilidades digitales, calidad del acceso y relevancia del contenido disponible.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card-enfoque card-green">
        <div class="card-icon">🏙️</div>
        <div class="card-title">Contexto Colombiano</div>
        <div class="card-text">Colombia registra profundas desigualdades territoriales. La pandemia de
        2020 aceleró la digitalización urbana pero profundizó la exclusión rural. Con 34 departamentos
        muy heterogéneos en infraestructura, ingresos y geografía, el país es un caso de estudio
        paradigmático.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Etiqueta sección dimensiones ---
st.markdown('<div class="section-label">Dimensiones de análisis</div>', unsafe_allow_html=True)

# --- Fila 2: tres tarjetas de dimensiones con color diferente cada una ---
col3, col4, col5 = st.columns(3, gap="medium")

with col3:
    st.markdown("""
    <div class="card-enfoque card-blue">
        <div class="card-icon">📡</div>
        <div class="card-title">Dimensión de Acceso</div>
        <div class="card-text">Disponibilidad de dispositivos y conexión en el hogar.
        Indicadores: % hogares con computador, celular, tablet e internet.</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card-enfoque card-amber">
        <div class="card-icon">🗺️</div>
        <div class="card-title">Dimensión Territorial</div>
        <div class="card-text">Variación entre departamentos y entre zonas de cabecera
        municipal vs. centros poblados y rural disperso.</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="card-enfoque card-purple">
        <div class="card-icon">📅</div>
        <div class="card-title">Dimensión Temporal</div>
        <div class="card-text">Cambios entre 2019 (prepandemia), 2022 (pospandemia) y 2023
        (consolidación), capturando el impacto del COVID-19.</div>
    </div>
    """, unsafe_allow_html=True)

