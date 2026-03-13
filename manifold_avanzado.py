import streamlit as st

def manifold():

    st.header("Manifold de Producción")

    pozo1 = st.checkbox("Pozo 1 activo")
    pozo2 = st.checkbox("Pozo 2 activo")
    pozo3 = st.checkbox("Pozo 3 activo")
    pozo4 = st.checkbox("Pozo 4 activo")

    produccion = 0

    if pozo1:
        produccion += 400

    if pozo2:
        produccion += 350

    if pozo3:
        produccion += 300

    if pozo4:
        produccion += 250

    st.metric("Producción total",produccion)
