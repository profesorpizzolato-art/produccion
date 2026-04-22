import streamlit as st
import pandas as pd
from datetime import datetime

def reporte_novedades():
    st.header("📋 Reporte de Novedades Operativas")
    st.subheader("Registro de Eventos y Novedades del Turno")

    # Formulario de entrada
    with st.container(border=True):
        col1, col2 = st.columns(2)
        
        with col1:
            operador = st.text_input("Operador Responsable", value=st.session_state.rol.upper())
            fecha_novedad = st.date_input("Fecha del Evento", datetime.now())
            equipo = st.selectbox("Equipo/Instalación", [
                "Pozo Productor P-01", 
                "Separador Bifásico S-101", 
                "Bomba de Inyección B-200", 
                "Sistema SCADA",
                "Planta de Tratamiento"
            ])
            
        with col2:
            prioridad = st.select_slider("Prioridad del Evento", options=["Baja", "Media", "Alta", "CRÍTICA"])
            tipo_evento = st.selectbox("Tipo de Novedad", [
                "Operación Normal", 
                "Falla Mecánica", 
                "Mantenimiento Preventivo", 
                "Parada de Emergencia",
                "Derrame/Incidente Ambiental"
            ])

        descripcion = st.text_area("Descripción detallada de la novedad")
        
        if st.button("💾 GUARDAR REPORTE EN BITÁCORA", use_container_width=True):
            if descripcion:
                # Aquí simulamos el guardado (podrías usar session_state para persistencia temporal)
                st.success(f"Novedad registrada exitosamente para {equipo}. Folio: #MNF-{datetime.now().strftime('%M%S')}")
                st.balloons()
            else:
                st.error("Por favor, describa la novedad antes de guardar.")

    st.markdown("---")
    
    # Tabla de Histórico Simulado
    st.subheader("📚 Historial Reciente de Novedades")
    data_historica = {
        "Fecha": ["2026-04-20", "2026-04-19", "2026-04-18"],
        "Equipo": ["Pozo P-01", "Planta de Gas", "Bomba B-200"],
        "Novedad": ["Cambio de orificio en choke", "Limpieza de filtros", "Falla en sello mecánico"],
        "Estado": ["Resuelto", "En Proceso", "Pendiente"]
    }
    df_historico = pd.DataFrame(data_historica)
    st.table(df_historico)

    # El Bot Guía de este módulo
    with st.expander("🤖 Asistencia Técnica"):
        st.write("""
        **Normativa Relacionada:** Según la gestión de integridad, toda novedad técnica debe 
        ser reportada en un plazo máximo de 2 horas desde su detección para mantener el 
        estándar de certificación IPCL.
        """)
