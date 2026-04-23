import streamlit as st

def show():
    st.header("⚙️ Simulador de Bombeo Mecánico")
    st.write("Instructor: Fabricio Pizzolato")
    
    # Aquí va todo tu código de la bomba, por ejemplo:
    st.subheader("Parámetros de Operación")
    ppm = st.slider("Carreras por minuto (PPM)", 0, 20, 8)
    longitud = st.number_input("Longitud de carrera (pulgadas)", value=86)
    
    # Cálculo simple de ejemplo
    produccion_estimada = ppm * longitud * 0.15 # Tu fórmula real aquí
    st.metric("Producción Estimada", f"{produccion_estimada} m3/d")
    
    # Lógica de la carta dinamométrica, etc.
