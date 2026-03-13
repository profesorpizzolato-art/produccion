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
