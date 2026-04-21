import streamlit as st
import pandas as pd
from datetime import datetime

def reporte_novedades():
    st.title("📝 Reporte Diario de Novedades")
    st.subheader("Seguimiento de Campo y Operaciones")

    st.info("Según la Clase 8: El Líder debe visualizar variaciones por fallas en bombeo, pulling o mantenimiento.")

    with st.form("form_novedades"):
        col1, col2 = st.columns(2)
        with col1:
            pozo = st.selectbox("Seleccione Pozo:", ["PZ-001", "PZ-002", "PZ-003", "PZ-004"])
            novedad = st.selectbox("Tipo de Novedad:", ["Falla de Bombeo", "Pulling", "Mantenimiento Eléctrico", "Pozo Nuevo", "Recuperación Secundaria"])
        
        with col2:
            fecha = st.date_input("Fecha del Evento", datetime.now())
            perdida_est = st.number_input("Pérdida Estimada (BPD):", min_value=0)

        descripcion = st.text_area("Descripción técnica de la novedad:")
        
        enviado = st.form_submit_button("Registrar Novedad en Base de Datos")
        
        if enviado:
            st.success(f"Novedad registrada para el pozo {pozo}. Se ha notificado al Equipo de Producción.")

    st.markdown("---")
    st.write("### Historial de Eventos Recientes")
    # Simulación de tabla de historial
    data = {
        "Fecha": ["2026-04-18", "2026-04-19"],
        "Pozo": ["PZ-002", "PZ-004"],
        "Evento": ["Paro por Corte Eléctrico", "Inicio de Pulling"],
        "Estado": ["Resuelto", "En Proceso"]
    }
    st.table(pd.DataFrame(data))
