import streamlit as st
import sys
import os

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="IPCL MENFA - Simulador 3.0", layout="wide")

# 2. MANEJO DE RUTAS
sys.path.append(os.path.join(os.path.dirname(__file__), "modulos"))
sys.path.append(os.path.join(os.path.dirname(__file__), "motor"))

# 3. IMPORTACIONES DE NUBE (Con manejo de errores para que la app no muera si falla la red)
try:
    from modulos.nube import leer_estado_actual, enviar_falla, resetear_planta, conectar_db
except Exception as e:
    st.error(f"Error de conexión a la nube: {e}")

# 4. INICIALIZACIÓN DEL ESTADO DE SESIÓN
if 'ingresado' not in st.session_state: 
    st.session_state.ingresado = False
if 'rol' not in st.session_state: 
    st.session_state.rol = "alumno"
if 'area_actual' not in st.session_state: 
    st.session_state.area_actual = "🏠 Dashboard"

# --- FUNCIONES DE ACCESO Y SEGURIDAD ---
def login():
    # 1. ESTILOS: Posicionamiento absoluto para "pisar" la imagen
    st.markdown("""
    <style>
    /* Fondo oscuro para toda la página */
    .stApp { background-color: #0e1117; }

    /* Contenedor principal */
    .contenedor-login {
        position: relative;
        width: 100%;
        max-width: 500px; /* Ajustamos al ancho de la imagen */
        margin: auto;
    }

    /* Estilo de los inputs para que sean transparentes y calcen en los cuadros */
    .stTextInput input {
        background-color: rgba(0,0,0,0) !important; /* Transparente total */
        color: white !important;
        border: none !important;
        font-size: 16px !important;
        height: 42px !important;
    }

    /* Ubicación exacta del Usuario */
    div[data-key="u_pizzolato"] {
        position: absolute;
        top: 435px; /* Ajustar este número si no cae justo */
        left: 65px;
        width: 310px;
        z-index: 10;
    }

    /* Ubicación exacta de la Contraseña */
    div[data-key="p_pizzolato"] {
        position: absolute;
        top: 490px; /* Ajustar este número si no cae justo */
        left: 65px;
        width: 310px;
        z-index: 10;
    }

    /* Ubicación exacta del Botón */
    div[data-key="btn_pizzolato"] {
        position: absolute;
        top: 550px;
        left: 65px;
        width: 310px;
        z-index: 10;
    }

    /* Ocultar etiquetas de Streamlit */
    label { display: none !important; }
    
    /* Hacer el botón de Streamlit invisible para que se vea el naranja de abajo */
    div[data-key="btn_pizzolato"] button {
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        height: 45px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 2. ESTRUCTURA: Ponemos la imagen y encima los campos
    st.markdown('<div class="contenedor-login">', unsafe_allow_html=True)
    
    # Imagen de fondo (la que ya tiene los cuadros dibujados)
    st.image("assets/login_menfa.png", use_container_width=True)

    # Inputs con llaves (keys) específicas para que el CSS los encuentre
    u = st.text_input("U", key="u_pizzolato")
    p = st.text_input("P", type="password", key="p_pizzolato")
    
    # Botón invisible sobre el botón naranja de la imagen
    if st.button("INGRESAR", key="btn_pizzolato", use_container_width=True):
        if u == "admin" and p == "menfa2026":
            st.session_state.ingresado = True
            st.session_state.rol = "instructor"
            st.rerun()
        elif u == "alumno" and p == "alumno2026":
            st.session_state.ingresado = True
            st.session_state.rol = "alumno"
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

    st.markdown('</div>', unsafe_allow_html=True)

def verificar_emergencias_remotas():
    """Función que bloquea al alumno si hay una falla activa en Firebase"""
    try:
        estado = leer_estado_actual()
        if estado and estado.get("activo"):
            st.markdown("<style>.stApp {background-color: #3e0000 !important;}</style>", unsafe_allow_html=True)
            st.error(f"🚨 EMG_LNZ OPR")
            st.header(estado['falla'])
            st.warning(estado['descripcion'])
            respuesta = st.text_area("Procedimiento de Maniobra:")
            if st.button("Enviar Respuesta"):
                st.success("Respuesta enviada. Esperando normalización.")
            st.stop() 
    except:
        pass

# --- PANEL DEL INSTRUCTOR (F. PIZZOLATO) ---

def modulo_instructor_pizzolato():
    st.title("👨‍🏫 Comando Maestro - Menfa 3.0")
    col1, col2 = st.columns(2)
    with col1:
        falla = st.selectbox("Inyectar Falla:", ["Fuga de H2S", "Cavitación", "BSW Alto", "ESD Activada"])
        detalles = st.text_area("Descripción del síntoma:")
        if st.button("🔴 LANZAR EMERGENCIA"):
            enviar_falla(falla, detalles)
            st.toast("Falla enviada")
    with col2:
        if st.button("🟢 NORMALIZAR PLANTA"):
            resetear_planta()
            st.success("Planta reseteada")

# --- NUEVO MÓDULO OPERATIVO: TAREAS DEL RECORREDOR ---

def mostrar_modulo_produccion_recorredor():
    import pandas as pd
    import time

    st.title("🏭 Módulo de Producción Petrolera y Tareas del Recorredor")
    st.caption("Software de Simulación y Capacitación - IPCL MENFA")

    # Pestañas del módulo basándonos en el manual técnico
    tab1, tab2, tab3 = st.tabs([
        "🌿 Proceso en Batería y Recorrida", 
        "🤖 Simulación de Señales SCADA (4-20mA)", 
        "📋 Evaluación de Seguridad y Operación"
    ])

    # ==========================================
    # PESTAÑA 1: PROCESO Y RECORRIDA
    # ==========================================
    with tab1:
        st.header("Flujo del Fluido y Operaciones en Batería")
        st.write(
            "La función principal de una batería es reunir la producción de un grupo de pozos "
            "para separar el gas, el agua y el petróleo, además de almacenar y medir caudales."
        )
        
        # Simulación visual del Manifold de ingreso
        st.subheader("🎛️ Operación del Manifold de Ingreso (Colector)")
        st.info(
            "**Regla Operativa:** La apertura y cierre de válvulas debe practicarse de forma "
            "simultánea (abrir primero, luego cerrar) de manera gradual para evitar golpes de ariete."
        )
        
        pozo_seleccionado = st.selectbox("Seleccionar Pozo para Ensayar:", ["Pozo Productor MENFA-01", "Pozo Productor MENFA-02", "Pozo Productor MENFA-03"])
        linea_derivacion = st.radio("Derivar flujo hacia:", ["Línea General (Producción Total)", "Separador de Ensayo (Control Individual)"])
        
        if st.button("Ejecutar Maniobra de Válvulas"):
            with st.spinner("Cambiando configuración en el colector..."):
                time.sleep(1.5)
                st.success(f"Maniobra exitosa. El {pozo_seleccionado} ahora está derivado a {linea_derivacion}.")
                st.warning("🔄 Recuerda revisar el circuito de flujo para comprobar la eficacia de la maniobra realizada.")

        st.markdown("---")
        st.subheader("⚙️ Equipos Principales y Línea de Tratamiento")
        
        with st.expander("1. Separadores y Gravitación"):
            st.write("La disociación gas-líquido en el interior del separador se produce principalmente por **efecto de gravitación**, separando los fluidos por diferencia de densidad.")
        
        with st.expander("2. Deshidratación del Gas e Hidratos"):
            st.write("El vapor de agua en el gas disminuye la eficiencia y, en invierno, provoca obstrucciones por congelamiento o formación de **hidratos** (compuestos sólidos con apariencia de hielo). Se requiere el uso de torres de absorción a glicol.")

        with st.expander("3. Transferencia de Custodia (Unidad LACT)"):
            st.write("El líquido acondicionado se almacena y transfiere a oleoductos mediante unidades de Transferencia Automática de Producción en Custodia (LACT).")

    # ==========================================
    # PESTAÑA 2: SIMULACIÓN SCADA
    # ==========================================
    with tab2:
        st.header("Conversión Analógica a Digital (Lógica del PLC/RTU)")
        st.write(
            "Los sistemas SCADA e instrumentos de campo utilizan el estándar industrial de **4-20 miliamperios (mA)** "
            "para transmitir variables físicas de forma eléctrica hacia la RTU o PLC."
        )
        st.info("💡 **Dato del Manual:** Cuando la variable está en 0, circula un mínimo de 4mA para verificar que el circuito eléctrico esté sano.")

        # Configuración del instrumento simulado
        rango_max_presion = st.number_input("Rango Máximo del Transmisor de Presión (PT) en Kg/cm²:", min_value=1.0, max_value=100.0, value=10.0)
        presion_actual = st.slider("Presión Actual en Campo (Kg/cm²):", min_value=0.0, max_value=float(rango_max_presion), value=float(rango_max_presion*0.4), step=0.1)

        # Cálculos de conversión basados en las fórmulas de cuentas y mA
        factor_ma = (presion_actual / rango_max_presion) * 16 + 4
        cuentas_plc = int((presion_actual / rango_max_presion) * (4000 - 800) + 800)

        # Renderizar en tres columnas visuales
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Presión Física", value=f"{presion_actual:.2f} Kg/cm²")
        col2.metric(label="Señal de Corriente", value=f"{factor_ma:.2f} mA")
        col3.metric(label="Cuentas en RTU/PLC", value=f"{cuentas_plc} pts")

        # Gráfico dinámico de simulación de alarma SCADA
        st.subheader("🚨 Lógica de Control de Alarmas (Set Points)")
        set_point_alto = rango_max_presion * 0.8
        
        st.write(f"**Set Point de Alarma Alta:** {set_point_alto:.1f} Kg/cm²")
        
        if presion_actual >= set_point_alto:
            st.error(f"⚠️ CONDICIÓN DE ALARMA: 'Alto Nivel / Presión en Instalación'. Notificando al Servidor SCADA central. Requiere reconocimiento del operador.")
        else:
            st.success("🟢 Operación normal de campo. Variables dentro de parámetros normales.")

    # ==========================================
    # PESTAÑA 3: EVALUACIÓN DE RECORREDOR
    # ==========================================
    with tab3:
        st.header("Examen Técnico de Normas Operativas y de Seguridad")
        st.write("Test de evaluación para personal ingresante y técnicos de producción.")

        puntaje = 0
        
        # Pregunta 1
        p1 = st.radio(
            "1. ¿Qué se deduce si un instrumento de campo reporta una corriente de 0 mA de forma lineal?",
            ["Que la variable medida está exactamente en cero.", 
             "Que existe una anomalía o rotura en el circuito eléctrico (ya que el cero equivale a 4mA).", 
             "Que el PLC está saturado."]
        )
        if p1 == "Que existe una anomalía o rotura en el circuito eléctrico (ya que el cero equivale a 4mA).":
            puntaje += 1.0

        # Pregunta 2
        p2 = st.radio(
            "2. Ante una duda en la ejecución de una maniobra operativa compleja en los pozos, ¿cuál es la acción correcta?",
            ["Proceder con cautela basándose en la experiencia previa.",
             "Preguntar la cantidad de veces que sea necesario al supervisor, aunque parezca molesto.",
             "Dejar la maniobra pendiente para el cambio de turno."]
        )
        if p2 == "Preguntar la cantidad de veces que sea necesario al supervisor, aunque parezca molesto.":
            puntaje += 1.0

        # Pregunta 3
        p3 = st.radio(
            "3. Si un recorredor presenta fatiga intensa o somnolencia severa durante su turno de conducción, ¿qué indica el procedimiento?",
            ["Consumir café o energizantes y circular a menor velocidad.",
             "Continuar la marcha para no retrasar el parte diario.",
             "Detener la conducción, hablar de forma franca con el supervisor y solicitar el relevo inmediato del día."]
        )
        if p3 == "Detener la conducción, hablar de forma franca con el supervisor y solicitar el relevo inmediato del día.":
            puntaje += 1.0

        # Botón de evaluar
        if st.button("Calificar Evaluación Técnico-Operativa"):
            porcentaje = (puntaje / 3.0) * 100
            if porcentaje >= 100:
                st.balloons()
                st.success(f"🎯 Calificación: {porcentaje:.1f}%. ¡Aprobado! El alumno incorpora plenamente los procedimientos de seguridad y cultura operativa.")
            else:
                st.warning(f"⚠️ Calificación: {porcentaje:.1f}%. Se sugiere repasar los capítulos de 'Señales Eléctricas' y 'Normas de Seguridad Humana' del manual.")

# --- APP PRINCIPAL (CON TODOS LOS MÓDULOS) ---

def main_app():
    if st.session_state.rol == "alumno":
        verificar_emergencias_remotas()

    # RESTAURACIÓN TOTAL DE OPCIONES
    opciones_menu = [
        "🏠 Dashboard", 
        "🛢️ Operaciones de Campo",
        "🗺️ Mapa del Campo", 
        "📊 Campo Petrolero",
        "🏭 Planta de Proceso",
        "📦 Equipos de Planta",
        "📈 Ingeniería",
        "⚙️ Ingeniería de Producción",
        "🖥️ Monitoreo SCADA",
        "📋 Gestión y Reportes",
        "🛠️ Mantenimiento e Integridad",
        "🧠 Evaluación",
        "🎯 Entrenamiento Operativo",
        "📘 Manual"
    ]

    with st.sidebar:
        try: st.image("assets/logo_menfa.png")
        except: st.write("### IPCL MENFA")
        
        st.write(f"👤 **Rol:** {st.session_state.rol.upper()}")
        
        try: idx = opciones_menu.index(st.session_state.area_actual)
        except: idx = 0

        area = st.radio("Navegación:", opciones_menu, index=idx)
        
        if area != st.session_state.area_actual:
            st.session_state.area_actual = area
            st.rerun()
        
        if st.button("🚪 Salir"):
            st.session_state.clear()
            st.rerun()

    # --- MOTOR DE ENRUTAMIENTO ---
    actual = st.session_state.area_actual

    if actual == "🏠 Dashboard":
        from modulos.dashboard_principal import dashboard_principal
        dashboard_principal()
    elif actual == "🛢️ Operaciones de Campo":
        from modulos.pozo_productor import pozo_productor
        pozo_productor()
    elif actual == "🗺️ Mapa del Campo":
        from modulos.mapa_campo import mostrar_mapa
        mostrar_mapa()
    elif actual == "📊 Campo Petrolero":
        from modulos.campo_petrolero import mostrar_estadisticas
        mostrar_estadisticas()
    elif actual == "🏭 Planta de Proceso":
        from modulos.planta_produccion import planta_produccion
        planta_produccion()
    elif actual == "📦 Equipos de Planta":
        from modulos.equipos_planta import mostrar_equipos_planta
        mostrar_equipos_planta()
    elif actual == "📈 Ingeniería":
        from modulos.ingenieria import mostrar_ingenieria
        mostrar_ingenieria()
    elif actual == "⚙️ Ingeniería de Producción":
        from modulos.ingenieria_produccion import mostrar_ingenieria_produccion
        mostrar_ingenieria_produccion()    
    elif actual == "🖥️ Monitoreo SCADA":
        from modulos.scada import show
        show()
    elif actual == "📋 Gestión y Reportes":
        from modulos.gestion_supervisor_prod import gestion_supervisor_prod
        gestion_supervisor_prod()
    elif actual == "🛠️ Mantenimiento e Integridad":
        from modulos.mantenimiento_integridad import mostrar_mantenimiento_integridad
        mostrar_mantenimiento_integridad()
    elif actual == "🧠 Evaluación":
        from modulos.evaluacion import evaluacion
        evaluacion()
    elif actual == "🎯 Entrenamiento Operativo":
        from modulos.entrenamiento import mostrar_entrenamiento
        mostrar_entrenamiento()
    elif actual == "📘 Manual":
        # Acoplamiento nativo de la lógica del recorredor y teoría del manual de campo
        mostrar_modulo_produccion_recorredor()

# --- EJECUCIÓN ---
def main():
    if not st.session_state.ingresado:
        login()
    else:
        if st.session_state.rol == "instructor":
            modo = st.sidebar.selectbox("Vista:", ["🖥️ Simulador", "🎮 Control Maestro"])
            if modo == "🎮 Control Maestro": modulo_instructor_pizzolato()
            else: main_app()
        else:
            main_app()

if __name__ == "__main__":
    main()
