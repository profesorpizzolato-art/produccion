import streamlit as st
from fpdf import FPDF
import time

def generar_certificado_pdf(nombre, dni, puntaje):
    # Configuración de fpdf2 para salida en bytes
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    # --- Estética MENFA ---
    pdf.set_draw_color(243, 156, 18) # Naranja MENFA
    pdf.set_line_width(3)
    pdf.rect(10, 10, 277, 190)
    
    pdf.set_font("Helvetica", "B", 35)
    pdf.set_text_color(243, 156, 18)
    pdf.cell(0, 40, "MENFA CAPACITACIONES", ln=True, align='C')
    
    pdf.set_font("Helvetica", "B", 25)
    pdf.set_text_color(0, 59, 70)
    pdf.cell(0, 10, "CERTIFICADO DE APROBACION", ln=True, align='C')
    
    pdf.set_font("Helvetica", "B", 35)
    pdf.set_text_color(20, 20, 20)
    pdf.ln(20)
    pdf.cell(0, 20, nombre.upper(), ln=True, align='C')
    
    pdf.set_font("Helvetica", "", 16)
    pdf.cell(0, 10, f"DNI: {dni}", ln=True, align='C')
    
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(0, 0, 0)
    texto_cert = f"Por haber aprobado satisfactoriamente la evaluacion IPCL MENFA 3.0 con {puntaje}/100 puntos."
    pdf.multi_cell(0, 10, txt=texto_cert, align='C')
    
    pdf.ln(20)
    pdf.cell(140, 10, "__________________________", 0, 0, 'C')
    pdf.cell(140, 10, "__________________________", 0, 1, 'C')
    pdf.cell(140, 5, "Fabricio Pizzolato", 0, 0, 'C')
    pdf.cell(140, 5, f"Mendoza, {time.strftime('%d/%m/%Y')}", 0, 1, 'C')
    
    # Retorna los bytes directamente para Streamlit
    return pdf.output()

def evaluacion():
    st.header("🧠 Mesa de Examen: Competencias Operativas")
    st.write("Examen técnico para la certificación oficial de **MENFA Capacitaciones**.")

    # 1. DATOS DEL ALUMNO (Keys únicas para evitar errores)
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre Completo del Alumno:", key="nom_eval")
        with col2:
            dni = st.text_input("DNI:", key="dni_eval")

    if not nombre or not dni:
        st.warning("⚠️ Debe ingresar sus datos para habilitar el examen.")
        return

    st.divider()
    puntos = 0

    # --- BANCO DE PREGUNTAS (Asegurate de que cada bloque sea único) ---
    st.markdown("#### 1. Sistema de Extracción")
    r1 = st.radio("¿A qué sistema pertenece un pozo con AIB?", ["Natural", "Bombeo Mecánico", "ESP"], index=None, key="q1")
    if r1 == "Bombeo Mecánico": puntos += 10

    st.markdown("#### 2. Procesos en Planta")
    r2 = st.radio("Objetivo del Separador Trifásico:", ["Aumentar Presión", "Separar Gas, Crudo y Agua", "Filtrar Arena"], index=None, key="q2")
    if r2 == "Separar Gas, Crudo y Agua": puntos += 10

    st.markdown("#### 3. Ingeniería de Producción")
    r3 = st.radio("Si la contrapresión aumenta en la línea de flujo:", ["El caudal baja", "El caudal sube", "No hay cambios"], index=None, key="q3")
    if r3 == "El caudal baja": puntos += 10

    st.markdown("#### 4. Seguridad de Procesos")
    r4 = st.radio("¿Qué significa la sigla ESD?", ["Data System", "Emergency Shutdown", "Electric Drive"], index=None, key="q4")
    if r4 == "Emergency Shutdown": puntos += 10

    st.markdown("#### 5. Operación de Calentadores")
    r5 = st.radio("Paso previo obligatorio antes del encendido del piloto:", ["Barrido de aire (Purge)", "Abrir gas principal", "Cerrar chimenea"], index=None, key="q5")
    if r5 == "Barrido de aire (Purge)": puntos += 10

    st.markdown("#### 6. Calidad de Crudo")
    r6 = st.radio("Si el BSW es alto (5%), ¿qué equipo de planta está fallando?", ["Bomba de transferencia", "Tratador Térmico / FWKO", "Compresor de gas"], index=None, key="q6")
    if r6 == "Tratador Térmico / FWKO": puntos += 10

    st.markdown("#### 7. Mantenimiento")
    r7 = st.radio("Sonido de 'piedras' en una bomba centrífuga indica:", ["Falla de motor", "Cavitación", "Exceso de aceite"], index=None, key="q7")
    if r7 == "Cavitación": puntos += 10

    st.markdown("#### 8. Maniobras de Válvulas")
    r8 = st.radio("Regla de oro para cambiar un pozo de Grupo a Control:", ["Abrir primero Control, luego cerrar Grupo", "Cerrar primero Grupo, luego abrir Control"], index=None, key="q8")
    if r8 == "Abrir primero Control, luego cerrar Grupo": puntos += 10

    st.markdown("#### 9. Riesgo Químico")
    r9 = st.radio("Gas altamente tóxico y corrosivo en yacimientos:", ["CO2", "H2S (Ácido Sulfhídrico)", "Nitrógeno"], index=None, key="q9")
    if r9 == "H2S (Ácido Sulfhídrico)": puntos += 10

    st.markdown("#### 10. Sistemas Artificiales")
    r10 = st.radio("El Gas Lift funciona mediante:", ["Inyección de gas para alivianar la columna", "Uso de una bomba de fondo"], index=None, key="q10")
    if r10 == "Inyección de gas para alivianar la columna": puntos += 10

    # --- PROCESAMIENTO FINAL (UN SOLO BOTÓN) ---
    st.divider()
    if st.button("Finalizar Examen y Calificar", use_container_width=True, key="btn_calificar_final"):
        if puntos >= 70:
            st.balloons()
            st.success(f"✅ EXAMEN APROBADO: {puntos}/100")
            
            pdf_data = generar_certificado_pdf(nombre, dni, puntos)
            
            st.download_button(
                label="🎓 DESCARGAR CERTIFICADO OFICIAL (PDF)",
                data=pdf_data,
                file_name=f"Certificado_MENFA_{nombre.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="btn_descarga_cert"
            )
        else:
            st.error(f"❌ REPROBADO: {puntos}/100. Se requiere 70 puntos para certificar.")
