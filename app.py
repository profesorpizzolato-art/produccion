import streamlit as st

from modulos.dashboard_principal import dashboard_principal
from modulos.pozo_productor import pozo_productor
from modulos.planta_produccion import planta_produccion
from modulos.diagrama_planta import diagrama_planta
from modulos.formulas_produccion import formulas_produccion
from modulos.ipr_vlp import ipr_vlp
from modulos.instrucciones_simulador import instrucciones_simulador
from modulos.entrenamiento_operativo import entrenamiento_operativo
from modulos.campo_petrolero import campo_petrolero
from modulos.mapa_campo import mapa_campo
st.set_page_config(
    page_title="Simulador MENFA",
    layout="wide"
)

if "modulo" not in st.session_state:
    st.session_state.modulo = "dashboard"

if st.session_state.modulo == "dashboard":

    dashboard_principal()

elif st.session_state.modulo == "pozo":

    if st.button("⬅ Volver"):
        st.session_state.modulo = "dashboard"

    pozo_productor()

elif st.session_state.modulo == "planta":

    if st.button("⬅ Volver"):
        st.session_state.modulo = "dashboard"

    planta_produccion()

elif st.session_state.modulo == "diagrama":

    if st.button("⬅ Volver"):
        st.session_state.modulo = "dashboard"

    diagrama_planta()

elif st.session_state.modulo == "formulas":

    if st.button("⬅ Volver"):
        st.session_state.modulo = "dashboard"

    formulas_produccion()

elif st.session_state.modulo == "ipr":

    if st.button("⬅ Volver"):
        st.session_state.modulo = "dashboard"

    ipr_vlp()
elif st.session_state.modulo == "manual":

    if st.button("⬅ Volver"):
        st.session_state.modulo = "dashboard"
elif st.session_state.modulo == "entrenamiento":

    if st.button("⬅ Volver"):
        st.session_state.modulo = "dashboard"

    entrenamiento_operativo()  
elif st.session_state.modulo == "campo":

    if st.button("⬅ Volver"):
        st.session_state.modulo = "dashboard"

    campo_petrolero()    
from modulos.mapa_campo import mapa_campo
