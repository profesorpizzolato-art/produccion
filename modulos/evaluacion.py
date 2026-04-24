import streamlit as st

def evaluacion():
    st.header("🧠 Evaluación de Competencias Operativas")
    st.write("Examen técnico para la certificación en Operaciones de Campo y Planta.")

    # --- 1. DATOS DEL ALUMNO ---
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre Completo del Alumno:")
        with col2:
            dni = st.text_input("DNI:")

    # --- 2. EXAMEN (Banco de Preguntas) ---
    st.divider()
    score = 0

    # Pregunta 1
    st.markdown("### 1. Sistema de Extracción")
    p1 = st.radio(
        "Si observamos que un pozo tiene un **AIB (Aparato Independiente de Bombeo)**, ¿a qué sistema de extracción pertenece?",
        ["Surgencia Natural", "Bombeo Mecánico", "Bombeo Electrosumergible (ESP)", "Plunger Lift"],
        index=None
    )
    if p1 == "Bombeo Mecánico": score += 25

    # Pregunta 2
    st.markdown("### 2. Control de Planta")
    p2 = st.radio(
        "¿Cuál es el objetivo principal del Separador Trifásico en la PTC?",
        ["Aumentar la presión del gas", "Separar el gas, el crudo y el agua de formación", "Calentar el petróleo para reducir viscosidad"],
        index=None
    )
    if p2 == "Separar el gas, el crudo y el agua de formación": score += 25

    # Pregunta 3
    st.markdown("### 3. Ingeniería y Producción")
    p3 = st.radio(
        "En el análisis nodal, si la curva VLP se desplaza hacia arriba (aumento de contrapresión), ¿qué sucede con el caudal de producción?",
        ["El caudal aumenta", "El caudal disminuye", "El caudal se mantiene constante"],
        index=None
    )
    if p3 == "El caudal disminuye": score += 25

    # Pregunta 4
    st.markdown("### 4. Seguridad Operativa")
    p4 = st.radio(
        "¿Qué significan las siglas **ESD** en una sala de control de planta?",
        ["Electric System Data", "Emergency Shutdown (Parada de Emergencia)", "Every Single Day"],
        index=None
    )
    if p4 == "Emergency Shutdown (Parada de Emergencia)": score += 25

    # --- 3. RESULTADOS ---
    st.divider()
    if st.button("Finalizar y Calificar", use_container_width=True):
        if not nombre or not dni:
            st.error("Por favor, ingrese sus datos antes de calificar.")
        else:
            st.subheader(f"Resultado para {nombre}")
            if score >= 75:
                st.balloons()
                st.success(f"✅ APROBADO - Calificación: {score}/100")
                st.info("Puede solicitar su certificado de asistencia a Menfa Capacitaciones.")
            else:
                st.error(f"❌ REPROBADO - Calificación: {score}/100")
                st.warning("Se recomienda repasar los módulos de Planta e Ingeniería.")
            
            # Opción para "Imprimir" o guardar
            st.button("Descargar Reporte de Examen (PDF)", disabled=True)
            st.caption("Función de exportación PDF disponible en la versión Pro.")
import streamlit as st
from fpdf import FPDF

def generar_certificado_pdf(nombre_alumno, puntaje):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    # Marco exterior (Dorado/Azul Petróleo)
    pdf.set_draw_color(0, 59, 70) # Azul Petróleo
    pdf.set_line_width(5)
    pdf.rect(5, 5, 287, 200) 
    
    # Encabezado
    pdf.set_font("Helvetica", "B", 30)
    pdf.set_text_color(0, 59, 70)
    pdf.cell(0, 40, "MENFA CAPACITACIONES", ln=True, align='C')
    
    pdf.set_font("Helvetica", "B", 40)
    pdf.cell(0, 20, "CERTIFICADO DE APROBACION", ln=True, align='C')
    pdf.ln(10)
    
    # Cuerpo del texto
    pdf.set_font("Helvetica", "", 18)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 15, "Se otorga el presente certificado a:", ln=True, align='C')
    
    pdf.set_font("Helvetica", "B", 35)
    pdf.set_text_color(196, 163, 90) # Dorado
    pdf.cell(0, 25, nombre_alumno.upper(), ln=True, align='C')
    
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(0, 0, 0)
    contenido = (
        f"Por haber completado y aprobado satisfactoriamente la simulacion operativa "
        f"IPCL MENFA 3.0 con un puntaje de {puntaje}/100. "
        "Demostrando competencias en Ingenieria de Produccion, Control de Procesos en Planta "
        "y Seguridad Operativa bajo normas API y Res. 148."
    )
    pdf.multi_cell(0, 10, txt=contenido, align='C')
    
    # Firmas
    pdf.ln(20)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(140, 10, "__________________________", 0, 0, 'C')
    pdf.cell(140, 10, "__________________________", 0, 1, 'C')
    pdf.cell(140, 5, "Fabricio Pizzolato", 0, 0, 'C')
    pdf.cell(140, 5, "Sello y Fecha", 0, 1, 'C')
    pdf.set_font("Helvetica", "I", 8)
    pdf.cell(140, 5, "Instructor Responsable", 0, 0, 'C')
    pdf.cell(140, 5, "Mendoza, Argentina", 0, 1, 'C')
    
    return bytes(pdf.output())

# --- DENTRO DE LA LÓGICA DE EVALUACIÓN ---
# Supongamos que 'puntaje' es la variable del resultado final
if 'examen_finalizado' in st.session_state and st.session_state.examen_finalizado:
    puntaje = st.session_state.puntaje_final
    
    if puntaje >= 70:
        st.success(f"🏆 ¡Felicitaciones! Has aprobado con {puntaje} puntos.")
        
        # Tomamos el nombre del alumno del st.session_state (donde hiciste el login)
        nombre_usuario = st.session_state.get('nombre_alumno', 'Participante')
        
        pdf_cert = generar_certificado_pdf(nombre_usuario, puntaje)
        
        st.download_button(
            label="🎓 Descargar mi Certificado Oficial",
            data=pdf_cert,
            file_name=f"Certificado_{nombre_usuario}.pdf",
            mime="application/pdf"
        )
    else:
        st.error(f"Puntaje: {puntaje}. Se requiere un mínimo de 70 para certificar.")
        st.info("Te recomendamos revisar el Manual y volver a intentar el entrenamiento.")
