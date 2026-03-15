import streamlit as st

def certificado():

    st.title("Certificado MENFA")

    nombre = st.text_input("Nombre del alumno")

    if st.button("Generar certificado"):

        st.success(f"Certificado generado para {nombre}")
