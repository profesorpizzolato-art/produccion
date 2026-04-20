import streamlit as st

def choke_control():
    st.header("🎮 Control de Choke (Orificio de Restricción)")
    st.write("Módulo de control de contrapresión del pozo.")
    
    # Ejemplo de control
    apertura = st.slider("Apertura del Choke (%)", 0, 100, 50)
    st.metric("Presión de Cabezal (whp)", f"{2000 * (1 - apertura/100)} psi")
