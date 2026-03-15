import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def pozo_productor():

    st.title("Simulador de Pozo Productor")
    st.subheader("IPCL MENFA - Ingeniería de Producción")

    st.markdown("### Parámetros del reservorio")

    col1, col2, col3 = st.columns(3)

    with col1:
        pr = st.slider("Presión Reservorio (psi)",1000,5000,3500)

    with col2:
        pwf = st.slider("Presión Fondo Fluyente (psi)",100,4000,1500)

    with col3:
        pi = st.slider("Índice de Productividad (PI)",0.1,5.0,1.5)

    st.markdown("---")

    # Cálculo producción
    q = pi * (pr - pwf)

    st.subheader("Producción del Pozo")

    st.metric("Producción estimada (BPD)", round(q,2))

    st.markdown("---")

    st.subheader("Curva IPR")

    pwf_range = np.linspace(0, pr, 50)

    q_ipr = pi * (pr - pwf_range)

    fig, ax = plt.subplots()

    ax.plot(q_ipr, pwf_range)

    ax.set_xlabel("Producción (BPD)")
    ax.set_ylabel("Presión fondo fluyente (psi)")
    ax.set_title("Curva IPR del pozo")

    ax.invert_yaxis()

    st.pyplot(fig)

    st.markdown("---")

    st.subheader("Estado del pozo")

    if q > 3000:
        st.success("Pozo de alta productividad")

    elif q > 1000:
        st.warning("Producción media")

    else:
        st.error("Producción baja")
