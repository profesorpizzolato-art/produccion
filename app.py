import streamlit as st
import sys
import os

# CONFIGURACIÓN (Debe ser lo primero)
st.set_page_config(page_title="IPCL MENFA - Simulador 3.0", layout="wide")

# AGREGAR CARPETA MODULOS
sys.path.append(os.path.join(os.path.dirname(__file__), "modulos"))
sys.path.append(os.path.join(os.path.dirname(__file__), "motor"))

# IMPORTACIONES AL RAS DEL MARGEN (Sin espacios al inicio)
from modulos.dashboard_principal import dashboard_principal
from modulos.pozo_productor import pozo_productor
from modulos.planta_produccion import planta_produccion
from modulos.gestion_supervisor_prod import gestion_supervisor_prod
from modulos.evaluacion import evaluacion
from modulos.banco_preguntas import CUESTIONARIO_PRODUCCION

# --- EL RESTO DEL CÓDIGO ---
# 4. ESTADO DE SESIÓN
if 'ingresado' not in st.session_state: st.session_state.ingresado = False
if 'rol' not in st.session_state: st.session_state.rol = "alumno"

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

def main_app():
    # --- MENÚ LATERAL ---
    with st.sidebar:
        # Asegúrate de tener la carpeta 'assets' con el logo
        st.image("assets/logo_menfa.png") 
        st.title("🛠️ Panel de Control")
        st.write(f"👤 **Rol:** {st.session_state.rol.upper()}")
        st.write("Instructor: Fabricio Pizzolato")
        st.divider()
        
        area = st.radio("Navegación:", [
            "🏠 Dashboard", 
            "🛢️ Operaciones de Campo", 
            "🏭 Planta de Tratamiento", 
            "🖥️ Monitoreo SCADA",
            "📋 Gestión y Reportes",
            "🧠 Evaluación"
        ])
        
        if st.button("🚪 Salir"):
            st.session_state.clear()
            st.rerun()

    # --- MOTOR DE EJECUCIÓN ---
    # Pasamos st.session_state.area_actual como el driver principal
    actual = st.session_state.area_actual 
    if area == "🏠 Dashboard":
        dashboard_principal()

    elif area == "🛢️ Operaciones de Campo":
        tab1, tab2, tab3 = st.tabs(["📍 Pozo Productor", "⚙️ Choke Control", "🏗️ Bomba Mecánica"])
        with tab1: pozo_productor()
        with tab2: st.info("Simulador de presión en cabeza de pozo (Choke Manifold).")
        with tab3: 
            import modulos.bomba_mecanica as bm
            bm.show()

    elif area == "🏭 Planta de Tratamiento":
        planta_produccion()

    elif area == "🖥️ Monitoreo SCADA":
        import modulos.scada as scada
        scada.show()

    elif area == "📋 Gestión y Reportes":
        gestion_supervisor_prod()

    elif area == "🧠 Evaluación":
        evaluacion() # Llama a la función del módulo

# --- FLUJO PRINCIPAL ---
if not st.session_state.ingresado:
    login()
else:
    main_app()
