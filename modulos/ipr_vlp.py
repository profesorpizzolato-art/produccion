import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def ipr_vlp():

    st.title("Análisis IPR - VLP")
    st.subheader("Simulador MENFA - Ingeniería de Producción")

    st.markdown("### Parámetros del reservorio")

    col1, col2, col3 = st.columns(3)

    with col1:
        pr = st.slider("Presión reservorio (psi)",1000,5000,3500)

    with col2:
        pb = st.slider("Presión burbuja (psi)",500,4000,2000)

    with col3:
        qmax = st.slider("Producción máxima (BPD)",500,5000,2500)

    st.markdown("---")

    st.subheader("Curva IPR Vogel")

    pwf = np.linspace(0,pr,50)

    q_ipr = qmax*(1-0.2*(pwf/pr)-0.8*(pwf/pr)**2)

    st.subheader("Curva VLP")

    q_vlp = np.linspace(0,qmax,50)

    pwf_vlp = 500 + 0.8*q_vlp

    fig, ax = plt.subplots()

    ax.plot(q_ipr,pwf,label="IPR")
    ax.plot(q_vlp,pwf_vlp,label="VLP")

    ax.set_xlabel("Producción (BPD)")
    ax.set_ylabel("Presión fondo fluyente (psi)")

    ax.legend()

    st.pyplot(fig)

    st.markdown("---")

    st.subheader("Estimación Punto de Operación")

    diferencia = abs(q_ipr - q_vlp)

    idx = diferencia.argmin()

    q_operacion = q_ipr[idx]
    pwf_operacion = pwf[idx]

    colA, colB = st.columns(2)

    colA.metric("Producción Operación BPD",round(q_operacion))
    colB.metric("Pwf Operación psi",round(pwf_operacion))
