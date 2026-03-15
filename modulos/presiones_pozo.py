import streamlit as st

def presiones():

    st.header("Presiones del Pozo")

    tubing = st.slider("Presión Tubing",100,3000,900)
    casing = st.slider("Presión Casing",100,3000,700)

    diferencial = tubing - casing

    st.metric("Diferencial de presión",diferencial)

    if diferencial < 100:

        st.warning("Diferencial bajo")
