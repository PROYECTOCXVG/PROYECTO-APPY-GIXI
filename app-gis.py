
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Brecha Digital", layout="wide")

with st.sidebar:
    # --- Encabezado del proyecto ---
    st.markdown("### Brecha Digital")
    st.caption("Colombia · 2019–2023")
    st.divider()

# Estilos visuales del sidebar
st.markdown("""
    <style>
    /* Fondo blanco del sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }
    /* Título Brecha Digital */
    .sidebar-title {
        font-size: 18px;
        font-weight: 700;
        color: #111111;
        font-family: sans-serif;
        margin-bottom: 2px;
    }
    /* Subtítulo Colombia 2019-2023 */
    .sidebar-subtitle {
        font-size: 12px;
        color: #999999;
        font-family: sans-serif;
        margin-bottom: 20px;
    }
    /* Línea decorativa separadora */
    .sidebar-divider {
        border: none;
        border-top: 1px solid #e0e0e0;
        margin: 8px 0 12px 0;
    }
    /* Color gris medio de las opciones del menú */
    [data-testid="stSidebarNav"] span {
        color: #666666 !important;
        font-size: 14px;
        font-family: sans-serif;
    }
    /* Etiquetas de sección (Contexto, Análisis, Resultados) */
    [data-testid="stSidebarNav"] > div > p {
        font-size: 11px !important;
        font-weight: 600 !important;
        color: #aaaaaa !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        font-family: sans-serif !important;
    /* Oculta el contenido del sidebar que va abajo */
    [data-testid="stSidebarUserContent"] {
        display: none;
    }
    /* Agrega el título arriba del menú con CSS */
    [data-testid="stSidebarNav"]::before {
        content: "Brecha Digital";
        display: block;
        font-size: 18px;
        font-weight: 700;
        color: #111111;
        font-family: sans-serif;
        padding: 20px 16px 2px 16px;
    }
    [data-testid="stSidebarNav"]::after {
        content: "Colombia · 2019–2023";
        display: block;
        font-size: 12px;
        color: #999999;
        font-family: sans-serif;
        padding: 0 16px 16px 16px;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 8px;
    /* Muestra todas las páginas del menú sin cortar */
    [data-testid="stSidebarNav"] ul 
        max-height: none !important;
        overflow: visible !important;
    /* Oculta el botón View less / View more */
    [data-testid="stSidebarNavItems"] ~ div {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Menú de navegación completo

pagina = st.navigation({
    "Contexto": [
        st.Page("pages/inicio.py",        title="Inicio",           icon="🏠"),
        st.Page("pages/enfoque.py",        title="Enfoque",          icon="🎯"),
        st.Page("pages/objetivo.py",       title="Objetivo",         icon="📋"),
        st.Page("pages/metodologia.py",    title="Metodología",      icon="📊"),
    ],
    "Análisis": [
        st.Page("pages/dashboard.py",      title="Dashboard",        icon="🗂️"),
        st.Page("pages/mapa.py",           title="Mapa coroplético", icon="🗺️"),
        st.Page("pages/evolucion.py",      title="Evolución",        icon="📈"),
        st.Page("pages/urbano_rural.py",   title="Urbano / rural",   icon="🏘️"),
        st.Page("pages/comparador.py",     title="Comparador",       icon="⚖️"),
        st.Page("pages/dispositivos.py",   title="Dispositivos",     icon="📱"),
        st.Page("pages/internet.py",       title="Internet",         icon="🌐"),
        st.Page("pages/datos_descarga.py", title="Datos y descarga", icon="📦"),
    ],
    "Resultados": [
        st.Page("pages/hallazgos.py",      title="Hallazgos",        icon="🔍"),
        st.Page("pages/conclusiones.py",   title="Conclusiones",     icon="✅"),
        st.Page("pages/informe_final.py",  title="Informe final",    icon="📄"),
        st.Page("pages/integrantes.py",    title="Integrantes",      icon="👥"),
    ],
})


pagina.run()