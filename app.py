import streamlit as st
import sys
import os
import json

# 1. CONFIGURACIÓN INICIAL (DEBE SER LO PRIMERO)
st.set_page_config(page_title="IPCL MENFA - Simulador 3.0", layout="wide")

# 2. MANEJO DE RUTAS Y LIBRERÍAS
sys.path.append(os.path.join(os.path.dirname(__file__), "modulos"))

try:
    from google.cloud import firestore
    from google.oauth2 import service_account
    from modulos.nube import leer_estado_actual, enviar_falla, resetear_planta, conectar_db
except Exception as e:
    st.error(f"Error cargando módulos de nube: {e}")

# 3. INICIALIZACIÓN DEL ESTADO DE SESIÓN
if 'ingresado' not in st.session_state: 
    st.session_state.ingresado = False
if 'rol' not in st.session_state: 
    st.session_state.rol = "alumno"
if 'area_actual' not in st.session_state: 
    st.session_state.area_actual = "🏠 Dashboard"

# --- FUNCIONES DE SOPORTE ---

def login():
    st.title("🔒 Acceso IPCL MENFA")
    col_log, _ = st.columns([1, 2])
    with col_log:
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.button("INGRESAR"):
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

def verificar_emergencias_remotas():
    """Bloquea la pantalla del alumno si el instructor lanza una falla"""
    try:
        estado = leer_estado_actual()
        if estado and estado.get("activo"):
            st.markdown("<style>#root {background-color: #4b0000 !important;}</style>", unsafe_allow_html=True)
            st.error("🚨 EMERGENCIA ACTIVA - CONTROL DE PROCESOS")
            st.subheader(estado['falla'])
            st.info(estado['descripcion'])
            
            resp = st.text_area("Describa su maniobra inmediata:")
            if st.button("Enviar Reporte"):
                # Aquí podrías agregar una función para guardar la respuesta en la DB
                st.success("Reporte enviado. Espere instrucciones del Instructor.")
            st.stop() # Detiene la ejecución del resto de la app
    except:
        pass

def modulo_instructor_pizzolato():
    st.title("👨‍🏫 Panel de Control Maestro")
    st.write("Bienvenido, Ing. Pizzolato. Desde aquí controla el entorno de los alumnos.")
    
    col1, col2 = st.columns(2)
    with col1:
        falla = st.selectbox("Inyectar Incidente:", [
            "Fuga de H2S en Manifold", "Cavitación en Bomba P-101", 
            "BSW Fuera de Especificación", "Parada de Emergencia (ESD)"
        ])
        detalles = st.text_area("Detalles del síntoma:", "Alarma sonora y caída de presión.")
        if st.button("🔴 LANZAR EMERGENCIA"):
            enviar_falla(falla, detalles)
            st.warning("Falla enviada a todos los alumnos.")
            
    with col2:
        if st.button("🟢 NORMALIZAR PLANTA"):
            resetear_planta()
            st.success("Planta en condiciones normales.")

# --- NÚCLEO DEL SIMULADOR ---

def main_app():
    # El alumno siempre chequea la nube
    if st.session_state.rol == "alumno":
        verificar_emergencias_remotas()

    lista_menu = [
        "🏠 Dashboard", "🛢️ Operaciones de Campo", "🏭 Planta de Proceso",
        "🖥️ Monitoreo SCADA", "📋 Gestión y Reportes", "📈 Ingeniería",
        "🧠 Evaluación", "📘 Manual"
    ]

    with st.sidebar:
        try:
            st.image("assets/logo_menfa.png")
        except:
            st.write("### IPCL MENFA")
            
        st.write(f"👤 **Usuario:** {st.session_state.rol.upper()}")
        
        # Sincronización del Radio
        try:
            idx = lista_menu.index(st.session_state.area_actual)
        except:
            idx = 0
            
        seleccion = st.radio("Navegación:", lista_menu, index=idx)
        
        if seleccion != st.session_state.area_actual:
            st.session_state.area_actual = seleccion
            st.rerun()

        if st.button("🚪 Salir"):
            st.session_state.clear()
            st.rerun()

    # --- ENRUTADOR DE MÓDULOS ---
    actual = st.session_state.area_actual

    if actual == "🏠 Dashboard":
        from modulos.dashboard_principal import dashboard_principal
        dashboard_principal()
    elif actual == "🛢️ Operaciones de Campo":
        from modulos.pozo_productor import pozo_productor
        pozo_productor()
    elif actual == "🏭 Planta de Proceso":
        from modulos.planta_produccion import planta_produccion
        planta_produccion()
    elif actual == "🖥️ Monitoreo SCADA":
        from modulos.scada import show
        show()
    elif actual == "📘 Manual":
        from modulos.manual_simulador import mostrar_manual
        mostrar_manual()
    else:
        st.info(f"El módulo {actual} está en mantenimiento o desarrollo.")

# --- FUNCIÓN DE CONTROL DE FLUJO ---

def main():
    if not st.session_state.ingresado:
        login()
    else:
        if st.session_state.rol == "instructor":
            # El instructor elige qué ver en el sidebar
            modo = st.sidebar.selectbox("Vista:", ["🖥️ Simulador", "🎮 Control Maestro"])
            if modo == "🎮 Control Maestro":
                modulo_instructor_pizzolato()
            else:
                main_app()
        else:
            main_app()

# --- EJECUCIÓN FINAL ---
if __name__ == "__main__":
    main()
