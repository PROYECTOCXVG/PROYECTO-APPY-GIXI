import pandas as pd
import streamlit as st

def aplicar_filtros(df):
    """Muestra filtros en el sidebar y retorna el df filtrado"""

    with st.sidebar:

        # --- Filtros globales ---
        st.markdown("**Filtros globales**")

        # Filtro de año
        años_disponibles = sorted(df["año"].unique().tolist())
        años_seleccionados = st.multiselect(
            label="Año",
            options=años_disponibles,
            default=años_disponibles,
        )

        # Filtro de zona
        zonas_disponibles = {
            "Urbano": "CABECERA",
            "Rural":    "CENTROS POBLADOS Y RURAL DISPERSO",
            "Total":    "TOTAL",
        }
        zonas_seleccionadas = st.multiselect(
            label="Zona",
            options=list(zonas_disponibles.keys()),
            default=list(zonas_disponibles.keys()),
        )

        # Filtro de departamento
        deptos = sorted(df["departamento"].unique().tolist())
        depto_seleccionado = st.selectbox(
            label="Departamento",
            options=["Todos"] + deptos,
        )

        st.divider()

    # --- Aplicar filtros al df ---
    valores_zonas = [zonas_disponibles[z] for z in zonas_seleccionadas]
    df_filtrado = df[df["año"].isin(años_seleccionados if años_seleccionados else años_disponibles)]
    df_filtrado = df_filtrado[df_filtrado["zona"].isin(valores_zonas if valores_zonas else list(zonas_disponibles.values()))]
    if depto_seleccionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["departamento"] == depto_seleccionado]

    return df_filtrado