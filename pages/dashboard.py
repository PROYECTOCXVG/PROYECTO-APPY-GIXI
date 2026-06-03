import streamlit as st
import plotly.express as px
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import df
from filtros import aplicar_filtros

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
    .dash-titulo {
        border-left: 4px solid #4a9fd4;
        padding-left: 12px;
        font-size: 22px; font-weight: 700;
        color: #ffffff; margin-bottom: 4px;
    }
    /* Subtítulo gris */
    .dash-subtitulo {
        font-size: 12px; color: #667788;
        margin-bottom: 24px; padding-left: 16px;
    }

    /* Tarjeta KPI */
    .kpi-card {
        background-color: #111827;
        border: 1px solid #1e2d40;
        border-radius: 10px;
        padding: 18px 20px;
        font-family: 'Inter', sans-serif;
    }
    /* Ícono arriba del KPI */
    .kpi-icon  { font-size: 20px; margin-bottom: 8px; }
    /* Etiqueta pequeña */
    .kpi-label {
        font-size: 10px; color: #667788;
        text-transform: uppercase; letter-spacing: 1px;
        margin-bottom: 6px;
    }
    /* Valor principal */
    .kpi-valor { font-size: 28px; font-weight: 800; color: #ffffff; }
    /* Valor más pequeño para textos largos como nombres de departamento */
    .kpi-valor-sm { font-size: 18px; font-weight: 800; color: #ffffff; }
    /* Barra de color bajo el valor */
    .kpi-bar {
        height: 3px; border-radius: 2px;
        margin: 8px 0 6px 0; width: 40px;
    }
    /* Subtexto positivo azul */
    .kpi-sub     { font-size: 11px; color: #4a9fd4; }
    /* Subtexto negativo rojo */
    .kpi-sub-red { font-size: 11px; color: #e05252; }

    /* Etiqueta de sección para gráficas */
    .grafica-label {
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
        margin-top: 8px;
        font-size: 11px; color: #445566;
    }
    </style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown('<div class="dash-titulo">Dashboard interactivo</div>', unsafe_allow_html=True)
st.markdown('<div class="dash-subtitulo">KPIs y gráficas principales · responde a los filtros globales</div>', unsafe_allow_html=True)

# --- Calcular KPIs desde df filtrado ---

# KPI 1: % promedio de hogares con internet (zona TOTAL si existe)
df_kpi = df_filtrado[df_filtrado["zona"] == "TOTAL"] if "TOTAL" in df_filtrado["zona"].values else df_filtrado
internet_prom = df_kpi["internet_proporcion"].mean()

# Variación respecto a 2019 (sobre df completo sin filtrar año)
internet_2019 = df[df["año"] == 2019]["internet_proporcion"].mean()
variacion = internet_prom - internet_2019

# KPI 2: Brecha urbano-rural en puntos porcentuales
cab   = df_filtrado[df_filtrado["zona"] == "Urbano"]["internet_proporcion"].mean()
rural = df_filtrado[df_filtrado["zona"] == "Rural"]["internet_proporcion"].mean()
brecha = cab - rural

# KPI 3 y 4: Depto con mayor acceso y mayor rezago (zona TOTAL)
df_depto = df_filtrado[df_filtrado["zona"] == "TOTAL"] if "TOTAL" in df_filtrado["zona"].values else df_filtrado
mayor_acceso = df_depto.groupby("departamento")["internet_proporcion"].mean().idxmax()
mayor_rezago  = df_depto.groupby("departamento")["internet_proporcion"].mean().idxmin()

# --- Datos de cada KPI: (ícono, label, valor, barra color, subtexto, clase subtexto) ---
kpis = [
    ("🌐", "Hogares con internet",
     f"{internet_prom:.1f}%", "#4a9fd4",
     f"↑ {variacion:.1f} pp vs 2019", "kpi-sub"),

    ("📊", "Brecha urbano–rural",
     f"{brecha:.1f} pp", "#f59e0b",
     "puntos porcentuales", "kpi-sub"),

    ("🏆", "Mayor acceso",
     mayor_acceso, "#4ade80",
     "internet hogares", "kpi-sub"),

    ("⚠️", "Mayor rezago",
     mayor_rezago, "#d44f4a",
     "internet hogares", "kpi-sub-red"),
]

# --- Renderizar KPIs en 4 columnas ---
cols = st.columns(4)
for col, (icono, label, valor, color, sub, sub_class) in zip(cols, kpis):
    # Usa tamaño pequeño si el valor es texto largo (nombre de departamento)
    valor_class = "kpi-valor-sm" if len(str(valor)) > 6 else "kpi-valor"
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icono}</div>
            <div class="kpi-label">{label}</div>
            <div class="{valor_class}">{valor}</div>
            <div class="kpi-bar" style="background-color:{color};"></div>
            <div class="{sub_class}">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Gráficas ---
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown('<div class="grafica-label">Evolución nacional · % hogares con internet</div>', unsafe_allow_html=True)

    # Agrupa por año zona TOTAL para línea de evolución
    df_evol = df_filtrado[df_filtrado["zona"] == "TOTAL"].groupby("año")["internet_proporcion"].mean().reset_index()
    df_evol.columns = ["Año", "% Hogares con internet"]   # renombra ejes para que se vean legibles

    fig1 = px.line(
        df_evol, x="Año", y="% Hogares con internet",
        markers=True,
        color_discrete_sequence=["#4a9fd4"]
    )
    fig1.update_layout(
        plot_bgcolor="#111827", paper_bgcolor="#111827",
        font_color="#aabbcc",
        xaxis=dict(showgrid=False, color="#445566"),
        yaxis=dict(showgrid=True, gridcolor="#1e2d40",
                   color="#445566", range=[0, 100]),  # eje Y desde 0 para no exagerar crecimiento
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False
    )
    fig1.update_traces(line_width=2.5)
    st.plotly_chart(fig1, use_container_width=True)

with col_g2:
    st.markdown('<div class="grafica-label">Brecha urbano / rural por año</div>', unsafe_allow_html=True)

    # Filtra cabecera y rural, agrupa por año y zona
    df_brecha = df_filtrado[df_filtrado["zona"].isin(["Urbano", "Rural"])]
    df_brecha = df_brecha.groupby(["año", "zona"])["internet_proporcion"].mean().reset_index()

    # Renombra valores y columnas para etiquetas legibles en el gráfico
    df_brecha["zona"] = df_brecha["zona"].replace({
        "CABECERA": "Urbano",
        "CENTROS POBLADOS Y RURAL DISPERSO": "Rural"
    })
    df_brecha.columns = ["Año", "Zona", "% Hogares con internet"]

    fig2 = px.bar(
        df_brecha, x="Año", y="% Hogares con internet",
        color="Zona", barmode="group",
        color_discrete_map={"Urbano": "#4a9fd4", "Rural": "#f59e0b"}
    )
    fig2.update_layout(
        plot_bgcolor="#111827", paper_bgcolor="#111827",
        font_color="#aabbcc",
        xaxis=dict(showgrid=False, color="#445566"),
        yaxis=dict(showgrid=True, gridcolor="#1e2d40",
                   color="#445566", range=[0, 100]),  # eje Y desde 0
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(bgcolor="#111827", font_color="#aabbcc")
    )
    st.plotly_chart(fig2, use_container_width=True)

# --- Franja de cierre ---
st.markdown("""
<div class="franja-cierre">
    📊 &nbsp; Los KPIs y gráficas responden a los <strong style="color:#667788;">filtros globales</strong>
    del sidebar · Año · Zona · Departamento
</div>
""", unsafe_allow_html=True)
