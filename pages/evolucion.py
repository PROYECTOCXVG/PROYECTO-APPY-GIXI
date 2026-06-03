import streamlit as st
import plotly.express as px
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import df
from filtros import aplicar_filtros

# --- Aplicar filtros globales ---
df_filtrado = aplicar_filtros(df)

# Renombrar zonas para mejor lectura
df_filtrado["zona"] = df_filtrado["zona"].replace({
    "CABECERA": "Urbano",
    "CENTROS POBLADOS Y RURAL DISPERSO": "Rural"
})

# --- Estilos visuales ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    /* Fondo oscuro general */
    .stApp { background-color: #0a0e1a; font-family: 'Inter', sans-serif; }

    /* Título con barra azul izquierda */
    .evol-titulo {
        border-left: 4px solid #4a9fd4;
        padding-left: 12px;
        font-size: 22px; font-weight: 700;
        color: #ffffff; margin-bottom: 4px;
    }
    /* Subtítulo gris */
    .evol-subtitulo {
        font-size: 12px; color: #667788;
        margin-bottom: 20px; padding-left: 16px;
    }
    /* Etiqueta de sección para gráficas */
    .graf-label {
        font-size: 10px; font-weight: 600;
        letter-spacing: 1.5px; color: #667788;
        text-transform: uppercase; margin-bottom: 8px;
    }
    /* Franja de cierre */
    .franja-cierre {
        background-color: #0d1422;
        border: 1px solid #1e2d40;
        border-radius: 8px;
        padding: 12px 20px;
        margin-top: 16px;
        font-size: 11px; color: #445566;
    }
    </style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown('<div class="evol-titulo">Evolución temporal 2019–2023</div>', unsafe_allow_html=True)
st.markdown('<div class="evol-subtitulo">Series de tiempo por departamento y zona · animación por año</div>', unsafe_allow_html=True)

# --- Preparar datos: quitar TOTAL NACIONAL ---
# Usa df completo para evolución, no el filtrado por sidebar
df_evol = df[df["departamento"] != "TOTAL NACIONAL"].copy()
# Renombrar zonas para mejor lectura
df_evol["zona"] = df_evol["zona"].replace({
    "CABECERA": "Urbano",
    "CENTROS POBLADOS Y RURAL DISPERSO": "Rural"
})

df_evol["año"] = df_evol["año"].astype(int)  # evita decimales en eje X

# --- Controles en una fila ---
col_ctrl1, col_ctrl2 = st.columns([1, 2])

with col_ctrl1:
    # Opciones fijas para no depender del sidebar ni del df filtrado
    zona_sel = st.selectbox(
        "Zona",
        options=["Urbano", "Rural", "TOTAL"],
        key="evol_zona"
    )

with col_ctrl2:
    # Selector de departamentos — por defecto muestra los primeros 6
    deptos_disp = sorted(df_evol["departamento"].unique().tolist())
    deptos_sel = st.multiselect(
        "Departamentos",
        options=deptos_disp,
        default=deptos_disp[:6],
        key="evol_deptos"
    )

# --- Lista efectiva de departamentos (si no selecciona ninguno usa todos) ---
deptos_activos = deptos_sel if deptos_sel else deptos_disp

# --- Filtrar por zona y departamentos seleccionados ---
df_lineas = df_evol[
    (df_evol["zona"] == zona_sel) &
    (df_evol["departamento"].isin(deptos_activos))
].groupby(["año", "departamento"])["internet_proporcion"].mean().reset_index()

# Renombrar columnas para etiquetas legibles en el gráfico
df_lineas.columns = ["Año", "Departamento", "% Internet"]

# --- Layout: gráfica principal izquierda + barras derecha ---
col_main, col_right = st.columns([2.5, 1])

with col_main:
    st.markdown('<div class="graf-label">Líneas de tiempo · departamentos seleccionados</div>', unsafe_allow_html=True)

    fig_lineas = px.line(
        df_lineas, x="Año", y="% Internet",
        color="Departamento",
        markers=True,
        labels={"% Internet": "% Internet", "Año": "Año"}
    )
    fig_lineas.update_layout(
        plot_bgcolor="#111827", paper_bgcolor="#111827",
        font_color="#aabbcc", height=420,
        xaxis=dict(
            showgrid=False, color="#445566",
            tickmode="array",                        # solo muestra los años exactos
            tickvals=[2019, 2022, 2023],
            ticktext=["2019", "2022", "2023"]
        ),
        yaxis=dict(showgrid=True, gridcolor="#1e2d40",
                   color="#445566", range=[0, 100]),  # eje Y desde 0
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(bgcolor="#111827", font=dict(color="#aabbcc"), title_text="")
    )
    st.plotly_chart(fig_lineas, use_container_width=True, key="evol_lineas")

with col_right:
    # --- Calcular cambio 2019-2023 SOLO para departamentos seleccionados ---
    df_2019 = df_evol[
        (df_evol["año"] == 2019) &
        (df_evol["zona"] == zona_sel) &
        (df_evol["departamento"].isin(deptos_activos))   # filtra por selección
    ].groupby("departamento")["internet_proporcion"].mean()

    df_2023 = df_evol[
        (df_evol["año"] == 2023) &
        (df_evol["zona"] == zona_sel) &
        (df_evol["departamento"].isin(deptos_activos))   # filtra por selección
    ].groupby("departamento")["internet_proporcion"].mean()

    # --- Gráfica cambio en puntos porcentuales ---
    st.markdown('<div class="graf-label">Cambio 2019–2023 (pp)</div>', unsafe_allow_html=True)

    df_cambio = pd.DataFrame({
        "Cambio (pp)": df_2023 - df_2019
    }).dropna().sort_values("Cambio (pp)", ascending=True).reset_index()
    df_cambio.columns = ["Departamento", "Cambio (pp)"]

    fig_cambio = px.bar(
        df_cambio, x="Cambio (pp)", y="Departamento",
        orientation="h",
        color="Cambio (pp)",
        color_continuous_scale=["#e05252", "#4a9fd4"],  # rojo negativo, azul positivo
        labels={"Cambio (pp)": "pp", "Departamento": ""}
    )
    fig_cambio.update_layout(
        plot_bgcolor="#111827", paper_bgcolor="#111827",
        font_color="#aabbcc", height=280,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False, coloraxis_showscale=False,
        xaxis=dict(showgrid=True, gridcolor="#1e2d40", color="#445566"),
        yaxis=dict(showgrid=False, color="#445566", tickfont=dict(size=9))
    )
    st.plotly_chart(fig_cambio, use_container_width=True, key="evol_cambio")

    # --- Gráfica tasa de crecimiento porcentual ---
    st.markdown('<div class="graf-label">Tasa de crecimiento</div>', unsafe_allow_html=True)

    df_tasa = pd.DataFrame({
        "Crecimiento (%)": ((df_2023 - df_2019) / df_2019 * 100)  # % de crecimiento relativo
    }).dropna().sort_values("Crecimiento (%)", ascending=True).reset_index()
    df_tasa.columns = ["Departamento", "Crecimiento (%)"]

    fig_tasa = px.bar(
        df_tasa, x="Crecimiento (%)", y="Departamento",
        orientation="h",
        color="Crecimiento (%)",
        color_continuous_scale=["#e05252", "#4a9fd4"],
        labels={"Crecimiento (%)": "% crecimiento", "Departamento": ""}
    )
    fig_tasa.update_layout(
        plot_bgcolor="#111827", paper_bgcolor="#111827",
        font_color="#aabbcc", height=280,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False, coloraxis_showscale=False,
        xaxis=dict(showgrid=True, gridcolor="#1e2d40", color="#445566"),
        yaxis=dict(showgrid=False, color="#445566", tickfont=dict(size=9))
    )
    st.plotly_chart(fig_tasa, use_container_width=True, key="evol_tasa")

# --- Franja de cierre dinámica ---
st.markdown(f"""
<div class="franja-cierre">
    📈 &nbsp; Mostrando <strong style="color:#667788;">{len(deptos_activos)} departamentos</strong> ·
    Zona <strong style="color:#667788;">{zona_sel}</strong> ·
    Período <strong style="color:#667788;">2019–2023</strong>
</div>
""", unsafe_allow_html=True)


    