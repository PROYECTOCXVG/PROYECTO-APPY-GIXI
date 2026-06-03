import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import df
from filtros import aplicar_filtros

df_filtrado = aplicar_filtros(df)  # Aplica filtros del sidebar

# --- Estilos generales ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

/* Fondo oscuro general */
.stApp { background-color: #0f1117; font-family: 'Inter', sans-serif; }

/* Título principal — reducido */
.titulo-pagina {
    font-size: 38px;             /* bajamos de 52px */
    font-weight: 800;
    color: #e0e0e0;              /* aclaramos */
    line-height: 1.1;
    margin-bottom: 4px;
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

/* Subtítulo gris — aclarado */
.seccion-subtitulo {
    font-size: 14px;             /* subimos de 13px */
    color: #99aabb;              /* aclaramos de #666666 */
    margin-bottom: 28px;
    padding-left: 16px;
}

/* Tarjeta de conclusión */
.card-conclusion {
    border-left: 4px solid;
    padding: 24px 28px;
    border-radius: 10px;
    margin-bottom: 16px;
    background-color: #1a1d27;
}

/* Badge P1, P2... — más grande y visible */
.card-badge {
    display: inline-block;
    font-size: 12px;             /* subimos de 10px */
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    background-color: #0f1117;
    border-radius: 4px;
    padding: 4px 10px;           /* más padding */
    margin-bottom: 12px;
}

/* Título de tarjeta */
.card-titulo {
    font-size: 18px;             /* subimos de 16px */
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 12px;
    line-height: 1.3;
}

/* Texto del cuerpo */
.card-body {
    font-size: 14px;             /* se mantiene */
    color: #ccd6e0;              /* aclaramos de #d0d0d0 */
    line-height: 1.8;
}

/* Franja de cierre */
.franja-cierre {
    background-color: #0d1422;
    border: 1px solid #1e2d40;
    border-radius: 8px;
    padding: 14px 20px;
    margin-top: 8px;
    font-size: 13px; color: #778899;
}
</style>
""", unsafe_allow_html=True)

# --- Título de página — solo uno, eliminado el duplicado ---
st.markdown('<div class="titulo-pagina">Conclusiones</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Subtítulo sección ---
st.markdown('<div class="seccion-titulo">Respuestas a las preguntas de investigación</div>', unsafe_allow_html=True)
st.markdown('<div class="seccion-subtitulo">Hallazgos principales derivados del análisis de datos DANE 2019–2023</div>', unsafe_allow_html=True)

# --- Fila 1: P1 y P2 ---
col1, col2 = st.columns(2, gap="medium")

with col1:  # Tarjeta azul — Evolución del acceso
    st.markdown("""
    <div class="card-conclusion" style="border-color: #38bdf8;">
        <span class="card-badge" style="color: #38bdf8;">P1</span>
        <div class="card-titulo">Evolución del acceso</div>
        <div class="card-body">
            El acceso a internet en hogares colombianos mostró un crecimiento sostenido entre 2019
            y 2023, con el mayor salto durante la pandemia (2019→2022). La tendencia es positiva
            pero desigual entre territorios, con departamentos que aún no superan el 40% de cobertura.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:  # Tarjeta verde — Brecha urbano-rural
    st.markdown("""
    <div class="card-conclusion" style="border-color: #4ade80;">
        <span class="card-badge" style="color: #4ade80;">P2</span>
        <div class="card-titulo">Brecha urbano-rural</div>
        <div class="card-body">
            La brecha entre cabeceras municipales y zonas rurales sigue siendo estructural y
            significativa. Aunque se redujo marginalmente en el periodo analizado, persiste como
            el principal desafío de equidad digital del país.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)  # Espaciado entre filas

# --- Fila 2: P3 y P4 ---
col3, col4 = st.columns(2, gap="medium")

with col3:  # Tarjeta amarilla — Líderes y rezagados
    st.markdown("""
    <div class="card-conclusion" style="border-color: #fbbf24;">
        <span class="card-badge" style="color: #fbbf24;">P3</span>
        <div class="card-titulo">Líderes y rezagados</div>
        <div class="card-body">
            Bogotá D.C. lidera consistentemente el acceso digital, mientras Vaupés, Amazonas y
            Guainía concentran el mayor rezago. Esta polarización territorial ha cambiado poco en
            el periodo analizado, evidenciando barreras estructurales difíciles de revertir en el
            corto plazo.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:  # Tarjeta morada — Celular vs internet fijo
    st.markdown("""
    <div class="card-conclusion" style="border-color: #a78bfa;">
        <span class="card-badge" style="color: #a78bfa;">P4</span>
        <div class="card-titulo">Celular vs internet fijo</div>
        <div class="card-body">
            El teléfono celular no compensa la ausencia de internet fijo. Las zonas con alta
            penetración móvil pero bajo internet fijo muestran limitaciones en uso productivo,
            educativo y laboral, evidenciando que la conectividad móvil no es equivalente en
            calidad ni capacidad.
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Franja de cierre ---
st.markdown("""
<div class="franja-cierre">
    ✅ &nbsp; Conclusiones basadas en el análisis de
    <strong style="color:#99aabb;">34 departamentos</strong> ·
    <strong style="color:#99aabb;">3 años</strong> ·
    <strong style="color:#99aabb;">2 zonas</strong> con datos del DANE 2019–2023
</div>
""", unsafe_allow_html=True)

