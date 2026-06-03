import streamlit as st
import plotly.express as px
from data import df
from filtros import aplicar_filtros

# --- Aplicar filtros globales ---
df_filtrado = aplicar_filtros(df)

# --- Estilos visuales ---
st.markdown("""
    <style>
    .stApp { background-color: #0a0e1a; }
    .disp-titulo {
        border-left: 4px solid #4a9fd4;
        padding-left: 12px;
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        font-family: sans-serif;
        margin-bottom: 4px;
    }
    .disp-subtitulo {
        font-size: 12px;
        color: #667788;
        font-family: sans-serif;
        margin-bottom: 16px;
        padding-left: 16px;
    }
    .graf-label {
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 1.5px;
        color: #667788;
        text-transform: uppercase;
        margin-bottom: 8px;
        font-family: sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown('<div class="disp-titulo">Análisis por dispositivo</div>', unsafe_allow_html=True)
st.markdown('<div class="disp-subtitulo">Composición de equipamiento tecnológico en los hogares colombianos</div>', unsafe_allow_html=True)

# --- Selector de año ---
años_disp = sorted(df_filtrado["año"].unique().tolist())
año_sel = st.radio("Año", options=años_disp, horizontal=True, key="disp_año")

# --- Preparar datos: filtrar por año, zona TOTAL, sin TOTAL NACIONAL ---
df_disp = df_filtrado[
    (df_filtrado["año"] == año_sel) &                          # Filtro por año seleccionado
    (df_filtrado["zona"] == "TOTAL") &                         # Solo zona total
    (df_filtrado["departamento"] != "TOTAL NACIONAL")          # Sin total nacional
][["departamento", "tel_celular_proporcion", "computador_proporcion", "tv_proporcion"]].copy()

# --- Configuración de cada dispositivo ---
dispositivos = [
    {"label": "% Hogares con Celular",    "col": "tel_celular_proporcion", "color": "#4a9fd4", "key": "disp_celular"},
    {"label": "% Hogares con Computador", "col": "computador_proporcion",  "color": "#2ecc71", "key": "disp_computador"},
    {"label": "% Hogares con TV",         "col": "tv_proporcion",          "color": "#f5a623", "key": "disp_tv"},
]

# --- Layout tres columnas ---
cols = st.columns(3)

for i, disp in enumerate(dispositivos):
    with cols[i]:
        st.markdown(f'<div class="graf-label">{disp["label"]}</div>', unsafe_allow_html=True)

        # Ordenar de mayor a menor
        df_sorted = df_disp[["departamento", disp["col"]]].sort_values(
            disp["col"], ascending=True
        ).dropna()

        # Rango dinámico desde el mínimo valor
        val_min = max(0, df_sorted[disp["col"]].min() - 5)
        val_max = min(100, df_sorted[disp["col"]].max() + 2)

        fig = px.bar(
            df_sorted,
            x=disp["col"],
            y="departamento",
            orientation="h",
            color_discrete_sequence=[disp["color"]],
            labels={disp["col"]: "%", "departamento": ""}
        )
        fig.update_layout(
            plot_bgcolor="#111827",
            paper_bgcolor="#111827",
            font_color="#aabbcc",
            height=550,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(
                showgrid=True,
                gridcolor="#1e2d40",
                color="#445566",
                range=[val_min, val_max]  # Rango dinámico
            ),
            yaxis=dict(showgrid=False, color="#445566", tickfont=dict(size=8))
        )
        st.plotly_chart(fig, use_container_width=True, key=disp["key"])