import streamlit as st

def dashboard_principal():

    st.title("SIMULADOR OPERATIVO MENFA")
    st.subheader("Centro de Entrenamiento en Producción Petrolera")

    st.markdown("---")

    st.write("Seleccione un módulo")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button("🛢 Pozo Productor"):
            st.session_state.modulo = "pozo"

        if st.button("🏭 SCADA Planta"):
            st.session_state.modulo = "planta"

    with col2:

        if st.button("📊 Diagrama Planta"):
            st.session_state.modulo = "diagrama"

        if st.button("📈 Fórmulas Producción"):
            st.session_state.modulo = "formulas"

    with col3:

        if st.button("📉 IPR - VLP"):
            st.session_state.modulo = "ipr"

        if st.button("🎓 Evaluación"):
            st.session_state.modulo = "evaluacion"
        if st.button("📘 Instrucciones"):
            st.session_state.modulo = "manual"
        if st.button("⚠ Entrenamiento"):
            st.session_state.modulo = "entrenamiento"
