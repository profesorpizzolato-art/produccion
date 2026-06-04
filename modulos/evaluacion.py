import streamlit as st
from fpdf import FPDF
import time

def generar_certificado_pdf(nombre, dni, puntaje):
    # Configuramos fpdf2 en modo Landscape
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    # --- 1. LOGO INSTITUCIONAL ---
    try:
        pdf.image("assets/logo_menfa.png", x=123.5, y=12, w=50) 
        pdf.ln(58) # Espacio después del logo
    except Exception as e:
        pdf.ln(50)

    # --- 2. MARCO NARANJA ---
    pdf.set_draw_color(243, 156, 18) 
    pdf.set_line_width(3)
    pdf.rect(10, 10, 277, 190)
    
    # --- 3. TÍTULOS ---
    pdf.set_font("Helvetica", "B", 35)
    pdf.set_text_color(243, 156, 18)
    pdf.cell(0, 15, "MENFA CAPACITACIONES", ln=True, align='C')
    
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(0, 59, 70) 
    pdf.cell(0, 12, "CERTIFICADO DE APROBACION", ln=True, align='C')
    
    pdf.ln(10) 
    
    # --- 4. DATOS DEL ALUMNO ---
    pdf.set_font("Helvetica", "B", 35)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 20, nombre.upper(), ln=True, align='C')
    
    pdf.set_font("Helvetica", "", 16)
    pdf.cell(0, 10, f"DNI: {dni}", ln=True, align='C')
    
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(0, 0, 0)
    texto_cert = f"Por haber aprobado satisfactoriamente la evaluacion IPCL MENFA 3.0 con {puntaje}/150 puntos."
    pdf.multi_cell(0, 10, txt=texto_cert, align='C')
    
    # --- 5. SECCIÓN DE FIRMAS ---
    pdf.ln(15) 
    
    # Columna Izquierda: Firma del Director
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(140, 10, "__________________________", 0, 0, 'C')
    # Columna Derecha: Fecha y Lugar
    pdf.cell(140, 10, "__________________________", 0, 1, 'C')
    
    # Nombres y Cargos
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(140, 5, "Fabricio Pizzolato", 0, 0, 'C')
    pdf.cell(140, 5, "Mendoza, Argentina", 0, 1, 'C')
    
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(140, 5, "Director Tecnico - MENFA", 0, 0, 'C')
    pdf.cell(140, 5, f"Fecha de emision: {time.strftime('%d/%m/%Y')}", 0, 1, 'C')
    
    return bytes(pdf.output())

def evaluacion():
    st.header("🧠 Mesa de Examen: Competencias Operativas")
    st.write("Examen técnico integral para la certificación oficial de **MENFA Capacitaciones**.")

    if 'motor' not in st.session_state:
        st.warning("⚠️ El motor de simulación no está inicializado. Regresá al Dashboard.")
        return

    # --- INICIALIZACIÓN DE PERSISTENCIA PARA EVITAR REBUILDS DE STREAMLIT ---
    if 'examen_calculado' not in st.session_state:
        st.session_state.examen_calculado = False
    if 'puntos_finales' not in st.session_state:
        st.session_state.puntos_finales = 0
    if 'bitacora_errores' not in st.session_state:
        st.session_state.bitacora_errores = []

    # 1. DATOS DEL ALUMNO
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre Completo del Alumno:", key="nom_eval")
        with col2:
            dni = st.text_input("DNI:", key="dni_eval")

    if not nombre or not dni:
        st.warning("⚠️ Debe ingresar sus datos para habilitar la mesa de examen.")
        return

    # Si el examen ya fue evaluado, bloqueamos la pantalla y mostramos el resultado definitivo
    if st.session_state.examen_calculado:
        st.divider()
        puntos = st.session_state.puntos_finales
        # El examen ahora suma sobre 150 puntos (100 de teoría + 50 de simulador)
        if puntos >= 105: # El 70% de 150
            st.balloons()
            st.success(f"🎉 ¡FELICITACIONES! EXAMEN APROBADO: {puntos} / 150 puntos.")
            
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
            st.error(f"❌ REPROBADO: {puntos} / 150 puntos. Se requiere un mínimo de 105 puntos (70%) para certificar.")
        
        if st.session_state.bitacora_errores:
            st.subheader("📋 Desvío Técnico Detectado")
            st.write("Durante la simulación de crisis se registraron los siguientes eventos desfavorables:")
            for err in st.session_state.bitacora_errores:
                st.caption(f"• {err}")

        if st.button("🔄 Rendir Examen de Nuevo"):
            st.session_state.examen_calculado = False
            st.session_state.puntos_finales = 0
            st.session_state.bitacora_errores = []
            st.session_state.motor.reset_planta()
            st.rerun()
        return

    # --- INTERFAZ DEL EXAMEN ACTIVO ---
    st.divider()
    
    tab_teoria, tab_simulador = st.tabs(["📝 Bloque 1: Cuestionario Técnico", "🕹️ Bloque 2: Gestión de Crisis Operativa"])
    
    # --- BLOQUE 1: TU BANCO DE PREGUNTAS ORIGINALES ---
    with tab_teoria:
        st.markdown("### Evaluación de Conceptos Clave (10 pts c/u)")
        
        st.markdown("#### 1. Sistema de Extracción")
        r1 = st.radio("¿A qué sistema pertenece un pozo con AIB?", ["Natural", "Bombeo Mecánico", "ESP"], index=None, key="q1")

        st.markdown("#### 2. Processes en Planta")
        r2 = st.radio("Objetivo del Separador Trifásico:", ["Aumentar Presión", "Separar Gas, Crudo y Agua", "Filtrar Arena"], index=None, key="q2")

        st.markdown("#### 3. Ingeniería de Producción")
        r3 = st.radio("Si la contrapresión aumenta en la línea de flujo:", ["El caudal baja", "El caudal sube", "No hay cambios"], index=None, key="q3")

        st.markdown("#### 4. Seguridad de Procesos")
        r4 = st.radio("¿Qué significa la sigla ESD?", ["Data System", "Emergency Shutdown", "Electric Drive"], index=None, key="q4")

        st.markdown("#### 5. Operación de Calentadores")
        r5 = st.radio("Paso previo obligatorio antes del encendido del piloto:", ["Barrido de aire (Purge)", "Abrir gas principal", "Cerrar chimenea"], index=None, key="q5")

        st.markdown("#### 6. Calidad de Crudo")
        r6 = st.radio("Si el BSW es alto (5%), ¿qué equipo de planta está fallando?", ["Bomba de transferencia", "Tratador Térmico / FWKO", "Compresor de gas"], index=None, key="q6")

        st.markdown("#### 7. Mantenimiento")
        r7 = st.radio("Sonido de 'piedras' en una bomba centrífuga indica:", ["Falla de motor", "Cavitación", "Exceso de aceite"], index=None, key="q7")

        st.markdown("#### 8. Maniobras de Válvulas")
        r8 = st.radio("Regla de oro para cambiar un pozo de Grupo a Control:", ["Abrir primero Control, luego cerrar Grupo", "Cerrar primero Grupo, luego abrir Control"], index=None, key="q8")

        st.markdown("#### 9. Riesgo Químico")
        r9 = st.radio("Gas altamente tóxico y corrosivo en yacimientos:", ["CO2", "H2S (Ácido Sulfhídrico)", "Nitrógeno"], index=None, key="q9")

        st.markdown("#### 10. Sistemas Artificiales")
        r10 = st.radio("El Gas Lift funciona mediante:", ["Inyección de gas para alivianar la columna", "Uso de una bomba de fondo"], index=None, key="q10")

    # --- BLOQUE 2: NUEVO ENTORNO DE TOMA DE DECISIONES OPERATIVAS ---
    with tab_simulador:
        st.markdown("### Escenarios Dinámicos en Planta de Proceso (10 pts c/u)")
        st.caption("Nota: Las decisiones incorrectas desestabilizarán el Motor de Simulación en tiempo real.")
        
        # Estado actual del motor en cabecera del bloque para que el alumno use el criterio técnico
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Presión de Separador en Línea", f"{st.session_state.motor.presion:.2f} PSI")
        with col_m2:
            st.metric("Caudal de Planta actual", f"{st.session_state.motor.caudal_base:.2f} m³/d")
            
        st.markdown("---")
        
        st.markdown("#### 11. Escenario de Inicio de Turno")
        st.info("Llegás a la planta y un operador informa una vibración inusual en la bomba de transferencia.")
        r11 = st.radio("Acción inmediata:", ["A) Ignorar el comentario", "B) Pedir datos de vibración y revisar historial", "C) Parar inmediatamente la planta", "D) Esperar una alarma"], index=None, key="q11")
        
        st.markdown("#### 12. Escenario de Inestabilidad Mecánica")
        st.info("Se confirma un aumento gradual de vibración en el equipo rotativo de despacho.")
        r12 = st.radio("Estrategia correctiva:", ["A) Analizar alineación y estado mecánico", "B) Aumentar velocidad", "C) Reducir presión del separador", "D) Ignorar"], index=None, key="q12")
        
        st.markdown("#### 13. Escenario de Caída de Gas")
        st.info("El caudal de gas cae de golpe y la presión interna del separador aumenta de manera peligrosa.")
        r13 = st.radio("Maniobra de control:", ["A) Verificar válvula de control de gas (PCV)", "B) Revisar tanque de almacenamiento", "C) Revisar calidad del petróleo", "D) Revisar sistema contra incendios"], index=None, key="q13")
        
        st.markdown("#### 14. Escenario de Anomalía Sonora")
        st.info("Se escuchan golpeteos metálicos y pulsaciones severas dentro de una línea acoplada a una válvula de control.")
        r14 = st.radio("Procedimiento diagnóstico:", ["A) Golpear la válvula físicamente", "B) Revisar tendencias operativas en el SCADA", "C) Ignorar la anomalía", "D) Abrir todas las válvulas"], index=None, key="q14")
        
        st.markdown("#### 15. Escenario de Control de Presión Crítica")
        st.info("La presión del separador rompe la tendencia normal y continúa aumentando de forma crítica sin detenerse.")
        r15 = st.radio("Acción de resguardo:", ["A) Revisar causa raíz de inmediato", "B) Esperar a ver si se normaliza sola", "C) Aumentar producción de pozos entrantes", "D) Desactivar alarmas operativas"], index=None, key="q15")

    # --- PROCESAMIENTO FINAL ---
    st.divider()
    if st.button("Finalizar Examen y Calificar", use_container_width=True, key="btn_calificar_final"):
        # Verificación obligatoria de completitud
        respuestas_teoria = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10]
        respuestas_simulador = [r11, r12, r13, r14, r15]
        
        if None in respuestas_teoria or None in respuestas_simulador:
            st.error("⚠️ No podés entregar el examen. Hay preguntas o escenarios sin responder en alguna de las dos pestañas.")
            return
            
        puntos_acumulados = 0
        bitacora = []
        
        # Calificación del bloque teórico
        if r1 == "Bombeo Mecánico": puntos_acumulados += 10
        if r2 == "Separar Gas, Crudo y Agua": puntos_acumulados += 10
        if r3 == "El caudal baja": puntos_acumulados += 10
        if r4 == "Emergency Shutdown": puntos_acumulados += 10
        if r5 == "Barrido de aire (Purge)": puntos_acumulados += 10
        if r6 == "Tratador Térmico / FWKO": puntos_acumulados += 10
        if r7 == "Cavitación": puntos_acumulados += 10
        if r8 == "Abrir primero Control, luego cerrar Grupo": puntos_acumulados += 10
        if r9 == "H2S (Ácido Sulfhídrico)": puntos_acumulados += 10
        if r10 == "Inyección de gas para alivianar la columna": puntos_acumulados += 10
        
        # Calificación y simulación física del bloque operativo
        if "B)" in r11: puntos_acumulados += 10
        else: bitacora.append("Escenario 11: Ignorar vibraciones mecánicas latentes puso en peligro el tren de despacho.")
            
        if "A)" in r12: puntos_acumulados += 10
        else: bitacora.append("Escenario 12: No analizar la alineación mecánica arriesgó un daño estructural severo.")
            
        if "A)" in r13: puntos_acumulados += 10
        else:
            bitacora.append("Escenario 13: Error al no verificar la PCV de gas. Se gatilló sobrapresión en el sistema.")
            st.session_state.motor.simular_golpe_de_gas() # Desestabiliza el motor físico real
            
        if "B)" in r14: puntos_acumulados += 10
        else: bitacora.append("Escenario 14: La falta de análisis de tendencias SCADA ocultó problemas erosivos en válvulas.")
            
        if "A)" in r15: puntos_acumulados += 10
        else:
            bitacora.append("Escenario 15: No buscar la causa raíz en alta presión forzó un evento inestable en el separador.")
            st.session_state.motor.simular_golpe_de_gas() # Desestabiliza el motor físico real

        # Guardamos todo en la sesión para congelar el resultado
        st.session_state.puntos_finales = puntos_acumulados
        st.session_state.bitacora_errores = bitacora
        st.session_state.examen_calculado = True
        st.rerun()
