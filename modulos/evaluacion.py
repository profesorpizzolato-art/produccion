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
    texto_cert = f"Por haber aprobado satisfactoriamente la evaluacion IPCL MENFA 3.0 con {puntaje}/250 puntos."
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
    st.write("Examen técnico integral para la certificación oficial de **MENFA Capacitaciones**.") [cite: 1]

    if 'motor' not in st.session_state:
        st.warning("⚠️ El motor de simulación no está inicializado. Regresá al Dashboard.")
        return

    # --- INICIALIZACIÓN DE PERSISTENCIA ---
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

    # --- PANTALLA DE RESULTADO CONGELADO ---
    if st.session_state.examen_calculado:
        st.divider()
        puntos = st.session_state.puntos_finales
        
        if puntos >= 175: # 70% de 250 puntos posibles
            st.balloons()
            st.success(f"🎉 ¡FELICITACIONES! EXAMEN APROBADO: {puntos} / 250 puntos.") [cite: 3]
            
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
            st.error(f"❌ REPROBADO: {puntos} / 250 puntos. Se requiere un mínimo de 175 puntos (70%) para certificar.") [cite: 3]
        
        if st.session_state.bitacora_errores:
            st.subheader("📋 Desvíos Operativos Detectados")
            st.write("Durante la simulación de crisis se registraron las siguientes anomalías por decisiones incorrectas:")
            for err in st.session_state.bitacora_errores:
                st.caption(f"• {err}")

        # Sección de Debate y Cierre en base a tu Escenario 15
        st.markdown("---")
        st.subheader("🗣️ Bloque 3: Cierre y Debate de Causa Raíz") [cite: 105, 106]
        st.info("**Pregunta del Taller:** ¿Cuál fue la clave para resolver la situación crítica en la planta?") [cite: 103]
        st.text_area("Análisis escrito del Alumno (Monitoreo, tendencias, comunicación, trabajo en equipo):", key="debate_alumno_prod") [cite: 104]
        
        st.markdown(f"""
        > 💡 *“En la operación real, las instalaciones hablan mediante presiones, niveles, temperaturas y caudales. El operador que sabe interpretar esas señales toma mejores decisiones antes de que aparezcan los problemas.”* [cite: 107]
        """)

        if st.button("🔄 Rendir Examen de Nuevo"):
            st.session_state.examen_calculado = False
            st.session_state.puntos_finales = 0
            st.session_state.bitacora_errores = []
            st.session_state.motor.reset_planta()
            st.rerun()
        return

    # --- INTERFAZ DEL EXAMEN ACTIVO ---
    st.divider()
    tab_teoria, tab_simulador = st.tabs(["📝 Bloque 1: Cuestionario Técnico", "🕹️ Bloque 2: Toma de Decisiones Operativas"])
    
    # --- BLOQUE 1: CUESTIONARIO TEÓRICO BASE ---
    with tab_teoria:
        st.markdown("### Evaluación de Conceptos Clave (10 pts c/u)")
        
        st.markdown("#### 1. Sistema de Extracción")
        r1 = st.radio("¿A qué sistema pertenece un pozo con AIB?", ["Natural", "Bombeo Mecánico", "ESP"], index=None, key="q1")

        st.markdown("#### 2. Procesos en Planta")
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

    # --- BLOQUE 2: SECUENCIA COMPLETA DEL WORD (ESCENARIOS 1 AL 14) ---
    with tab_simulador:
        st.markdown("### Escenarios de Simulación en Planta de Proceso (10 pts c/u)") [cite: 2]
        st.caption("Monitoreá las variables del Core. Decisiones incorrectas desestabilizarán el sistema físico.")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Presión Monitoreada (Core)", f"{st.session_state.motor.presion:.2f} PSI")
        with col_m2:
            st.metric("Caudal de Planta actual", f"{st.session_state.motor.caudal_base:.2f} m³/d")
            
        st.markdown("---")
        
        st.markdown("#### Escenario 1 - Inicio de turno") [cite: 4]
        st.info("Llegás a la planta y un operador informa una vibración inusual en la bomba de transferencia.") [cite: 5]
        r11 = st.radio("Selección de maniobra (E1):", ["A) Ignorar el comentario", "B) Pedir datos de vibración y revisar historial", "C) Parar inmediatamente la planta", "D) Esperar una alarma"], index=None, key="q11") [cite: 6, 7, 8, 9]
        
        st.markdown("#### Escenario 2 - La vibración aumenta") [cite: 11]
        st.info("Se confirma un aumento gradual de vibración.") [cite: 12]
        r12 = st.radio("Selección de maniobra (E2):", ["A) Analizar alineación y estado mecánico", "B) Aumentar velocidad", "C) Reducir presión del separador", "D) Ignorar"], index=None, key="q12") [cite: 13, 14, 15, 16]
        
        st.markdown("#### Escenario 3 - Problema de gas") [cite: 18]
        st.info("El caudal de gas cae y la presión del separador aumenta.") [cite: 19]
        r13 = st.radio("Selección de maniobra (E3):", ["A) Verificar válvula de control de gas", "B) Revisar tanque", "C) Revisar calidad del petróleo", "D) Revisar sistema contra incendios"], index=None, key="q13") [cite: 20, 21, 22, 23]
        
        st.markdown("#### Escenario 4 - Ruido extraño") [cite: 25]
        st.info("Se escuchan golpeteos en una válvula.") [cite: 26]
        r14 = st.radio("Selección de maniobra (E4):", ["A) Golpear la válvula", "B) Revisar tendencias operativas", "C) Ignorar", "D) Abrir todas las válvulas"], index=None, key="q14") [cite: 27, 28, 29, 30]
        
        st.markdown("#### Escenario 5 - Alta presión") [cite: 32]
        st.info("La presión continúa aumentando.") [cite: 33]
        r15 = st.radio("Selección de maniobra (E5):", ["A) Revisar causa", "B) Esperar", "C) Aumentar producción", "D) Desactivar alarmas"], index=None, key="q15") [cite: 34, 35, 36, 37]
        
        st.markdown("#### Escenario 6 - Uso del bypass") [cite: 39]
        st.info("La válvula principal responde lentamente.") [cite: 40]
        r16 = st.radio("Selección de maniobra (E6):", ["A) Implementar bypass controlado", "B) Nada", "C) Forzar válvula", "D) Cerrar instalación"], index=None, key="q16") [cite: 41, 42, 43, 44]
        
        st.markdown("#### Escenario 7 - Nivel alto en separador") [cite: 46]
        st.info("El nivel llega al 85%.") [cite: 47]
        r17 = st.radio("Selección de maniobra (E7):", ["A) Verificar instrumentación de nivel", "B) Color del tanque", "C) Viento", "D) Iluminación"], index=None, key="q17") [cite: 48, 49, 50, 51]
        
        st.markdown("#### Escenario 8 - Arrastre de líquidos") [cite: 53]
        st.info("Aparece líquido en la línea de gas.") [cite: 54]
        r18 = st.radio("Selección de maniobra (E8):", ["A) Riesgo de daño aguas abajo", "B) Ninguno", "C) Menor consumo", "D) Mejor separación"], index=None, key="q18") [cite: 55, 56, 57, 58]
        
        st.markdown("#### Escenario 9 - Caída de producción") [cite: 60]
        st.info("Un pozo cae de 150 a 90 m³/d.") [cite: 61]
        r19 = st.radio("Selección de maniobra (E9):", ["A) Restricción", "B) Fantasmas", "C) Clima", "D) Ninguna"], index=None, key="q19") [cite: 62, 63, 64, 65]
        
        st.markdown("#### Escenario 10 - Falla eléctrica") [cite: 67]
        st.info("Una bomba se detiene inesperadamente.") [cite: 68]
        r20 = st.radio("Selección de maniobra (E10):", ["A) Revisar alimentación eléctrica", "B) Comprar otra", "C) Reiniciar varias veces", "D) Esperar"], index=None, key="q20") [cite: 69, 70, 71, 72]
        
        st.markdown("#### Escenario 11 - Alarma de alta presión") [cite: 74]
        st.info("Se activa una alarma.") [cite: 75]
        r21 = st.radio("Selección de maniobra (E11):", ["A) Confirmar lectura", "B) Ignorar", "C) Apagar alarma", "D) Continuar"], index=None, key="q21") [cite: 76, 77, 78, 79]
        
        st.markdown("#### Escenario 12 - Válvula reparada") [cite: 81]
        st.info("Finalizó el mantenimiento.") [cite: 82]
        r22 = st.radio("Selección de maniobra (E12):", ["A) Realizar prueba funcional", "B) Arrancar directo", "C) Ignorar procedure", "D) Desconectar instrumentos"], index=None, key="q22") [cite: 83, 84, 85, 86]
        
        st.markdown("#### Escenario 13 - Fin del evento") [cite: 88]
        st.info("La situación vuelve a la normalidad.") [cite: 89]
        r23 = st.radio("Selección de maniobra (E13):", ["A) Elaborar informe técnico", "B) Nada", "C) Borrar registros", "D) Olvidar incidente"], index=None, key="q23") [cite: 90, 91, 92, 93]
        
        st.markdown("#### Escenario 14 - Lecciones aprendidas") [cite: 95]
        st.info("Documentación posterior al evento.") [cite: 96]
        r24 = st.radio("Selección de maniobra (E14):", ["A) Evitar repetición", "B) Costumbre", "C) Archivo", "D) Sin motivo"], index=None, key="q24") [cite: 97, 98, 99, 100]


    # --- EVALUACIÓN GENERAL DE RESPUESTAS ---
    st.divider()
    if st.button("Finalizar Examen y Calificar", use_container_width=True, key="btn_calificar_final"):
        
        # Validamos que no queden casilleros vacíos
        respuestas_t1 = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10]
        respuestas_t2 = [r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24]
        
        if None in respuestas_t1 or None in respuestas_t2:
            st.error("⚠️ No podés procesar la entrega. Faltan responder preguntas o escenarios en las pestañas.")
            return
            
        puntos_acumulados = 0
        bitacora = []
        
        # Corrección Bloque Técnico (10 c/u)
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
        
        # Corrección Bloque Operativo Simulador (10 c/u)
        if "B)" in r11: puntos_acumulados += 10 [cite: 10]
        else: bitacora.append("Escenario 1: Ignorar la vibración reportada incrementó el riesgo de daño en la bomba.") [cite: 5, 6]
            
        if "A)" in r12: puntos_acumulados += 10 [cite: 17]
        else: bitacora.append("Escenario 2: No analizar la alineación aceleró la inestabilidad mecánica del sistema.") [cite: 12, 13]
            
        if "A)" in r13: puntos_acumulados += 10 [cite: 24]
        else: 
            bitacora.append("Escenario 3: No verificar la válvula de control (PCV) generó un pico de presión brusco.") [cite: 19, 20]
            st.session_state.motor.simular_golpe_de_gas()
            
        if "B)" in r14: puntos_acumulados += 10 [cite: 31]
        else: bitacora.append("Escenario 4: Los golpeteos requerían un análisis profundo de tendencias operativas.") [cite: 26, 28]
            
        if "A)" in r15: puntos_acumulados += 10 [cite: 38]
        else: 
            bitacora.append("Escenario 5: No buscar la causa raíz ante un aumento sostenido saturó la línea.") [cite: 33, 34]
            st.session_state.motor.simular_golpe_de_gas()
            
        if "A)" in r16: puntos_acumulados += 10 [cite: 45]
        else: bitacora.append("Escenario 6: La respuesta lenta de la válvula principal requería un bypass controlado.") [cite: 40, 41]
            
        if "A)" in r17: puntos_acumulados += 10 [cite: 52]
        else: bitacora.append("Escenario 7: Un nivel al 85% exige contrastar la instrumentación de medición campo-lazo.") [cite: 47, 48]
            
        if "A)" in r18: puntos_acumulados += 10 [cite: 59]
        else: bitacora.append("Escenario 8: El arrastre latente de líquidos expone a daños críticos a los compresores aguas abajo.") [cite: 54, 55]
            
        if "A)" in r19: puntos_acumulados += 10 [cite: 66]
        else: bitacora.append("Escenario 9: La caída abrupta de 150 a 90 m³/d sugería una restricción física o estrangulamiento.") [cite: 61, 62]
            
        if "A)" in r20: puntos_acumulados += 10 [cite: 73]
        else: bitacora.append("Escenario 10: La detención imprevista exigía el chequeo prioritario del lazo eléctrico.") [cite: 68, 69]
            
        if "A)" in r21: puntos_acumulados += 10 [cite: 80]
        else: bitacora.append("Escenario 11: Ante alarmas de alta presión, la primera regla es validar la lectura.") [cite: 75, 76]
            
        if "A)" in r22: puntos_acumulados += 10 [cite: 87]
        else: bitacora.append("Escenario 12: Arrancar sin prueba funcional post-mantenimiento viola el protocolo de seguridad.") [cite: 82, 83]
            
        if "A)" in r23: puntos_acumulados += 10 [cite: 94]
        else: bitacora.append("Escenario 13: El cierre formal de un evento requiere obligatoriamente un informe técnico.") [cite: 89, 90]
            
        if "A)" in r24: puntos_acumulados += 10 [cite: 101]
        else: bitacora.append("Escenario 14: Documentar las lecciones aprendidas es la única vía para mitigar repeticiones.") [cite: 96, 97]

        # Guardado y congelamiento de estado
        st.session_state.puntos_finales = puntos_acumulados
        st.session_state.bitacora_errores = bitacora
        st.session_state.examen_calculado = True
        st.rerun()
