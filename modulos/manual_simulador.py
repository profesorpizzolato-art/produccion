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
        },
        # --- AGREGAR ESTO A TU DICCIONARIO 'teoria_petrolera' ---

        "5. Operaciones de Campo y Pozos": {
            "resumen": "Manejo de AIB y Control de Fluidos.",
            "detalle": (
                "1. GOLPE DE FLUIDO: Ocurre cuando el barril de la bomba no se llena completamente. Se detecta por vibracion en la viga y ruidos en la caja de valvulas.\n"
                "2. CARRERA POR MINUTO (CPM): Un aumento exagerado de CPM sin aumento de caudal indica falla en la valvula viajera o rotura de varillas.\n"
                "3. PREVENTOR DE REVENTONES (BOP): El operario debe verificar la integridad de las esclusas mensualmente.\n"
                "4. GAS LOCK: Bloqueo de la bomba por gas libre. Se soluciona espaciando la bomba o aumentando la sumergencia.\n"
                "5. PRESIÓN DE CASING: Si la presion de casing iguala a la de tuberia, hay una comunicacion (pinchadura de tubing)."
            ),
            "formula": "Sumergencia = (P_anular / Gradiente) + Prof_Bomba"
        },
        "6. Tratamiento y Quimica de Proceso": {
            "resumen": "Control de Emulsiones y Corrosion.",
            "detalle": (
                "6. BSW (Basic Sediment and Water): El limite fiscal en Argentina suele ser 0.5% - 1%.\n"
                "7. DEMULSIFICANTE: Su funcion es romper la tension interfacial. Se debe inyectar lo mas cerca del pozo posible.\n"
                "8. INHIBIDOR DE INCRUSTACIONES: Previene la formacion de Carbonatos y Sulfatos que tapan el tubing.\n"
                "9. CORROSION POR H2S: El sulfuro de hidrogeno vuelve fragil el acero (Sulfide Stress Cracking).\n"
                "10. TEMPERATURA DE VERTIDO (Pour Point): Temperatura minima a la que el crudo fluye. Vital en Mendoza por las parafinas."
            ),
            "formula": "Dosis (ppm) = (Caudal_Q * 0.001) / R_quimico"
        },
        "7. Equipos de Planta y Scada": {
            "resumen": "Control y Proteccion de Recipientes.",
            "detalle": (
                "11. PSV (Pressure Safety Valve): Valvula mecanica de ultima instancia. Debe setearse al 110% de la MAOP.\n"
                "12. DISCO DE RUPTURA: Proteccion ante picos de presion instantaneos. Una vez activado, debe reemplazarse.\n"
                "13. SETPOINTS SCADA: Los retardos (delays) en alarmas evitan paradas falsas por baches de gas.\n"
                "14. UNIDAD LACT: Sistema de transferencia de custodia. Incluye medidor de flujo, monitor de BSW y tomamuestras.\n"
                "15. VÁLVULA DE CONTROL (PCV): Si falla 'abierta', se dice Fail Open (FO); si falla 'cerrada', Fail Close (FC)."
            ),
            "formula": "MAOP = Presion_Diseño * Factor_Seguridad"
        },
        "8. Integridad y Medio Ambiente": {
            "resumen": "Gestion de Activos y Contingencias.",
            "detalle": (
                "16. PRUEBA HIDRAULICA: Se realiza a 1.5 veces la presion de trabajo segun Res. 148.\n"
                "17. ENSAYO DE ESTANQUEIDAD: Obligatorio para tanques de almacenamiento para detectar fugas en el fondo.\n"
                "18. PROTECCION CATODICA: Uso de anodos de sacrificio para evitar que el suelo 'se coma' la cañeria.\n"
                "19. PLAN DE CONTINGENCIA: Todo derrame mayor a 1 m3 fuera de recinto debe activarlo inmediatamente.\n"
                "20. ABANDONO DE POZOS: Requiere tapones de cemento validados segun profundidad y presion de formacion."
            ),
            "formula": "P_prueba = P_operacion * 1.5"
        },
        "9. Termodinámica y Dinámica de Fluidos": {
            "resumen": "Comportamiento del Crudo y Gas bajo presión.",
            "detalle": (
                "21. PUNTO DE BURBUJA (Bubble Point): Presion a la cual el primer gas se desprende del petroleo. Si operamos por debajo, el gas libre reduce la eficiencia de la bomba.\n"
                "22. VISCOSIDAD DINÁMICA: Propiedad que se opone al flujo. En Mendoza, el crudo parafínico requiere calor para mantener la viscosidad baja y evitar taponamientos.\n"
                "23. RÉGIMEN DE FLUJO: Puede ser Laminar o Turbulento. El flujo turbulento aumenta la erosion en los codos de la cañeria.\n"
                "24. GOR (Gas Oil Ratio): Relacion gas-petroleo. Un aumento repentino de GOR puede indicar una entrada de gas desde la capa superior del reservorio.\n"
                "25. COMPRESIBILIDAD DEL GAS: A diferencia del agua, el gas se comprime. Esto causa el efecto 'resorte' en las lineas de transporte."
            ),
            "formula": "GOR = Caudal_Gas / Caudal_Petroleo"
        },
        "10. Integridad de Pozos (Well Integrity)": {
            "resumen": "Barreras y Protección de la formación.",
            "detalle": (
                "26. CASING DE SUPERFICIE: Su funcion principal es proteger los acuiferos de agua dulce de la contaminacion por hidrocarburos.\n"
                "27. ANULAR: El espacio entre dos cañerias. El monitoreo de presiones en el anular es vital para detectar fugas de cemento.\n"
                "28. PACKER DE PRODUCCIÓN: Elemento sellador que aisla el anular del flujo de produccion, protegiendo el casing de la corrosion.\n"
                "29. CABEZAL DE POZO (Christmas Tree): Conjunto de valvulas que controlan el flujo. La valvula 'Master' solo debe operarse en emergencias.\n"
                "30. ENSAYO DE ADMISIÓN: Prueba para verificar cuanto fluido puede recibir un pozo inyector sin romper la formacion."
            ),
            "formula": "Presion_Hidrostatica = 0.433 * Gravedad_Esp * Profundidad"
        },
        "11. Mantenimiento Mecánico y Eléctrico": {
            "resumen": "Confiabilidad de Equipos Rotantes.",
            "detalle": (
                "31. CAVITACIÓN EN BOMBAS: Formacion de burbujas de vapor que implosionan y destruyen el impulsor. Se evita manteniendo el NPSH disponible.\n"
                "32. ALINEACIÓN LÁSER: Crucial para evitar vibraciones en el conjunto Motor-Bomba que dañan los sellos mecanicos.\n"
                "33. VARIADOR DE FRECUENCIA (VFD): Permite ajustar la velocidad del motor del AIB segun el llenado de la bomba, ahorrando energia.\n"
                "34. GOLPE DE ARIETE: Sobrepresion causada por el cierre brusco de una valvula. Puede reventar bridas y cañerias.\n"
                "35. TERMOGRAFÍA: Uso de camaras infrarrojas para detectar puntos calientes en tableros electricos antes de que ocurra un cortocircuito."
            ),
            "formula": "Potencia (HP) = (Q * P) / (1714 * Eficiencia)"
        },
        "12. Química y Control de Emulsiones II": {
            "resumen": "Separación avanzada de fluidos.",
            "detalle": (
                "36. TIEMPO DE RETENCIÓN: Tiempo que el fluido permanece en el separador. Un crudo pesado requiere mas tiempo (hasta 30 min) para soltar el agua.\n"
                "37. DESARENADORES: Equipos que usan fuerza centrifuga para eliminar solidos antes de que dañen las bombas de la planta.\n"
                "38. TRATAMIENTO TÉRMICO: El calor rompe la tension superficial de las gotas de agua, facilitando la coalescencia.\n"
                "39. BACTERICIDAS: Inyectados en el sistema de agua de inyeccion para evitar que las bacterias sulfato-reductoras generen H2S en el pozo.\n"
                "40. TEST DE JARRA (Bottle Test): Ensayo de laboratorio para determinar la dosis exacta de quimico demulsificante necesaria."
            ),
            "formula": "T_retencion = Volumen_Recipiente / Caudal_Total"
        },
        "13. Intervención de Pozos (Workover & Pulling)": {
            "resumen": "Mantenimiento del Downhole y Recuperación.",
            "detalle": (
                "41. PESCA (Fishing): Operacion para recuperar objetos caidos o herramientas atrapadas en el pozo mediante 'Overshots' o 'Spears'.\n"
                "42. APRIETE DE ROSCAS: El torque debe ser preciso. Un exceso de torque daña la rosca (gall), y la falta de torque causa filtraciones.\n"
                "43. FLUIDO DE TERMINACION: Salmueras filtradas que se usan para controlar la presion del pozo sin dañar la permeabilidad de la roca.\n"
                "44. PUNZONADO (Perforating): Uso de cargas explosivas para crear tuneles entre el pozo y la formacion para que fluya el petroleo.\n"
                "45. ACIDIFICACIÓN: Inyeccion de acidos para disolver carbonatos y limpiar el daño de formacion cerca del pozo."
            ),
            "formula": "Presion_Fondo = Presion_Cabeza + P_Hidrostatica"
        },
        "14. Equipos Especiales y Auxiliares": {
            "resumen": "Sistemas de Apoyo en Planta.",
            "detalle": (
                "46. ANTIFLAMA (Flame Arrestor): Dispositivo de seguridad en venteos que evita que una llama exterior retroceda hacia el tanque.\n"
                "47. TRAMPAS DE SCRAPER (Pig Launchers): Estaciones para lanzar 'chanchos' (pigs) que limpian la parafina de los oleoductos.\n"
                "48. AEROTIEMPOS (Air Coolers): Ventiladores gigantes que enfrian el crudo o gas antes de su despacho.\n"
                "49. SISTEMA DE TELESUPERVISIÓN: Uso de RTU (Remote Terminal Units) para transmitir datos de pozos remotos via radio o satelite.\n"
                "50. BOMBAS MULTIFASICAS: Equipos capaces de bombear petroleo, agua y gas juntos sin necesidad de separarlos en el pozo."
            ),
            "formula": "Caudal_Gas = Caudal_Liquido * GOR"
        },
        "15. Laboratorio y Calidad de Crudo": {
            "resumen": "Especificaciones para Venta.",
            "detalle": (
                "51. PUNTO DE INFLAMACIÓN (Flash Point): Temperatura minima a la que el crudo desprende vapores que pueden arder.\n"
                "52. CONTENIDO DE SAL: El exceso de sal (PTB) en el crudo causa corrosion severa en las torres de destilacion de la refineria.\n"
                "53. DESTILACIÓN ASTM D86: Ensayo para determinar que porcentaje de crudo se evapora a distintas temperaturas.\n"
                "54. COLOR DEL PETRÓLEO: Indica su origen y composicion. Crudos livianos suelen ser verdosos/amarillos; pesados son negros.\n"
                "55. SEDIMENTOS (S): Arena o arcilla que viaja con el fluido. Se miden por centrifugado junto con el agua (BSW)."
            ),
            "formula": "API = (141.5 / GE) - 131.5"
        },
        "16. Gestión de Riesgos y Emergencias": {
            "resumen": "Respuesta Ante Incidentes.",
            "detalle": (
                "56. GASES COMBUSTIBLES (LEL): Limite Inferior de Explosividad. Si el gas en el aire esta entre el LEL y UEL, puede explotar.\n"
                "57. ESPACIOS CONFINADOS: El ingreso a tanques requiere medicion de oxigeno, vigia permanente y permiso especial de trabajo.\n"
                "58. VIENTOS DOMINANTES: En caso de fuga de H2S, el personal debe evacuarse siempre en direccion perpendicular al viento.\n"
                "59. EXTINTORES CLASE B: Los unicos aptos para fuegos de hidrocarburos. Actuan por sofocacion (espuma o CO2).\n"
                "60. ROL DE EMERGENCIAS: Listado de funciones y jerarquias que se activa ante un incendio o derrame mayor."
            ),
            "formula": "LEL_Mezcla = Punto_Ignicion / Concentracion"
        },
        "17. Optimización y Eficiencia Energética": {
            "resumen": "Reducción de Costos Operativos (OPEX).",
            "detalle": (
                "61. CUIDADO DEL COSENO DE FI: Un bajo factor de potencia en los motores del AIB genera multas en la factura electrica. Se corrige con bancos de capacitores.\n"
                "62. EQUILIBRIO DE MASAS: Un aparato de bombeo mal balanceado consume hasta un 30% mas de energia y daña los rodamientos de la caja reductora.\n"
                "63. RECUPERACIÓN DE VAPORES (VRU): Captura los gases livianos que escapan de los tanques, reduciendo emisiones y recuperando producto vendible.\n"
                "64. PÉRDIDAS POR FRICCIÓN: El uso de reductores de friccion (DRA) permite bombear mas caudal con la misma potencia de bomba.\n"
                "65. CICLOS DE BOMBEO: Programar paradas en pozos de baja productividad permite que el reservorio recupere nivel, evitando el golpe de fluido."
            ),
            "formula": "Eficiencia = (Energia_Util / Energia_Consumida) * 100"
        },
        "18. Geología y Petrofísica para Técnicos": {
            "resumen": "Entendiendo la roca reservorio.",
            "detalle": (
                "66. POROSIDAD: El espacio vacio en la roca donde se aloja el petroleo. Se mide en porcentaje (%).\n"
                "67. PERMEABILIDAD: La facilidad con la que el fluido se mueve a traves de los poros. Se mide en Darcy (D) o milidarcy (mD).\n"
                "68. AGUA DE FORMACIÓN: Agua salada atrapada con el petroleo. Su resistividad electrica ayuda a identificar zonas productivas en los perfiles.\n"
                "69. ROCA MADRE: La arcilla donde se origino el hidrocarburo. En No Convencionales, se estimula directamente esta roca.\n"
                "70. SATURACIÓN DE AGUA (Sw): Porcentaje del poro ocupado por agua. Si es muy alto, el pozo solo producira agua (Corte de agua alto)."
            ),
            "formula": "Porosidad = (Vol_Vacio / Vol_Total) * 100"
        },
        "19. Gas Natural y Procesamiento": {
            "resumen": "Acondicionamiento para Venta.",
            "detalle": (
                "71. PUNTO DE ROCÍO (Dew Point): Temperatura a la cual el vapor de agua o hidrocarburos pesados empiezan a condensar en la linea.\n"
                "72. GAS DULCE VS AMARGO: El gas amargo contiene H2S y CO2, requiriendo plantas de aminas para ser comercializable.\n"
                "73. HIDRATOS DE GAS: Cristales de hielo y gas que taponan lineas en invierno. Se previenen inyectando Metanol o Glicol.\n"
                "74. CALOR ESPECÍFICO DEL GAS: Propiedad que determina cuanta energia se necesita para calentar el gas en los calentadores de paso.\n"
                "75. PODER CALORÍFICO: Cantidad de energia por m3. El gas de venta debe cumplir con un minimo (aprox 9300 kcal/m3)."
            ),
            "formula": "P_Rocio = f(Presion, Temperatura, Composicion)"
        },
        "20. Gestión de Activos y Liderazgo Técnico": {
            "resumen": "El rol del Técnico en la Organización.",
            "detalle": (
                "76. MANTENIMIENTO PREDICTIVO: Basado en analisis de vibraciones y aceite, para intervenir antes de que el equipo falle.\n"
                "77. ANALISIS DE CAUSA RAIZ (RCA): Metodo para entender por que fallo un equipo y evitar que se repita el incidente.\n"
                "78. GESTIÓN DEL CAMBIO (MOC): Protocolo para asegurar que cualquier modificacion en la planta sea evaluada por seguridad.\n"
                "79. COSTO DEL BARRIL (Lifting Cost): Lo que cuesta sacar un barril a superficie. El tecnico influye bajando consumos y roturas.\n"
                "80. TRABAJO EN EQUIPO: La comunicacion entre el Recorredor, el Panelista y el Supervisor es la barrera de seguridad mas fuerte."
            ),
            "formula": "Lifting_Cost = Gastos_Operativos / Produccion_Total"
        },
        "21. El Ojo del Experto: Diagnóstico Sensorial": {
            "resumen": "Detección de fallas mediante sentidos y experiencia.",
            "detalle": (
                "81. RUIDO DE 'CAVALLEO': En bombas centrifugas, indica entrada de aire o cavitacion inminente.\n"
                "82. OLOR A HUEVO PODRIDO: Señal clasica de H2S. El problema es que a altas concentraciones el gas duerme el olfato; nunca confie solo en su nariz.\n"
                "83. VIBRACIÓN RÍTMICA EN AIB: Suele indicar un perno de biela flojo o falta de lubricacion en el cojinete de ecualizador.\n"
                "84. TEMPERATURA EN PRENSAESTOPAS: Si el prensa esta demasiado caliente al tacto, las empaquetaduras estan muy apretadas y dañaran el vástago.\n"
                "85. COLOR DE LA LLAMA EN CALENTADOR: Una llama naranja/amarilla indica mala combustion (falta de aire). Debe ser azulada y estable."
            ),
            "formula": "Diagnóstico = Observación + Tendencia + Experiencia"
        },
        "22. Control de Pérdidas y Mermas": {
            "resumen": "Protegiendo el volumen de venta.",
            "detalle": (
                "86. MERMAS POR EVAPORACIÓN: El venteo de gas asociado en tanques reduce el volumen de crudo y su grado API (el crudo se 'pesifica').\n"
                "87. FUGAS FUGITIVAS: Pequeñas filtraciones en bridas y sellos de valvulas que, sumadas, representan una perdida ambiental y economica grave.\n"
                "88. CALIBRACIÓN DE TANQUES: El uso de la 'cinta de medicion' con pasta detectora de agua es el metodo mas confiable para verificar stock.\n"
                "89. ERROR DE MEDICIÓN: Un medidor descalibrado un 1% en un yacimiento de 1000 m3/d genera una perdida de 10 m3 diarios.\n"
                "90. DRENAJE DE AGUA: Realizar purgas excesivas en tanques de despacho puede enviar crudo al pileton de purga (perdida de producto)."
            ),
            "formula": "Merma (%) = (Vol_Entrada - Vol_Salida) / Vol_Entrada"
        },
        "23. Transición y Futuro: Energías Híbridas": {
            "resumen": "La industria hacia el 2030.",
            "detalle": (
                "91. ELECTRIFICACIÓN DE YACIMIENTOS: Reemplazo de motores a gas por electricos para reducir la huella de carbono local.\n"
                "92. PANELES SOLARES EN POZOS: Uso de energia fotovoltaica para alimentar equipos de telemetria y proteccion catodica en zonas remotas.\n"
                "93. INYECCIÓN DE CO2 (EOR): Uso de dioxido de carbono para empujar el petroleo remanente, capturando el gas de efecto invernadero bajo tierra.\n"
                "94. ECONOMÍA CIRCULAR: El agua de produccion tratada puede reutilizarse para riego industrial o generacion de vapor.\n"
                "95. MONITOREO POR DRONES: Inspeccion de oleoductos para detectar derrames o intrusos de forma automatizada y segura."
            ),
            "formula": "Huella_Carbono = f(Consumo_Combustible, Emisiones_Venteo)"
        },
        "24. Ética Profesional y Seguridad de Procesos": {
            "resumen": "El compromiso del Técnico Superior.",
            "detalle": (
                "96. DERECHO A DECIR NO: Todo tecnico tiene la autoridad de detener una tarea si considera que no es segura (Stop Work Authority).\n"
                "97. VERIFICACIÓN DE LÍNEAS: Nunca asuma que una linea esta despresurizada porque el manometro marca cero; verifique con una purga testigo.\n"
                "98. ORDEN Y LIMPIEZA (5S): Una locacion sucia esconde derrames y riesgos de tropiezos. El orden es parte de la seguridad operacional.\n"
                "99. TRANSMISIÓN DE CONOCIMIENTO: El tecnico senior tiene la obligacion moral de formar a los ingresantes para evitar accidentes.\n"
                "100. INTEGRIDAD: Operar bajo normas no para evitar multas, sino para proteger la vida, el ambiente y el recurso de Mendoza."
            ),
            "formula": "Seguridad = Prevision + Disciplina"
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
