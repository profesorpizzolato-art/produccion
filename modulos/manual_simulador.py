import streamlit as st
from fpdf import FPDF

def mostrar_manual():
    st.header("📘 Manual de Especialización - IPCL MENFA")
    st.write("Soporte Teórico-Operativo y Herramientas para Técnicos Superiores.")
    st.divider()

    # --- 1. BASE DE DATOS TEÓRICA ---
    teoria_petrolera = {
        "1. Ingeniería de Reservorio": {
            "resumen": "La gestión de la energía del yacimiento.",
            "detalle": "El Indice de Productividad (IP) es la métrica reina. Representa cuántos metros cúbicos entrega el pozo por cada psi de caída de presión. TEORIA DEL DRAWDOWN: Es la diferencia entre la presión estática y la fluyente. LEY DE DARCY: El flujo es proporcional a la permeabilidad y al área, e inversamente proporcional a la viscosidad.",
            "formula": r"J = \frac{Q}{P_r - P_{wf}}"
        },
        "2. Separación Física": {
            "resumen": "Principios de Gravedad, Momento y Coalescencia.",
            "detalle": "La separación ocurre por diferencia de densidades. LEY DE STOKES: Define la velocidad de caída de una gota de agua en el crudo. A mayor viscosidad, más lento cae el agua; por eso en Mendoza se usa calor para bajar la viscosidad y acelerar la separación.",
            "formula": r"v = \frac{2 \cdot r^2 \cdot g \cdot (d_1 - d_2)}{9 \cdot \eta}"
        },
        "3. Medición AGA 3": {
            "resumen": "Medición de gas por presión diferencial.",
            "detalle": "Se basa en el Efecto Venturi. Al restringir el paso con una placa de orificio, la velocidad aumenta y la presión cae. PUNTOS CRÍTICOS: La placa debe tener el borde filoso hacia aguas arriba. Si la placa está sucia o roma, medirá menos gas del real.",
            "formula": r"Q = C' \cdot \sqrt{h_w \cdot P_f}"
        },
        "4. Normativa y Seguridad": {
            "resumen": "Resolución 148/07 y API RP 14C.",
            "detalle": "La Res. 148 de Mendoza exige auditorías de integridad. PROTOCOLOS: PSH (Alta presión), LSH (Alto nivel) y LOTO (Lock Out - Tag Out) para bloqueo físico con candado durante mantenimiento.",
            "formula": "Normas: API 14C / Res. 148"
        }
    }

    # --- 2. PESTAÑAS DE INTERFAZ ---
    tab_teoria, tab_utilitarios = st.tabs(["📖 Teoría y PDF", "🧮 Utilitarios y Tablas"])

    with tab_teoria:
        # Selector de teoría interactiva
        capitulo = st.selectbox("Seleccione área de estudio:", list(teoria_petrolera.keys()))
        col_txt, col_pdf = st.columns([2, 1])

        with col_txt:
            st.markdown(f"### {capitulo}")
            st.info(teoria_petrolera[capitulo]["resumen"])
            st.write(teoria_petrolera[capitulo]["detalle"])
            st.latex(teoria_petrolera[capitulo]["formula"])

        with col_pdf:
            st.write("**Certificación y Descarga**")
            
            # --- FUNCIÓN GENERADORA DE PDF (DENTRO DEL BOTÓN PARA EVITAR ERRORES) ---
            def generar_pdf_pro():
                pdf = FPDF()
                pdf.add_page()
                
                # Sello de Certificación (Si aprobó con 80+)
                if st.session_state.get('puntaje_examen', 0) >= 80:
                    pdf.set_font("Helvetica", "B", 12)
                    pdf.set_text_color(0, 128, 0)
                    pdf.cell(0, 10, "ESTADO: USUARIO CERTIFICADO EN COMPETENCIAS OPERATIVAS", ln=True, align='C')
                    pdf.ln(5)
                
                pdf.set_font("Helvetica", "B", 16)
                pdf.set_text_color(0, 51, 102)
                pdf.cell(0, 10, "MANUAL TECNICO DE PRODUCCION IPCL 3.0", ln=True, align='C')
                pdf.set_font("Helvetica", "I", 10)
                pdf.set_text_color(100, 100, 100)
                pdf.cell(0, 10, "Menfa Capacitaciones - Instructor: F. Pizzolato", ln=True, align='C')
                pdf.ln(10)

                for tit, info in teoria_petrolera.items():
                    pdf.set_font("Helvetica", "B", 12)
                    pdf.set_fill_color(230, 230, 230)
                    pdf.set_text_color(0, 0, 0)
                    pdf.cell(0, 10, tit, ln=True, fill=True)
                    pdf.set_font("Helvetica", size=10)
                    pdf.multi_cell(0, 7, info['detalle'].encode('latin-1', 'ignore').decode('latin-1'))
                    pdf.ln(5)

                # Firmas
                pdf.ln(20)
                y_f = pdf.get_y()
                pdf.line(20, y_f, 80, y_f)
                pdf.line(120, y_f, 180, y_f)
                pdf.set_font("Helvetica", "B", 8)
                pdf.text(35, y_f + 5, "Firma Alumno")
                pdf.text(130, y_f + 5, "Firma F. Pizzolato")
                return bytes(pdf.output())

            try:
                btn_pdf = generar_pdf_pro()
                st.download_button(
                    label="📥 Descargar Manual (PDF)",
                    data=btn_pdf,
                    file_name="Manual_Tecnico_Menfa.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error PDF: {e}")

    with tab_utilitarios:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.write("**Conversor de Caudal**")
            m3 = st.number_input("Metros Cúbicos/día:", value=10.0)
            st.success(f"{m3} m³/d = **{round(m3 * 6.29, 2)} bpd**")
        with col_c2:
            st.write("**Referencia API**")
            st.table({
                "Tipo": ["Pesado", "Mediano", "Ligero"],
                "Grados": ["10 - 22", "22 - 31", "> 31"]
            })

    st.divider()
    st.caption("IPCL MENFA 3.0 - Mendoza, Argentina.")
