import streamlit as st
from fpdf import FPDF

def mostrar_manual():
    st.header("📘 Manual Tecnico y Normativo - IPCL MENFA")
    st.write("Guia integral: Ingenieria, Procesos, Seguridad y Normativa Legal.")
    st.divider()

    def generar_pdf():
        pdf = FPDF()
        pdf.add_page()
        
        # --- ENCABEZADO ---
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(0, 51, 102) # Azul oscuro profesional
        pdf.cell(200, 10, txt="MANUAL TECNICO Y DE SEGURIDAD OPERATIVA", ln=True, align='C')
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(200, 10, txt="Menfa Capacitaciones - Simulador IPCL 3.0", ln=True, align='C')
        pdf.ln(10)

        # --- SECCIONES TÉCNICAS ---
        sections = [
            ("1. INGENIERIA DE PRODUCCION Y FORMULAS", [
                "Indice de Productividad (IP): J = Q / (Pr - Pwf)",
                "Calculo de Eficiencia Volumetrica: Ev = (Q_real / Q_teorico) x 100",
                "Presion de Fluido (Hidrostatica): Ph = 0.052 x Densidad x Profundidad"
            ]),
            ("2. SEGURIDAD OPERATIVA Y NORMAS (SSMA)", [
                "Res. SEN 148/07: Normas de integridad y abandono.",
                "API RP 14C: Analisis de seguridad en instalaciones de superficie.",
                "Protocolos LOTO: Bloqueo y Etiquetado para intervenciones seguras."
            ])
        ]

        # --- AQUÍ ESTABA EL ERROR: El bucle debe estar dentro de la función ---
        for title, content in sections:
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_fill_color(240, 240, 240)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, txt=title, ln=True, fill=True)
            pdf.set_font("Helvetica", size=10)
            for line in content:
                # Usamos un guion para evitar errores de fuente Unicode
                pdf.cell(0, 7, txt=f" - {line}", ln=True) 
            pdf.ln(5)
       
        # --- SECCIÓN DE COMPROMISO Y FIRMA ---
        pdf.ln(20)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, txt="4. COMPROMISO DE SEGURIDAD OPERATIVA", ln=True)
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(0, 7, txt=(
            "Como operario/tecnico capacitado por Menfa Capacitaciones, entiendo los riesgos "
            "asociados a las operaciones de petroleo y gas. Me comprometo a respetar las "
            "presiones maximas (MAOP), utilizar los elementos de proteccion personal (EPP) "
            "y nunca puentear sistemas de seguridad sin la debida autorizacion."
        ))
        
        pdf.ln(30)
        # Líneas para firma
        y_actual = pdf.get_y()
        col_width = pdf.w / 2.5
        pdf.line(20, y_actual, 20 + col_width, y_actual) # Línea Alumno
        pdf.line(110, y_actual, 110 + col_width, y_actual) # Línea Instructor
        
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_y(y_actual + 2)
        pdf.set_x(35)
        pdf.cell(col_width, 5, txt="Firma del Alumno")
        pdf.set_x(125)
        pdf.cell(col_width, 5, txt="Firma Instructor (F. Pizzolato)")

        return bytes(pdf.output())

    # --- INTERFAZ STREAMLIT ---
    col_info, col_btn = st.columns([2, 1])

    with col_info:
        st.markdown("""
        ### 📋 ¿Qué incluye este manual?
        * **Ingeniería:** Fórmulas para cálculo de IP y eficiencia.
        * **Normativa:** Resumen de la Res. 148 y Normas API.
        * **Seguridad:** Protocolos de bloqueo (LOTO) y parada de emergencia (ESD).
        * **Compromiso:** Hoja de firmas para validación de competencia.
        """)

    with col_btn:
        try:
            # Primero intentamos generar los bytes
            pdf_bytes = generar_pdf()
            st.success("PDF generado con éxito.")
            st.download_button(
                label="📥 Descargar Manual y Compromiso",
                data=pdf_bytes,
                file_name="Manual_Seguridad_IPCL_MENFA.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error al preparar el PDF: {e}")

    st.divider()
    st.info("💡 **Consejo para el alumno:** Imprima este manual y manténgalo en su legajo técnico personal.")
