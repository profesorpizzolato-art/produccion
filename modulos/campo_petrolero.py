import streamlit as st

def campo():

    st.title("Campo Petrolero - Visualización")

    st.subheader("Infraestructura del campo")

    col1, col2, col3 = st.columns(3)

    with col1:
        pozo1 = st.checkbox("Pozo 1")
        pozo2 = st.checkbox("Pozo 2")
        pozo3 = st.checkbox("Pozo 3")

    with col2:
        pozo4 = st.checkbox("Pozo 4")
        pozo5 = st.checkbox("Pozo 5")
        pozo6 = st.checkbox("Pozo 6")

    with col3:
        pozo7 = st.checkbox("Pozo 7")
        pozo8 = st.checkbox("Pozo 8")
        pozo9 = st.checkbox("Pozo 9")

    produccion = 0

    if pozo1:
        produccion += 120
    if pozo2:
        produccion += 150
    if pozo3:
        produccion += 130
    if pozo4:
        produccion += 140
    if pozo5:
        produccion += 110
    if pozo6:
        produccion += 160
    if pozo7:
        produccion += 100
    if pozo8:
        produccion += 170
    if pozo9:
        produccion += 125

    st.markdown("---")

    st.subheader("Instalaciones")

    colA, colB, colC = st.columns(3)

    colA.metric("Manifold", "Activo")
    colB.metric("Separador", "Operativo")
    colC.metric("Tanque", "Disponible")

    st.markdown("---")

    st.subheader("Producción del campo")

    st.metric("Producción total (BPD)", produccion)

    if produccion > 900:
        st.success("Campo produciendo a alta capacidad")

    elif produccion > 400:
        st.warning("Producción media")

    else:
        st.error("Producción baja")
