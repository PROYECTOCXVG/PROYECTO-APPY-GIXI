import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data import df
from filtros import aplicar_filtros

# --- Aplicar filtros globales ---
df_filtrado = aplicar_filtros(df)

# --- Estilos visuales ---
st.markdown("""
    <style>
    .stApp { background-color: #0a0e1a; }
    .comp-titulo {
        border-left: 4px solid #4a9fd4;
        padding-left: 12px;
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        font-family: sans-serif;
        margin-bottom: 4px;
    }
    .comp-subtitulo {
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
st.markdown('<div class="comp-titulo">Comparador de departamentos</div>', unsafe_allow_html=True)
st.markdown('<div class="comp-subtitulo">Selecciona 2 o 3 departamentos y compáralos en todas las variables</div>', unsafe_allow_html=True)

# --- Variables del radar ---
variables = {
    "Internet":    "internet_proporcion",
    "Celular":     "tel_celular_proporcion",
    "Computador":  "computador_proporcion",
    "TV":          "tv_proporcion",
    "Smartphone":  "smartphone_proporcion",
}

# --- Selector de departamentos ---
deptos_disp = sorted(df_filtrado[
    df_filtrado["departamento"] != "TOTAL NACIONAL"
]["departamento"].unique().tolist())

deptos_sel = st.multiselect(
    "Seleccionar departamentos",
    options=deptos_disp,
    default=["BOGOTÁ D.C.", "VAUPÉS"],
    max_selections=3,  # Máximo 3 departamentos
    key="comp_deptos"
)

if not deptos_sel:
    st.warning("Selecciona al menos un departamento.")
    st.stop()

# --- Preparar datos: promedio por departamento zona TOTAL ---
df_comp = df_filtrado[
    (df_filtrado["departamento"].isin(deptos_sel)) &
    (df_filtrado["zona"] == "TOTAL")
].groupby("departamento")[list(variables.values())].mean().reset_index()

# Normalizar columnas decimales a porcentaje
for col in variables.values():
    if df_comp[col].mean() < 2:
        df_comp[col] = df_comp[col] * 100

# --- Layout dos columnas ---
col1, col2 = st.columns(2)

# Colores por departamento
colores = ["#4a9fd4", "#f5a623", "#2ecc71"]

with col1:
    st.markdown('<div class="graf-label">Radar · todas las variables</div>', unsafe_allow_html=True)

    fig_radar = go.Figure()

    for i, row in df_comp.iterrows():
        valores = [row[v] for v in variables.values()]
        valores += [valores[0]]  # Cerrar el radar

        fig_radar.add_trace(go.Scatterpolar(
            r=valores,
            theta=list(variables.keys()) + [list(variables.keys())[0]],
            fill="toself",
            name=row["departamento"],
            line_color=colores[i % len(colores)],
            fillcolor=colores[i % len(colores)],
            opacity=0.3
        ))

    fig_radar.update_layout(
        polar=dict(
            bgcolor="#111827",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                color="#445566",
                gridcolor="#1e2d40"
            ),
            angularaxis=dict(color="#aabbcc")
        ),
        plot_bgcolor="#111827",
        paper_bgcolor="#111827",
        font_color="#aabbcc",
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(bgcolor="#111827", font=dict(color="#aabbcc"))
    )
    st.plotly_chart(fig_radar, use_container_width=True, key="comp_radar")

with col2:
    st.markdown('<div class="graf-label">Evolución comparada 2019–2023</div>', unsafe_allow_html=True)

    # Líneas de evolución por departamento
    df_evol = df_filtrado[
        (df_filtrado["departamento"].isin(deptos_sel)) &
        (df_filtrado["zona"] == "TOTAL")
    ].groupby(["año", "departamento"])["internet_proporcion"].mean().reset_index()
    df_evol["año"] = df_evol["año"].astype(int)

    fig_evol = px.line(
        df_evol, x="año", y="internet_proporcion",
        color="departamento",
        markers=True,
        color_discrete_sequence=colores,
        labels={"internet_proporcion": "% Internet", "año": "Año", "departamento": "Departamento"}
    )
    fig_evol.update_layout(
        plot_bgcolor="#111827",
        paper_bgcolor="#111827",
        font_color="#aabbcc",
        height=400,
        xaxis=dict(
            showgrid=False,
            color="#445566",
            tickmode="array",
            tickvals=[2019, 2022, 2023],
            ticktext=["2019", "2022", "2023"]
        ),
        yaxis=dict(showgrid=True, gridcolor="#1e2d40", color="#445566"),
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(bgcolor="#111827", font=dict(color="#aabbcc"), title_text="")
    )
    st.plotly_chart(fig_evol, use_container_width=True, key="comp_evol")