import streamlit as st

def separador():

    st.header("Separador Trifásico")

    petroleo = st.slider("Petróleo",100,4000,1500)
    agua = st.slider("Agua",0,2000,300)

    eficiencia = petroleo/(petroleo+agua)*100

    st.metric("Eficiencia separación",round(eficiencia,2))

    if eficiencia < 70:

        st.error("Separación deficiente")
