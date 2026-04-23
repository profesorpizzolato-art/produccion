import streamlit as st

def show():
    st.header("⚠️ Panel de Simulación de Fallas")
    st.write("Simula condiciones adversas para observar el impacto en las curvas de producción.")

    # Inicializamos el estado de la falla si no existe
    if 'factor_obstruccion' not in st.session_state:
        st.session_state.factor_obstruccion = 1.0

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Seleccionar Evento")
        falla = st.selectbox("Tipo de Falla", [
            "Operación Normal",
            "Obstrucción en Línea de Flujo (Parafinas)",
            "Aumento de Contrapresión en Separador",
            "Incremento de Corte de Agua (Aumento de Densidad)"
        ])

        if falla == "Operación Normal":
            st.session_state.factor_obstruccion = 1.0
            st.success("Sistema operando en condiciones de diseño.")
        
        elif falla == "Obstrucción en Línea de Flujo (Parafinas)":
            st.session_state.factor_obstruccion = 2.5
            st.warning("Se detecta restricción de flujo. La curva VLP aumentará su pendiente.")

        elif falla == "Aumento de Contrapresión en Separador":
            st.session_state.factor_obstruccion = 1.8
            st.warning("Presión de llegada a planta elevada.")

    with col2:
        st.info("💡 **Dato Técnico:** En la cuenca cuyana, la deposición de parafinas es una de las causas principales del desplazamiento de la curva VLP hacia la izquierda, reduciendo el caudal de aporte.")
