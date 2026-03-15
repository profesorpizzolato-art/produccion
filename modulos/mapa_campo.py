import streamlit as st

def mapa_campo():

    st.title("Mapa del Campo Petrolero")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.button("Pozo A")
        st.button("Pozo B")

    with col2:
        st.button("Pozo C")
        st.button("Pozo D")

    with col3:
        st.button("Pozo E")
        st.button("Pozo F")

    st.markdown("---")

    st.info("Flujo de producción")

    st.write("Pozos → Manifold → Separador → Tanques")
