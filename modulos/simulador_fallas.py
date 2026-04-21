import streamlit as st
import random

def simulador_fallas():

    eventos = [

    "Slugging en línea",
    "Gas lock",
    "Cavitación bomba",
    "Alta presión separador",
    "Bloqueo línea"

    ]

    if st.button("Simular incidente"):

        evento = random.choice(eventos)

        st.error(evento)
