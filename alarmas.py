import streamlit as st

def alarmas():

    st.header("Alarmas Operativas")

    presion = st.slider("Presión línea",100,3000,900)

    if presion > 2000:

        st.error("Alta presión en línea")

    elif presion > 1500:

        st.warning("Presión elevada")

    else:

        st.success("Sistema estable")
