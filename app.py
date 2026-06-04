import streamlit as st
import sys
import os

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="IPCL MENFA - Simulador 3.0", layout="wide")

# 2. MANEJO DE RUTAS
sys.path.append(os.path.join(os.path.dirname(__file__), "modulos"))
sys.path.append(os.path.join(os.path.dirname(__file__), "motor"))

# 3. IMPORTACIONES DE MÓDULOS INTERNOS
try:
    from manual_simulador import mostrar_manual
except ModuleNotFoundError:
    st.error("⚠️ No se encontró el archivo 'manual_simulador.py'. Verificá que esté subido a la raíz de GitHub con ese nombre exacto.")

try:
    from modulos.nube import leer_estado_actual, enviar_falla, resetear_planta, conectar_db
except Exception as e:
    st.error(f"Error de conexión a la nube: {e}")

# 📦 IMPORTACIÓN DEL NUEVO MÓDULO DE FÓRMULAS
try:
    from modulos.formulas_produccion import formulas_produccion
except ModuleNotFoundError:
    st.error("⚠️ No se encontró el archivo 'formulas_produccion.py' en la carpeta 'modulos'.")

# 🧠 INTERCONEXIÓN TÉCNICA: IMPORTACIÓN DEL MOTOR DESDE LA CARPETA 'MODULOS' (SIN ACENTOS)
try:
    # Como 'modulos' ya está incorporado al sys.path, Python busca el archivo directamente
    from motor_simulacion import MotorSimulacion
except ModuleNotFoundError:
    try:
        from modulos.motor_simulacion import MotorSimulacion
    except ModuleNotFoundError:
        st.error("⚠️ No se encontró 'motor_simulacion.py'. Verificá las rutas físicas en tu repositorio de GitHub.")

# 4. INICIALIZACIÓN DEL ESTADO DE SESIÓN (PERSISTENCIA GLOBAL)
if 'ingresado' not in st.session_state: 
    st.session_state.ingresado = False
if 'rol' not in st.session_state: 
    st.session_state.rol = "alumno"
if 'area_actual' not in st.session_state: 
    st.session_state.area_actual = "🏠 Dashboard"

# 🚀 INYECCIÓN DEL MOTOR CENTRAL: Inicialización segura en st.session_state
if 'motor' not in st.session_state and 'MotorSimulacion' in locals():
    st.session_state.motor = MotorSimulacion()

# --- FUNCIONES DE ACCESO Y SEGURIDAD ---
def login():
    st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .contenedor-login { position: relative; width: 100%; max-width: 500px; margin: auto; }
    .stTextInput input { background-color: rgba(0,0,0,0) !important; color: white !important; border: none !important; font-size: 16px !important; height: 42px !important; }
    div[data-key="u_pizzolato"] { position: absolute; top: 435px; left: 65px; width: 310px; z-index: 10; }
    div[data-key="p_pizzolato"] { position: absolute; top: 490px; left: 65px; width: 310px; z-index: 10; }
    div[data-key="btn_pizzolato"] { position: absolute; top: 550px; left: 65px; width: 310px; z-index: 10; }
    label { display: none !important; }
    div[data-key="btn_pizzolato"] button { background: transparent !important; border: none !important; color: transparent !important; height: 45px !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="contenedor-login">', unsafe_allow_html=True)
    try:
        st.image("assets/login_menfa.png", use_container_width=True)
    except:
        st.warning("Falta cargar el asset: assets/login_menfa.png")

    u = st.text_input("U", key="u_pizzolato")
    p = st.text_input("P", type="password", key="p_pizzolato")
    
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
    try:
        estado = leer_estado_actual()
        if estado and estado.get("activo"):
            st.markdown("<style>.stApp {background-color: #3e0000 !important;}</style>", unsafe_allow_html=True)
            st.error(f"🚨 EMG_LNZ OPR")
            st.header(estado['falla'])
            st.warning(estado['descripcion'])
            
            # Sincronizar la falla de la nube con el motor físico local usando el método del commit
            if 'motor' in st.session_state:
                st.session_state.motor.simular_golpe_de_gas()
                
            respuesta = st.text_area("Procedimiento de Maniobra:")
            if st.button("Enviar Respuesta"):
                st.success("Respuesta enviada. Esperando normalización.")
            st.stop() 
    except:
        pass

# --- PANEL DEL INSTRUCTOR ---
def modulo_instructor_pizzolato():
    st.title("👨‍🏫 Comando Maestro - Menfa 3.0")
    col1, col2 = st.columns(2)
    with col1:
        falla = st.selectbox("Inyectar Falla:", ["Fuga de H2S", "Cavitación", "BSW Alto", "ESD Activada"])
        detalles = st.text_area("Descripción del síntoma:")
        if st.button("🔴 LANZAR EMERGENCIA"):
            enviar_falla(falla, detalles)
            if 'motor' in st.session_state:
                if falla == "ESD Activada":
                    st.session_state.motor.activar_esd()
                else:
                    st.session_state.motor.simular_golpe_de_gas()
            st.toast("Falla enviada e inyectada en el motor")
    with col2:
        if st.button("🟢 NORMALIZAR PLANTA"):
            resetear_planta()
            if 'motor' in st.session_state:
                st.session_state.motor.reset_planta()
            st.success("Planta reseteada en entorno local y nube")

# --- PANEL AUXILIAR DEL RECORREDOR ---
def mostrar_modulo_produccion_recorredor():
    st.title("🏭 Módulo Operativo de Respaldo")
    tab1, tab2 = st.tabs(["🎛️ Operación de Colector", "🤖 Lazo SCADA"])
    with tab1:
        st.subheader("Manifold de Ingreso Local")
        pozo = st.selectbox("Seleccionar Pozo:", ["Pozo MENFA-01", "Pozo MENFA-02"])
        if st.button("Traspasar Pozo"):
            st.success(f"{pozo} Conmutado con éxito.")
    with tab2:
        if 'motor' in st.session_state and hasattr(st.session_state.motor, 'estado'):
            presion_real = st.session_state.motor.estado["separador"]["presion"]
            ma = 4.0 + (presion_real / 160.0) * 16.0
            st.metric("Señal patrón Transmisor Presión", f"{ma:.2f} mA")
        elif 'motor' in st.session_state:
            # Compatibilidad con las variables directas de tu motor actual en GitHub
            presion_real = st.session_state.motor.presion
            ma = 4.0 + (presion_real / 160.0) * 16.0
            st.metric("Señal patrón Transmisor Presión (Modo Directo)", f"{ma:.2f} mA")
        else:
            st.metric("Señal patrón", "12.00 mA")

# --- APP PRINCIPAL (CON TODOS LOS MÓDULOS) ---
def main_app():
    if st.session_state.rol == "alumno":
        verificar_emergencias_remotas()

    opciones_menu = [
        "🏠 Dashboard", 
        "🛢️ Operaciones de Campo",
        "🗺️ Mapa del Campo", 
        "📊 Campo Petrolero",
        "🏭 Planta de Proceso",
        "📦 Equipos de Planta",
        "📈 Ingeniería",
        "⚙️ Ingeniería de Producción",
        "🧮 Fórmulas de Producción Petrolera",
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

    # --- MOTOR DE ENRUTAMIENTO (Actualización de físicas en background) ---
    actual = st.session_state.area_actual

    # Ejecución adaptada a los métodos reales del commit en tu GitHub (Evita el AttributeError)
    if 'motor' in st.session_state:
        if hasattr(st.session_state.motor, 'actualizar_ciclo'):
            st.session_state.motor.actualizar_ciclo()
        else:
            # Llama al método existente que calcula fluctuaciones aleatorias en tu código de hace 2 meses
            _ = st.session_state.motor.obtain_datos() if hasattr(st.session_state.motor, 'obtain_datos') else st.session_state.motor.obtener_datos()

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
    elif actual == "🧮 Fórmulas de Producción Petrolera":
        formulas_produccion()
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
        try:
            mostrar_manual()
        except NameError:
            st.warning("La función 'mostrar_manual' no se pudo ejecutar porque falló la importación inicial.")

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
