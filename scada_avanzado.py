import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def scada():

    st.header("SCADA Producción")

    produccion = np.random.normal(1200,100,60)

    presion = np.random.normal(900,50,60)

    fig, ax = plt.subplots()

    ax.plot(produccion,label="Producción BPD")
    ax.plot(presion,label="Presión PSI")

    ax.legend()

    st.pyplot(fig)
