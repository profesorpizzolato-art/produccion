import streamlit as st
import pandas as pd
import numpy as np

def mostrar_estadisticas():
    st.header("📊 Estadísticas de Producción del Campo")
    
    # Métricas de cabecera
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Producción Total", "2,450 m³/d", "+5%")
    m2.metric("Corte de Agua (WC)", "42%", "-1.5%")
    m3.metric("Gas Producido", "1,200 MSCFD", "Estable")
    m4.metric("Pozos Activos", "12 / 15", "Normal")

    st.divider()

    # Gráfico de tendencia
    st.subheader("📈 Evolución Diaria (Últimos 30 días)")
    chart_data = pd.DataFrame(
        np.random.randn(30, 2) / [10, 20] + [120, 45],
        columns=['Presión Promedio (psi)', 'Caudal (m³/d)']
    )
    st.line_chart(chart_data)

    # Estado de Sistemas de Extracción
    st.subheader("⚙️ Distribución de Sistemas de Extracción")
    col_a, col_b = st.columns(2)
    with col_a:
        st.bar_chart({"AIB (Mecánico)": 8, "ESP (Sumergible)": 3, "PCP (Tornillo)": 2, "Surgencia": 2})
    with col_b:
        st.write("**Alertas Operativas:**")
        st.warning("⚠️ Pozo MENFA-002: Requiere cambio de cuplas por fatiga.")
        st.error("🚨 Baja presión en línea de transferencia hacia Batería 2.")
