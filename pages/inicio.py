import streamlit as st
import base64
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import df
from filtros import aplicar_filtros

df_filtrado = aplicar_filtros(df)

# --- Función para convertir imagen a base64 ---
def img_a_base64(ruta):
    """Lee imagen del disco y la convierte a base64 para usarla en CSS"""
    with open(ruta, "rb") as f:
        datos = f.read()
    extension = ruta.split(".")[-1].lower()
    mime = "image/jpeg" if extension in ["jpg", "jpeg"] else "image/png"
    return f"data:{mime};base64,{base64.b64encode(datos).decode()}"

# --- Ruta de la imagen de encabezado ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img_hero = img_a_base64(os.path.join(BASE_DIR, "img", "img_encabezado.png"))

# --- Estilos visuales ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    /* Fondo oscuro general */
    .stApp { background-color: #0a0e1a; font-family: 'Inter', sans-serif; }

    /* Hero con imagen de fondo */
    .hero {
        border-radius: 14px;
        padding: 56px 48px;              /* padding uniforme arriba/abajo */
        margin-bottom: 28px;
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center 30%;
        min-height: 260px;
        display: flex;
        flex-direction: column;
        justify-content: center;         /* centra el texto verticalmente */
    }

    /* Subtítulo pequeño azul arriba */
    .sup-title {
        font-size: 13px;                 /* subimos de 12px */
        letter-spacing: 2.5px;
        color: #7dd3fc;
        text-transform: uppercase;
        margin-bottom: 10px;
        text-shadow: 0 1px 8px rgba(0,0,0,0.9);
        font-weight: 600;
    }

    /* Título principal */
    .main-title {
        font-size: 44px;                 /* subimos de 40px */
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 10px;
        line-height: 1.1;
        text-shadow: 0 2px 16px rgba(0,0,0,0.9);  /* sombra fuerte */
    }

    /* Descripción debajo del título */
    .sub-desc {
        font-size: 16px;                 /* subimos de 15px */
        color: #ccd6e0;                  /* aclaramos */
        margin-bottom: 0px;
        text-shadow: 0 1px 8px rgba(0,0,0,0.9);
    }

    /* Tarjeta de métrica */
    /* Tarjeta de métrica — borde izquierdo de color como conclusiones */
    .card {
        background-color: #1a1d27;       /* mismo fondo que conclusiones */
        border: 1px solid #1e2d40;
        border-left: 4px solid;          /* borde izquierdo — color se pone inline */
        border-radius: 10px;
        padding: 22px 16px;
        text-align: center;
}

    /* Ícono arriba */
    .card-icon { font-size: 26px; margin-bottom: 10px; }

    /* Número grande */
    .card-number {
        font-size: 36px; font-weight: 800;
        color: #ffffff; line-height: 1;
    }
    /* Barra de color */
    .card-bar {
        height: 3px; border-radius: 2px;
        margin: 10px auto 8px auto; width: 40px;
    }
    /* Etiqueta debajo — más visible */
    .card-label {
        font-size: 13px;                 /* subimos de 12px */
        color: #99aabb;                  /* aclaramos */
        text-transform: lowercase;
        letter-spacing: 1px;
        font-weight: 500;
    }

    /* Etiqueta de sección */
    .section-label {
        font-size: 12px; letter-spacing: 2px;
        color: #778899;                  /* aclaramos */
        text-transform: uppercase;
        margin-top: 28px; margin-bottom: 12px;
    }

    /* Caja de pregunta */
  /* Caja de pregunta — borde izquierdo de color */
    .pregunta {
        background-color: #1a1d27;       /* mismo fondo que conclusiones */
        border: 1px solid #1e2d40;
        border-left: 4px solid;          /* color se pone inline */
        border-radius: 8px;
        padding: 16px 18px 14px 18px;
        margin-bottom: 10px;
}
    /* Fila badge + texto */
    .pregunta-header {
        display: flex; align-items: center;
        gap: 8px; margin-bottom: 6px;
    }
    /* Badge P1, P2... */
    .badge {
        background-color: #1e3a50; color: #4a9fd4;
        font-size: 12px; font-weight: 700;  /* subimos de 11px */
        padding: 3px 7px; border-radius: 4px;
        flex-shrink: 0;
    }
    /* Texto principal de la pregunta */
    .pregunta-texto {
        font-size: 14px;                 /* subimos de 13px */
        color: #dde6f0;                  /* aclaramos */
        font-weight: 600;
    }
    /* Descripción adicional */
    .pregunta-desc {
        font-size: 13px;                 /* subimos de 12px */
        color: #889aaa;                  /* aclaramos */
        margin-left: 32px;
        line-height: 1.6;
    }

    /* Franja de fuente de datos */
    .fuente-datos {
        background-color: #0d1422;
        border: 1px solid #1e2d40;
        border-radius: 8px;
        padding: 14px 20px;
        margin-top: 20px;
        font-size: 13px; color: #778899;  /* aclaramos */
        display: flex; align-items: center; gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Hero con imagen de fondo y gradiente ---
st.markdown(f"""
<div class="hero" style="background-image: linear-gradient(
    to bottom,
    rgba(10,14,26,0.15) 0%,
    rgba(10,14,26,0.55) 65%,
    rgba(10,14,26,1.0)  100%
), url('{img_hero}');">
    <div class="sup-title">Proyecto de Análisis de Datos · 2026</div>
    <div class="main-title">Brecha Digital en Colombia</div>
    <div class="sub-desc">Análisis territorial del acceso tecnológico en hogares · 2019-2023</div>
</div>
""", unsafe_allow_html=True)

# --- Calcular métricas desde el df ---
num_datasets      = 6                             # Valor fijo
num_departamentos = df["departamento"].nunique()  # Conteo único de departamentos
num_años          = df["año"].nunique()           # Conteo único de años
num_secciones     = 16                            # Valor fijo

# --- Datos de cada tarjeta: (ícono, número, label, color de barra) ---
tarjetas = [
    ("🗂️", num_datasets,      "datasets",      "#1F92DA"),
    ("🗺️", num_departamentos, "departamentos", "#4ade80"),
    ("📅", num_años,          "años",          "#f59e0b"),
    ("📄", num_secciones,     "secciones",     "#a78bfa"),
]

# --- Renderizar tarjetas en 4 columnas ---
# --- Colores por tarjeta: mismo esquema que conclusiones ---
tarjetas = [
    ("🗂️", num_datasets,      "datasets",      "#1F92DA"),  # azul
    ("🗺️", num_departamentos, "departamentos", "#4ade80"),  # verde
    ("📅", num_años,          "años",          "#f59e0b"),  # amarillo
    ("📄", num_secciones,     "secciones",     "#a78bfa"),  # morado
]

cols = st.columns(4)
for col, (icono, numero, label, color) in zip(cols, tarjetas):
    with col:
        st.markdown(f"""
        <div class="card" style="border-left-color: {color};">
            <div class="card-icon">{icono}</div>
            <div class="card-number">{numero}</div>
            <div class="card-bar" style="background-color:{color};"></div>
            <div class="card-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# --- Preguntas de investigación ---
st.markdown('<div class="section-label">Preguntas de Investigación</div>', unsafe_allow_html=True)

# Cada pregunta: (badge, texto principal, descripción corta)
preguntas = [
    ("P1", "¿Cómo evolucionó el acceso a internet en hogares colombianos entre 2019 y 2023?",
           "Tendencia nacional y por departamento en el período analizado."),
    ("P2", "¿Qué tan grande es la brecha digital entre zonas urbanas y rurales por departamento?",
           "Comparación cabecera vs. rural disperso en acceso tecnológico."),
    ("P3", "¿Qué departamentos lideran y cuáles presentan mayor rezago digital?",
           "Ranking territorial por indicadores de conectividad."),
    ("P4", "¿El celular compensa la falta de internet fijo en zonas remotas?",
           "Relación entre telefonía móvil e internet fijo en áreas rurales."),
]

# --- Mostrar preguntas en 2 columnas ---
# Colores por pregunta: igual que P1/P2/P3/P4 en conclusiones
colores_preguntas = ["#38bdf8", "#4ade80", "#fbbf24", "#a78bfa"]  # azul, verde, amarillo, morado

col_a, col_b = st.columns(2)
for i, (badge, texto, desc) in enumerate(preguntas):
    col = col_a if i % 2 == 0 else col_b
    color = colores_preguntas[i]     # color correspondiente a cada pregunta
    with col:
        st.markdown(f"""
        <div class="pregunta" style="border-left-color: {color};">
            <div class="pregunta-header">
                <span class="badge" style="background-color:#0f1117; color:{color};">{badge}</span>
                <span class="pregunta-texto">{texto}</span>
            </div>
            <div class="pregunta-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# --- Franja de fuente de datos al fondo ---
st.markdown("""
<div class="fuente-datos">
    📦 &nbsp; <strong style="color:#99aabb;">Fuente:</strong>&nbsp;
    DANE · Encuesta de Calidad de Vida (ECV) · Microdatos anonimizados 2019, 2022 y 2023
</div>
""", unsafe_allow_html=True)




