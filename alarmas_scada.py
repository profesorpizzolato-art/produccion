import streamlit as st

def alarmas():

    st.header("Sistema de Alarmas")

    presion = st.slider("Presión Línea",100,3000,800)
    temperatura = st.slider("Temperatura",20,120,60)

    if presion > 2000:

        st.error("ALARMA: Alta presión")

    if temperatura > 100:

        st.warning("Temperatura elevada")

    if presion < 200:

        st.error("Presión baja crítica")
