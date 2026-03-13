import streamlit as st

def flujo():

    st.header("Flujo Multifásico")

    petroleo = st.slider("Petróleo BPD",100,5000,1200)
    gas = st.slider("Gas m3/d",500,20000,5000)
    agua = st.slider("Agua BPD",0,2000,300)

    total_liquido = petroleo + agua

    glr = gas / petroleo

    st.metric("Líquido total",total_liquido)
    st.metric("Relación gas petróleo",round(glr,2))

    if glr > 8:

        st.warning("GLR elevado")
