import streamlit as st

from modulos.panel_operador import panel_operador
from modulos.scada import scada
from modulos.campo_pozos import campo
from modulos.manifold import manifold
from modulos.separador import separador
from modulos.bomba_superficie import bomba
from modulos.linea_flujo import linea
from modulos.tanques import tanques
from modulos.compresor_gas import compresor
from modulos.tendencias import tendencias
from modulos.balance_produccion import balance
from modulos.alarmas import alarmas
from modulos.simulador_fallas import fallas

st.set_page_config(layout="wide")

st.title("SIMULADOR DE PRODUCCIÓN PETROLERA")
st.subheader("IPCL MENFA – Centro de Entrenamiento")

menu = st.sidebar.selectbox(
"Menú",
[
"Panel Operador",
"SCADA",
"Campo Pozos",
"Manifold",
"Separador",
"Bomba",
"Línea Flujo",
"Tanques",
"Compresor",
"Tendencias",
"Balance Producción",
"Alarmas",
"Fallas"
]
)

if menu == "Panel Operador":
    panel_operador()

elif menu == "SCADA":
    scada()

elif menu == "Campo Pozos":
    campo()

elif menu == "Manifold":
    manifold()

elif menu == "Separador":
    separador()

elif menu == "Bomba":
    bomba()

elif menu == "Línea Flujo":
    linea()

elif menu == "Tanques":
    tanques()

elif menu == "Compresor":
    compresor()

elif menu == "Tendencias":
    tendencias()

elif menu == "Balance Producción":
    balance()

elif menu == "Alarmas":
    alarmas()

elif menu == "Fallas":
    fallas()
from modulos.tendencias import tendencias
from modulos.corte_agua import corte_agua
from modulos.choke_control import choke
from modulos.presiones_pozo import presiones
from modulos.alarmas_scada import alarmas
from modulos.simulacion_produccion import simulacion
from modulos.dashboard import dashboard
from modulos.modelo_reservorio import reservorio
from modulos.flujo_multifasico import flujo
from modulos.manifold_avanzado import manifold
from modulos.eficiencia_separador import separador
from modulos.eventos_operativos import eventos
from modulos.scada_avanzado import scada
