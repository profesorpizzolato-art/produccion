import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def panel_operador():

    st.title("Panel del Operador")
    st.subheader("IPCL MENFA - Simulador de Producción")

    st.sidebar.header("Controles del Pozo")

    presion_tubing = st.sidebar.slider("Presión Tubing (psi)",100,3000,900)
    presion_casing = st.sidebar.slider("Presión Casing (psi)",100,3000,700)

    choke = st.sidebar.slider("Apertura Choke (%)",0,100,40)

    petroleo = choke * 15
    gas = choke * 60
    agua = choke * 5

    estado_pozo = "Produciendo"

    if choke == 0:
        estado_pozo = "Cerrado"

    if presion_tubing > 2500:
        estado_pozo = "Alta Presión"

    st.markdown("## Indicadores del Pozo")

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Presión Tubing",presion_tubing)
    col2.metric("Presión Casing",presion_casing)
    col3.metric("Apertura Choke",f"{choke}%")
    col4.metric("Estado del Pozo",estado_pozo)

    st.markdown("## Producción")

    col5,col6,col7 = st.columns(3)

    col5.metric("Petróleo (BPD)",petroleo)
    col6.metric("Gas (m3/d)",gas)
    col7.metric("Agua (BPD)",agua)

    st.markdown("## Tendencia de Producción")

    tiempo = np.arange(0,50)

    produccion = petroleo - tiempo*0.5 + np.random.normal(0,5,50)

    fig, ax = plt.subplots()

    ax.plot(tiempo,produccion)

    ax.set_title("Tendencia de Producción")

    ax.set_xlabel("Tiempo")

    ax.set_ylabel("Producción")

    st.pyplot(fig)

    st.markdown("## Alarmas Operativas")

    if presion_tubing > 2000:
        st.error("ALARMA: Alta presión en tubing")

    if presion_casing > 2000:
        st.warning("Advertencia: presión casing elevada")

    if choke > 85:
        st.warning("Choke muy abierto")

    if choke < 10 and choke > 0:
        st.warning("Producción restringida")
