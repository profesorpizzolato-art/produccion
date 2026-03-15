import streamlit as st

def bomba_mecanica():

    st.title("Simulador de Bombeo Mecánico")

    carrera = st.slider("Carrera bomba (in)",10,200,80)
    spm = st.slider("Golpes por minuto",1,20,8)

    eficiencia = st.slider("Eficiencia (%)",40,100,75)

    produccion = carrera * spm * eficiencia * 0.1

    st.metric("Producción estimada BPD",round(produccion))
