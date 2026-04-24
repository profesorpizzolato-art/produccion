import streamlit as st
from fpdf import FPDF

def mostrar_manual():
    st.header("📘 Manual Técnico y Normativo - IPCL MENFA")
    st.write("Guía integral: Ingeniería, Procesos, Seguridad y Normativa Legal.")

    def generar_pdf():
        pdf = FPDF()
        pdf.add_page()
        
        # --- ENCABEZADO ---
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(200, 10, txt="MANUAL TECNICO Y DE SEGURIDAD OPERATIVA", ln=True, align='C')
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(200, 10, txt="Menfa Capacitaciones - Simulador IPCL 3.0", ln=True, align='C')
        pdf.ln(10)

        # --- SECCIÓN 1: INGENIERÍA Y FÓRMULAS ---
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(0, 10, txt="1. INGENIERIA DE PRODUCCION Y FORMULAS", ln=True, fill=True)
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(0, 7, txt=(
            "Indice de Productividad (IP): J = Q / (Pr - Pwf)\n"
            "Calculo de Eficiencia Volumetrica: Ev = (Q_real / Q_teorico) x 100\n"
            "Presion de Fluido (Hidrostatica): Ph = 0.052 x Densidad x Profundidad\n"
            "Velocidad Critica de Erosion: v = C / (rho^0.5)"
        ))
        pdf.ln(5)

        # --- SECCIÓN 2: FUNCIONES DEL PERSONAL ---
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, txt="2. FUNCIONES Y RESPONSABILIDADES", ln=True, fill=True)
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(0, 7, txt=(
            "- SUPERVISOR: Asegurar la integridad de las instalaciones, validar permisos de trabajo "
            "y optimizar el balance de masa diario (Control de Perdidas).\n"
            "- OPERADOR DE PLANTA: Monitorear el SCADA, ajustar setpoints de separadores y "
            "actuar ante alarmas de nivel (LSH) o presion (PSH).\n"
            "- RECORREDOR DE CAMPO: Inspeccion visual de locaciones, toma de presiones en boca "
            "de pozo y deteccion temprana de fugas o parafinas."
        ))
        pdf.ln(5)

        # --- SECCIÓN 3: SEGURIDAD OPERATIVA Y NORMATIVA ---
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, txt="3. SEGURIDAD OPERATIVA (SSMA) Y NORMAS", ln=True, fill=True)
        pdf.set_font("Helvetica", size=10)
        
        texto_seguridad = (
            "NORMATIVAS CLAVE:\n"
            "- Res. SEN 148/07: Normas para el abandono de pozos e integridad.\n"
            "- API RP 14C: Analisis, diseño e instalacion de sistemas de seguridad en plataformas y plantas.\n"
            "- ISO 14001: Gestion Ambiental para el control de derrames.\n\n"
            "PROTOCOLOS CRITICOS:\n"
            "1. ESD (Emergency Shutdown): Parada total por sobrepresion o fuego.\n"
            "2. LOTO (Lock Out - Tag Out): Bloqueo y etiquetado para mantenimiento de bombas.\n"
            "3. MAOP: Nunca exceder la Presion Maxima de Operacion Admisible en lineas."
        )
        pdf.multi_cell(0, 7, txt=texto_seguridad)

        return bytes(pdf.output())

    # --- RENDERIZADO ---
    try:
        pdf_data = generar_pdf()
        st.success("Manual actualizado con secciones de Seguridad, Funciones y Normativa (API/Res. 148).")
        
        st.download_button(
            label="💾 Descargar Manual Profesional (PDF)",
            data=pdf_data,
            file_name="manual_operativo_menfa_pro.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Error técnico al compilar el PDF: {e}")
