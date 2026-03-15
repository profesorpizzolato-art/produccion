import streamlit as st

def diagrama_planta():

    st.title("Diagrama Operativo de Planta")
    st.subheader("Simulador MENFA")

    st.markdown("### Parámetros del sistema")

    presion = st.slider("Presión del sistema (psi)", 500, 5000, 2500)
    caudal = st.slider("Caudal producción (BPD)", 100, 5000, 1200)

    st.markdown("---")

    st.subheader("Flujo de Producción")

    if presion > 4000:
        color = "red"
        estado = "Alta presión"
    elif caudal < 300:
        color = "orange"
        estado = "Baja producción"
    else:
        color = "green"
        estado = "Operación normal"

    st.markdown(
        f"""
        <div style="text-align:center">

        <div style="background:{color};padding:10px;border-radius:10px">POZO</div>

        ↓

        <div style="background:{color};padding:10px;border-radius:10px">FLOWLINE</div>

        ↓

        <div style="background:{color};padding:10px;border-radius:10px">MANIFOLD</div>

        ↓

        <div style="background:{color};padding:10px;border-radius:10px">SEPARADOR</div>

        ↓

        <div style="background:{color};padding:10px;border-radius:10px">TANQUE</div>

        ↓

        <div style="background:{color};padding:10px;border-radius:10px">COMPRESOR</div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.metric("Estado del sistema", estado)
