import streamlit as st
from fpdf import FPDF
import time

def generar_certificado_pdf(nombre, dni, puntaje):
    # Configuramos fpdf2 en modo Paisaje (Landscape)
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    # --- 1. LOGOTIPO INSTITUCIONAL ---
    try:
        pdf.image("assets/logo_menfa.png", x=123.5, y=12, w=50)
        pdf.ln(58) 
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
    texto_cert = f"Por haber aprobado satisfactoriamente la evaluación IPCL MENFA 3.0 con {puntaje}/180 puntos."
    pdf.multi_cell(0, 10, txt=texto_cert, align='C')
    
    # --- 5. SECCIÓN DE FIRMAS ---
    pdf.ln(15)
    
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(140, 10, "__________________________", 0, 0, 'C')
    pdf.cell(140, 10, "__________________________", 0, 1, 'C')
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(140, 5, "Fabricio Pizzolato", 0, 0, 'C')
    pdf.cell(140, 5, "Mendoza, Argentina", 0, 1, 'C')
    
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(140, 5, "Director Técnico - MENFA", 0, 0, 'C')
    pdf.cell(140, 5, f"Fecha de emisión: {time.strftime('%d/%m/%Y')}", 0, 1, 'C')
    
    return bytes(pdf.output())

def evaluacion():
    st.header("🧠 Mesa de Examen: Competencias Operativas Avanzadas")
    st.write("Examen técnico de planta e ingeniería de procesos para la certificación oficial de **MENFA Capacitaciones**.")

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
        st.warning("⚠️ Debe ingresar sus datos personales (Nombre y DNI) para habilitar los reactivos de examen.")
        return

    # --- PANTALLA DE RESULTADO CONGELADO (POST-ENTREGA) ---
    if st.session_state.examen_calculado:
        st.divider()
        puntos = st.session_state.puntos_finales
        
        if puntos >= 126: 
            st.balloons()
            st.success(f"🎉 ¡FELICITACIONES! EXAMEN APROBADO: {puntos} / 180 puntos.")
            
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
            st.error(f"❌ REPROBADO: {puntos} / 180 puntos. Se requiere un mínimo de 126 puntos (70%) para certificar.")
        
        if st.session_state.bitacora_errores:
            st.subheader("📋 Desvíos Operativos Detectados en Simulador")
            for err in st.session_state.bitacora_errores:
                st.caption(f"• {err}")

        st.markdown("---")
        st.subheader("🗣️ Bloque de Cierre y Análisis de Causa Raíz")
        st.info("**Pregunta de Taller:** ¿Cuál es el criterio analítico clave para mitigar las paradas imprevistas (ESD) en una estación de producción?")
        st.text_area("Análisis escrito por el Operador (Tendencias de SCADA, control químico y preventivo):", key="debate_alumno_prod")
        return

    # --- BIBLIOTECA TÉCNICA DE REFERENCIA ---
    with st.expander("📚 BIBLIOTECA TÉCNICA DE REFERENCIA (Manual de Operaciones MENFA 3.0)", expanded=False):
        st.markdown("### 🎛️ 1. Formulación Hidráulica: Ecuación de NPSH y Cavitación")
        st.write("Para garantizar que una bomba centrífuga no sufra daños catastróficos por cavitación, el operador en consola debe monitorear constantemente que el **NPSH Disponible** ($NPSH_D$) en el sistema sea mayor al **NPSH Requerido** ($NPSH_R$):")
        st.latex(r"NPSH_D = P_{succ\_abs} - P_{vapor\_abs}")
        st.markdown("""
        * Si $NPSH_D \le NPSH_R$, las burbujas de vapor implotarán al entrar al impulsor, arrancando el acero por fatiga mecánica micro-local.
        * **Acción correctiva:** Estrangular la descarga desplaza el punto operativo reduciendo drásticamente el $NPSH_R$.
        """)
        
        st.write("---")
        st.markdown("### 🧪 2. Dinámica Química de Emulsiones (Ley de Stokes)")
        st.write("La velocidad de separación gravitacional de las gotas de agua dentro de un Tratador Térmico responde a la Ley de Stokes:")
        st.latex(r"v = \frac{2 \cdot g \cdot r^2 \cdot (\rho_{agua} - \rho_{crudo})}{9 \cdot \mu}")
        st.markdown("""
        * **Criterio de Control:** Para acelerar la velocidad de decantación ($v$), el operador debe aumentar la temperatura para reducir la viscosidad ($\mu$) o inyectar desemulsionante para aumentar el radio de la gota ($r$).
        """)
        
        st.write("---")
        st.markdown("### ☣️ 3. Umbrales de Exposición Letal por $H_2S$")
        st.table([
            {"Concentración (ppm)": "0.1 - 5 ppm", "Efecto Fisiológico": "Olor a huevo podrido. Umbral de percepción.", "Acción Requerida": "Monitoreo preventivo."},
            {"Concentración (ppm)": "10 ppm", "Efecto Fisiológico": "Límite Máximo de Exposición Permisible (TWA) para 8 hs.", "Acción Requerida": "Evacuación si no hay ventilación."},
            {"Concentración (ppm)": "100 ppm", "Efecto Fisiológico": "Parálisis inmediata del nervio olfativo. Deja de oler.", "Acción Requerida": "🚨 Evacuación inmediata con uso de ERA."},
        ])

    # --- PANTALLAS DE EXAMEN ACTIVO ---
    tab1, tab2 = st.tabs(["📝 Bloque 1: Ingeniería y Conceptos Fundamentales", "🎛️ Bloque 2: Casos de Campo y Diagnóstico SCADA"])

    with tab1:
        st.markdown("### Examen Teórico de Producción Petrolera")
        
        r1 = st.radio("**1. ¿Qué sistema de extracción artificial utiliza un árbol de surgencia acoplado a una sarta de varillas y una bomba de profundidad?**", 
                      ["Surgencia Natural", "Bombeo Mecánico", "Plunger Lift", "Gas Lift"], key="r1_ev")
        
        r2 = st.radio("**2. ¿Cuál es el objetivo termodinámico principal de un separador de producción bifásico o trifásico?**", 
                      ["Aumentar la presión del sistema", "Separar Gas, Crudo y Agua", "Deshidratar el gas por glicol", "Fraccionar las cadenas de hidrocarburos"], key="r2_ev")
        
        r3 = st.radio("**3. Si se presenta un taponamiento por parafinas rígidas en la línea de flujo de un pozo, ¿qué ocurre en la SCADA?**", 
                      ["La presión del colector aumenta", "El caudal baja y la presión de línea aguas arriba del bloqueo se incrementa", "El BSW se eleva drásticamente", "El motor eléctrico reduce su consumo"], key="r3_ev")
        
        r4 = st.radio("**4. ¿Qué acción mandatoria ejecuta automáticamente un lazo instrumentado de seguridad ante la condición PSHH (Presión Muy Alta Alta) en un separador?**", 
                      ["Apertura de válvulas de venteo", "Apagado de Emergencia (ESD Nivel 1 o 2)", "Encendido de bombas auxiliares", "Cierre manual del estrangulador"], key="r4_ev")
        
        r5 = st.radio("**5. ¿Qué procedimiento de seguridad se efectúa antes de ingresar hidrocarburos a una línea nueva o intervenida para evitar mezclas explosivas?**", 
                      ["Prueba hidrostática de ruptura", "Barrido de aire (Purge) con gas inerte o nitrógeno", "Calentamiento de la tubería", "Lavado con sosa cáustica"], key="r5_ev")
        
        r6 = st.radio("**6. ¿Qué equipo dinámico o térmico de superficie se utiliza para romper emulsiones duras W/O mediante coalescencia térmica y química?**", 
                      ["Separador de Prueba", "Tratador Térmico / FWKO", "Bomba de Cavidad Progresiva", "Tanque de Almacenamiento Atmosférico"], key="r6_ev")
        
        r7 = st.radio("**7. ¿Qué fenómeno destructivo ocurre si la presión estática del crudo cae por debajo de su presión de vapor en el ojo del impulsor de una bomba?**", 
                      ["Corrosión galvánica", "Cavitación", "Flujo bifásico estable", "Fragilización por azufre"], key="r7_ev")
        
        r8 = st.radio("**8. Para alinear un pozo desde el Manifold local al colector general sin generar golpes de ariete mecánicos, ¿cuál es el orden correcto?**", 
                      ["Abrir primero Control, luego cerrar Grupo", "Cerrar Grupo y esperar 30 minutos", "Abrir Grupo antes de cerrar la línea de bypass", "Cerrar la válvula de retención"], key="r8_ev")
        
        r9 = st.radio("**9. ¿Qué compuesto químico gaseoso altamente letal se asocia al crudo agrio y bloquea el sistema respiratorio humano destruyendo el olfato?**", 
                      ["CO2", "H2S (Ácido Sulfhídrico)", "Metano puro", "Sulfato de bario"], key="r9_ev")
        
        r10 = st.radio("**10. ¿Cuál es el principio operativo básico del sistema de levantamiento artificial por Gas Lift (Planta de Inyección)?**", 
                       ["Aumentar el peso del crudo", "Inyección de gas para aliviar la columna hidrostática en el tubing", "Sellar las perforaciones de fondo", "Generar vacío mecánico"], key="r10_ev")

        r15 = st.radio("**11. ¿Qué fenómeno ocurre en una línea de flujo bifásico cuando el gas empuja al líquido en forma de tapones o baches violentos, generando transitorios de alta presión?**",
                       ["Flujo Anular", "Flujo Slug (Baches de líquido)", "Flujo Estratificado Liso", "Flujo de Burbujas Dispersas"], key="r15_ev")

        r16 = st.radio("**12. Al operar un compresor alternativo de gas, ¿cuál es la función de los tanques amortiguadores (*Pulsation Dampeners*) colocados en la succión y descarga?**",
                       ["Separar el BSW remanente", "Aumentar la relación de compresión isotérmica", "Atenuar las ondas de pulsación y vibraciones mecánicas generadas por el movimiento recíprocante del pistón", "Enfriar el gas mediante expansión Joule-Thomson"], key="r16_ev")

        r17 = st.radio("**13. Si el lazo de control de presión de un separador (PV) se descalibra y la válvula de control se cierra por completo (*Fail Close*), ¿cuál es la secuencia de alarmas en el SCADA?**",
                       ["Caída de presión, LSL y posterior parada por ESD", "PSH (Alerta de Presión Alta), PSHH (Presión Muy Alta Alta) y disparo automático de la válvula de seguridad por SIS", "Aumento instantáneo del BSW en el tratador", "Disparo térmico del motor de transferencia de crudo"], key="r17_ev")

        r18 = st.radio("**14. ¿Qué parámetro químico mide la agresividad corrosiva del agua de producción asociada que ataca el acero al carbono por picaduras (*pitting*) en los oleoductos?**",
                       ["Concentración de Cloruros y presencia de bacterias sulfato-reductoras (BSR)", "Porcentaje de parafinas disueltas", "Grados API del crudo estabilizado", "Índice de refracción del metano"], key="r18_ev")

    with tab2:
        st.markdown("### Casos de Estudio y Análisis bajo Presión")
        
        st.info("**Caso A: Crisis de Deshidratación (BSW)**\n\nEl deshidratador electrostático procesa $1200\\text{ m}^3/\\text{d}$. El BSW sube del **15% al 42%** por el pozo MENFA-02. El transformador tiene picos de cortocircuito por alta salinidad.")
        r11 = st.radio("**15. ¿Cuál es la primera intervención en sala de control?**", 
                       ["A) Incrementar el voltaje del campo eléctrico.", "B) Desviar fluidos al Test Tank, ajustar inyección de desemulsionante y abrir purga de agua al 100%."], key="r11_ev")
        
        st.info("**Caso B: Parámetros Termodinámicos de Bombeo**\n\nUna bomba centrífuga transfiere crudo a $65^\\circ\\text{C}$ desde un tanque a nivel de $1.2\\text{ m}$. Presión en succión: $0.75\\text{ bar}$ abs. Presión de vapor del crudo: $0.68\\text{ bar}$ abs. NPSH requerido por la bomba: $1.5\\text{ m}$. Emite ruido a metralla.")
        r12 = st.radio("**16. ¿Cuál es el diagnóstico e intervención de ingeniería?**", 
                       ["A) Cavitación por NPSH Disponible insuficiente ($0.07\\text{ bar} \\approx 0.7\\text{ m} < 1.5\\text{ m}$). Se debe estrangular la descarga para reducir el caudal y bajar el NPSH requerido.", "B) El impulsor tiene acumulación de parafinas. Inyectar fluido caliente."], key="r12_ev")
        
        st.info("**Caso C: Emergencia Química Crítica**\n\nFuga de gas en la brida de entrada del separador. El sensor de la trinchera marca paso de $2\\text{ ppm}$ a **$140\\text{ ppm}$ en 30 segundos**. Viento soplando del Este (E) hacia el Oeste (O).")
        r13 = st.radio("**17. ¿Cuál es la ruta de evacuación y plan de contingencia inmediata?**", 
                       ["A) Declarar Emergencia. Evacuar al personal hacia el ESTE (viento arriba) y exigir el uso obligatorio de Equipo de Respiración Autónomo (ERA).", "B) Enviar al recorredor con máscara de filtro de carbón común al Oeste para cerrar la válvula de bloqueo manual."], key="r13_ev")
        
        st.info("**Caso D: Secuencia Lógica de Alarmas**\n\nLa planta sufre una ESD general. La pantalla de eventos (SOE) del PLC registra en milisegundos: 1. PSHH-305 (Presión Alta Gas Compresor), 2. LSHH-201 (Nivel Alto Separador), 3. Cierre de válvula general de entrada.")
        r14 = st.radio("**18. ¿Cuál es el 'First Out' real que causó la parada?**", 
                       ["A) Una falla en la bomba de transferencia de líquido provocó el nivel alto en la vasija.", "B) La restricción u obstrucción en la línea del compresor (PSHH-305) generó contrapresión en el sistema, colapsando la separación física."], key="r14_ev")

    # --- CONTROL DE ENTREGA Y CORRECCIÓN ---
    st.divider()
    if st.button("PROCESAR Y ENTREGAR MESA DE EXAMEN", use_container_width=True):
        puntos_acumulados = 0
        bitacora = []
        
        # --- CORRECCIÓN BLOQUE TÉCNICO (10 puntos c/u) ---
        if r1 == "Bombeo Mecánico": puntos_acumulados += 10
        if r2 == "Separar Gas, Crudo y Agua": puntos_acumulados += 10
        if r3 == "El caudal baja y la presión de línea aguas arriba del bloqueo se incrementa": puntos_acumulados += 10
        if r4 == "Apagado de Emergencia (ESD Nivel 1 o 2)": puntos_acumulados += 10
        if r5 == "Barrido de aire (Purge) con gas inerte o nitrógeno": puntos_acumulados += 10
        if r6 == "Tratador Térmico / FWKO": puntos_acumulados += 10
        if r7 == "Cavitación": puntos_acumulados += 10
        if r8 == "Abrir primero Control, luego cerrar Grupo": puntos_acumulados += 10
        if r9 == "H2S (Ácido Sulfhídrico)": puntos_acumulados += 10
        if r10 == "Inyección de gas para aliviar la columna hidrostática en el tubing": puntos_acumulados += 10
        if r15 == "Flujo Slug (Baches de líquido)": puntos_acumulados += 10
        if r16 == "Atenuar las ondas de pulsación y vibraciones mecánicas generadas por el movimiento recíprocante del pistón": puntos_acumulados += 10
        if r17 == "PSH (Alerta de Presión Alta), PSHH (Presión Muy Alta Alta) y disparo automático de la válvula de seguridad por SIS": puntos_acumulados += 10
        if r18 == "Concentración de Cloruros y presencia de bacterias sulfato-reductoras (BSR)": puntos_acumulados += 10
        
        # --- CORRECCIÓN BLOQUE ESCENARIOS AVANZADOS (10 puntos c/u) ---
        if "B)" in r11: puntos_acumulados += 10
        else: bitacora.append("Caso 1 (BSW): Intentar aumentar el voltaje con agua libre acelera el corto del transformador.")
            
        if "A)" in r12: puntos_acumulados += 10
        else: bitacora.append("Caso 2 (Cavitación): No corregir el NPSH destruye el impulsor por microimplosiones.")
            
        if "A)" in r13: puntos_acumulados += 10
        else: 
            bitacora.append("Caso 3 (H2S): Mandar personal viento abajo (Oeste) o sin ERA ante 140 ppm es fatal.")
            st.session_state.motor.simular_golpe_de_gas()
            
        if "B)" in r14: puntos_acumulados += 10
        else: bitacora.append("Caso 4 (ESD): Confundir la alarma de nivel con la causa raíz bloquea el diagnóstico preventivo.")

        # Persistencia en Session State y Rerun Seguro
        st.session_state.puntos_finales = puntos_acumulados
        st.session_state.bitacora_errores = bitacora
        st.session_state.examen_calculado = True
        st.rerun()
