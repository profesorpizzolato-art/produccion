import streamlit as st

def choke():

    st.header("Control de Choke")

    apertura = st.slider("Apertura Choke (%)",0,100,40)

    presion = 2000 - (apertura*10)

    produccion = apertura*20

    st.metric("Presión Tubing",presion)
    st.metric("Producción estimada",produccion)

    if apertura > 80:

        st.warning("Apertura alta")
