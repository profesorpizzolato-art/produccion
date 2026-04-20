import streamlit as st
import base64

# --- IMPORTACIONES DINÁMICAS (ORDENADAS POR CATEGORÍA) ---
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

# CONFIGURACION DE PAGINA
st.set_page_config(
    page_title="IPCL MENFA - Producción Petrolera",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR COMPLETO ---
with st.sidebar:
    st.title("MENFA Simulator")
    
    categoria = st.radio(
        "Seleccione Área de Trabajo:",
        ["🏠 Inicio", "📍 Campo y Pozos", "🏢 Planta de Proceso", "🖥️ Sistema SCADA", "📊 Ingeniería", "🧠 Evaluación"]
    )
    
    st.markdown("---")
    
    # Lógica de selección de módulo
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
        
    elif categoria == "🧠 Evaluación":
        menu = st.selectbox("Módulo:", ["Manual de Instrucciones", "Entrenamiento", "Simulador de Fallas", "Examen Final"])

# --- RENDERIZADO DE MÓDULOS ---

if menu == "Dashboard":
    dashboard_principal()

# Pozos
elif menu == "Mapa del Campo":
    mapa_campo()
elif menu == "Estado del Pozo":
    pozo_productor()
elif menu == "Control de Choke":
    choke_control()
elif menu == "Campo Petrolero":
    campo_petrolero()

# Planta
elif menu == "Operación de Planta":
    planta_produccion()
elif menu == "Diagrama de Proceso (P&ID)":
    diagrama_planta()

# SCADA
elif menu == "Monitor Principal":
    scada_planta()
elif menu == "Gestión de Alarmas":
    alarmas_scada()
elif menu == "Tendencias Históricas":
    tendencias()

# Ingeniería
elif menu == "Análisis IPR/VLP":
    ipr_vlp()
elif menu == "Cálculos de Producción":
    formulas_produccion()

# Entrenamiento y Evaluación
elif menu == "Manual de Instrucciones":
    instrucciones_simulador()
elif menu == "Entrenamiento":
    entrenamiento_operativo()
elif menu == "Simulador de Fallas":
    simulador_fallas()
elif menu == "Examen Final":
    evaluacion()

# Pie de página en Sidebar
st.sidebar.markdown("---")
st.sidebar.caption("Software de Simulación | Mendoza, Argentina")
