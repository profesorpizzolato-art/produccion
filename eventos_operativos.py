import streamlit as st
import random

def eventos():

    st.header("Eventos Operativos")

    eventos = [

    "Slugging en línea de flujo",
    "Cavitación en bomba",
    "Alta presión separador",
    "Gas lock",
    "Falla válvula choke",
    "Bloqueo línea producción",
    "Nivel alto tanque"

    ]

    if st.button("Generar evento operativo"):

        evento = random.choice(eventos)

        st.error(evento)
