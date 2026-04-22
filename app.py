import streamlit as st
import base64
import sys
import os

# AGREGAR CARPETA MODULOS AL CAMINO DE PYTHON
sys.path.append(os.path.join(os.path.dirname(__file__), "modulos"))

# --- IMPORTACIONES ---
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
from modulos.protocolos_intervencion import protocolos_intervencion

# INTENTO DE IMPORTACIÓN DE LOS NUEVOS MÓDULOS DIFERENCIADOS
try:
    from modulos.gestion_supervisor_prod import gestion_supervisor_prod
    from modulos.gestion_company_man import gestion_company_man
except ImportError:
    def gestion_supervisor_prod(): st.error("Archivo 'gestion_supervisor_prod.py' no encontrado.")
    def gestion_company_man(): st.error("Archivo 'gestion_company_man.py' no encontrado.")

# CONFIGURACION DE PAGINA
st.set_page_config(
    page_title="IPCL MENFA - Producción Petrolera 3.0",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTADO DE SESIÓN ---
if 'ingresado' not in st.session_state:
    st.session_state.ingresado = False
if 'rol' not in st.session_state:
    st.session_state.rol = None

# --- PANTALLA DE INICIO ---
if not st.session_state.ingresado:
    col1, col_center, col3 = st.columns([1, 2, 1])
    with col_center:
        st.markdown("<h1 style='text-align: center; color: #E67E22;'>IPCL MENFA</h1>", unsafe_allow_html=True)
        st.image("assets/logo_menfa.png", caption="Capacitación Técnica Profesional")
        with st.container(border=True):
            st.markdown("#### 🔐 Acceso al Sistema")
            usuario = st.text_input("Usuario")
            clave = st.text_input("Contraseña", type="password")
            if st.button("INGRESAR", use_container_width=True):
                if (usuario == "admin" and clave == "menfa2026") or (usuario == "alumno" and clave == "alumno2026"):
                    st.session_state.ingresado = True
                    st.session_state.rol = "instructor" if usuario == "admin" else "alumno"
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
    st.stop()

# --- SIDEBAR (DEFINICIÓN DEL MENÚ) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #E67E22;'>MENFA</h2>", unsafe_allow_html=True)
    if st.button("🚪 Cerrar Sesión"):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("---")
    categoria = st.radio("Área de Trabajo:", ["🏠 Inicio", "📍 Campo y Pozos", "🏢 Planta de Proceso", "🖥️ Sistema SCADA", "📊 Ingeniería", "📋 Gestión", "🧠 Evaluación"])
    
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
        menu = st.selectbox("Módulo:", [
            "Control de Producción (Supervisor)", 
            "Operaciones de Campo (Company Man)",
            "Reporte de Novedades", 
            "Control de Pérdidas", 
            "Protocolos de Intervención"
        ])
    elif categoria == "🧠 Evaluación":
        opciones_eval = ["Manual de Instrucciones", "Entrenamiento", "Examen Final"]
        if st.session_state.rol == "instructor": opciones_eval.insert(2, "Simulador de Fallas")
        menu = st.selectbox("Módulo:", opciones_eval)

# --- LÓGICA DE RENDERING (EL MOTOR DE LA APP) ---
def ejecutar_modulo(m):
    # --- ÁREA INICIO ---
    if m == "Dashboard": dashboard_principal()
    
    # --- ÁREA CAMPO ---
    elif m == "Mapa del Campo": mapa_campo()
    elif m == "Estado del Pozo": pozo_productor()
    elif m == "Control de Choke": choke_control()
    elif m == "Campo Petrolero": campo_petrolero()
    
    # --- ÁREA PLANTA (CORREGIDO) ---
    elif m == "Operación de Planta": planta_produccion()
    elif m == "Diagrama de Proceso (P&ID)": diagrama_planta()
    
    # --- ÁREA SCADA ---
    elif m == "Monitor Principal": scada_planta()
    elif m == "Gestión de Alarmas": alarmas_scada()
    elif m == "Tendencias Históricas": tendencias()
    
    # --- ÁREA INGENIERÍA (CORREGIDO) ---
    elif m == "Análisis IPR/VLP": ipr_vlp()
    elif m == "Cálculos de Producción": formulas_produccion()
    
    # --- ÁREA GESTIÓN ---
    elif m == "Control de Producción (Supervisor)": gestion_supervisor_prod()
    elif m == "Operaciones de Campo (Company Man)": gestion_company_man()
    elif m == "Reporte de Novedades": reporte_novedades()
    elif m == "Control de Pérdidas": control_perdidas()
    elif m == "Protocolos de Intervención": protocolos_intervencion()
    
    # --- ÁREA EVALUACIÓN ---
    elif m == "Manual de Instrucciones": instrucciones_simulador()
    elif m == "Entrenamiento": entrenamiento_operativo()
    elif m == "Simulador de Fallas": simulador_fallas()
    elif m == "Examen Final": evaluacion()

# --- VALIDACIÓN DE SEGURIDAD PARA MÓDULOS CRÍTICOS ---
modulos_criticos = ["Estado del Pozo", "Control de Choke", "Protocolos de Intervención", "Operaciones de Campo (Company Man)"]

if menu in modulos_criticos:
    st.subheader(f"🛡️ Validación de Seguridad: {menu}")
    with st.container(border=True):
        st.caption("Referencia: Programas de Pozo (Clase 12)")
        c1, c2 = st.columns(2)
        with c1:
            s1 = st.checkbox("Boca de pozo descomprimida a pileta")
            s2 = st.checkbox("Charla de seguridad realizada")
        with c2:
            s3 = st.checkbox("Checklist de equipo verificado")
            s4 = st.checkbox("EPP y Kit de derrames ok")
        
        if s1 and s2 and s3 and s4:
            st.success("Acceso habilitado.")
            ejecutar_modulo(menu)
        else:
            st.error("🔒 Comandos bloqueados por seguridad.")
else:
    ejecutar_modulo(menu)

st.sidebar.markdown("---")
st.sidebar.caption("MENFA 3.0 | Mendoza, Argentina")
