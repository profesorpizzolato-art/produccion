import streamlit as st

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
