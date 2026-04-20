import streamlit as st
import base64

# --- IMPORTACIONES ---
from modulos.dashboard_principal import dashboard_principal
from modulos.pozo_productor import pozo_productor
from modulos.mapa_campo import mapa_campo
from modulos.campo_petrolero import campo_petrolero
from modulos.formulas_produccion import formulas_produccion
from modulos.entrenamiento_operativo import entrenamiento_operativo
from modulos.instrucciones_simulador import instrucciones_simulador

# Intentar importar módulos avanzados
try:
    from modulos.planta_produccion import planta_produccion
    from modulos.scada_planta import scada_planta
    from modulos.ipr_vlp import ipr_vlp
except ImportError:
    st.warning("Aviso: Algunos módulos de planta no se encontraron.")
    
# CONFIGURACION DE PAGINA
st.set_page_config(
    page_title="IPCL MENFA - Producción Petrolera",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- NAVEGACIÓN POR SIDEBAR ---
with st.sidebar:
    # Espacio para el logo
    try:
        st.image("assets/logo_menfa.png", use_column_width=True)
    except:
        st.title("IPCL MENFA")
    
    st.markdown("### 🛠️ Panel de Simulación")
    
    # Agrupamos los módulos por categorías para que sea más ordenado
    categoria = st.radio(
        "Ir a sección:",
        ["🏠 Inicio", "📍 Campo y Pozos", "🏢 Planta y SCADA", "📊 Ingeniería y Fórmulas", "🧠 Entrenamiento y Test"]
    )

    st.markdown("---")
    
    # Sub-navegación según la categoría seleccionada
    if categoria == "🏠 Inicio":
        menu = "Dashboard"
    
    elif categoria == "📍 Campo y Pozos":
        menu = st.selectbox("Módulo:", ["Mapa del Campo", "Estado del Pozo", "Control de Choke", "Campo Petrolero"])
    
    elif categoria == "🏢 Planta y SCADA":
        menu = st.selectbox("Módulo:", ["Planta de Producción", "Sistema SCADA", "Diagrama de Planta"])
        
    elif categoria == "📊 Ingeniería y Fórmulas":
        menu = st.selectbox("Módulo:", ["Análisis IPR/VLP", "Fórmulas de Producción", "Flujo Multifásico"])
        
    elif categoria == "🧠 Entrenamiento y Test":
        menu = st.selectbox("Módulo:", ["Instrucciones", "Entrenamiento Operativo", "Simulador de Fallas", "Examen de Evaluación"])

    st.sidebar.info("Usuario: Operador de Planta")

# --- LÓGICA DE VISUALIZACIÓN ---

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

# Planta y SCADA
elif menu == "Planta de Producción":
    st.header("🏢 Planta de Tratamiento de Crudo")
    planta_produccion()
elif menu == "Sistema SCADA":
    st.header("🖥️ Monitor SCADA Avanzado")
    scada_planta()
elif menu == "Diagrama de Planta":
    # Aquí puedes llamar a diagrama_planta.py si es una visualización estática
    st.subheader("Esquema de Proceso")

# Ingeniería
elif menu == "Análisis IPR/VLP":
    ipr_vlp()
elif menu == "Fórmulas de Producción":
    formulas_produccion()

# Entrenamiento
elif menu == "Instrucciones":
    instrucciones_simulador()
elif menu == "Simulador de Fallas":
    simulador_fallas()
elif menu == "Examen de Evaluación":
    evaluacion()
    

# PIE DE PAGINA (Se mantiene siempre visible)
st.sidebar.markdown("---")
st.sidebar.caption("MENFA | Software de Simulación Industrial v2.0")
