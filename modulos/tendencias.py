import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def tendencias():

    st.header("Tendencias de Producción")

    dias = np.arange(0,100)

    petroleo = np.random.normal(1200,80,100)
    gas = np.random.normal(5000,400,100)
    agua = np.random.normal(300,50,100)

    fig, ax = plt.subplots()

    ax.plot(dias,petroleo,label="Petróleo BPD")
    ax.plot(dias,gas,label="Gas m3/d")
    ax.plot(dias,agua,label="Agua BPD")

    ax.legend()

    ax.set_title("Histórico Producción")

    st.pyplot(fig)
