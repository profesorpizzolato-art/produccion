import streamlit as st
import streamlit as st

from modulos.dashboard_principal import dashboard_principal
from modulos.pozo_productor import pozo_productor
from modulos.planta_produccion import planta_produccion
from modulos.diagrama_planta import diagrama_planta
from modulos.formulas_produccion import formulas_produccion
from modulos.ipr_vlp import ipr_vlp
from modulos.evaluacion import evaluacion
if "modulo" not in st.session_state:
    st.session_state.modulo = "dashboard"
if st.session_state.modulo == "dashboard":
    dashboard_principal()

elif st.session_state.modulo == "pozo":
    pozo_productor()

elif st.session_state.modulo == "planta":
    planta_produccion()

elif st.session_state.modulo == "diagrama":
    diagrama_planta()

elif st.session_state.modulo == "formulas":
    formulas_produccion()

elif st.session_state.modulo == "ipr":
    ipr_vlp()

elif st.session_state.modulo == "evaluacion":
    evaluacion()
if st.button("⬅ Volver al menú"):
    st.session_state.modulo = "dashboard"
# IMPORTAR MODULOS

from modulos.dashboard import dashboard
from modulos.panel_operador import panel_operador
from modulos.campo_petrolero import campo
from modulos.scada_planta import scada_planta
from modulos.scada_avanzado import scada
from modulos.pozo_productor import pozo_productor
from modulos.modelo_reservorio import reservorio
from modulos.flujo_multifasico import flujo
from modulos.manifold_avanzado import manifold
from modulos.eficiencia_separador import separador
from modulos.tendencias import tendencias
from modulos.corte_agua import corte_agua
from modulos.choke_control import choke
from modulos.presiones_pozo import presiones
from modulos.simulacion_produccion import simulacion
from modulos.alarmas_scada import alarmas
from modulos.eventos_operativos import eventos
from modulos.mapa_campo import mapa_campo
from modulos.bomba_mecanica import bomba_mecanica
from modulos.dinamometro import dinamometro
from modulos.evaluacion import evaluacion
from modulos.formulas_produccion import formulas_produccion
from modulos.certificado import certificado
from modulos.ipr_vlp import ipr_vlp
from modulos.planta_produccion import planta_produccion
from modulos.diagrama_planta import diagrama_planta
# CONFIGURACION

st.set_page_config(
    page_title="Simulador Producción MENFA",
    layout="wide"
)

# TITULO

st.title("SIMULADOR DE PRODUCCIÓN PETROLERA")
st.subheader("IPCL MENFA - Centro de Entrenamiento Operativo")

# MENU

menu = st.sidebar.selectbox(
    "Menú del simulador",
    [
        "Dashboard",
        "Panel Operador",
        "Campo Petrolero",
        "SCADA Planta",
        "SCADA Avanzado",
        "Diagrama Planta"
        "Pozo Productor",
        "Modelo Reservorio",
        "Flujo Multifásico",
        "Manifold",
        "Separador",
        "Tendencias",
        "Corte Agua",
        "Control Choke",
        "Presiones Pozo",
        "Simulación Producción",
        "Alarmas",
        "Fórmulas Producción",
        "IPR - VLP",
        "Eventos Operativos"
    ]
)

# EJECUCION MODULOS

if menu == "Dashboard":
    dashboard()

elif menu == "Panel Operador":
    panel_operador()

elif menu == "Campo Petrolero":
    campo()

elif menu == "SCADA Planta":
    scada_planta()

elif menu == "SCADA Avanzado":
    scada()

elif menu == "Pozo Productor":
    pozo_productor()

elif menu == "Modelo Reservorio":
    reservorio()

elif menu == "Flujo Multifásico":
    flujo()

elif menu == "Manifold":
    manifold()

elif menu == "Separador":
    separador()

elif menu == "Tendencias":
    tendencias()

elif menu == "Corte Agua":
    corte_agua()

elif menu == "Control Choke":
    choke()

elif menu == "Presiones Pozo":
    presiones()

elif menu == "Simulación Producción":
    simulacion()

elif menu == "Alarmas":
    alarmas()

elif menu == "Eventos Operativos":
    eventos()
elif menu == "Fórmulas Producción":
    formulas_produccion()
elif menu == "IPR - VLP":
    ipr_vlp()
elif menu == "SCADA Planta":
    planta_produccion() 
elif menu == "Diagrama Planta":
    diagrama_planta()
