import streamlit as st

def mostrar_manual():
    st.header("📘 Manual de Usuario - IPCL MENFA")
    
    tab1, tab2, tab3 = st.tabs(["🚀 Inicio Rápido", "⚙️ Guía de Operación", "🚨 Protocolos"])

    with tab1:
        st.subheader("Bienvenido al Simulador 3.0")
        st.write("""
        Este software ha sido diseñado para entrenar técnicos en el manejo de yacimientos y plantas de tratamiento.
        
        **Pasos iniciales:**
        1. **Navegación:** Utilice el panel lateral para saltar entre el Mapa, la Planta y la Ingeniería.
        2. **Monitoreo:** Revise constantemente el módulo SCADA para detectar alertas.
        3. **Interacción:** El simulador reacciona a sus cambios. Si sube la temperatura en la planta, verá el efecto en la eficiencia.
        """)
        st.info("💡 **Dato:** Todos los datos están basados en estándares de la Cuenca Cuyana.")

    with tab2:
        st.subheader("Control de Procesos")
        
        with st.expander("🛢️ Operaciones de Campo"):
            st.write("""
            * **Pozos:** Identificados por sistema de extracción (AIB, ESP, PCP).
            * **Fallas Comunes:** Si un pozo aparece en **amarillo**, requiere inspección por fatiga o mecánica.
            """)
            
        with st.expander("🏭 Planta de Proceso (PTC)"):
            st.write("""
            * **Separador V-01:** Es el corazón de la planta. Si la presión supera los 150 psi, se activará una alarma en el SCADA.
            * **Calentador E-01:** Crucial para reducir la viscosidad. Rango óptimo: 60°C - 70°C.
            """)

    with tab3:
        st.subheader("Protocolos de Emergencia")
        st.error("**ESD (Emergency Shutdown):**")
        st.write("""
        En caso de una alerta roja en el SCADA o una presión incontrolable en el manifold, el operador debe:
        1. Pulsar el botón **ESD** en el módulo de Planta.
        2. Verificar el cierre de válvulas en el Mapa de Campo.
        3. Reportar la novedad en el panel de Gestión.
        """)

    st.divider()
    st.download_button(
        label="📄 Descargar Manual Completo (PDF)",
        data="Contenido del manual para exportar...",
        file_name="manual_menfa_2026.pdf",
        mime="application/pdf",
        help="Descarga la guía técnica para estudio offline."
    )
