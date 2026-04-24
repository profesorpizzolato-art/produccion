import streamlit as st
from fpdf import FPDF
def mostrar_utilitarios():
    st.subheader("🧮 Calculadora y Tablas de Referencia")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Conversor de Caudal**")
        m3_dia = st.number_input("Metros Cúbicos por día (m³/d):", value=1.0)
        st.write(f"Equivale a: **{m3_dia * 6.29:.2f} Barriles por día (bpd)**")
    
    with col2:
        st.write("**Tabla de Gravedad API (Referencia)**")
        st.table({
            "Tipo de Crudo": ["Extra Pesado", "Pesado", "Mediano", "Ligero"],
            "Grados API": ["< 10", "10 - 22.3", "22.3 - 31.1", "> 31.1"]
        })
def mostrar_manual():
    st.header("📘 Manual de Especialización en Producción Petrolera")
    st.write("Soporte Teórico-Operativo para Técnicos Superiores.")
    st.divider()

    # --- BASE DE DATOS TEÓRICA ---
    # Centralizamos la info para que sea fácil editarla
    teoria_petrolera = {
        "1. Ingeniería de Reservorio": {
            "resumen": "La gestión de la energía del yacimiento.",
            "detalle": (
                "El Indice de Productividad (IP) es la métrica reina. Representa cuántos metros cúbicos "
                "entrega el pozo por cada psi de caída de presión. \n\n"
                "TEORIA DEL DRAWDOWN: Es la diferencia entre la presión estática y la fluyente. "
                "Un drawdown excesivo puede provocar 'conificación' de agua o arenamiento. \n"
                "LEY DE DARCY: El flujo es proporcional a la permeabilidad y al área, "
                "e inversamente proporcional a la viscosidad del fluido."
            ),
            "formula": "J = Q / (Pr - Pwf)"
        },
        "2. Separación Física": {
            "resumen": "Principios de Gravedad, Momento y Coalescencia.",
            "detalle": (
                "La separación ocurre por diferencia de densidades. En un separador horizontal, "
                "el petróleo necesita 'Tiempo de Residencia' para soltar las burbujas de gas. \n\n"
                "LEY DE STOKES: Define la velocidad de caída de una gota de agua en el crudo. "
                "A mayor viscosidad, más lento cae el agua; por eso en Mendoza se usa calor "
                "para bajar la viscosidad y acelerar la separación."
            ),
            "formula": "v = (2 * r² * g * (d1 - d2)) / (9 * n)"
        },
        "3. Medición AGA 3": {
            "resumen": "Medición de gas por presión diferencial.",
            "detalle": (
                "Se basa en el Efecto Venturi. Al restringir el paso con una placa de orificio, "
                "la velocidad aumenta y la presión cae. Esa 'Diferencial' nos dice cuánto gas pasa. \n\n"
                "PUNTOS CRÍTICOS: La placa debe tener el borde filoso hacia aguas arriba. "
                "Si la placa está sucia o roma, medirá menos gas del real (Pérdida económica)."
            ),
            "formula": "Q = C' * sqrt(hw * Pf)"
        },
        "4. Normativa y Seguridad": {
            "resumen": "Resolución 148/07 y API RP 14C.",
            "detalle": (
                "La Res. 148 de Mendoza exige auditorías de integridad. No es opcional. \n\n"
                "PROTOCOLOS DE SEGURIDAD: \n"
                "- PSH (Pressure Switch High): Protege el equipo de una explosión.\n"
                "- LSH (Level Switch High): Evita que el crudo pase a la línea de gas.\n"
                "- LOTO: Bloqueo físico (candado) para que nadie arranque una bomba mientras la reparas."
            ),
            "formula": "Normas: API 14C / Res. 148 Mendoza"
        }
    }

    # --- FUNCIÓN GENERADORA DE PDF ---
    def generar_pdf_pro():
        pdf = FPDF()
        pdf.add_page()
        
        # Portada/Encabezado
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "MANUAL TECNICO DE PRODUCCION IPCL 3.0", ln=True, align='C')
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 10, "Desarrollado por Menfa Capacitaciones - Instructor: F. Pizzolato", ln=True, align='C')
        pdf.ln(10)

        for titulo, info in teoria_petrolera.items():
            # Título de Sección
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(0, 10, titulo, ln=True, fill=True)
            
            # Cuerpo Teórico
            pdf.set_font("Helvetica", size=10)
            # Limpiamos tildes para evitar errores de fuente
            texto_limpio = info['detalle'].encode('latin-1', 'ignore').decode('latin-1')
            pdf.multi_cell(0, 7, texto_limpio)
            
            # Fórmula Destacada
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(200, 0, 0)
            pdf.cell(0, 7, f"Formula Clave: {info['formula']}", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(5)

        # Hoja de firmas
        pdf.ln(10)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 10, "VALIDACION DE COMPETENCIAS", ln=True)
        pdf.ln(20)
        y = pdf.get_y()
        pdf.line(20, y, 80, y)
        pdf.line(120, y, 180, y)
        pdf.text(35, y+5, "Firma Alumno")
        pdf.text(125, y+5, "Firma F. Pizzolato")

        return bytes(pdf.output())

    # --- RENDERIZADO EN PANTALLA ---
    st.subheader("📖 Biblioteca de Consulta Rápida")
    
    # Selector de teoría interactiva
    capitulo = st.selectbox("Seleccione el área de estudio:", list(teoria_petrolera.keys()))
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {capitulo}")
        st.info(teoria_petrolera[capitulo]["resumen"])
        st.write(teoria_petrolera[capitulo]["detalle"])
        st.latex(teoria_petrolera[capitulo]["formula"])

    with col2:
        st.write("---")
        st.write("**Acciones Técnicas:**")
        try:
            pdf_data = generar_pdf_pro()
            st.download_button(
                label="📥 Descargar Manual Extendido (PDF)",
                data=pdf_data,
                file_name="Manual_Produccion_Menfa_Pro.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error PDF: {e}")
        
        if st.button("❓ Troubleshooting (Fallas)"):
            st.warning("**Caso:** Si sube la presión y baja el nivel... \n\n **Diagnóstico:** Obstrucción en la salida de gas o válvula de control trabada.")

    st.divider()
    st.caption("IPCL MENFA 3.0 - Mendoza, Argentina.")
