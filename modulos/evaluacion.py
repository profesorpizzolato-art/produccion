import streamlit as st
from fpdf import FPDF
import time

def generar_certificado_pdf(nombre_alumno, dni, puntaje):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    # --- Estética MENFA: Marco y Colores ---
    pdf.set_draw_color(243, 156, 18) # Naranja MENFA (#f39c12)
    pdf.set_line_width(3)
    pdf.rect(10, 10, 277, 190) # Marco exterior
    pdf.set_draw_color(0, 59, 70) # Azul Petróleo
    pdf.set_line_width(1)
    pdf.rect(12, 12, 273, 186) # Marco interior elegante
    
    # Encabezado con Identidad del Instituto
    pdf.set_font("Helvetica", "B", 35)
    pdf.set_text_color(243, 156, 18) # Naranja
    pdf.cell(0, 40, "MENFA CAPACITACIONES", ln=True, align='C')
    
    pdf.set_font("Helvetica", "B", 25)
    pdf.set_text_color(0, 59, 70) # Azul Petróleo
    pdf.cell(0, 10, "CERTIFICADO DE APROBACION", ln=True, align='C')
    pdf.ln(15)
    
    # Cuerpo del Certificado
    pdf.set_font("Helvetica", "", 18)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Se otorga el presente a:", ln=True, align='C')
    
    pdf.set_font("Helvetica", "B", 40)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 30, nombre_alumno.upper(), ln=True, align='C')
    
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"DNI: {dni}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Helvetica", "", 14)
    contenido = (
        f"Por haber aprobado satisfactoriamente la Evaluacion de Competencias Operativas "
        f"en el simulador IPCL MENFA 3.0 con un puntaje de {puntaje}/100. "
        "El titular demuestra conocimientos solidos en Procesos de Planta (PTC), "
        "Ingenieria de Produccion, Sistemas de Extraccion y Seguridad Operativa."
    )
    pdf.multi_cell(0, 8, txt=contenido, align='C')
    
    # Firmas y Ubicación
    pdf.ln(25)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(140, 10, "__________________________", 0, 0, 'C')
    pdf.cell(140, 10, "__________________________", 0, 1, 'C')
    pdf.cell(140, 5, "Fabricio Pizzolato", 0, 0, 'C')
    pdf.cell(140, 5, "Sello y Fecha", 0, 1, 'C')
    
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(140, 5, "Director Tecnico - MENFA", 0, 0, 'C')
    pdf.cell(140, 5, f"Mendoza, Argentina - {time.strftime('%d/%m/%Y')}", 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1')

def mostrar_evaluacion():
    st.header("🧠 Mesa de Examen: Competencias Operativas")
    st.write("Complete el examen para obtener su certificación oficial.")

    # 1. DATOS DEL ALUMNO
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre Completo del Alumno:", placeholder="Ej. Juan Perez")
        with col2:
            dni = st.text_input("DNI:", placeholder="Sin puntos")

    if not nombre or not dni:
        st.warning("⚠️ Debe ingresar sus datos para habilitar el examen.")
        return

    st.divider()
    puntos = 0

    # --- BANCO DE 10 PREGUNTAS ---
    
    # P1: AIB
    st.markdown("#### 1. Sistema de Extracción")
    r1 = st.radio("¿A qué sistema pertenece un pozo con AIB?", ["Natural", "Bombeo Mecánico", "ESP"], index=None)
    if r1 == "Bombeo Mecánico": puntos += 10

    # P2: Separador
    st.markdown("#### 2. Procesos en Planta")
    r2 = st.radio("Objetivo del Separador Trifásico:", ["Aumentar Presión", "Separar Gas, Crudo y Agua", "Filtrar Arena"], index=None)
    if r2 == "Separar Gas, Crudo y Agua": puntos += 10

    # P3: Nodal
    st.markdown("#### 3. Ingeniería de Producción")
    r3 = st.radio("Si la contrapresión aumenta en la línea de flujo:", ["El caudal baja", "El caudal sube", "No hay cambios"], index=None)
    if r3 == "El caudal baja": puntos += 10

    # P4: Seguridad
    st.markdown("#### 4. Seguridad de Procesos")
    r4 = st.radio("¿Qué significa la sigla ESD?", ["Data System", "Emergency Shutdown", "Electric Drive"], index=None)
    if r4 == "Emergency Shutdown": puntos += 10

    # P5: Calentadores
    st.markdown("#### 5. Operación de Calentadores")
    r5 = st.radio("Paso previo obligatorio antes del encendido del piloto:", ["Barrido de aire (Purge)", "Abrir gas principal", "Cerrar chimenea"], index=None)
    if r5 == "Barrido de aire (Purge)": puntos += 10

    # P6: BSW
    st.markdown("#### 6. Calidad de Crudo")
    r6 = st.radio("Si el BSW es alto (5%), ¿qué equipo de planta está fallando?", ["Bomba de transferencia", "Tratador Térmico / FWKO", "Compresor de gas"], index=None)
    if r6 == "Tratador Térmico / FWKO": puntos += 10

    # P7: Cavitación
    st.markdown("#### 7. Mantenimiento")
    r7 = st.radio("Sonido de 'piedras' en una bomba centrífuga indica:", ["Falla de motor", "Cavitación", "Exceso de aceite"], index=None)
    if r7 == "Cavitación": puntos += 10

    # P8: Manifold
    st.markdown("#### 8. Maniobras de Válvulas")
    r8 = st.radio("Regla de oro para cambiar un pozo de Grupo a Control:", ["Abrir primero Control, luego cerrar Grupo", "Cerrar primero Grupo, luego abrir Control"], index=None)
    if r8 == "Abrir primero Control, luego cerrar Grupo": puntos += 10

    # P9: H2S
    st.markdown("#### 9. Riesgo Químico")
    r9 = st.radio("Gas altamente tóxico y corrosivo en yacimientos:", ["CO2", "H2S (Ácido Sulfhídrico)", "Nitrógeno"], index=None)
    if r9 == "H2S (Ácido Sulfhídrico)": puntos += 10

    # P10: Gas Lift
    st.markdown("#### 10. Sistemas Artificiales")
    r10 = st.radio("El Gas Lift funciona mediante:", ["Inyección de gas para alivianar la columna", "Uso de una bomba de fondo"], index=None)
    if r10 == "Inyección de gas para alivianar la columna": puntos += 10

    # --- PROCESAMIENTO FINAL ---
    st.divider()
    if st.button("Finalizar Examen y Calificar", use_container_width=True):
        st.session_state.examen_listo = True
        st.session_state.puntos_finales = puntos

    if st.session_state.get('examen_listo'):
        p = st.session_state.puntos_finales
        if p >= 70:
            st.balloons()
            st.success(f"✅ EXAMEN APROBADO: {p}/100")
            
            # Generar PDF
            pdf_data = generar_certificado_pdf(nombre, dni, p)
            
            st.download_button(
                label="🎓 DESCARGAR CERTIFICADO OFICIAL (PDF)",
                data=pdf_data,
                file_name=f"Certificado_MENFA_{nombre.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.error(f"❌ REPROBADO: {p}/100. Se requiere 70 puntos para certificar.")
            st.warning("Te recomendamos volver a practicar en los módulos de entrenamiento.")
