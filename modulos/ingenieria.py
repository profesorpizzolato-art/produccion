import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def mostrar_ingenieria():  # <--- Este nombre tiene que coincidir exactamente
  st.header("📊 Modelado, Análisis Nodal, EOR y Yacimiento 3D")
  st.markdown(
      "Ecosistema integral de simulación y análisis de producción de MenFa"
      " Capacitaciones."
  )

  # Pestañas principales de navegación del módulo
  tabs = st.tabs(
      [
          "🔗 Análisis Nodal (IPR-VLP)",
          "📉 Declinación de Producción",
          "🛢️ Balance de Materia (OOIP)",
          "💧 Recuperación Mejorada (EOR)",
          "🧊 Modelo 3D y Frente de Agua",
      ]
  )

  # ... [Aquí debajo van todas las pestañas con sus respectivos "with tabs[x]:"] ...
