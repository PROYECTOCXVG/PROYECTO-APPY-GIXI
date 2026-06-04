import streamlit as st
import base64
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import df
from filtros import aplicar_filtros

df_filtrado = aplicar_filtros(df)

# --- Ruta del PDF ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_pdf = os.path.join(BASE_DIR, "img", "Informefinal.pdf")

# --- Leer y convertir PDF a base64 ---
with open(ruta_pdf, "rb") as f:
    pdf_base64 = base64.b64encode(f.read()).decode("utf-8")

# --- Estilos visuales ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

/* Fondo oscuro general */
.stApp { background-color: #0a0e1a; font-family: 'Inter', sans-serif; }

/* Título con barra azul */
.inf-titulo {
    border-left: 4px solid #4a9fd4;
    padding-left: 12px;
    font-size: 26px; font-weight: 700;
    color: #ffffff; margin-bottom: 4px;
}
/* Subtítulo gris */
.inf-subtitulo {
    font-size: 14px; color: #889aaa;
    margin-bottom: 20px; padding-left: 16px;
}

/* Contenedor del visor con sombra y bordes redondeados */
.visor-container {
    border-radius: 12px;
    overflow: hidden;                    /* recorta esquinas del iframe */
    border: 1px solid #1e2d40;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);  /* sombra para profundidad */
}

/* Franja de cierre */
.franja-cierre {
    background-color: #0d1422;
    border: 1px solid #1e2d40;
    border-radius: 8px;
    padding: 12px 20px;
    margin-top: 16px;
    font-size: 13px; color: #778899;
}
</style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown('<div class="inf-titulo">Informe Final</div>', unsafe_allow_html=True)
st.markdown('<div class="inf-subtitulo">Documento completo del proyecto · Análisis de Datos · 2025</div>', unsafe_allow_html=True)

# --- Visor PDF con iframe en contenedor estilizado ---
st.markdown(f"""
<div class="visor-container">
    <iframe
        src="data:application/pdf;base64,{pdf_base64}"
        width="100%"
        height="820px"
        type="application/pdf"
        style="display:block; border:none;"
    ></iframe>
</div>
""", unsafe_allow_html=True)

# --- Franja de cierre ---
st.markdown("""
<div class="franja-cierre">
    📄 &nbsp; Documento generado como parte del
    <strong style="color:#99aabb;">Proyecto Final · Análisis de Datos</strong> ·
    Universidad de Antioquia × MinTIC · 2026
</div>
""", unsafe_allow_html=True)
