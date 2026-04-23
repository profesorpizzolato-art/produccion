# modulos/banco_preguntas.py

CUESTIONARIO_PRODUCCION = [
    # --- BLOQUE 1: INGENIERÍA DE NODOS ---
    {
        "tipo": "TEORIA",
        "pregunta": "¿Qué representa técnicamente el punto donde se cruzan las curvas IPR y VLP?",
        "opciones": ["La presión máxima del reservorio", "El caudal máximo teórico (AOF)", "El punto de operación real del sistema pozo-línea", "El límite de burbuja del fluido"],
        "respuesta": 2
    },
    {
        "tipo": "TAREA",
        "pregunta": "PRÁCTICA: En el módulo IPR/VLP, sube el Índice de Productividad (IP) a 3.0. ¿Qué efecto observas en la curva de oferta (IPR)?",
        "opciones": ["La curva se vuelve más vertical (menos pendiente)", "La curva se vuelve más horizontal (mayor aporte)", "La curva no se mueve", "La presión de reservorio aumenta"],
        "respuesta": 1
    },
    # --- BLOQUE 2: PROCESAMIENTO Y SEPARACIÓN ---
    {
        "tipo": "TEORIA",
        "pregunta": "En un separador horizontal, ¿para qué sirve la placa deflectora (inlet diverter) en la entrada?",
        "opciones": ["Para aumentar la presión de entrada", "Para el cambio brusco de cantidad de movimiento y separación inicial", "Para calentar el crudo", "Para medir el caudal de gas"],
        "respuesta": 1
    },
    {
        "tipo": "TEORIA",
        "pregunta": "¿Cuál es la función del 'Vortex Breaker' en la salida de líquido de un recipiente?",
        "opciones": ["Evitar que el gas sea arrastrado con el líquido", "Aumentar la velocidad de drenaje", "Separar el agua del petróleo", "Filtrar los sólidos"],
        "respuesta": 0
    },
    # --- BLOQUE 3: FALLAS Y OPERACIÓN ---
    {
        "tipo": "TAREA",
        "pregunta": "DESAFÍO: Activa 'Aumento de Contrapresión' en el Simulador de Fallas. ¿Cómo afecta esto a la energía requerida por la VLP?",
        "opciones": ["Requiere menos presión para mover el mismo caudal", "La curva VLP baja", "Requiere más presión de fondo para vencer la resistencia", "El pozo fluye con mayor facilidad"],
        "respuesta": 2
    },
    {
        "tipo": "TEORIA",
        "pregunta": "Si el nivel de la interfase agua-petróleo en el separador es demasiado alto, ¿qué riesgo operativo es inminente?",
        "opciones": ["Arrastre de petróleo en la línea de agua (Oil carry-over)", "Gas seco en la línea de crudo", "Aumento de la presión de burbuja", "Falla en el compresor de gas"],
        "respuesta": 0
    },
    # --- BLOQUE 4: SEGURIDAD Y PROTOCOLOS (ESD) ---
    {
        "tipo": "TAREA",
        "pregunta": "PROTOCOLO: Activa el ESD en el SCADA. Según el procedimiento de MENFA, ¿qué campo del reporte es vital para el seguro?",
        "opciones": ["La hora del almuerzo", "La descripción detallada de la causa de la parada", "El color de la línea en el gráfico", "El nombre de la empresa de transporte"],
        "respuesta": 1
    },
    {
        "tipo": "TEORIA",
        "pregunta": "¿Qué significa que una válvula SDV sea 'Fail-Safe Close'?",
        "opciones": ["Que abre si pierde suministro de aire/energía", "Que cierra ante una falla de suministro por seguridad", "Que nunca falla", "Que requiere operación manual siempre"],
        "respuesta": 1
    },
    # --- BLOQUE 5: DIAGNÓSTICO AVANZADO ---
    {
        "tipo": "TEORIA",
        "pregunta": "¿Cuál es el principal efecto de la presencia de gas libre en una bomba centrífuga de transferencia?",
        "opciones": ["Aumento de la eficiencia", "Cavitación y pérdida de altura (head)", "Reducción de la viscosidad", "Aumento de la presión de descarga"],
        "respuesta": 1
    },
    {
        "tipo": "TAREA",
        "pregunta": "FINAL: Observa el SCADA en modo normal. Si la presión es 115 psi y el caudal 450 bpd, y de golpe el caudal cae a 100 bpd sin activar el ESD, ¿qué diagnosticarías?",
        "opciones": ["Falla total del reservorio", "Obstrucción severa o rotura de línea de flujo", "El separador se llenó de gas", "Operación normal de rutina"],
        "respuesta": 1
    }
]
