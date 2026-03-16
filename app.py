import streamlit as st
import base64

# IMPORTAR MODULOS EXISTENTES

from modulos.dashboard_principal import dashboard_principal
from modulos.pozo_productor import pozo_productor
from modulos.mapa_campo import mapa_campo
from modulos.campo_petrolero import campo_petrolero
from modulos.formulas_produccion import formulas_produccion
from modulos.entrenamiento_operativo import entrenamiento_operativo
from modulos.instrucciones_simulador import instrucciones_simulador


# CONFIGURACION DE PAGINA

st.set_page_config(
    page_title="IPCL MENFA - Producción",
    layout="wide"
)


# FONDO MENFA

def fondo_app():
def estilo_menfa():

    st.markdown("""
    <style>

    h1 {
        color: #0E4C92;
        font-weight: 700;
    }

    h2 {
        color: #0E4C92;
    }

    h3 {
        color: #1A1A1A;
    }

    .stMetric {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
    }

    div.stButton > button {
        background-color: #0E4C92;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 55px;
    }

    div.stButton > button:hover {
        background-color: #1565C0;
        color: white;
    }

    </style>
    """, unsafe_allow_html=True)
def estilo_menfa():

    st.markdown("""
    <style>

    h1 {
        color: #0E4C92;
        font-weight: 700;
    }

    h2 {
        color: #0E4C92;
    }

    h3 {
        color: #1A1A1A;
    }

    .stMetric {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
    }

    div.stButton > button {
        background-color: #0E4C92;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 55px;
    }

    div.stButton > button:hover {
        background-color: #1565C0;
        color: white;
    }

    </style>
    """, unsafe_allow_html=True)
    try:
        with open("assets/logo_menfa.png", "rb") as img:
            encoded = base64.b64encode(img.read()).decode()

        fondo = f"""
        <style>

        .stApp {{
            background-image: linear-gradient(
                rgba(255,255,255,0.90),
                rgba(255,255,255,0.90)
            ),
            url("data:image/png;base64,{encoded}");
            
            background-size: 45%;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        </style>
        """

        st.markdown(fondo, unsafe_allow_html=True)

    except:
        pass
# ESTADO DE MODULOS

if "modulo" not in st.session_state:
    st.session_state.modulo = "dashboard"


# CABECERA

col1, col2 = st.columns([8,2])

with col1:
    st.title("IPCL MENFA - Simulador de Producción")

with col2:
    if st.button("🏠 Inicio"):
        st.session_state.modulo = "dashboard"


st.markdown("---")


# CONTROL DE MODULOS

if st.session_state.modulo == "dashboard":

    dashboard_principal()


elif st.session_state.modulo == "pozo":

    if st.button("⬅ Volver"):
        st.session_state.modulo = "dashboard"

    pozo_productor()


elif st.session_state.modulo == "mapa":

    if st.button("⬅ Volver"):
        st.session_state.modulo = "dashboard"

    mapa_campo()


elif st.session_state.modulo == "campo":

    if st.button("⬅ Volver"):
        st.session_state.modulo = "dashboard"

    campo_petrolero()


elif st.session_state.modulo == "formulas":

    if st.button("⬅ Volver"):
        st.session_state.modulo = "dashboard"

    formulas_produccion()


elif st.session_state.modulo == "entrenamiento":

    if st.button("⬅ Volver"):
        st.session_state.modulo = "dashboard"

    entrenamiento_operativo()


elif st.session_state.modulo == "manual":

    if st.button("⬅ Volver"):
        st.session_state.modulo = "dashboard"

    instrucciones_simulador()


# PIE DE PAGINA

st.markdown("---")

st.caption("MENFA | Simulador de Producción Petrolera | Plataforma de entrenamiento")
