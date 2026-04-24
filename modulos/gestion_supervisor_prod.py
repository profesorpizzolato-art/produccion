import streamlit as st
import pandas as pd
from datetime import datetime

def gestion_supervisor_prod():
    st.header("📋 Gestión del Supervisor de Producción")
    
    menu = st.tabs(["📌 Acciones del Supervisor", "📝 Reporte de Novedades", "📉 Control de Pérdidas"])

    with menu[0]:
        st.subheader("Checklist de Turno")
        st.checkbox("Verificación de presiones en Manifold de entrada.")
        st.checkbox("Control de niveles en tanques de despacho.")
        st.checkbox("Revisión de parámetros de inyección de química (Desemulsionante).")
        st.checkbox("Validación de permisos de trabajo en caliente.")
        
    with menu[1]:
        st.subheader("Libro de Novedades Digital")
        with st.form("novedad_form"):
            sector = st.selectbox("Sector:", ["Campo", "Planta", "Logística", "Mantenimiento"])
            prioridad = st.select_slider("Prioridad:", ["Baja", "Media", "Alta", "CRÍTICA"])
            detalle = st.text_area("Descripción de la novedad:")
            if st.form_submit_button("Cargar Novedad"):
                st.toast(f"Novedad registrada en {sector}")
                # Aquí se guardaría en una base de datos real

    with menu[2]:
        mostrar_control_perdidas()

def mostrar_control_perdidas():
    st.subheader("📉 Control de Pérdidas (Diferencial de Inventario)")
    st.write("Cálculo de pérdidas por evaporación, fugas o medición.")
    
    col1, col2 = st.columns(2)
    ingreso = col1.number_input("Producción Fiscalizada (BPD)", value=2000)
    egreso = col2.number_input("Volumen Despachado (BPD)", value=1985)
    
    perdida = ingreso - egreso
    porcentaje = (perdida / ingreso) * 100
    
    st.metric("Pérdida de Crudo", f"{perdida} bbls", f"-{porcentaje:.2f}%")
    
    if porcentaje > 0.5:
        st.error("🚨 ALERTA: La pérdida supera el margen admisible (0.5%). Revisar venteos o fugas.")
    else:
        st.success("✅ BALANCE OK: Dentro de los límites tolerables.")
