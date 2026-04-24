import streamlit as st
from fpdf import FPDF
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
 # --- LÓGICA PARA GENERAR EL PDF (VERSIÓN FINAL) ---
    def generar_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16) # Cambiado a Helvetica (estándar)
        pdf.cell(200, 10, txt="MANUAL TECNICO - IPCL MENFA 3.0", ln=True, align='C')
        
        pdf.set_font("Helvetica", size=12)
        pdf.ln(10)
        
        contenido = (
            "Este documento certifica las normas operativas del simulador.\n\n"
            "1. OPERACIONES DE CAMPO: Control de sistemas AIB, ESP y PCP.\n"
            "2. PLANTA DE PROCESO: Gestion de presiones (V-01) y temperaturas (E-01).\n"
            "3. SEGURIDAD: Protocolo de parada de emergencia (ESD).\n"
            "4. INGENIERIA: Analisis de curvas IPR y VLP."
        )
        
        pdf.multi_cell(0, 10, txt=contenido)
        
        # Obtenemos el bytearray y lo convertimos a bytes puros
        return bytes(pdf.output()) 

    try:
        # Generamos los bytes reales
        pdf_data = generar_pdf()

        st.download_button(
            label="📄 Descargar Manual Completo (PDF)",
            data=pdf_data,
            file_name="manual_menfa_operacines_campo_2026.pdf",
            mime="application/pdf"
        )
        st.success("✅ PDF listo para descarga.")
    except Exception as e:
        st.error(f"Error técnico: {e}")
   
