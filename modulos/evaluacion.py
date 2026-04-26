import streamlit as st
from fpdf import FPDF
import time

# Nombre de función ajustado para evitar el ImportError
def evaluacion():
    st.header("🧠 Mesa de Examen: Competencias Operativas")
    st.write("Examen técnico para la certificación oficial de **MENFA Capacitaciones**.")

    # 1. DATOS DEL ALUMNO (Interfaz basada en tu captura)
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre Completo del Alumno:", placeholder="Ej. Fabricio Pizzolato")
        with col2:
            dni = st.text_input("DNI:", placeholder="Sin puntos")

    if not nombre or not dni:
        st.warning("⚠️ Debe ingresar sus datos para habilitar el examen.")
        return

    st.divider()
    puntos = 0

    # --- BANCO DE PREGUNTAS ---
    st.markdown("#### 1. Sistema de Extracción")
    r1 = st.radio("¿A qué sistema pertenece un pozo con AIB?", ["Natural", "Bombeo Mecánico", "ESP"], index=None)
    if r1 == "Bombeo Mecánico": puntos += 10

    st.markdown("#### 2. Procesos en Planta")
    r2 = st.radio("Objetivo del Separador Trifásico:", ["Aumentar Presión", "Separar Gas, Crudo y Agua", "Filtrar Arena"], index=None)
    if r2 == "Separar Gas, Crudo y Agua": puntos += 10

    st.markdown("#### 3. Ingeniería de Producción")
    r3 = st.radio("Si la contrapresión aumenta en la línea de flujo:", ["El caudal baja", "El caudal sube", "No hay cambios"], index=None)
    if r3 == "El caudal baja": puntos += 10

    st.markdown("#### 4. Seguridad de Procesos")
    r4 = st.radio("¿Qué significa la sigla ESD?", ["Data System", "Emergency Shutdown", "Electric Drive"], index=None)
    if r4 == "Emergency Shutdown": puntos += 10

    st.markdown("#### 5. Operación de Calentadores")
    r5 = st.radio("Paso previo obligatorio antes del encendido del piloto:", ["Barrido de aire (Purge)", "Abrir gas principal", "Cerrar chimenea"], index=None)
    if r5 == "Barrido de aire (Purge)": puntos += 10

    st.markdown("#### 6. Calidad de Crudo")
    r6 = st.radio("Si el BSW es alto (5%), ¿qué equipo de planta está fallando?", ["Bomba de transferencia", "Tratador Térmico / FWKO", "Compresor de gas"], index=None)
    if r6 == "Tratador Térmico / FWKO": puntos += 10

    st.markdown("#### 7. Mantenimiento")
    r7 = st.radio("Sonido de 'piedras' en una bomba centrífuga indica:", ["Falla de motor", "Cavitación", "Exceso de aceite"], index=None)
    if r7 == "Cavitación": puntos += 10

    st.markdown("#### 8. Maniobras de Válvulas")
    r8 = st.radio("Regla de oro para cambiar un pozo de Grupo a Control:", ["Abrir primero Control, luego cerrar Grupo", "Cerrar primero Grupo, luego abrir Control"], index=None)
    if r8 == "Abrir primero Control, luego cerrar Grupo": puntos += 10

    st.markdown("#### 9. Riesgo Químico")
    r9 = st.radio("Gas altamente tóxico y corrosivo en yacimientos:", ["CO2", "H2S (Ácido Sulfhídrico)", "Nitrógeno"], index=None)
    if r9 == "H2S (Ácido Sulfhídrico)": puntos += 10

    st.markdown("#### 10. Sistemas Artificiales")
    r10 = st.radio("El Gas Lift funciona mediante:", ["Inyección de gas para alivianar la columna", "Uso de una bomba de fondo"], index=None)
    if r10 == "Inyección de gas para alivianar la columna": puntos += 10

    # --- PROCESAMIENTO FINAL ---
    st.divider()
    if st.button("Finalizar Examen y Calificar", use_container_width=True):
        if puntos >= 70:
            st.balloons()
            st.success(f"✅ EXAMEN APROBADO: {puntos}/100")
            
            # Generar PDF (Aquí llamamos a tu función de PDF)
            pdf_data = generar_certificado_pdf(nombre, dni, puntos)
            
            st.download_button(
                label="🎓 DESCARGAR CERTIFICADO OFICIAL (PDF)",
                data=pdf_data,
                file_name=f"Certificado_MENFA_{nombre.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.error(f"❌ REPROBADO: {puntos}/100. Se requiere 70 puntos para certificar.")

def generar_certificado_pdf(nombre, dni, puntaje):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    # ... (todo tu código de diseño de marcos, textos y firmas igual que antes) ...
    
    # --- CAMBIO AQUÍ PARA FPDF2 ---
    # Generamos el contenido del PDF como una cadena de bytes
    pdf_bytes = pdf.output() 
    
    # Si pdf.output() devuelve None o un objeto, forzamos la salida a bytes
    if isinstance(pdf_bytes, str):
        return pdf_bytes.encode('latin-1')
    
    return pdf_bytes

# --- DENTRO DE TU FUNCIÓN evaluacion() ---
if st.button("Finalizar Examen y Calificar", use_container_width=True):
    if puntos >= 70:
        st.balloons()
        st.success(f"✅ EXAMEN APROBADO: {puntos}/100")
        
        # Generar los bytes del PDF
        pdf_data = generar_certificado_pdf(nombre, dni, puntos)
        
        # Verificación de seguridad antes del botón
        if pdf_data:
            st.download_button(
                label="🎓 DESCARGAR CERTIFICADO OFICIAL (PDF)",
                data=pdf_data, # Aquí enviamos los bytes puros
                file_name=f"Certificado_MENFA_{nombre.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
