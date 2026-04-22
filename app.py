import streamlit as st
import base64
import sys
import os

# AGREGAR CARPETA MODULOS AL CAMINO DE PYTHON
sys.path.append(os.path.join(os.path.dirname(__file__), "modulos"))

# IMPORTACIONES
from modulos.dashboard_principal import dashboard_principal
from modulos.pozo_productor import pozo_productor
from modulos.mapa_campo import mapa_campo
from modulos.campo_petrolero import campo_petrolero
from modulos.formulas_produccion import formulas_produccion
from modulos.entrenamiento_operativo import entrenamiento_operativo
from modulos.instrucciones_simulador import instrucciones_simulador
from modulos.planta_produccion import planta_produccion
from modulos.scada_planta import scada_planta
from modulos.diagrama_planta import diagrama_planta
from modulos.ipr_vlp import ipr_vlp
from modulos.choke_control import choke_control
from modulos.simulador_fallas import simulador_fallas
from modulos.evaluacion import evaluacion
from modulos.alarmas_scada import alarmas_scada
from modulos.tendencias import tendencias
from modulos.acciones_supervisor import acciones_supervisor
from modulos.reporte_novedades import reporte_novedades
from modulos.control_perdidas import control_perdidas

# CONFIGURACION DE PAGINA
st.set_page_config(
    page_title="IPCL MENFA - Producción Petrolera 3.0",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTADO DE SESIÓN (LOGIN Y ROLES) ---
if 'ingresado' not in st.session_state:
    st.session_state.ingresado = False
if 'rol' not in st.session_state:
    st.session_state.rol = None
if 'modulo' not in st.session_state:
    st.session_state.modulo = "dashboard"

# --- PANTALLA DE INICIO / CARÁTULA ---
if not st.session_state.ingresado:
    col1, col_center, col3 = st.columns([1, 2, 1])
    
    with col_center:
        st.markdown("<h1 style='text-align: center; color: #E67E22;'>IPCL MENFA</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>SIMULADOR DE PRODUCCIÓN 3.0</h2>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1516195851888-6f1a981a862e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", caption="Centro de Entrenamiento - Mendoza")
        
        with st.container(border=True):
            st.markdown("#### 🔐 Acceso al Sistema")
            usuario = st.text_input("Usuario")
            clave = st.text_input("Contraseña", type="password")
            
            if st.button("INGRESAR AL SIMULADOR", use_container_width=True):
                if usuario == "admin" and clave == "menfa2026":
                    st.session_state.ingresado = True
                    st.session_state.rol = "instructor"
                    st.rerun()
                elif usuario == "alumno" and clave == "ypf2026":
                    st.session_state.ingresado = True
                    st.session_state.rol = "alumno"
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
    st.stop()

# --- SIDEBAR (Solo visible tras login) ---
with st.sidebar:
    st.markdown(f"### Bienvenido, {st.session_state.rol.upper()}")
    if st.button("🚪 Cerrar Sesión"):
        st.session_state.ingresado = False
        st.session_state.rol = None
        st.rerun()
    
    st.markdown("---")
    categoria = st.radio(
        "Área de Trabajo:",
        ["🏠 Inicio", "📍 Campo y Pozos", "🏢 Planta de Proceso", "🖥️ Sistema SCADA", "📊 Ingeniería", "📋 Gestión", "🧠 Evaluación"]
    )
    
    # Lógica de selección
    if categoria == "🏠 Inicio":
        menu = "Dashboard"
    elif categoria == "📍 Campo y Pozos":
        menu = st.selectbox("Módulo:", ["Mapa del Campo", "Estado del Pozo", "Control de Choke", "Campo Petrolero"])
    elif categoria == "🏢 Planta de Proceso":
        menu = st.selectbox("Módulo:", ["Operación de Planta", "Diagrama de Proceso (P&ID)"])
    elif categoria == "🖥️ Sistema SCADA":
        menu = st.selectbox("Módulo:", ["Monitor Principal", "Gestión de Alarmas", "Tendencias Históricas"])
    elif categoria == "📊 Ingeniería":
        menu = st.selectbox("Módulo:", ["Análisis IPR/VLP", "Cálculos de Producción"])
    elif categoria == "📋 Gestión":
        menu = st.selectbox("Módulo:", ["Acciones del Supervisor", "Reporte de Novedades", "Control de Pérdidas"])
    elif categoria == "🧠 Evaluación":
        opciones_eval = ["Manual de Instrucciones", "Entrenamiento", "Examen Final"]
        # El Simulador de Fallas solo aparece si es instructor
        if st.session_state.rol == "instructor":
            opciones_eval.insert(2, "Simulador de Fallas")
        menu = st.selectbox("Módulo:", opciones_eval)

# --- SINCRONIZACIÓN DASHBOARD ---
if st.session_state.modulo != "dashboard":
    mapeo = {
        "pozo": "Estado del Pozo", "mapa": "Mapa del Campo", "campo": "Campo Petrolero",
        "planta": "Operación de Planta", "formulas": "Cálculos de Producción",
        "entrenamiento": "Entrenamiento", "manual": "Manual de Instrucciones",
        "supervisor": "Acciones del Supervisor", "reporte_novedades": "Reporte de Novedades",
        "control_perdidas": "Control de Pérdidas", "fallas": "Simulador de Fallas"
    }
    if st.session_state.modulo in mapeo:
        menu = mapeo[st.session_state.modulo]
    st.session_state.modulo = "dashboard"

# --- RENDERIZADO ---
if menu == "Dashboard": dashboard_principal()
elif menu == "Mapa del Campo": mapa_campo()
elif menu == "Estado del Pozo": pozo_productor()
elif menu == "Control de Choke": choke_control()
elif menu == "Campo Petrolero": campo_petrolero()
elif menu == "Operación de Planta": planta_produccion()
elif menu == "Diagrama de Proceso (P&ID)": diagrama_planta()
elif menu == "Monitor Principal": scada_planta()
elif menu == "Gestión de Alarmas": alarmas_scada()
elif menu == "Tendencias Históricas": tendencias()
elif menu == "Análisis IPR/VLP": ipr_vlp()
elif menu == "Cálculos de Producción": formulas_produccion()
elif menu == "Acciones del Supervisor": acciones_supervisor()
elif menu == "Reporte de Novedades": reporte_novedades()
elif menu == "Control de Pérdidas": control_perdidas()
elif menu == "Manual de Instrucciones": instrucciones_simulador()
elif menu == "Entrenamiento": entrenamiento_operativo()
elif menu == "Simulador de Fallas": simulador_fallas()
elif menu == "Examen Final": evaluacion()

st.sidebar.markdown("---")
st.sidebar.caption("MENFA 3.0 | Mendoza, Argentina")
