import streamlit as st
from fpdf import FPDF
import time  
import datetime
import pandas as pd
def mostrar_manual(): 
    # ==========================================
    # 1. EL GRAN DICCIONARIO TÉCNICO (50 PUNTOS)
    # ==========================================
    teoria_petrolera = {
        "1. Ingeniería de Reservorio": {
            "resumen": "La gestión de la energía del yacimiento.",
            "detalle": "El Índice de Productividad (IP) es la métrica reina para evaluar el aporte del reservorio ante una caída de presión determinada en el fondo del pozo.",
            "formula": r"J = \frac{Q}{P_r - P_{wf}}"
        },
        "2. Separación Física": {
            "resumen": "Principios de Gravedad, Momento y Coalescencia.",
            "detalle": "La separación ocurre por diferencia de densidades. LEY DE STOKES: Define la velocidad de caída de una gota de agua en el crudo. A mayor viscosidad, más lento cae el agua; por eso en Mendoza se usa calor para bajar la viscosidad y facilitar la separación por gravitación.",
            "formula": r"v = \frac{2 \cdot r^2 \cdot g \cdot (d_1 - d_2)}{9 \cdot \eta}"
        },
        "3. Medición AGA 3": {
            "resumen": "Medición de gas por presión diferencial.",
            "detalle": "Se basa en el Efecto Venturi. Al restringir el paso con una placa de orificio, la velocidad aumenta y la presión cae. PUNTOS CRÍTICOS: La placa debe tener el borde filoso hacia aguas arriba. Si la placa está sucia o roma, medirá menos gas del real.",
            "formula": r"Q = C' \cdot \sqrt{h_w \cdot P_f}"
        },
        "4. Normativa y Seguridad": {
            "resumen": "Resolución 148/07 y API RP 14C.",
            "detalle": "La Res. 148 de Mendoza exige auditorías de integridad de pozos e instalaciones. PROTOCOLOS: PSH (Alta presión), LSH (Alto nivel) y LOTO (Lock Out - Tag Out) para bloqueo físico con candado durante mantenimiento.",
            "formula": "API 14C / Res. 148/07"
        },
        "5. Operaciones de Campo y Pozos": {
            "resumen": "Manejo de AIB y Control de Fluidos.",
            "detalle": (
                "1. GOLPE DE FLUIDO: Ocurre cuando el barril de la bomba no se llena completamente. Se detecta por vibración en la viga y ruidos en la caja de válvulas.\n"
                "2. CARRERA POR MINUTO (CPM): Un aumento exagerado de CPM sin aumento de caudal indica falla en la válvula viajera o rotura de varillas.\n"
                "3. PREVENTOR DE REVENTONES (BOP): El operario debe verificar la integridad de las esclusas mensualmente.\n"
                "4. GAS LOCK: Bloqueo de la bomba por gas libre. Se soluciona espaciando la bomba o aumentando la inmersión.\n"
                "5. PRESIÓN DE CASING: Si la presión de casing es igual a la de tubería, hay una comunicación (pinchadura de tubing)."
            ),
            "formula": r"Sumergencia = \frac{P_{anular}}{Gradiente} + Prof_{Bomba}"
        },
        "6. Tratamiento y Química de Proceso": {
            "resumen": "Control de Emulsiones y Corrosión.",
            "detalle": (
                "6. BSW (Sedimentos Básicos y Agua): El límite fiscal estipulado en Argentina suele rondar entre el 0,5% y 1%.\n"
                "7. DEMULSIFICANTE: Su función es romper la tensión interfacial de la emulsión. Se debe inyectar lo más cerca del pozo posible.\n"
                "8. INHIBIDOR DE INCRUSTACIONES: Previene la precipitación y formación de Carbonatos y Sulfatos que obstruyen el tubing.\n"
                "9. CORROSIÓN POR H2S: El sulfuro de hidrógeno vuelve frágil el acero provocando fisuras severas (Sulfide Stress Cracking).\n"
                "10. TEMPERATURA DE VERTIDO (Pour Point): Temperatura mínima a la que el crudo fluye. Vital en Mendoza por la naturaleza parafínica del crudo."
            ),
            "formula": r"Dosis (ppm) = \frac{Caudal_Q \cdot 0.001}{R_{quimico}}"
        },
        "7. Equipos de Planta y SCADA": {
            "resumen": "Control y Protección de Destinatarios.",
            "detalle": (
                "11. PSV (Pressure Safety Valve): Válvula mecánica de seguridad de última instancia. Debe setearse al 110% de la MAOP.\n"
                "12. DISCO DE RUPTURA: Protección ante picos de presión instantánea. Una vez activado por sobrepresión, debe reemplazarse.\n"
                "13. SETPOINTS SCADA: Los retardos en alarmas evitan paradas falsas por baches transitorios de gas en las líneas.\n"
                "14. UNIDAD LACT: Sistema automático de transferencia de custodia. Incluye medidor de flujo, monitor de BSW continuo y tomamuestras.\n"
                "15. VÁLVULA DE CONTROL (PCV): Si falla abierta se denomina Fail Open (FO); si falla cerrada es Fail Close (FC)."
            ),
            "formula": r"MAOP = Presion_{Diseno} \cdot Factor_{Seguridad}"
        },
        "8. Integridad y Medio Ambiente": {
            "resumen": "Gestión de Activos y Contingencias.",
            "detalle": (
                "16. PRUEBA HIDRÁULICA: Se realiza reglamentariamente a 1.5 veces la presión de trabajo según dicta la Res. 148.\n"
                "17. ENSAYO DE ESTANQUEIDAD: Obligatorio para tanques de almacenamiento con el fin de detectar microfugas destructivas en el fondo.\n"
                "18. PROTECCIÓN CATÓDICA: Uso de ánodos de sacrificio e inversión de corriente para evitar que el suelo corroa la cañería.\n"
                "19. PLAN DE CONTINGENCIA: Todo derrame mayor a 1 m³ fuera de los recintos de contención exige activar el protocolo de mitigación inmediatamente.\n"
                "20. ABANDONO DE POZOS: Requiere la colocación de tapones de cemento validados según profundidad y presión de la formación aislada."
            ),
            "formula": r"P_{prueba} = P_{operacion} \cdot 1.5"
        },
        "9. Termodinámica y Dinámica de Fluidos": {
            "resumen": "Comportamiento del Crudo y Gas bajo presión.",
            "detalle": (
                "21. PUNTO DE BURBUJA (Bubble Point): Presión a la cual el primer gas se desprende del petróleo. Operar debajo de este punto reduce la eficiencia de bombeo.\n"
                "22. VISCOSIDAD DINÁMICA: Propiedad molecular que se opone al flujo libre. En Mendoza, el crudo parafínico requiere mantener calor estable en el circuito.\n"
                "23. RÉGIMEN DE FLUJO: Clasificado en Laminar o Turbulento. El flujo turbulento severo acelera la erosión mecánica en los codos.\n"
                "24. GOR (Gas Oil Ratio): Relación gas-petróleo. Un incremento repentino puede indicar la irrupción de gas desde la capa superior del yacimiento.\n"
                "25. COMPRESIBILIDAD DEL GAS: Factor de desviación Z. A diferencia del agua, el gas es altamente compresible, actuando como resorte."
            ),
            "formula": r"GOR = \frac{Caudal_{Gas}}{Caudal_{Petroleo}}"
        },
        "10. Integridad de Pozos": {
            "resumen": "Barreras y Protección de la formación.",
            "detalle": (
                "26. CASING DE SUPERFICIE: Su función crítica primordial es aislar y proteger los acuíferos de agua dulce de cualquier contaminación.\n"
                "27. ESPACIO ANULAR: Espacio físico entre dos cañerías. El monitoreo de presiones anulares detecta fallas de cementación o tubing de forma temprana.\n"
                "28. PACKER DE PRODUCCIÓN: Elemento elastómero sellador que aísla el anular del flujo de producción, protegiendo el casing productivo.\n"
                "29. CABEZAL DE POZO (Árbol de Navidad): Conjunto de válvulas de alta presión que controlan el pozo. La válvula Master solo opera en emergencias.\n"
                "30. ENSAYO DE ADMISIÓN: Prueba estricta para verificar cuánto fluido puede recibir un pozo inyector sin fracturar hidráulicamente la roca."
            ),
            "formula": r"P_{hidrostatica} = 0.0981 \cdot \gamma \cdot Profundidad"
        },
        "11. Mantenimiento Mecánico y Eléctrico": {
            "resumen": "Confiabilidad de Equipos Rotantes.",
            "detalle": (
                "31. CAVITACIÓN EN BOMBAS: Formación e implosión destructiva de burbujas de vapor en el impulsor. Se evita garantizar el NPSH disponible.\n"
                "32. ALINEACIÓN LÁSER: Crucial para mitigar vibraciones armónicas en el conjunto motor-bomba que destruyen los sellos mecánicos.\n"
                "33. VARIADOR DE FRECUENCIA (VFD): Permite ajustar dinámicamente los ciclos del motor del AIB según el nivel de llenado de la bomba de fondo.\n"
                "34. GOLPE DE ARIETE: Onda de sobrepresión peligrosa causada por el cierre brusco de válvulas. Puede fracturar bridas y cañerías rígidas.\n"
                "35. TERMOGRAFÍA: Inspección infrarroja periódica para detectar puntos calientes por resistencia en tableros eléctricos antes de una falla."
            ),
            "formula": r"Potencia (HP) = \frac{Q \cdot P}{1714 \cdot Eficiencia}"
        },
        "12. Química y Control de Emulsiones II": {
            "resumen": "Separación avanzada de fluidos.",
            "detalle": (
                "36. TIEMPO DE RETENCIÓN: Período de residencia del fluido en el separador. Un crudo pesado requiere hasta 30 minutos para liberar el agua.\n"
                "37. DESARENADORES: Equipos que aprovechan la fuerza centrífuga para decantar sólidos abrasivos antes del ingreso a las bombas de la planta.\n"
                "38. TRATAMIENTO TÉRMICO: El aporte térmico rompe la tensión superficial de las gotas de agua emulsionadas, induciendo la coalescencia.\n"
                "39. BACTERICIDAS: Compuestos inyectados en líneas de agua para neutralizar bacterias sulfato-reductoras generadoras de gas H2S nocivo.\n"
                "40. TEST DE JARRA (Bottle Test): Ensayo empírico de laboratorio para determinar la dosificación óptima de agente demulsificante químico."
            ),
            "formula": r"T_{retencion} = \frac{Volumen_{Recipiente}}{Caudal_{Total}}"
        },
        "13. Intervención de Pozos y Seguridad Vial (Recorredor)": {
            "resumen": "Mantenimiento de Fondo y Cultura de Seguridad Diaria.",
            "detalle": (
                "41. PESCA DE FONDO: Recuperación de herramientas o varillas cortadas alojadas en el pozo mediante el uso de Overshots o Spears.\n"
                "42. MANIOBRAS EN MANIFOLD: El traspaso de pozos a ensayo debe ser simultáneo (abrir primero la válvula de destino, luego cerrar la anterior) de modo gradual para evitar sobrepresiones.\n"
                "43. SEÑALES SCADA (4-20mA): Lógica basada en el 'Cero Vivo'. Si un cable de instrumentación se corta, la corriente cae a 0 mA, disparando una alarma de lazo abierto en el PLC en vez de marcar erróneamente una variable en cero.\n"
                "44. CONDUCTA ANTE LA DUDA: Ante dudas operativas complejas en el campo, la regla obliga a preguntar las veces que sea necesario al supervisor.\n"
                "45. FATIGA Y CONDUCCIÓN: Conducir con somnolencia o fatiga extrema es causal de incidentes graves. El operador debe detener la marcha de inmediato, notificar con total franqueza a la supervisión y solicitar el relevo obligatorio de la jornada.\n"
                "46. FIRMA DE CAPACITACIONES: Las planillas de capacitación firmadas por el operador avalan legalmente su conocimiento ante el Comité de Investigación de Incidentes.\n"
                "47. COMUNICACIÓN VHF: Antes de transmitir por radio, se debe estructurar el mensaje mentalmente y esperar 3 segundos para evitar saturar el canal de emergencias.\n"
                "48. MANEJO DEFENSIVO EN YACIMIENTO: El respeto irrestricto de las velocidades máximas en caminos de tierra evita voladuras y pérdidas de control mecánicas.\n"
                "49. SISTEMAS ESD: Los botones de Parada de Emergencia (Emergency Shutdown) aíslan por completo la instalación neumática y eléctricamente en segundos.\n"
                "50. ORDEN Y LIMPIEZA EN LOCACIÓN: Mantener las piletas de purga libres de hidrocarburos y los recintos limpios previene la contaminación del suelo y mitiga riesgos de fuego."
            ),
            "formula": r"Cuentas_{PLC} = \left(\frac{P_{actual}}{P_{max}}\right) \cdot (4000 - 800) + 800"
        }
    }

    # ==========================================
    # 2. DEFINICIÓN DE PESTAÑAS EN LA INTERFAZ
    # ==========================================
    tab1, tab2, tab3, tab4 = st.tabs([
        "📘 Manual de Estudio (50 Puntos)",
        "🎛️ Operaciones en Batería", 
        "🤖 Señales SCADA (4-20mA)", 
        "📋 Evaluación Técnico-Operativa"
    ])

    # ------------------------------------------
    # PESTAÑA 1: EL MANUAL INTERACTIVO Y EXPORTACIÓN PDF
    # ------------------------------------------
    with tab1:
        st.header("Manual Técnico de Producción e Integridad 3.0")
        st.caption("Estructura Pedagógica y Material de Consulta — IPCL MENFA")

        tema_seleccionado = st.selectbox("Seleccionar Capítulo de Estudio:", list(teoria_petrolera.keys()))
        info_tema = teoria_petrolera[tema_seleccionado]
        st.subheader(info_tema["resumen"])
        st.info(info_tema["detalle"])
        
        st.markdown("**Fórmula / Parámetro de Control asociado:**")
        if "\\" in info_tema["formula"]:
            st.latex(info_tema["formula"])
        else:
            st.code(info_tema["formula"], language="markdown")

        st.markdown("---")
        st.subheader("📥 Exportación y Certificación del Alumno")
        st.write("Generá el documento PDF oficial del manual con fines de auditoría o estudio.")

        def generar_pdf_pro():
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            try:
                pdf.image("assets/logo_menfa.png", x=10, y=10, w=30)
                pdf.ln(20)
            except:
                pdf.ln(10)

            puntaje_actual = st.session_state.get('puntaje_examen', 0)
            if puntaje_actual >= 80:
                pdf.set_font("Helvetica", "B", 11)
                pdf.set_text_color(0, 128, 0)
                pdf.cell(0, 10, f"ESTADO: OPERADOR CERTIFICADO ({puntaje_actual}/100 PTS)", ln=True, align='C')
                pdf.ln(5)
            
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_text_color(0, 51, 102)
            pdf.cell(0, 10, "MANUAL TECNICO DE PRODUCCION IPCL 3.0", ln=True, align='C')
            
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 10, "Menfa Capacitaciones — Director Técnico: Fabricio Pizzolato", ln=True, align='C')
            pdf.ln(10)

            for tit, info in teoria_petrolera.items():
                pdf.set_font("Helvetica", "B", 11)
                pdf.set_fill_color(243, 156, 18)
                pdf.set_text_color(255, 255, 255)
                tit_limpio = tit.encode('latin-1', 'ignore').decode('latin-1')
                pdf.cell(0, 8, tit_limpio, ln=True, fill=True)
                pdf.ln(2)
                
                pdf.set_font("Helvetica", size=9)
                pdf.set_text_color(0, 0, 0)
                detalle_limpio = info['detalle'].encode('latin-1', 'ignore').decode('latin-1')
                pdf.multi_cell(0, 5, detalle_limpio)
                pdf.ln(1)
                
                pdf.set_font("Courier", "I", 8)
                pdf.set_text_color(80, 80, 80)
                formula_limpia = info['formula'].replace('\\', '').encode('latin-1', 'ignore').decode('latin-1')
                pdf.cell(0, 6, f"Ecuacion/Referencia: {formula_limpia}", ln=True)
                pdf.ln(4)

            pdf.ln(15)
            y_f = pdf.get_y()
            if y_f > 260:
                pdf.add_page()
                y_f = pdf.get_y() + 10
                
            pdf.line(20, y_f, 80, y_f)
            pdf.line(120, y_f, 180, y_f)
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(0, 0, 0)
            pdf.text(35, y_f + 5, "Firma del Alumno Evaluado")  
            pdf.text(135, y_f + 5, "Firma de Autoría: F. Pizzolato")
            
            return pdf.output(dest='S').encode('latin-1')

        try:
            btn_pdf_data = generar_pdf_pro()
            st.download_button(
                label="📥 Descargar Manual Técnico Completo (PDF)",
                data=btn_pdf_data,
                file_name=f"Manual_Tecnico_MENFA_{datetime.date.today().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="btn_manual_pdf_fijo"
            )
        except Exception as e:
            st.error(f"Aviso del motor PDF: {e}")

    # ------------------------------------------
    # PESTAÑA 2: SIMULADOR DE COLECTOR / RECORRIDA
    # ------------------------------------------
    with tab2:
        st.header("Flujo del Fluido y Operaciones en Batería")
        st.write("La función principal de una batería es reunir la producción para separar gas, agua y petróleo.")
        
        st.subheader("🎛️ Operación del Manifold de Ingreso (Colector)")
        st.info("**Regla Operativa:** La apertura y cierre de válvulas debe practicarse de forma simultánea (abrir primero, luego cerrar) de manera gradual para evitar golpes de ariete.")
        
        pozo_seleccionado = st.selectbox("Seleccionar Pozo para Ensayar:", ["Pozo Productor MENFA-01", "Pozo Productor MENFA-02", "Pozo Productor MENFA-03"])
        linea_derivacion = st.radio("Derivar flujo hacia:", ["Línea General (Producción Total)", "Separador de Ensayo (Control Individual)"])
        
        if st.button("Ejecutar Maniobra de Válvulas"):
            with st.spinner("Cambiando configuración en el colector..."):
                time.sleep(1.5)
                st.success(f"Maniobra exitosa. El {pozo_seleccionado} ahora está derivado a {linea_derivacion}.")
                st.warning("🔄 Recuerda revisar el circuito de flujo para comprobar la eficacia de la maniobra realizada.")

    # ------------------------------------------
    # PESTAÑA 3: LAZO DE INSTRUMENTACIÓN SCADA 4-20mA
    # ------------------------------------------
    with tab3:
        st.header("Conversión Analógica a Digital (Lógica del PLC/RTU)")
        st.write("Los sistemas SCADA e instrumentos de campo utilizan el estándar industrial de **4-20 miliamperios (mA)**.")
        st.info("💡 **Dato del Manual:** Cuando la variable está en 0, circula un mínimo de 4mA (Cero Vivo) para verificar que el circuito eléctrico esté sano.")

        rango_max_presion = st.number_input("Rango Máximo del Transmisor de Presión (PT) en Kg/cm²:", min_value=1.0, max_value=100.0, value=10.0)
        presion_actual = st.slider("Presión Actual en Campo (Kg/cm²):", min_value=0.0, max_value=float(rango_max_presion), value=float(rango_max_presion*0.4), step=0.1)

        factor_ma = (presion_actual / rango_max_presion) * 16 + 4
        cuentas_plc = int((presion_actual / rango_max_presion) * (4000 - 800) + 800)

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Presión Física", value=f"{presion_actual:.2f} Kg/cm²")
        col2.metric(label="Señal de Corriente", value=f"{factor_ma:.2f} mA")
        col3.metric(label="Cuentas en RTU/PLC", value=f"{cuentas_plc} pts")

        st.subheader("🚨 Lógica de Control de Alarmas (Set Points)")
        set_point_alto = rango_max_presion * 0.8
        st.write(f"**Set Point de Alarma Alta:** {set_point_alto:.1f} Kg/cm²")
        
        if presion_actual >= set_point_alto:
            st.error("⚠️ CONDICIÓN DE ALARMA: 'Alto Nivel / Presión en Instalación'. Notificando al Servidor SCADA central. Requiere reconocimiento.")
        else:
            st.success("🟢 Operación normal de campo. Variables dentro de parámetros normales.")

    # ------------------------------------------
    # PESTAÑA 4: EVALUACIÓN DE PROCEDIMIENTOS
    # ------------------------------------------
    with tab4:
        st.header("Examen Técnico de Normas Operativas y de Seguridad")
        st.write("Test de evaluación para personal ingresante y técnicos de producción.")

        puntaje = 0
        
        p1 = st.radio(
            "1. ¿Qué se deduce si un instrumento de campo reporta una corriente de 0 mA de forma lineal?",
            ["Que la variable medida está exactamente en cero.", 
             "Que existe una anomalía o rotura en el circuito eléctrico (ya que el cero equivale a 4mA).", 
             "Que el PLC está saturado."]
        )
        if p1 == "Que existe una anomalía o rotura en el circuito eléctrico (ya que el cero equivale a 4mA).":
            puntaje += 1.0

        p2 = st.radio(
            "2. Ante una duda en la ejecución de una maniobra operativa compleja en los pozos, ¿cuál es la acción correcta?",
            ["Proceder con cautela basándose en la experiencia previa.",
             "Preguntar la cantidad de veces que sea necesario al supervisor, aunque parezca molesto.",
             "Dejar la maniobra pendiente para el cambio de turno."]
        )
        if p2 == "Preguntar la cantidad de veces que sea necesario al supervisor, aunque parezca molesto.":
            puntaje += 1.0

        p3 = st.radio(
            "3. Si un recorredor presenta fatiga intensa o somnolencia severa durante su turno de conducción, ¿qué indica el procedimiento?",
            ["Consumir café o energizantes y circular a menor velocidad.",
             "Continuar la marcha para no retrasar el parte diario.",
             "Detener la conducción, hablar de forma franca con el supervisor y solicitar el relevo inmediato del día."]
        )
        if p3 == "Detener la conducción, hablar de forma franca con el supervisor y solicitar el relevo inmediato del día.":
            puntaje += 1.0

        if st.button("Calificar Evaluación Técnico-Operativa"):
            porcentaje = (puntaje / 3.0) * 100
            st.session_state.puntaje_examen = int(porcentaje) # Guardamos en sesion para el PDF
            if porcentaje >= 100:
                st.balloons()
                st.success(f"🎯 Calificación: {porcentaje:.1f}%. ¡Aprobado! El alumno incorpora plenamente los procedimientos de seguridad y cultura operativa.")
            else:
                st.warning(f"⚠️ Calificación: {porcentaje:.1f}%. Se sugiere repasar los capítulos de 'Señales Eléctricas' y 'Normas de Seguridad Humana' del manual.")

    st.divider()
    st.caption("IPCL MENFA 3.0 — Mendoza, Argentina.")
