import streamlit as st
import pandas as pd
import numpy as np

def control_perdidas():
    st.title("💵 Control de Performance y Pérdidas")
    
    st.markdown("""
    > *'La producción de petróleo es el objetivo básico y principal del supervisor de campo.'*
    """)

    # --- GRÁFICO ESTADÍSTICO ---
    st.subheader("📈 Control Estadístico de Producción")
    dias = np.arange(1, 11)
    prod_real = [1850, 1840, 1835, 1700, 1650, 1800, 1810, 1820, 1815, 1810]
    prod_prog = [1850] * 10

    df_stats = pd.DataFrame({
        "Día": dias,
        "Programado": prod_prog,
        "Real": prod_real
    }).set_index("Día")

    st.line_chart(df_stats)
    st.caption("Visualización de variaciones: Diferencia entre la meta programada y la realidad de campo.")

    # --- SECCIÓN TÉCNICA DE CAÑERÍAS (Info de Clase 8) ---
    st.markdown("---")
    st.subheader("📋 Especificaciones Técnicas de Materiales")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Materiales (Normas API 15 LR/HR):**")
        st.markdown("""
        - **Termoplásticos:** Se deforman con menor temperatura (Poliuretano/Polipropileno).
        - **Termoestables:** Resinas epóxicas con fibra de vidrio. Soportan más presión y temperatura.
        """)
    
    with col_b:
        st.write("**Estándares de Conexión:**")
        st.info("Rosca API de 8 hilos por pulgada. Tubos normalizados de 9 metros.")

    st.warning("⚠️ IMPORTANTE: Consultar compatibilidad química de la fibra con el hidrocarburo antes de la instalación.")
