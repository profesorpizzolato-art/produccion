import streamlit as st

def dashboard():

    st.header("Dashboard Producción MENFA")

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Producción Campo",1200)
    col2.metric("Gas Producción",5000)
    col3.metric("Agua",300)
    col4.metric("Presión Línea",850)
