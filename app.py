import streamlit as st
import sys
import os

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="IPCL MENFA - Simulador 3.0", layout="wide")

# 2. MANEJO DE RUTAS
BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(BASE_DIR, "modulos"))
sys.path.append(os.path.join(BASE_DIR, "motor"))

# 3. IMPORTACIONES DE MÓDULOS INTERNOS
try:
    from manual_simulador import mostrar_manual
except ModuleNotFoundError:
    mostrar_manual = None

try:
    from modulos.nube import leer_estado_actual, enviar_falla, resetear_planta, conectar_db
except Exception as e:
    leer_estado_actual = None
    enviar_falla = None
    resetear_planta = None

# MÓDULO DE FÓRMULAS
try:
    from modulos.formulas_produccion import formulas_produccion
except ModuleNotFoundError:
    formulas_produccion = None

# MOTOR DE SIMULACIÓN
MotorSimulacion = None
try:
    from motor_simulacion import MotorSimulacion
except ModuleNotFoundError:
    try:
        from modulos.motor_simulacion import MotorSimulacion
    except ModuleNotFoundError:
        st.error("⚠️ No se encontró 'motor_simulacion.py'. Verificá las rutas en tu repositorio.")

# 4. INICIALIZACIÓN DEL ESTADO DE SESIÓN
if 'ingresado' not in st.session_state: 
    st.session_state.ingresado = False
if 'rol' not in st.session_state: 
    st.session_state.rol = "alumno"
if 'area_actual' not in st.session_state: 
    st.session_state.area_actual = "🏠 Dashboard"

if 'motor' not in st.session_state and MotorSimulacion is not None:
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
    if os.path.exists("assets/login_menfa.png"):
        st.image("assets/login_menfa.png", use_container_width=True)
    else:
        st.info("📌 IPCL MENFA - Control de Acceso")

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
    if not callable(leer_estado_actual):
        return
    try:
        estado = leer_estado_actual()
        if estado and estado.get("activo"):
            st.markdown("<style>.stApp {background-color: #3e0000 !important;}</style>", unsafe_allow_html=True)
            st.error("🚨 EMG_LNZ OPR")
            st.header(estado.get('falla', 'Emergencia Remota'))
            st.warning(estado.get('descripcion', 'Atención requerida'))
            
            if 'motor' in st.session_state and hasattr(st.session_state.motor, 'simular_golpe_de_gas'):
                st.session_state.motor.simular_golpe_de_gas()
                
            respuesta = st.text_area("Procedimiento de Maniobra:")
            if st.button("Enviar Respuesta"):
                st.success("Respuesta enviada. Esperando normalización.")
            st.stop() 
    except Exception as e:
        st.sidebar.caption(f"Status Nube: Desconectado ({e})")

# --- PANEL DEL INSTRUCTOR ---
from streamlit_autorefresh import st_autorefresh

# --- PANEL DEL INSTRUCTOR ---
def modulo_instructor_pizzolato():
    st.title("👨‍🏫 Comando Maestro - Menfa 3.0")
    
    # 🔄 Configurar auto-refresco cada 3 segundos
    st_autorefresh(interval=3000, key="auto_refresco_instructor")
    
    # 🔍 Consultamos el estado actual en la nube
    if callable(leer_estado_actual):
        estado_nube = leer_estado_actual()
        if estado_nube:
            falla_activa = estado_nube.get("activo", False)
            respuesta_alumno = estado_nube.get("respuesta", "")
            calificacion_actual = estado_nube.get("calificacion", "")
            
            with st.container():
                st.subheader("📊 Monitoreo de Emergencia Activa")
                if falla_activa:
                    st.warning(f"⚠️ **Falla en curso:** {estado_nube.get('falla', 'N/A')} — *{estado_nube.get('descripción', '')}*")
                else:
                    st.success("🟢 Sistema Normalizado. No hay emergencias activas.")
                
                # Visualización de la respuesta y botones de calificación
                st.markdown("### 📥 Respuesta del Alumno:")
                if respuesta_alumno and respuesta_alumno.strip() != "":
                    st.success("¡El alumno ha enviado su procedimiento de maniobra!")
                    st.info(f"**Procedimiento redactado:**\n\n{respuesta_alumno}")
                    
                    # Estado de la calificación actual
                    if calificacion_actual == "Aprobado":
                        st.success("⭐ **Estado:** Calificado como **APROBADO** por el instructor.")
                    elif calificacion_actual == "Rechazado":
                        st.error("❌ **Estado:** Calificado como **RECHAZADO**. El alumno debe reintentar.")
                    else:
                        st.warning("⚠️ Pendiente de calificación.")
                    
                    # Botones de evaluación
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("✅ Aprobar Respuesta"):
                            from modulos.nube import calificar_respuesta_alumno
                            if calificar_respuesta_alumno("Aprobado"):
                                st.toast("¡Respuesta aprobada con éxito!")
                                st.rerun()
                    with col_btn2:
                        if st.button("❌ Rechazar Respuesta"):
                            from modulos.nube import calificar_respuesta_alumno
                            if calificar_respuesta_alumno("Rechazado"):
                                st.toast("Respuesta rechazada.")
                                st.rerun()
                else:
                    st.info("⏳ Esperando que el alumno envíe el procedimiento...")
            
            st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        falla = st.selectbox("Inyectar Falla:", ["Fuga de H2S", "Cavitación", "BSW Alto", "ESD Activada"])
        detalles = st.text_area("Descripción del síntoma:")
        if st.button("🔴 LANZAR EMERGENCIA"):
            if callable(enviar_falla):
                enviar_falla(falla, detalles)
            if 'motor' in st.session_state:
                if falla == "ESD Activada" and hasattr(st.session_state.motor, 'activar_esd'):
                    st.session_state.motor.activar_esd()
                elif hasattr(st.session_state.motor, 'simular_golpe_de_gas'):
                    st.session_state.motor.simular_golpe_de_gas()
            st.toast("Falla enviada e inyectada en el motor")
            st.rerun()
            
    with col2:
        if st.button("🟢 NORMALIZAR PLANTA"):
            if callable(resetear_planta):
                resetear_planta()
            if 'motor' in st.session_state and hasattr(st.session_state.motor, 'reset_planta'):
                st.session_state.motor.reset_planta()
            st.success("Planta reseteada en entorno local y nube")
            st.rerun()

# --- APP PRINCIPAL ---
def main_app():
    if st.session_state.rol == "alumno":
        verificar_emergencias_remotas()

    opciones_menu = [
        "🏠 Dashboard", 
        "🛢️ Operaciones de Campo",
        "🗺️ Mapa del Campo", 
        "📊 Campo Petrolero",
        "🏭 Planta de Proceso",
        "🔬 Laboratorio de Crudo",
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
        if os.path.exists("assets/logo_menfa.png"):
            st.image("assets/logo_menfa.png")
        else:
            st.write("### IPCL MENFA")
        
        st.write(f"👤 **Rol:** {st.session_state.rol.upper()}")
        
        try:
            idx = opciones_menu.index(st.session_state.area_actual)
        except ValueError:
            idx = 0

        area = st.radio("Navegación:", opciones_menu, index=idx)
        
        if area != st.session_state.area_actual:
            st.session_state.area_actual = area
            st.rerun()
        
        if st.button("🚪 Salir"):
            st.session_state.clear()
            st.rerun()

    # --- ACTUALIZACIÓN DE FÍSICAS EN BACKGROUND ---
    if 'motor' in st.session_state:
        motor = st.session_state.motor
        if hasattr(motor, 'actualizar_ciclo'):
            motor.actualizar_ciclo()
        elif hasattr(motor, 'obtain_datos'):
            motor.obtain_datos()
        elif hasattr(motor, 'obtener_datos'):
            motor.obtener_datos()

    # --- MOTOR DE ENRUTAMIENTO SEGURO ---
    actual = st.session_state.area_actual

    try:
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
        elif actual == "🔬 Laboratorio de Crudo":
            from modulos.laboratorio import mostrar_laboratorio_crudo
            if 'motor' in st.session_state:
                bsw_val = getattr(st.session_state.motor, 'bsw', 0.4)
                rvp_val = getattr(st.session_state.motor, 'rvp', 65.0)
                q_val = getattr(st.session_state.motor, 'caudal_base', 450.0)
                mostrar_laboratorio_crudo(bsw_motor=bsw_val, rvp_motor=rvp_val, caudal_motor=q_val)
            else:
                mostrar_laboratorio_crudo()    
        elif actual == "📦 Equipos de Planta":
            from modulos.equipos_planta import mostrar_equipos_planta
            # Extraemos valores dinámicos del motor si están disponibles
            if 'motor' in st.session_state:
                q_act = getattr(st.session_state.motor, 'caudal_base', 450.0)
                bsw_act = getattr(st.session_state.motor, 'bsw', 1.0)
                mostrar_equipos_planta(q_pozo=q_act, bsw_pozo=bsw_act)
            else:
                mostrar_equipos_planta()
        elif actual == "📈 Ingeniería":
            from modulos.ingenieria import mostrar_ingenieria
            mostrar_ingenieria()
        elif actual == "⚙️ Ingeniería de Producción":
            from modulos.ingenieria_produccion import mostrar_ingenieria_produccion
            mostrar_ingenieria_produccion()    
        elif actual == "🧮 Fórmulas de Producción Petrolera":
            if formulas_produccion:
                formulas_produccion()
            else:
                st.warning("⚠️ Módulo de fórmulas no disponible.")
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
            if mostrar_manual:
                mostrar_manual()
            else:
                st.warning("La función 'mostrar_manual' no se pudo ejecutar porque falló la importación inicial.")
    except Exception as err:
        st.error(f"❌ Error al cargar el módulo '{actual}': {err}")

# --- EJECUCIÓN ---
def main():
    if not st.session_state.ingresado:
        login()
    else:
        if st.session_state.rol == "instructor":
            modo = st.sidebar.selectbox("Vista:", ["🖥️ Simulador", "🎮 Control Maestro"])
            if modo == "🎮 Control Maestro": 
                modulo_instructor_pizzolato()
            else: 
                main_app()
        else:
            main_app()

if __name__ == "__main__":
    main()
