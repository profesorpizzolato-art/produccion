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
    # 1. ESTILOS DE PRECISIÓN: Esto ubica los campos EXACTAMENTE sobre la imagen
    st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* El contenedor que encierra la imagen y los inputs */
    .contenedor-login {
        position: relative;
        width: 100%;
        max-width: 800px;
        margin: auto;
    }

    /* CAMPO USUARIO: Ajustado para caer sobre el primer rectángulo */
    .posicion-usuario {
        position: absolute;
        top: 450px; /* Si ves que queda alto o bajo, tocá este número */
        right: 80px;
        width: 250px;
        z-index: 1000;
    }

    /* CAMPO CONTRASEÑA: Ajustado para caer sobre el segundo rectángulo */
    .posicion-password {
        position: absolute;
        top: 515px; /* Si ves que queda alto o bajo, tocá este número */
        right: 80px;
        width: 250px;
        z-index: 1000;
    }

    /* BOTÓN INICIAR: Ajustado para caer sobre el botón naranja */
    .posicion-boton {
        position: absolute;
        top: 590px;
        right: 80px;
        width: 250px;
        z-index: 1000;
    }

    /* ESTILO INVISIBLE: Hace que los cuadros de Streamlit no tengan fondo ni bordes */
    .stTextInput input {
        background-color: transparent !important;
        color: white !important;
        border: none !important;
        font-size: 16px !important;
    }
    
    /* Ocultar etiquetas feas de Streamlit */
    label { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    # 2. ESTRUCTURA VISUAL
    st.markdown('<div class="contenedor-login">', unsafe_allow_html=True)
    
    # Ponemos la imagen de fondo completa
    try:
        st.image("assets/login_menfa.png", use_container_width=True)
    except:
        st.error("No se encontró la imagen en assets/login_menfa.png")

    # Inyectamos los inputs en las posiciones que definimos arriba
    with st.container():
        # Campo Usuario
        st.markdown('<div class="posicion-usuario">', unsafe_allow_html=True)
        u = st.text_input("U", placeholder="Escribí tu usuario...", key="u_pizzolato")
        st.markdown('</div>', unsafe_allow_html=True)

        # Campo Contraseña
        st.markdown('<div class="posicion-password">', unsafe_allow_html=True)
        p = st.text_input("P", type="password", placeholder="Escribí tu clave...", key="p_pizzolato")
        st.markdown('</div>', unsafe_allow_html=True)

        # Botón invisible sobre el botón naranja
        st.markdown('<div class="posicion-boton">', unsafe_allow_html=True)
        if st.button("⠀", key="btn_pizzolato", use_container_width=True): # Usamos un caracter invisible para el botón
            if u == "admin" and p == "menfa2026":
                st.session_state.ingresado = True
                st.session_state.rol = "instructor"
                st.rerun()
            elif u == "alumno" and p == "alumno2026":
                st.session_state.ingresado = True
                st.session_state.rol = "alumno"
                st.rerun()
            else:
                st.error("Datos incorrectos")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
def verificar_emergencias_remotas():
    """Función que bloquea al alumno si hay una falla activa en Firebase"""
    try:
        estado = leer_estado_actual()
        if estado and estado.get("activo"):
            st.markdown("<style>.stApp {background-color: #3e0000 !important;}</style>", unsafe_allow_html=True)
            st.error(f"🚨 EMERGENCIA LANZADA POR EL INSTRUCTOR")
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

    # --- MOTOR DE ENRUTAMIENTO (RESTAURADO) ---
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
        from modulos.manual_simulador import mostrar_manual
        mostrar_manual()

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
