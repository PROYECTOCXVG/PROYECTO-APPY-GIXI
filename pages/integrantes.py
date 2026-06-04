import streamlit as st
import base64
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import df
from filtros import aplicar_filtros

df_filtrado = aplicar_filtros(df)

# --- Función para convertir imagen local a base64 ---
def img_a_base64(ruta):
    """Lee imagen del disco y la convierte a base64 para incrustarla en HTML"""
    with open(ruta, "rb") as f:
        datos = f.read()
    extension = ruta.split(".")[-1].lower()
    mime = "image/jpeg" if extension in ["jpg", "jpeg"] else "image/png"
    return f"data:{mime};base64,{base64.b64encode(datos).decode()}"

# --- Rutas de imágenes ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_claudia = os.path.join(BASE_DIR, "img", "Claudia.png")
ruta_ingrid  = os.path.join(BASE_DIR, "img", "Ingrid.png")

# --- Convertir fotos a base64 ---
foto_claudia = img_a_base64(ruta_claudia)
foto_ingrid  = img_a_base64(ruta_ingrid)

# --- Estilos ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

/* Fondo oscuro general */
.stApp { background-color: #0f1117; font-family: 'Inter', sans-serif; }

/* Título reducido y aclarado */
.titulo-pagina {
    font-size: 38px; font-weight: 800;   /* bajamos de 52px */
    color: #e0e0e0;                      /* aclaramos de #cccccc */
    line-height: 1.1; margin-bottom: 0px;
}
/* Título sección con borde verde */
.seccion-titulo {
    font-size: 22px; font-weight: 700;
    color: #ffffff;
    border-left: 4px solid #4ade80;
    padding-left: 12px; margin-bottom: 4px;
}
/* Subtítulo aclarado */
.seccion-subtitulo {
    font-size: 14px; color: #99aabb;     /* aclaramos de #666666 */
    margin-bottom: 28px; padding-left: 16px;
}

/* Tarjeta integrante — altura fija para que ambas sean iguales */
.card-integrante {
    background-color: #1a1d27;
    border-radius: 14px;
    padding: 32px 28px;                  /* más padding uniforme */
    margin-bottom: 16px;
    text-align: center;
    height: 100%;                        /* misma altura en ambas tarjetas */
    box-sizing: border-box;
}

/* Foto circular */
.foto-avatar {
    width: 120px;                        /* subimos de 110px */
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    object-position: center 5%;         /* enfoca la cara */
    box-shadow: 0 0 0 3px #4ade80;      /* borde verde sin gap */
    margin: 0 auto 20px auto;
    display: block;
    background-color: #1a1d27;
}

/* Nombre */
.nombre {
    font-size: 19px; font-weight: 700;   /* subimos de 17px */
    color: #ffffff; margin-bottom: 8px;
}
/* Programa */
.programa {
    font-size: 13px; color: #4ade80;     /* subimos de 12px */
    font-weight: 600; letter-spacing: 0.5px;
    margin-bottom: 12px;
}
/* Rol */
.rol {
    font-size: 14px; color: #99aabb;     /* subimos de 13px, aclaramos */
    line-height: 1.7; margin-bottom: 20px;
}

/* Chips centrados */
.chips { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }
.chip  {
    background-color: #0f1117;
    border: 1px solid #2a2d3a;
    color: #ccd6e0;                      /* aclaramos de #cccccc */
    font-size: 12px; font-weight: 600;   /* subimos de 11px */
    padding: 5px 12px; border-radius: 20px;
    letter-spacing: 0.5px;
}

/* Franja de cierre */
.franja-cierre {
    background-color: #0d1422;
    border: 1px solid #1e2d40;
    border-radius: 8px;
    padding: 14px 20px;
    margin-top: 20px;
    font-size: 13px; color: #778899;
}
</style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown('<div class="titulo-pagina">Integrantes</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="seccion-titulo">Integrantes del grupo</div>', unsafe_allow_html=True)
st.markdown('<div class="seccion-subtitulo">Equipo de investigación · Análisis de datos · Universidad de Antioquia × MinTIC</div>', unsafe_allow_html=True)

# --- Columnas centradas con márgenes laterales vacíos ---
col_izq, col1, col2, col_der = st.columns([0.5, 3, 3, 0.5], gap="medium")

with col1:
    # Tarjeta Claudia
    st.markdown(f"""
    <div class="card-integrante">
        <img src="{foto_claudia}" class="foto-avatar">
        <div class="nombre">Claudia Ximena Vargas García</div>
        <div class="programa">Análisis de Datos · Nivel Básico · Universidad de Antioquia × MinTic</div>
        <div class="rol">Rol en el proyecto: investigación, redacción del informe,
        análisis de política pública y revisión de hallazgos.</div>
        <div class="chips">
            <span class="chip">Investigación</span>
            <span class="chip">Política pública</span>
            <span class="chip">Redacción</span>
            <span class="chip">Revisión</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Tarjeta Ingrid
    st.markdown(f"""
    <div class="card-integrante">
        <img src="{foto_ingrid}" class="foto-avatar">
        <div class="nombre">Ingrid Giselle Guzmán Castaño</div>
        <div class="programa">Análisis de Datos · Nivel Básico · Universidad de Antioquia × MinTic</div>
        <div class="rol">Rol en el proyecto: análisis de datos, visualizaciones,
        procesamiento ETL y construcción del tablero interactivo.</div>
        <div class="chips">
            <span class="chip">Python</span>
            <span class="chip">Pandas</span>
            <span class="chip">Streamlit</span>
            <span class="chip">Plotly</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Franja de cierre ---
st.markdown("""
<div class="franja-cierre">
    👥 &nbsp; Proyecto desarrollado en el marco del programa
    <strong style="color:#99aabb;">Talento Tech</strong> ·
    <strong style="color:#99aabb;">Universidad de Antioquia × MinTIC</strong> · 2025
</div>
""", unsafe_allow_html=True)



