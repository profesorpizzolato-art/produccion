import streamlit as st
import pandas as pd
import time
from datetime import datetime

def show():
    st.header("🖥️ Sistema de Monitoreo SCADA - PTC Menfa")
    st.write(f"⏱️ **Tiempo Real:** {datetime.now().strftime('%H:%M:%S')} | **Estado del Servidor:** ONLINE")

    # --- 1. LÓGICA DE SENSORES (Simulación de variabilidad) ---
    # Usamos session_state para que los valores "vivan" y fluctúen
    if 'presion_manifold' not in st.session_state:
        st.session_state.presion_manifold = 145.0
    
    # Simulación de fluctuación leve
    import random
    st.session_state.presion_manifold += random.uniform(-0.5, 0.5)

    # --- 2. VISTA DE PLANTA (KPIs Críticos) ---
    col1, col2, col3, col4 = st.columns(4)
    
    # Presión con alerta visual
    p = st.session_state.presion_manifold
    if p > 150:
        col1.metric("P-Manifold", f"{p:.1f} psi", "ALTA", delta_color="inverse")
    else:
        col1.metric("P-Manifold", f"{p:.1f} psi", "Normal")

    col2.metric("Nivel Separador V-01", "68%", "Estable")
    col3.metric("Temp. E-01", "62.4 °C", "Óptima")
    col4.metric("Voltaje Bombas", "380V", "Fase OK")

    # --- 3. PANEL DE ALARMAS ACTIVAS ---
    st.divider()
    st.subheader("🚨 Registro de Alarmas (HMI)")
    
    with st.container(border=True):
        if p > 150:
            st.error("⚠️ **CRITICAL:** High Pressure in Inlet Manifold - Check SDV-101")
        
        # Simulamos un historial de alarmas
        data_alarmas = {
            "Tag": ["LSH-101", "TSH-202", "PSH-105"],
            "Descripción": ["Nivel Alto Tanque 1", "Alta Temp Calentador", "Baja Presión Instrumentos"],
            "Prioridad": ["Media", "Alta", "Baja"],
            "Estado": ["ACK", "ACTIVA", "CLEAR"]
        }
        df_alarmas = pd.DataFrame(data_alarmas)
        
        def color_prioridad(val):
            color = 'red' if val == 'Alta' else 'orange' if val == 'Media' else 'green'
            return f'color: {color}'

        st.table(df_alarmas.style.applymap(color_prioridad, subset=['Prioridad']))

    # --- 4. TENDENCIAS (TRENDS) ---
    st.divider()
    st.subheader("📈 Tendencias de Proceso")
    
    # Generamos datos de tendencia para los últimos 60 segundos
    chart_data = pd.DataFrame(
        np.random.randn(20, 2) + [145, 60],
        columns=['Presión (psi)', 'Temp (°C)']
    )
    st.line_chart(chart_data)

    # --- 5. CONTROL REMOTO ---
    st.divider()
    with st.expander("🛠️ Comandos de Operación Remota"):
        c_a, c_b = st.columns(2)
        with c_a:
            if st.button("🔄 Resetear Alarmas", use_container_width=True):
                st.toast("Reiniciando panel de alarmas...")
        with c_b:
            if st.button("🔓 Abrir Bypass Entrada", use_container_width=True):
                st.warning("Operación de Bypass en curso - Proceder con precaución.")

    # Auto-refresh simple para simular SCADA (cada 5 seg)
    # st.empty() # Placeholder para refresco
