import streamlit as st
import sys
import os

# 1. CONFIGURACIÓN (Debe ser lo primero absoluto)
st.set_page_config(page_title="IPCL MENFA - Simulador 3.0", layout="wide")

# 2. MANEJO DE RUTAS
sys.path.append(os.path.join(os.path.dirname(__file__), "modulos"))
sys.path.append(os.path.join(os.path.dirname(__file__), "motor"))

# 3. ESTADO DE SESIÓN (Inicialización segura)
if 'ingresado' not in st.session_state: 
    st.session_state.ingresado = False
if 'rol' not in st.session_state: 
    st.session_state.rol = "alumno"
if 'area_actual' not in st.session_state: 
    st.session_state.area_actual = "🏠 Dashboard"

# 4. IMPORTACIONES
from modulos.dashboard_principal import dashboard_principal
from modulos.pozo_productor import pozo_productor
from modulos.planta_produccion import planta_produccion
from modulos.gestion_supervisor_prod import gestion_supervisor_prod
from modulos.evaluacion import evaluacion
from modulos.ingenieria import mostrar_ingenieria # Agregá esta importación

# --- SISTEMA DE ACCESO ---
def login():
    st.title("🔒 Acceso IPCL MENFA")
    u = st.text_input("Usuario")
    p = st.text_input("Contraseña", type="password")
    if st.button("INGRESAR"):
        if (u == "admin" and p == "menfa2026") or (u == "alumno" and p == "alumno2026"):
            st.session_state.ingresado = True
            st.session_state.rol = "instructor" if u == "admin" else "alumno"
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

# --- APLICACIÓN PRINCIPAL ---
def main_app():
    opciones = [
        "🏠 Dashboard", 
        "🛢️ Operaciones de Campo",
        "🗺️ Mapa del Campo", 
        "📊 Campo Petrolero",
        "🏭 Planta de Proceso",
        "📈 Ingeniería",
        "🖥️ Monitoreo SCADA",
        "📋 Gestión y Reportes",
        "🧠 Evaluación",
        "🎯 Entrenamiento Operativo",
        "📘 Manual"
    ]

    # --- MENÚ LATERAL ---
    with st.sidebar:
        # Asegúrate de que assets/logo_menfa.png exista
        try:
            st.image("assets/logo_menfa.png") 
        except:
            st.warning("Logo no encontrado en assets/")
            
        st.title("🛠️ Panel de Control")
        st.write(f"👤 **Rol:** {st.session_state.rol.upper()}")
        st.write("Instructor: Fabricio Pizzolato")
        st.divider()
        
        # Sincronización: El radio lee de area_actual
        try:
            indice_actual = opciones.index(st.session_state.area_actual)
        except ValueError:
            indice_actual = 0

        area = st.radio("Navegación:", opciones, index=indice_actual)
        
        # Si el usuario cambia el radio, actualizamos el estado global
        if area != st.session_state.area_actual:
            st.session_state.area_actual = area
            st.rerun()
        
        if st.button("🚪 Salir"):
            st.session_state.clear()
            st.rerun()

    # --- MOTOR DE EJECUCIÓN ---
    # Usamos st.session_state.area_actual como la única fuente de verdad
    actual = st.session_state.area_actual

    if actual == "🏠 Dashboard":
        dashboard_principal()

    elif actual == "🛢️ Operaciones de Campo":
        tab1, tab2, tab3 = st.tabs(["📍 Pozo Productor", "⚙️ Choke Control", "🏗️ Bomba Mecánica"])
        with tab1: pozo_productor()
        with tab2: st.info("Simulador de presión en cabeza de pozo (Choke Manifold).")
        with tab3: 
            try:
                import modulos.bomba_mecanica as bm
                bm.show()
            except ImportError:
                st.error("No se pudo cargar el módulo de Bomba Mecánica.")

   
    elif actual == "🗺️ Mapa del Campo":
         from mapa_campo import mostrar_mapa
         mostrar_mapa()
    elif actual == "📊 Campo Petrolero":
         from campo_petrolero import mostrar_estadisticas
         mostrar_estadisticas()
    elif actual == "🏭 Planta de Proceso": # <-- Verificá que la 'P' sea mayúscula
        from modulos.planta_produccion import planta_produccion
        planta_produccion()
    elif actual == "📈 Ingeniería":
        mostrar_ingenieria()
    elif actual == "🖥️ Monitoreo SCADA":
        try:
            import modulos.scada as scada
            scada.show()
        except ImportError:
            st.error("No se pudo cargar el sistema SCADA.")

    elif actual == "📋 Gestión y Reportes":
        from modulos.gestion_supervision_prod import gestion_supevision_prod
        gestion_supervisor_prod()
    elif actual == "🎯 Entrenamiento Operativo":
        from modulos.entrenamiento import mostrar_entrenamiento
        mostrar_entrenamiento()
    elif actual == "🧠 Evaluación":
        evaluacion()
    elif actual == "📘 Manual":
        from modulos.manual_simulador import mostrar_manual
        mostrar_manual()
# --- FLUJO PRINCIPAL ---
if not st.session_state.ingresado:
    login()
else:
    main_app()
