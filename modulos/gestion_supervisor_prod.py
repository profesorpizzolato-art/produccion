import streamlit as st
import pandas as pd

def gestion_supervisor_prod():
    st.header("📈 Gestión del Supervisor de Producción")
    st.subheader("Control de Procesos y Optimización de Planta")

    # Pestañas para organizar la nueva información técnica
    tab1, tab2, tab3 = st.tabs(["📊 Indicadores (KPI)", "📐 Cálculos de Niveles", "⛽ Separación y Gas"])

    with tab1:
        st.markdown("### Eficiencia Operativa (Ref. Clase 11)")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Frecuencia de Intervención", "1.8 años", "-0.2", help="Meta: 1 intervención cada 2 años")
            st.info("El costo de pulling representa el 30% del OPEX total.")
        with col2:
            st.metric("Producción Planta", "200 m³/día", "Estable")
            st.write("**Tratamiento de Crudo:** Deshidratación mediante métodos químicos y térmicos para romper emulsiones W/O.")

    with tab2:
        st.markdown("### Control de Niveles - Tanque de Lavado")
        st.write("Cálculos para la deshidratación de crudo Mesa 30 (Estación Amana).")
        
        with st.container(border=True):
            # Información técnica extraída de tus documentos de cálculos
            st.markdown("**Parámetros de Diseño Críticos:**")
            st.write("- **Tiempo de Residencia:** 2.5 horas (mínimo necesario para coalescencia).")
            st.write("- **Altura del Distribuidor:** 1.85 metros (6 ft).")
            st.write("- **Altura de Lavado e Interfaz:** 13.9 ft (mínimo recomendado).")
            
            # Simulador de nivel para el alumno
            nivel_actual = st.slider("Nivel de Interfaz Agua/Crudo (ft):", 0.0, 20.0, 14.0)
            if nivel_actual < 13.9:
                st.warning("⚠️ Nivel insuficiente para garantizar la calidad del crudo (sedimentación incompleta).")
            else:
                st.success("✅ Nivel de lavado óptimo para desestabilización de la emulsión.")

    with tab3:
        st.markdown("### Operación de Gas Natural")
        st.write("Gestión de contaminantes (H2S y CO2) según protocolos de planta.")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Mallas Moleculares:**")
            st.caption("Absorción física y deshidratación del gas mediante lechos fijos.")
        with col_b:
            st.markdown("**Membranas:**")
            st.caption("Separación por afinidad y difusividad. Ojo con la pérdida de hidrocarburos.")
        
        # 

        if st.button("Generar Reporte de Calidad de Gas"):
            st.download_button("Descargar PDF (Simulado)", "Contenido del reporte...", "reporte_gas.txt")

    st.divider()
    st.caption("MENFA - Basado en Clases de Tratamiento.")
