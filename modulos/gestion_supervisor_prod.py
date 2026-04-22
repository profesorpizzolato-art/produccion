import streamlit as st

def gestion_supervisor_prod():
    st.header("📈 Panel del Supervisor de Producción")
    st.subheader("Optimización de Costos y Eficiencia del Yacimiento")

    # Métricas clave basadas en Clase 11
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Frecuencia de Intervención", "1.8 años", "-0.2", help="Meta: 2 años (Clase 11)")
    with col2:
        st.metric("Incidencia en Costos", "30%", "Crítico", delta_color="inverse")
    with col3:
        st.metric("Producción Bruta", "200 m³/día", "+5%")

    st.markdown("---")
    st.subheader("📑 Autorización de Movimiento de Equipos")
    
    with st.expander("Analizar Pozos con Baja Producción", expanded=True):
        pozo = st.selectbox("Seleccione Pozo:", ["Pozo P-101 (Falla BES)", "Pozo P-205 (Rotura de Varilla)"])
        if "P-205" in pozo:
            st.warning("Diagnóstico: El pozo no produce. El costo de intervención se justifica por potencial.")
            if st.button("AUTORIZAR PULLING"):
                st.success("Orden enviada. Se busca mejorar el KPI de 2 años de estabilidad.")

    st.info("💡 **Dato de Clase 11:** El objetivo es realizar operaciones tan optimizadas que disminuya la frecuencia de intervención.")
