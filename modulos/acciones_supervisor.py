import streamlit as st
import pandas as pd
import numpy as np

def acciones_supervisor():
    st.title("📋 Panel de Acciones del Supervisor")
    st.subheader("Control Estadístico y Seguimiento de Performance")
    
    st.info("""
    **Objetivo:** Prevenir pérdidas de producción antes de que sucedan y analizar causas mediante el seguimiento permanente de indicadores.
    """)

    # --- SECCIÓN 1: CONTROL ESTADÍSTICO ---
    st.markdown("### 📈 Control de Producción Diario/Semanal")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Simulación de gráfica de declinación y fallas mencionada en el doc
        dias = np.arange(1, 31)
        prod_esperada = 1850 - (dias * 2) # Declinación natural
        prod_real = prod_esperada.copy()
        prod_real[15:20] = prod_real[15:20] * 0.8 # Simulación de falla en bombeo
        
        df_prod = pd.DataFrame({
            "Día": dias,
            "Producción Esperada (BPD)": prod_esperada,
            "Producción Real (BPD)": prod_real
        }).set_index("Día")
        
        st.line_chart(df_prod)
        st.caption("Gráfico de control para visualizar declinación natural y pérdidas por fallas.")

    with col2:
        st.metric("Declinación Mensual", "2.4%", "-0.5%")
        st.metric("Pérdida por Fallas", "120 BBL", delta_color="inverse")
        if st.button("Generar Reporte de Novedades"):
            st.success("Reporte enviado al Equipo de Producción.")

    st.markdown("---")

    # --- SECCIÓN 2: PLANES DE ACCIÓN ---
    st.markdown("### 🛠️ Seguimiento y Planes de Acción")
    
    tab1, tab2, tab3 = st.tabs(["Fallas de Bombeo", "Mantenimiento/Pulling", "Pozos Nuevos"])
    
    with tab1:
        st.write("**Acciones Preventivas:**")
        st.checkbox("Revisión de parámetros de bombeo mecánico")
        st.checkbox("Análisis de cartas dinamométricas (Preventivo)")
        
    with tab2:
        st.write("**Logística de Equipos:**")
        st.selectbox("Estado de equipo de Pulling", ["En Locación", "En Traslado", "Stand-by", "Mantenimiento"])
        
    with tab3:
        st.write("**Nuevos Proyectos:**")
        st.number_input("Influencia de recuperación secundaria (BPD)", value=45)

    # --- SECCIÓN 3: ESPECIFICACIONES TÉCNICAS (Fibra de Vidrio) ---
    with st.expander("📝 Especificaciones de Cañerías (Normas API 15 LR/HR)"):
        st.write("""
        Según los estándares de diseño para supervisor:
        - **Termoplásticos:** Se deforman con menor temperatura.
        - **Termoestables (Epóxicas):** Soportan mayores temperaturas y esfuerzos mecánicos.
        - **Conexiones:** Rosca API de 8 hilos por pulgada (tubos de 9 metros).
        """)
