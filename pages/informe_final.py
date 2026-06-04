import streamlit as st
import base64
import os
import sys
from pdf2image import convert_from_path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import df
from filtros import aplicar_filtros

df_filtrado = aplicar_filtros(df)

# --- Ruta del PDF ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_pdf = os.path.join(BASE_DIR, "img", "Informefinal.pdf")

# --- Leer PDF para descarga ---
with open(ruta_pdf, "rb") as f:
    pdf_bytes = f.read()

# --- Vista previa: solo primera página ---
preview = convert_from_path(ruta_pdf, first_page=1, last_page=1, dpi=150)[0]

# ... (mismos estilos CSS que arriba) ...

# --- Encabezado ---
st.markdown('<div class="inf-titulo">Informe Final</div>', unsafe_allow_html=True)
st.markdown('<div class="inf-subtitulo">Documento completo del proyecto · Análisis de Datos · 2025</div>', unsafe_allow_html=True)

# --- Vista previa + Descarga ---
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="visor-container">', unsafe_allow_html=True)
    st.image(preview, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.download_button(
        label="📥 Descargar PDF",
        data=pdf_bytes,
        file_name="Informefinal.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    st.info("Vista previa de la primera página. Descarga el documento completo.")

# --- Franja de cierre ---
st.markdown("""
<div class="franja-cierre">
    📄 &nbsp; Documento generado como parte del
    <strong style="color:#99aabb;">Proyecto Final · Análisis de Datos</strong> ·
    Universidad de Antioquia × MinTIC · 2026
</div>
""", unsafe_allow_html=True)
