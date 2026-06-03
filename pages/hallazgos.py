import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import df
from filtros import aplicar_filtros

df_filtrado = aplicar_filtros(df)

# --- Estilos generales ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

/* Fondo oscuro general */
.stApp { background-color: #0f1117; font-family: 'Inter', sans-serif; }

/* Título principal de página — reducido y aclarado */
.titulo-pagina {
    font-size: 38px;             /* bajamos de 52px */
    font-weight: 800;
    color: #e0e0e0;              /* aclaramos — eliminamos línea duplicada */
    margin-bottom: 0px;
    line-height: 1.1;
}

/* Título de sección con borde verde */
.seccion-titulo {
    font-size: 22px;             /* subimos de 20px */
    font-weight: 700;
    color: #ffffff;
    border-left: 4px solid #4ade80;
    padding-left: 12px;
    margin-bottom: 4px;
}

/* Subtítulo gris debajo del título */
.seccion-subtitulo {
    font-size: 14px;             /* subimos de 13px */
    color: #99aabb;              /* aclaramos de #888888 */
    margin-bottom: 24px;
    padding-left: 16px;
}

/* Encabezado de columna */
.col-header {
    font-size: 13px;             /* subimos de 11px */
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 16px;
    padding-bottom: 6px;
}
/* Color encabezado esperados — verde */
.col-header-expected   { color: #4ade80; border-bottom: 1px solid #4ade8033; }
/* Color encabezado inesperados — naranja */
.col-header-unexpected { color: #fb923c; border-bottom: 1px solid #fb923c33; }

/* Tarjeta de hallazgo */
.card {
    border-left: 4px solid;
    padding: 18px 22px;          /* más padding */
    border-radius: 8px;
    margin-bottom: 14px;
    background-color: #1a1d27;
}
.card-expected   { border-color: #4ade80; }
.card-unexpected { border-color: #fb923c; }

/* Título dentro de la tarjeta */
.card-title {
    font-size: 13px;             /* subimos de 11px */
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.card-title-expected   { color: #4ade80; }
.card-title-unexpected { color: #fb923c; }

/* Texto del hallazgo */
.card-text {
    font-size: 14px;             /* subimos de 13px */
    color: #ccd6e0;              /* aclaramos de #aaaaaa */
    line-height: 1.7;
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

# --- Título de página ---
st.markdown('<div class="titulo-pagina">Hallazgos</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Subtítulo sección ---
st.markdown('<div class="seccion-titulo">Hallazgos esperados e inesperados</div>', unsafe_allow_html=True)
st.markdown('<div class="seccion-subtitulo">Resultados del análisis exploratorio basados en los datos reales del DANE 2019–2023</div>', unsafe_allow_html=True)

# --- Dos columnas: esperados e inesperados ---
col1, col2 = st.columns(2, gap="medium")

with col1:
    # --- Encabezado columna esperados ---
    st.markdown('<p class="col-header col-header-expected">✓ &nbsp; Hallazgos esperados</p>', unsafe_allow_html=True)

    # --- Tarjetas hallazgos esperados ---
    st.markdown("""
    <div class="card card-expected">
        <div class="card-title card-title-expected">Brecha urbano-rural persistente</div>
        <div class="card-text">El acceso a internet en cabeceras municipales supera consistentemente
        al de zonas rurales en todos los años analizados. Aunque la brecha se reduce entre 2019 y
        2023, sigue siendo estructural y significativa.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-expected">
        <div class="card-title card-title-expected">Crecimiento acelerado post-COVID</div>
        <div class="card-text">El salto en conectividad entre 2019 y 2022 fue notablemente mayor
        que el registrado entre 2022 y 2023, evidenciando el efecto impulsor de la pandemia sobre
        la adopción tecnológica en el país.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-expected">
        <div class="card-title card-title-expected">Alta penetración del teléfono celular</div>
        <div class="card-text">El celular es el dispositivo con mayor cobertura en todas las zonas
        y años, confirmando su rol central como puerta de entrada a la conectividad digital
        en Colombia.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # --- Encabezado columna inesperados ---
    st.markdown('<p class="col-header col-header-unexpected">⚡ &nbsp; Hallazgos inesperados</p>', unsafe_allow_html=True)

    # --- Tarjetas hallazgos inesperados ---
    st.markdown("""
    <div class="card card-unexpected">
        <div class="card-title card-title-unexpected">Celular no compensa el internet fijo</div>
        <div class="card-text">A pesar de la alta penetración del celular en zonas rurales, el
        internet fijo sigue siendo escaso. Esto limita el aprovechamiento real de la conectividad
        para actividades educativas y laborales de calidad.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-unexpected">
        <div class="card-title card-title-unexpected">Departamentos en "trampa media"</div>
        <div class="card-text">Varios departamentos con ingresos medios presentan estancamiento
        en acceso digital, sugiriendo que las barreras no son solo económicas sino también de
        infraestructura, cultura digital y oferta de servicios.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-unexpected">
        <div class="card-title card-title-unexpected">Estancamiento en televisión tradicional</div>
        <div class="card-text">Mientras el streaming crece, la TV convencional muestra caída
        sostenida incluso en zonas rurales, indicando una transición más rápida de lo esperado
        hacia contenidos digitales bajo demanda.</div>
    </div>
    """, unsafe_allow_html=True)

# --- Franja de cierre ---
st.markdown("""
<div class="franja-cierre">
    🔍 &nbsp; Hallazgos derivados del análisis de
    <strong style="color:#99aabb;">34 departamentos</strong> ·
    <strong style="color:#99aabb;">3 años</strong> ·
    <strong style="color:#99aabb;">2 zonas</strong> con datos del DANE 2019–2023
</div>
""", unsafe_allow_html=True)




