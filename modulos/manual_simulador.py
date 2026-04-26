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
        },
         "25. Fenómenos de Flujo: Parafinas y Asfaltenos": {
            "resumen": "Gestión de obstrucciones en climas fríos (Mendoza).",
            "detalle": (
                "1. PUNTO DE NUBE (Cloud Point): Temperatura a la cual empiezan a formarse cristales de parafina sólidos. Vital para el seteo de calentadores en invierno.\n"
                "2. TRATAMIENTO QUÍMICO: Uso de dispersantes y solventes aromáticos. La inyección debe ser continua para evitar que la parafina se adhiera a las paredes del tubing.\n"
                "3. SCRAPPING MECÁNICO: Uso de herramientas cortadoras bajadas con Wireline para limpiar el pozo sin necesidad de equipo de Pulling."
            ),
            "formula": "T_operacion > T_nube + 10°C"
        },
        "26. Sistemas de Extracción: Bombeo Electrosumergible (BES)": {
            "resumen": "Producción de altos caudales y pozos profundos.",
            "detalle": (
                "1. ETAPAS DE LA BOMBA: Cada etapa (impulsor + difusor) aporta una cantidad de presión (head). A mayor cantidad de etapas, más profundidad puede manejar.\n"
                "2. SENSOR DE FONDO: Mide presión y temperatura del motor. Un aumento de temperatura indica falta de enfriamiento (poco flujo) o sobrecarga eléctrica.\n"
                "3. MANEJO DE GAS: El gas libre en la succión causa 'gas lock' o cavitación. Se soluciona con separadores de gas rotativos antes de la entrada a la bomba."
            ),
            "formula": "TDH = Prof_Vertical + Perdidas_Friccion + P_Cabeza"
        },
        "27. Tratamiento de Agua de Inyección": {
            "resumen": "Recuperación Secundaria y Calidad de Agua.",
            "detalle": (
                "1. FILTRACIÓN: El agua debe estar libre de sólidos para no tapar los poros de la formación inyectora.\n"
                "2. REMOCIÓN DE OXÍGENO: El oxígeno causa corrosión severa en las cañerías. Se elimina mediante torres de desaireación o secuestrantes químicos.\n"
                "3. COMPATIBILIDAD: El agua inyectada no debe reaccionar con los minerales de la roca (arcillas hinchables) para evitar el daño de formación."
            ),
            "formula": "Indice_Inyectividad = Caudal / (P_Inyeccion - P_Reservorio)"
        },
        "28. Control de Pozos: El fenómeno del 'Kick'": {
            "resumen": "Seguridad Crítica durante intervenciones.",
            "detalle": (
                "1. SURGENCIA (Kick): Entrada no deseada de fluido de formación al pozo. Se detecta por aumento de nivel en piletas o flujo con bombas apagadas.\n"
                "2. CIERRE DE BOP: Procedimiento inmediato ante un kick para evitar un reventón (Blowout).\n"
                "3. MÉTODO DEL PERFORADOR: Técnica para circular el gas hacia afuera del pozo de forma controlada, manteniendo la presión de fondo constante."
            ),
            "formula": "P_Fondo = P_Hidrostatica + P_Anular"
        },
        "29. Deshidratación de Crudo: Electrotécnicos": {
            "resumen": "Tratadores de alta eficiencia.",
            "detalle": (
                "1. COALESCENCIA ELECTROSTÁTICA: Uso de campos eléctricos de alto voltaje (15kV - 30kV) para polarizar las gotas de agua y hacer que se junten más rápido.\n"
                "2. TIEMPO DE RESIDENCIA: En Mendoza, crudos de 18-24° API requieren tiempos de retención mayores a 45 minutos para lograr un BSW < 0.5%.\n"
                "3. EFECTO DE LA SAL: El agua remanente lleva sales (cloruros). El lavado con agua dulce (wash water) ayuda a diluir y extraer estas sales."
            ),
            "formula": "V_asentamiento = (Diferencia_Densidades * g * d^2) / (18 * viscosidad)"
        },
        "30. Dinámica de Pozos: Curvas IPR (Inflow Performance Relationship)": {
            "resumen": "Relación entre presión de fondo y caudal de producción.",
            "detalle": (
                "1. MÉTODO DE VOGEL: Utilizado para reservorios donde hay gas libre (empuje por gas disuelto). La curva no es lineal.\n"
                "2. EFECTO SKIN (Daño): Un Skin positivo indica que la formación cerca del pozo está tapada por lodos o finos, reduciendo la productividad.\n"
                "3. OPTIMIZACIÓN: Al cruzar la IPR con la curva de levantamiento (VLP), el técnico determina el punto óptimo de operación de la bomba."
            ),
            "formula": r"Q/Q_{max} = 1 - 0.2(P_{wf}/P_r) - 0.8(P_{wf}/P_r)^2"
        },
        "31. Separación de Gas: Plantas de Ajuste de Punto de Rocío (Dew Point)": {
            "resumen": "Eliminación de hidrocarburos pesados en corrientes de gas.",
            "detalle": (
                "1. EFECTO JOULE-THOMSON: Al expandir el gas bruscamente a través de una válvula JT, la temperatura cae drásticamente, condensando los líquidos.\n"
                "2. CICLO DE REFRIGERACIÓN: Uso de propano externo para enfriar el gas y extraer gasolinas (LPG).\n"
                "3. TORRES ESTABILIZADORAS: Separan los componentes livianos de los líquidos condensados para que el producto sea estable para transporte."
            ),
            "formula": "T_{final} = f(P_{entrada}, P_{salida}, \gamma_{gas})"
        },
        "32. Corrosión Atmosférica e Interna: Monitoreo Crítico": {
            "resumen": "Degradación química de metales en instalaciones.",
            "detalle": (
                "1. CUPONES DE CORROSIÓN: Placas de metal testigo que se insertan en la cañería para medir la pérdida de peso por año (mpy).\n"
                "2. CORROSIÓN POR CO2 (Sweet Corrosion): Forma ácido carbónico que genera picaduras (pitting) profundas.\n"
                "3. CORROSIÓN MICROBIOLÓGICA (SRB): Bacterias que 'comen' hierro y generan H2S localmente, causando fallas catastróficas."
            ),
            "formula": "mpy = (534 \cdot Perdida\_Peso) / (Area \cdot Tiempo \cdot Densidad)"
        },
        "33. Instrumentación Avanzada: Lazos de Control PID": {
            "resumen": "Automatización y estabilidad de procesos en planta.",
            "detalle": (
                "1. ACCIÓN PROPORCIONAL (P): Responde al error actual.\n"
                "2. ACCIÓN INTEGRAL (I): Elimina el error residual acumulado en el tiempo.\n"
                "3. ACCIÓN DERIVATIVA (D): Predice errores futuros según la velocidad del cambio. Vital para control de nivel en separadores pequeños."
            ),
            "formula": "Salida = K_p \cdot e(t) + K_i \int e(t)dt + K_d \frac{de}{dt}"
        },
        "34. Bombas de Cavidad Progresiva (PCP)": {
            "resumen": "Producción de crudos viscosos y con arena.",
            "detalle": (
                "1. ESTATOR Y ROTOR: El estator es de elastómero (goma) y el rotor de acero cromado. La interferencia entre ambos genera el sello.\n"
                "2. ELASTÓMEROS: Deben elegirse según el tipo de crudo (aromático o parafínico) para evitar que la goma se hinche o se degrade.\n"
                "3. TORSIÓN DE VARILLAS: A diferencia del AIB, aquí las varillas rotan. Un torque excesivo puede desenroscar o cortar la sarta."
            ),
            "formula": "Q_{teorico} = 4 \cdot E \cdot D \cdot P \cdot RPM"
        },
        "35. Gestión de Tanques: Calibración y Aforo": {
            "resumen": "Control de inventarios y transferencia de custodia.",
            "detalle": (
                "1. TABLA DE AFORO: Convierte cm de nivel en m3. Debe contemplar la deformación del tanque por el peso del líquido (flecha).\n"
                "2. TECHO FLOTANTE: Reduce las pérdidas por evaporación y el riesgo de incendio al eliminar el espacio gaseoso.\n"
                "3. AGUA LIBRE VS AGUA EMULSIONADA: La purga solo elimina el agua libre del fondo; la emulsionada requiere químicos y tiempo."
            ),
            "formula": "V_{neto} = V_{bruto} \cdot FCT \cdot FP"
        },
        "36. Seguridad de Procesos: Análisis de Capas de Protección (LOPA)": {
            "resumen": "Prevención de eventos de baja probabilidad y alta consecuencia.",
            "detalle": (
                "1. BARRERAS PASIVAS: Diques de contención y muros cortafuego.\n"
                "2. BARRERAS ACTIVAS: Válvulas ESD, PSV y sistemas de diluvio.\n"
                "3. SIL (Safety Integrity Level): Nivel de confiabilidad de un sistema instrumentado de seguridad."
            ),
            "formula": "Riesgo = Frecuencia \cdot Consecuencia"
        },
        "37. Geomecánica y Estimulación Hidráulica (Fracking)": {
            "resumen": "Intervención en reservorios no convencionales.",
            "detalle": (
                "1. PRESIÓN DE RUPTURA: Presión necesaria para vencer el esfuerzo mínimo de la roca y abrir una fractura.\n"
                "2. AGENTE SOSTÉN (Proppant): Arena de alta resistencia que mantiene la fractura abierta cuando cesa la presión de bombeo.\n"
                "3. MICRO-SÍSMICA: Monitoreo de los 'ruidos' de la roca para mapear hacia dónde creció la fractura."
            ),
            "formula": "P_{frac} = P_{friccion} + P_{hidrostatica} + P_{cabeza}"
        },
        "38. Sistemas de Gas Lift (Bombeo Neumático)": {
            "resumen": "Inyección de gas para alivianar la columna de fluido.",
            "detalle": (
                "1. VÁLVULAS DE MANDRIL: Válvulas calibradas que abren a distintas presiones para permitir el paso de gas al tubing.\n"
                "2. PUNTO DE INYECCIÓN: El gas se inyecta lo más profundo posible para maximizar la reducción de densidad.\n"
                "3. INTERMITENTE VS CONTINUO: El intermitente se usa en pozos de baja productividad (acumula y empuja un bache)."
            ),
            "formula": "\Delta P = \rho_{fluido} \cdot g \cdot h"
        },
        "39. Calentadores de Fuego Directo e Indirecto": {
            "resumen": "Preparación del crudo para separación y bombeo.",
            "detalle": (
                "1. BAÑO DE AGUA: En calentadores indirectos, el fuego calienta agua y esta calienta el serpentín del crudo (más seguro).\n"
                "2. EFICIENCIA TÉRMICA: Una mala combustión (exceso de aire) desperdicia gas y genera depósitos de hollín en los tubos.\n"
                "3. CONTROL DE LLAMA: El sistema 'Burner Management System' (BMS) corta el gas si detecta que la llama se apagó."
            ),
            "formula": "Q = m \cdot C_p \cdot (T_{salida} - T_{entrada})"
        },
        "40. Despacho de Crudo: Oleoductos y Estaciones de Bombeo": {
            "resumen": "Transporte masivo de hidrocarburos.",
            "detalle": (
                "1. LÍNEA DE GRADIENTE HIDRÁULICO: Representa la caída de presión a lo largo del ducto debido a la fricción.\n"
                "2. SOBREPRESIONES (Surge): Causadas por el cierre rápido de válvulas. Se protegen con sistemas de alivio de transitorios.\n"
                "3. RASHIG RINGS / SCRAPERS: Limpieza interna periódica para mantener la capacidad de transporte."
            ),
            "formula": "h_f = f \cdot \frac{L}{D} \cdot \frac{v^2}{2g}"
        },
        "41. Análisis de Fallas en Varillas de Bombeo": {
            "resumen": "Identificación de fatiga y fallas mecánicas en AIB.",
            "detalle": (
                "1. FATIGA POR TENSIÓN: Causa el 90% de las roturas. Se identifica por una superficie de fractura lisa con marcas de 'playa'.\n"
                "2. CORROSIÓN-FATIGA: El H2S o CO2 acelera el proceso de rotura. Se previene con inhibidores y evitando el pandeo (buckling).\n"
                "3. MARCAS DE LLAVE: Una mala manipulación con las llaves de potencia crea concentradores de tensión que inician la grieta."
            ),
            "formula": "Tension_Max = (Carga_Pulida / Area_Varilla)"
        },
        "42. Tecnología de Inyección de Polímeros (EOR)": {
            "resumen": "Recuperación Terciaria para mejorar la eficiencia de barrido.",
            "detalle": (
                "1. VISCOSIFICACIÓN: El polímero aumenta la viscosidad del agua inyectada para que 'empuje' mejor el petróleo pesado.\n"
                "2. RELACIÓN DE MOVILIDAD: El objetivo es que el agua no 'dedee' (fingering) a través del petróleo.\n"
                "3. DEGRADACIÓN MECÁNICA: El polímero es sensible al cizallamiento en válvulas y bombas; debe manejarse con baja velocidad de flujo."
            ),
            "formula": "M = (k_w / \mu_w) / (k_o / \mu_o)"
        },
        "43. Medición Multifásica (Virtual Flow Metering)": {
            "resumen": "Estimación de caudales sin separación física.",
            "detalle": (
                "1. PRINCIPIO: Uso de modelos matemáticos y sensores de presión/temperatura para deducir cuánto gas, agua y crudo fluye.\n"
                "2. VENTAJAS: Reduce el costo de instalar grandes separadores de ensayo en locaciones remotas.\n"
                "3. REDES NEURONALES: Los sistemas modernos aprenden del comportamiento histórico del pozo para ganar precisión."
            ),
            "formula": "Q_{total} = f(P_{anular}, P_{tubing}, \%Choke)"
        },
        "44. Estabilidad de Pozo y Ventana Operativa": {
            "resumen": "Geomecánica aplicada para evitar colapsos.",
            "detalle": (
                "1. PRESIÓN DE POROS: La presión natural de los fluidos dentro de la roca.\n"
                "2. GRADIENTE DE FRACTURA: El límite superior de presión antes de romper la formación de forma no deseada.\n"
                "3. DENSIDAD DEL LODO: Debe mantenerse dentro de la 'ventana' para que el pozo no fluya (kick) ni se pierda circulación."
            ),
            "formula": "P_{pore} < P_{hidrostatica} < P_{fractura}"
        },
        "45. Deshidratación de Gas con Glicol (TEG)": {
            "resumen": "Proceso de absorción para alcanzar especificación de venta.",
            "detalle": (
                "1. TORRE CONTACTORA: El glicol pobre 'cae' y absorbe el agua del gas que 'sube'.\n"
                "2. REGENERACIÓN: El glicol rico (con agua) se calienta en el reboiler para evaporar el agua y reutilizar el glicol.\n"
                "3. PUNTO DE ROCÍO DE GAS: El objetivo suele ser < 7 lb H2O / MMSCF para evitar hidratos en el gasoducto."
            ),
            "formula": "Eficiencia = f(Tasa_Glicol, Nro_Platos)"
        },
        "46. Gestión de Paros de Planta (Turnarounds)": {
            "resumen": "Planificación de mantenimiento mayor.",
            "detalle": (
                "1. CAMINO CRÍTICO: Identificación de las tareas que, si se retrasan, postergan todo el arranque de la planta.\n"
                "2. DESPRESURIZACIÓN Y PURGADO: El paso más crítico para la seguridad del personal de mantenimiento.\n"
                "3. TRABAJOS EN CALIENTE: Protocolos estrictos de medición de explosividad (LEL) constantes."
            ),
            "formula": "Disponibilidad = (Tiempo_Operativo / Tiempo_Total) * 100"
        },
        "47. Caracterización de Crudos: Curva TBP": {
            "resumen": "True Boiling Point y rendimiento de destilería.",
            "detalle": (
                "1. FRACCIONAMIENTO: Determinación de qué porcentaje de crudo se convertirá en Nafta, Gasoil o Residuos.\n"
                "2. FACTOR DE CARACTERIZACIÓN (K): Indica si un crudo es más parafínico, nafténico o aromático.\n"
                "3. CONTENIDO DE AZUFRE: Crucial para el precio de venta (crudos 'sweet' vs 'sour')."
            ),
            "formula": "K = (VARTB)^{1/3} / GE"
        },
        "48. Telemetría y Edge Computing": {
            "resumen": "El futuro del control remoto en yacimientos inteligentes.",
            "detalle": (
                "1. IIoT (Internet Industrial de las Cosas): Sensores inalámbricos de bajo consumo que reportan cada 1 segundo.\n"
                "2. EDGE COMPUTING: El procesamiento de datos ocurre en el pozo, no en la nube, permitiendo cierres de emergencia instantáneos.\n"
                "3. PROTOCOLO MQTT: Estándar liviano para transmitir datos en zonas con mala señal de celular."
            ),
            "formula": "Latencia < Tiempo_Respuesta_Seguridad"
        },
        "49. Logística de Hidrocarburos: Baches y Planificación": {
            "resumen": "Manejo de poliductos y transporte.",
            "detalle": (
                "1. INTERFASE: La zona de mezcla entre dos productos diferentes (ej. crudo liviano y pesado) en un mismo ducto.\n"
                "2. PROGRAMACIÓN DE BOMBEO: Coordinación para que el producto llegue a la refinería justo cuando se necesita (Just in Time).\n"
                "3. ALMACENAMIENTO ESTRATÉGICO: Gestión de stock para absorber paradas imprevistas en los yacimientos."
            ),
            "formula": "Vol_Interface = f(Diametro, Longitud, Reynolds)"
        },
        "50. Liderazgo en Gestión de la Seguridad Operacional (PSM)": {
            "resumen": "Cultura de seguridad para el Técnico Líder.",
            "detalle": (
                "1. DISCIPLINA OPERATIVA: Hacer las tareas siempre de la misma forma, siguiendo el procedimiento, incluso cuando nadie mira.\n"
                "2. GESTIÓN DEL ERROR HUMANO: Aceptar que el humano se equivoca y diseñar sistemas que perdonen el error (Poka-yoke).\n"
                "3. LECCIONES APRENDIDAS: Analizar incidentes de otras plantas para evitar que ocurran en la propia (Memoria Institucional)."
            ),
            "formula": "Cultura = Comportamiento + Compromiso"
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
            
# --- DENTRO DE LA FUNCIÓN mostrar_manual() ---

        with col_pdf:
            st.write("**Certificación y Descarga**")
            
            def generar_pdf_pro():
                pdf = FPDF()
                pdf.add_page()
                
                # --- Encabezado Institucional ---
                try:
                    # Agregamos el logo al manual también
                    pdf.image("assets/logo_menfa.png", x=10, y=10, w=30)
                    pdf.ln(20)
                except:
                    pdf.ln(10)

                # Sello de Certificación (Si aprobó con 80+)
                puntaje_actual = st.session_state.get('puntaje_examen', 0)
                if puntaje_actual >= 80:
                    pdf.set_font("Helvetica", "B", 12)
                    pdf.set_text_color(0, 128, 0)
                    pdf.cell(0, 10, f"ESTADO: USUARIO CERTIFICADO ({puntaje_actual}/100 PTS)", ln=True, align='C')
                    pdf.ln(5)
                
                pdf.set_font("Helvetica", "B", 16)
                pdf.set_text_color(0, 51, 102) # Azul Petróleo
                pdf.cell(0, 10, "MANUAL TECNICO DE PRODUCCION IPCL 3.0", ln=True, align='C')
                
                pdf.set_font("Helvetica", "I", 10)
                pdf.set_text_color(100, 100, 100)
                pdf.cell(0, 10, "Menfa Capacitaciones - Director: Fabricio Pizzolato", ln=True, align='C')
                pdf.ln(10)

                # --- Contenido Dinámico ---
                for tit, info in teoria_petrolera.items():
                    # Título de Sección
                    pdf.set_font("Helvetica", "B", 12)
                    pdf.set_fill_color(243, 156, 18) # Naranja MENFA
                    pdf.set_text_color(255, 255, 255)
                    pdf.cell(0, 10, tit.encode('latin-1', 'ignore').decode('latin-1'), ln=True, fill=True)
                    
                    # Detalle (con limpieza de caracteres para evitar errores)
                    pdf.set_font("Helvetica", size=10)
                    pdf.set_text_color(0, 0, 0)
                    texto_limpio = info['detalle'].encode('latin-1', 'ignore').decode('latin-1')
                    pdf.multi_cell(0, 7, texto_limpio)
                    
                    # Fórmula en texto simple para el PDF
                    pdf.set_font("Courier", "I", 9)
                    pdf.cell(0, 8, f"Formula Ref: {info['formula']}", ln=True)
                    pdf.ln(5)

                # --- Pie de Página con Firmas ---
                pdf.ln(20)
                y_f = pdf.get_y()
                # Si el contenido es muy largo y la firma queda al borde, fpdf añade hoja sola
                pdf.line(20, y_f, 80, y_f)
                pdf.line(120, y_f, 180, y_f)
                pdf.set_font("Helvetica", "B", 8)
                pdf.text(35, y_f + 5, "Firma Alumno")
                pdf.text(135, y_f + 5, "Firma F. Pizzolato")
                
                return bytes(pdf.output())

            try:
                # Generamos los bytes del PDF
                btn_pdf_data = generar_pdf_pro()
                
                st.download_button(
                    label="📥 Descargar Manual Completo (PDF)",
                    data=btn_pdf_data,
                    file_name=f"Manual_Tecnico_MENFA_{time.strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="btn_manual_pdf"
                )
                st.caption("⚠️ El manual incluye los 24 módulos técnicos actualizados.")
            except Exception as e:
                st.error(f"Error al generar el manual: {e}")

    st.divider()
    st.caption("IPCL MENFA 3.0 - Mendoza, Argentina.")
