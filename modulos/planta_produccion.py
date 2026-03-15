import streamlit as st
import numpy as np
import time

def planta_produccion():

    st.title("SCADA Planta de Producción")
    st.subheader("Simulador Operativo MENFA")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    presion_pozo = st.slider("Presión Pozo (psi)",500,5000,2500)
    temperatura = st.slider("Temperatura Fluido (°C)",20,120,60)
    caudal = st.slider("Caudal Producción (BPD)",100,5000,1200)

    st.markdown("---")

    st.subheader("Flujo del Sistema")

    st.info("Pozo → Flowline → Manifold → Separador → Tanques")

    colA, colB, colC, colD = st.columns(4)

    colA.metric("Presión Pozo",f"{presion_pozo} psi")
    colB.metric("Temperatura",f"{temperatura} °C")
    colC.metric("Caudal",f"{caudal} BPD")

    nivel_tanque = caudal * 0.8

    colD.metric("Nivel Tanque",f"{round(nivel_tanque)} bbl")

    st.markdown("---")

    st.subheader("Estado de Equipos")

    colE, colF, colG = st.columns(3)

    if presion_pozo > 4000:
        colE.error("Alta presión en pozo")
    else:
        colE.success("Presión normal")

    if temperatura > 100:
        colF.warning("Alta temperatura")
    else:
        colF.success("Temperatura normal")

    if caudal < 300:
        colG.warning("Producción baja")
    else:
        colG.success("Producción estable")
