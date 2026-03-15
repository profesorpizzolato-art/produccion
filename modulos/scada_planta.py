import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def scada_planta():

    st.title("SCADA Planta de Producción")
    st.subheader("IPCL MENFA - Flujo del proceso")

    st.markdown("### Controles Operativos")

    col1, col2, col3 = st.columns(3)

    with col1:
        presion_pozo = st.slider("Presión Pozo (psi)", 500, 3000, 1200)

    with col2:
        apertura_choke = st.slider("Apertura Choke (%)", 0, 100, 40)

    with col3:
        nivel_tanque = st.slider("Nivel Tanque (%)", 0, 100, 55)

    st.markdown("---")

    # Cálculos simples de proceso
    caudal = apertura_choke * 12
    presion_linea = presion_pozo * 0.7
    eficiencia_separador = 85 + np.random.randint(-5,5)

    st.markdown("## Diagrama del proceso")

    colA, colB, colC, colD = st.columns(4)

    with colA:
        st.metric("Pozo", f"{presion_pozo} psi")

    with colB:
        st.metric("Línea Flujo", f"{round(presion_linea)} psi")

    with colC:
        st.metric("Separador", f"{eficiencia_separador}% eficiencia")

    with colD:
        st.metric("Tanque", f"{nivel_tanque}% nivel")

    st.markdown("---")

    st.subheader("Producción estimada")

    colX, colY, colZ = st.columns(3)

    petroleo = caudal
    gas = caudal * 3
    agua = caudal * 0.25

    colX.metric("Petróleo BPD", round(petroleo))
    colY.metric("Gas m3/d", round(gas))
    colZ.metric("Agua BPD", round(agua))

    st.markdown("---")

    st.subheader("Tendencia de Producción")

    tiempo = np.arange(0,50)
    produccion = petroleo - tiempo*0.8 + np.random.normal(0,3,50)

    fig, ax = plt.subplots()

    ax.plot(tiempo,produccion)
    ax.set_title("Declinación de producción")

    st.pyplot(fig)

    st.markdown("---")

    st.subheader("Alarmas del sistema")

    if presion_pozo > 2500:
        st.error("Alta presión en pozo")

    if nivel_tanque > 90:
        st.warning("Nivel alto en tanque")

    if apertura_choke > 85:
        st.warning("Choke muy abierto")
