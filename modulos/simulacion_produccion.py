import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def simulacion():

    st.header("Simulación Dinámica de Producción")

    presion = st.slider("Presión reservorio",1000,4000,2500)
    permeabilidad = st.slider("Permeabilidad",50,500,150)
    viscosidad = st.slider("Viscosidad",1,10,3)

    q = (presion*permeabilidad)/viscosidad

    st.metric("Producción estimada",round(q,2))

    tiempo = np.arange(0,50)

    produccion = q - tiempo*2

    fig, ax = plt.subplots()

    ax.plot(tiempo,produccion)

    ax.set_title("Declinación producción")

    st.pyplot(fig)
