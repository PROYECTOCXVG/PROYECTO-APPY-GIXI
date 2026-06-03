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

/* Título con barra verde izquierda */
.obj-titulo {
    border-left: 4px solid #4ade80;
    padding-left: 12px;
    font-size: 26px; font-weight: 700;   /* subimos de 22px a 26px */
    color: #ffffff; margin-bottom: 4px;
}
/* Subtítulo gris */
.obj-subtitulo {
    font-size: 14px; color: #889aaa;     /* subimos de 12px y aclaramos color */
    margin-bottom: 24px; padding-left: 16px;
}

/* Tarjeta objetivo general */
.card-general {
    background-color: #111827;
    border: 1px solid #1e2d40;
    border-left: 4px solid #4ade80;
    border-radius: 10px;
    padding: 20px 22px;
    margin-bottom: 20px;
}
/* Etiqueta OBJETIVO GENERAL */
.card-general-label {
    font-size: 12px; font-weight: 700;   /* subimos de 10px a 12px */
    letter-spacing: 1.5px; color: #4ade80;
    text-transform: uppercase; margin-bottom: 10px;
}
/* Texto objetivo general */
.card-general-text {
    font-size: 15px; color: #ccd6e0; line-height: 1.8;  /* subimos de 13px, aclaramos color */
}

/* Etiqueta sección objetivos específicos */
.section-label {
    font-size: 12px; letter-spacing: 2px;   /* subimos de 10px a 12px */
    color: #667788; text-transform: uppercase;
    margin-bottom: 12px;
}

/* Tarjeta objetivo específico */
.card-obj {
    background-color: #111827;
    border: 1px solid #1e2d40;
    border-radius: 10px;
    padding: 18px 20px;
    display: flex;
    align-items: flex-start;
    gap: 14px;
    margin-bottom: 12px;
}

/* Número del objetivo — círculo con color */
.obj-num {
    font-size: 13px; font-weight: 800;   /* subimos de 12px a 13px */
    width: 34px; height: 34px;           /* círculo más grande */
    border-radius: 50%;
    display: flex; align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
/* Colores individuales para cada número */
.num-1 { background-color: #1a3a4a; color: #4a9fd4; }
.num-2 { background-color: #1a3a2a; color: #4ade80; }
.num-3 { background-color: #3a2a10; color: #f59e0b; }
.num-4 { background-color: #2a1a3a; color: #a78bfa; }

/* Texto del objetivo específico */
.obj-text {
    font-size: 14px; color: #aabbcc; line-height: 1.8;  /* subimos de 12px, aclaramos color */
    padding-top: 4px;
}

/* Franja de cierre al fondo */
.franja-cierre {
    background-color: #0d1422;
    border: 1px solid #1e2d40;
    border-radius: 8px;
    padding: 12px 20px;
    margin-top: 8px;
    font-size: 13px; color: #667788;   /* subimos de 11px, aclaramos color */
}
    </style>
""", unsafe_allow_html=True)

# --- Encabezado --- (sin st.title para evitar título duplicado)
st.markdown('<div class="obj-titulo">Objetivo del proyecto</div>', unsafe_allow_html=True)
st.markdown('<div class="obj-subtitulo">Propósito general y objetivos específicos que orientan el análisis</div>', unsafe_allow_html=True)

# --- Objetivo general ---
st.markdown("""
<div class="card-general">
    <div class="card-general-label">Objetivo General</div>
    <div class="card-general-text">Caracterizar y visualizar la evolución de la brecha digital
    en Colombia entre 2019 y 2023, identificando patrones territoriales y socioeconómicos que
    permitan formular recomendaciones de política pública orientadas a la reducción de las
    desigualdades en el acceso tecnológico.</div>
</div>
""", unsafe_allow_html=True)

# --- Etiqueta sección específicos ---
st.markdown('<div class="section-label">Objetivos Específicos</div>', unsafe_allow_html=True)

# --- Lista de objetivos: (clase de color, número, texto) ---
objetivos = [
    ("num-1", "01", "Unificar y limpiar los 6 datasets del DANE para construir un panel longitudinal consistente de 34 departamentos × 3 años × 2 zonas."),
    ("num-2", "02", "Medir la magnitud de la brecha urbano-rural y su evolución mediante indicadores cuantitativos comparables en el tiempo."),
    ("num-3", "03", "Construir visualizaciones interactivas que comuniquen los hallazgos a audiencias técnicas y no técnicas de manera efectiva."),
    ("num-4", "04", "Formular recomendaciones de política pública concretas y priorizadas con base en los patrones identificados en los datos."),
]

# --- Renderizar objetivos en 2 columnas ---
col1, col2 = st.columns(2, gap="medium")

for i, (color_class, numero, texto) in enumerate(objetivos):
    col = col1 if i % 2 == 0 else col2   # alterna entre columna izquierda y derecha
    with col:
        st.markdown(f"""
        <div class="card-obj">
            <div class="obj-num {color_class}">{numero}</div>
            <div class="obj-text">{texto}</div>
        </div>
        """, unsafe_allow_html=True)

# --- Franja de cierre ---
st.markdown("""
<div class="franja-cierre">
    🎯 &nbsp; Los objetivos se articulan con las secciones de <strong style="color:#667788;">
    Análisis</strong> y <strong style="color:#667788;">Resultados</strong> del tablero.
</div>
""", unsafe_allow_html=True)

