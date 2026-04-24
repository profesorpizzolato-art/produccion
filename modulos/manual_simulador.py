import streamlit as st
from fpdf import FPDF

def mostrar_manual():
    st.header("📘 Manual Técnico y Normativo - IPCL MENFA")
    st.write("Guía integral: Ingeniería, Procesos, Seguridad y Normativa Legal.")
    st.divider()

    # --- FUNCIÓN PARA GENERAR EL PDF ---
    def generar_pdf():
        pdf = FPDF()
        pdf.add_page()
        
        # Encabezado con estilo
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(200, 10, txt="MANUAL TÉCNICO Y DE SEGURIDAD OPERATIVA", ln=True, align='C')
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(200, 10, txt="Menfa Capacitaciones - Simulador IPCL 3.0", ln=True, align='C')
        pdf.ln(10)

        # SECCIÓN 1: INGENIERÍA
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(0, 10, txt="1. INGENIERÍA DE PRODUCCIÓN Y FÓRMULAS", ln=True, fill=True)
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(0, 7, txt=(
            "Índice de Productividad (IP): J = Q / (Pr - Pwf)\n"
            "Cálculo de Eficiencia Volumétrica: Ev = (Q_real / Q_teorico) x 100\n"
            "Presión de Fluido (Hidrostática): Ph = 0.052 x Densidad x Profundidad\n"
            "Velocidad Crítica de Erosión: v = C / (rho^0.5)"
        ))
        pdf.ln(5)

        # SECCIÓN 2: ROLES
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, txt="2. FUNCIONES Y RESPONSABILIDADES", ln=True, fill=True)
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(0, 7, txt=(
            "- SUPERVISOR: Asegurar la integridad de las instalaciones y validar permisos.\n"
            "- OPERADOR DE PLANTA: Monitorear SCADA y actuar ante alarmas LSH/PSH.\n"
            "- RECORREDOR DE CAMPO: Inspección visual y detección de parafinas."
        ))
        pdf.ln(5)

        # SECCIÓN 3: SEGURIDAD
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, txt="3. SEGURIDAD OPERATIVA (SSMA) Y NORMAS", ln=True, fill=True)
        pdf.set_font("Helvetica", size=10)
        texto_seguridad = (
            "NORMATIVAS:\n"
            "- Res. SEN 148/07: Integridad de pozos y abandono.\n"
            "- API RP 14C: Sistemas de seguridad en plantas.\n"
            "PROTOCOLOS:\n"
            "1. ESD: Parada de emergencia.\n"
            "2. LOTO: Bloqueo y etiquetado."
        )
        pdf.multi_cell(0, 7, txt=texto_seguridad)

        return bytes(pdf.output())

    # --- INTERFAZ EN EL SIMULADOR ---
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📚 Contenidos del Módulo")
        with st.expander("Ver Fórmulas de Ingeniería"):
            st.code("J = Q / (Pr - Pwf)\nPh = 0.052 * d * h")
        with st.expander("Ver Normativa y Seguridad"):
            st.write("**Res. 148/07:** Control de integridad en Mendoza.")
            st.write("**API RP 14C:** Dispositivos de protección (LSH, PSH, SDV).")

    with col2:
        st.info("Generar versión PDF para imprimir o estudiar fuera de línea.")
        try:
            pdf_data = generar_pdf()
            st.download_button(
                label="💾 Descargar Manual (PDF)",
                data=pdf_data,
                file_name="manual_operativo_menfa_pro.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error al generar PDF: {e}")
