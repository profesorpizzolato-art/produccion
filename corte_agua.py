import streamlit as st

def corte_agua():

    st.header("Corte de Agua")

    petroleo = st.slider("Producción Petróleo",100,5000,1200)
    agua = st.slider("Producción Agua",0,2000,300)

    total = petroleo + agua

    wc = (agua/total)*100

    st.metric("Corte de Agua (%)",round(wc,2))

    if wc > 60:

        st.error("Corte de agua alto")
