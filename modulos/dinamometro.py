import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def dinamometro():

    st.title("Carta Dinamométrica")

    x = np.linspace(0,10,100)
    y = np.sin(x) + np.random.normal(0,0.1,100)

    fig, ax = plt.subplots()

    ax.plot(x,y)

    ax.set_title("Carta de bomba")

    st.pyplot(fig)
