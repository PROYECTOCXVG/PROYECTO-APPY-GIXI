import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import df
from filtros import aplicar_filtros

df_filtrado = aplicar_filtros(df)

# --- Estilos visuales ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    /* Fondo oscuro general */
    .stApp { background-color: #0a0e1a; font-family: 'Inter', sans-serif; }

    /* Título con barra amarilla izquierda */
    .met-titulo {
        border-left: 4px solid #f59e0b;
        padding-left: 12px;
        font-size: 26px; font-weight: 700;   /* subimos de 22px */
        color: #ffffff; margin-bottom: 4px;
    }
    /* Subtítulo gris */
    .met-subtitulo {
        font-size: 14px; color: #889aaa;     /* subimos de 12px, aclaramos */
        margin-bottom: 24px; padding-left: 16px;
    }
    /* Etiqueta de sección */
    .met-label {
        font-size: 12px; font-weight: 700;   /* subimos de 10px */
        letter-spacing: 1.5px; color: #889aaa;
        text-transform: uppercase; margin-bottom: 12px;
    }

    /* Contenedor pipeline — horizontal con flex */
    .pipeline {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 28px;
        flex-wrap: wrap;
    }
    /* Cada paso del pipeline */
    .paso {
        border-radius: 8px;
        padding: 14px 18px;           /* más padding */
        font-size: 13px;              /* subimos de 12px */
        font-weight: 700;
        text-align: center;
        min-width: 120px;
        flex: 1;
    }
    /* Subtexto dentro del paso */
    .paso-sub {
        font-size: 11px; font-weight: 400;   /* subimos de 10px */
        margin-top: 4px; opacity: 0.9;
    }
    /* Colores por paso — p3 ahora azul para diferenciarlo de p2 */
    .p1 { background-color: #2a1f00; color: #f59e0b; border: 1px solid #f59e0b; }
    .p2 { background-color: #002a1a; color: #4ade80; border: 1px solid #4ade80; }
    .p3 { background-color: #001a2a; color: #4a9fd4; border: 1px solid #4a9fd4; }  /* azul — antes verde igual que p2 */
    .p4 { background-color: #1a0a2a; color: #a78bfa; border: 1px solid #a78bfa; }
    .p5 { background-color: #1a1200; color: #f59e0b; border: 1px solid #f59e0b; }  /* ámbar — más visible que gris */

    /* Flecha entre pasos */
    .arrow { color: #667788; font-size: 20px; flex-shrink: 0; }  /* más visible */

    /* Tarjeta fuente de datos */
    .card-fuente {
        background-color: #111827;
        border: 1px solid #1e2d40;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 14px;
    }
    /* Badges de fuente — más grandes */
    .badge-dane  { background-color: #1e3a50; color: #4a9fd4; font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 4px; white-space: nowrap; }
    .badge-datco { background-color: #1a2a1a; color: #4ade80; font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 4px; white-space: nowrap; }
    .badge-geo   { background-color: #2a1f00; color: #f59e0b; font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 4px; white-space: nowrap; }

    /* Texto de fuente */
    .fuente-text { font-size: 13px; color: #99aabb; line-height: 1.5; }  /* subimos de 12px */

    /* Chips tecnología — más visibles */
    .chip {
        display: inline-block;
        background-color: #111827;
        border: 1px solid #2a3a4a;       /* borde más visible */
        border-radius: 20px;
        padding: 6px 14px;               /* más padding */
        font-size: 12px; color: #ccd6e0; /* subimos de 11px, aclaramos */
        margin: 3px;
    }
    /* Chips variables — azul más visible */
    .chip-var {
        display: inline-block;
        background-color: #0d1f33;
        border: 1px solid #2a4a6a;
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 12px; color: #6ab8e8;  /* aclaramos */
        margin: 3px;
    }

    /* Franja de cierre */
    .franja-cierre {
        background-color: #0d1422;
        border: 1px solid #1e2d40;
        border-radius: 8px;
        padding: 14px 20px;
        margin-top: 20px;
        font-size: 13px; color: #778899;  /* subimos de 11px, aclaramos */
    }
    </style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown('<div class="met-titulo">Metodología, herramientas y datos</div>', unsafe_allow_html=True)
st.markdown('<div class="met-subtitulo">Pipeline de datos · stack tecnológico · fuentes y proceso de ETL</div>', unsafe_allow_html=True)

# --- Pipeline de análisis ---
st.markdown('<div class="met-label">Pipeline de Análisis</div>', unsafe_allow_html=True)
st.markdown("""
<div class="pipeline">
    <div class="paso p1">01 · INGESTA<div class="paso-sub">6 Excel del DANE</div></div>
    <div class="arrow">→</div>
    <div class="paso p2">02 · LIMPIEZA<div class="paso-sub">Python · Pandas</div></div>
    <div class="arrow">→</div>
    <div class="paso p3">03 · UNIFICACIÓN<div class="paso-sub">Panel único merged</div></div>
    <div class="arrow">→</div>
    <div class="paso p4">04 · ANÁLISIS<div class="paso-sub">EDA · correlaciones</div></div>
    <div class="arrow">→</div>
    <div class="paso p5">05 · VISUALIZACIÓN<div class="paso-sub">Plotly · Folium</div></div>
</div>
""", unsafe_allow_html=True)

# --- Dos columnas balanceadas: fuentes y stack ---
col1, col2 = st.columns(2, gap="large")

with col1:
    # --- Fuentes de datos ---
    st.markdown('<div class="met-label">Fuentes de Datos</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card-fuente">
        <span class="badge-dane">DANE</span>
        <span class="fuente-text">Encuesta de Calidad de Vida (ECV) 2019, 2022, 2023 — módulo TIC hogares</span>
    </div>
    <div class="card-fuente">
        <span class="badge-datco">DATCO</span>
        <span class="fuente-text">Datos Abiertos Colombia — tablas departamentales por zona</span>
    </div>
    <div class="card-fuente">
        <span class="badge-geo">GEO</span>
        <span class="fuente-text">GeoJSON Colombia departamentos para mapas coropléticos</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # --- Stack tecnológico ---
    st.markdown('<div class="met-label">Stack Tecnológico</div>', unsafe_allow_html=True)
    st.markdown("""
    <div>
        <span class="chip">⚙ Python 3.11</span>
        <span class="chip">Pandas 2.x</span>
        <span class="chip">NumPy</span>
        <span class="chip">Plotly</span>
        <span class="chip">Folium</span>
        <span class="chip">Jupyter</span>
        <span class="chip">GeoPandas</span>
        <span class="chip">Streamlit</span>
        <span class="chip">Matplotlib</span>
        <span class="chip">Seaborn</span>
    </div>
    """, unsafe_allow_html=True)

    # --- Variables principales ---
    st.markdown('<div class="met-label" style="margin-top:18px;">Variables Principales</div>', unsafe_allow_html=True)
    st.markdown("""
    <div>
        <span class="chip-var">% internet hogar</span>
        <span class="chip-var">% celular</span>
        <span class="chip-var">% computador</span>
        <span class="chip-var">% televisor</span>
        <span class="chip-var">Zona cab/rural</span>
        <span class="chip-var">Depto · año</span>
    </div>
    """, unsafe_allow_html=True)

# --- Franja de cierre ---
st.markdown("""
<div class="franja-cierre">
    🔧 &nbsp; Los datos fueron procesados con <strong style="color:#99aabb;">Python + Pandas</strong>
    y visualizados con <strong style="color:#99aabb;">Plotly + Folium</strong> dentro del entorno
    <strong style="color:#99aabb;">Streamlit</strong>.
</div>
""", unsafe_allow_html=True)
