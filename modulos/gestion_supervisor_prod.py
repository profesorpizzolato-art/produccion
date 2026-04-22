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

import streamlit as st

def gestion_supervisor_prod():
    st.header("📈 Gestión del Supervisor de Producción")
    
    # Pestañas basadas en tus nuevos documentos
    tab1, tab2, tab3 = st.tabs(["📊 Control de Proceso", "📐 Ingeniería de Niveles", "⛽ Tratamiento de Gas"])

    with tab1:
        st.subheader("Optimización de Planta (Ref: Plantas de Tratamiento.pdf)")
        st.write("El tratamiento principal consiste en la **deshidratación del petróleo**.")
        col1, col2 = st.columns(2)
        col1.metric("Tiempo de Residencia", "2.5 Horas", "Requerido")
        col2.metric("Costo de Intervención", "30%", "Límite OPEX")
        st.info("Métodos utilizados: Químico (desemulsificantes) y Térmico (calor para reducir viscosidad).")

    with tab2:
        st.subheader("Cálculos de Operación (Ref: PDVSA Monagas)")
        st.markdown("Cálculos para **Tanque de Lavado** (Crudo Mesa 30):")
        
        # Datos extraídos de CALCULOS_PARA_NIVELES_DE_OPER.docx
        st.write("- **Altura del distribuidor de flujo:** 1.85 m (6 ft)")
        st.write("- **Altura mínima zona de lavado/interfaz:** 13.9 ft")
        st.write("- **Altura de toma de succión (Bomba P-01C):** 17 ft")
        
        nivel = st.number_input("Ingrese Nivel Actual del Tanque (ft):", value=14.0)
        if nivel < 13.9:
            st.error("⚠️ Alerta: Nivel por debajo del límite de sedimentación. Riesgo de arrastre de agua.")
        else:
            st.success("✅ Operación normal: Coalescencia y sedimentación garantizada.")

    with tab3:
        st.subheader("Separación de Gas Natural")
        st.write("Gestión de componentes ácidos (H2S y CO2).")
        
        st.markdown("""
        **Tecnologías de Separación:**
        * **Mallas Moleculares:** Lechos fijos para absorción física y deshidratación.
        * **Membranas:** Separación por afinidad y difusividad (Cuidado con pérdidas de hidrocarburos).
        """)
        #
