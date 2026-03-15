import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def reservorio():

    st.header("Modelo de Reservorio")

    presion_inicial = st.slider("Presión inicial reservorio",2000,5000,3500)
    declinacion = st.slider("Factor declinación (%)",1,20,5)

    tiempo = np.arange(0,100)

    presion = presion_inicial * np.exp(-declinacion/100 * tiempo)

    fig, ax = plt.subplots()

    ax.plot(tiempo,presion)

    ax.set_title("Declinación de presión del reservorio")

    st.pyplot(fig)
