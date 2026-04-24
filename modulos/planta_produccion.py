import streamlit as st
import pandas as pd

def planta_produccion():
    st.header("🏭 Planta de Tratamiento de Crudo (PTC) - Control Central")
    st.write("Monitoreo de Tren de Separación, Calentamiento y Deshidratación.")

    # --- 1. ESTADO DE LA PLANTA (Session State para interactividad) ---
    if 'presion_sep' not in st.session_state:
        st.session_state.presion_sep = 120.0
    if 'temp_calentador' not in st.session_state:
        st.session_state.temp_calentador = 65.0

    # --- 2. LAYOUT PRINCIPAL ---
    col_proceso, col_control = st.columns([3, 1])

    with col_proceso:
        st.subheader("Esquema de Flujo (P&ID Simplificado)")
        
        # Representación visual del flujo
        st.info("📥 Manifold de Entrada ➔ 🛢️ Separador Trifásico ➔ 🔥 Calentador ➔ 💧 Tanque Cortador ➔ 🚛 Despacho")
        
        # Métricas de Proceso en tiempo real
        m1, m2, m3 = st.columns(3)
        m1.metric("Presión Separador", f"{st.session_state.presion_sep} psi", "Normal")
        m2.metric("Temperatura Crudo", f"{st.session_state.temp_calentador} °C", "Óptima")
        m3.metric("Caudal de Entrada", "1850 BPD", "+12 BPD")

        # Gráfico de Niveles en Tanques
        st.write("**Niveles de Tanques de Almacenamiento (TK-101 / TK-102)**")
        niveles = pd.DataFrame({
            'Tanque': ['TK-01 (Crudo)', 'TK-02 (Agua)', 'TK-03 (Aux)'],
            'Nivel (%)': [75, 20, 45]
        })
        st.bar_chart(niveles.set_index('Tanque'))

    with col_control:
        st.subheader("🎮 Operación")
        st.write("Ajuste de Setpoints:")
        
        # Sliders para variar la simulación
        nueva_p = st.slider("Consigna Presión (psi)", 50, 250, int(st.session_state.presion_sep))
        nueva_t = st.slider("Consigna Temp (°C)", 40, 90, int(st.session_state.temp_calentador))
        
        if st.button("Aplicar Cambios en Planta"):
            st.session_state.presion_sep = nueva_p
            st.session_state.temp_calentador = nueva_t
            st.success("Setpoints actualizados en el sistema SCADA.")
            st.rerun()

        st.divider()
        st.write("**Parada de Emergencia (ESD):**")
        if st.button("🚨 ACTIVAR ESD", use_container_width=True):
            st.error("PLANTA BLOQUEADA. Válvulas de entrada cerradas.")

    # --- 3. SECCIÓN TÉCNICA: EFICIENCIA DE SEPARACIÓN ---
    st.divider()
    with st.expander("📊 Análisis de Eficiencia de Separación"):
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**Calidad del Crudo (Salida)**")
            st.write("- BSW: 0.5%")
            st.write("- Salinidad: 20 PTB")
        with col_b:
            st.write("**Calidad del Agua (Drenaje)**")
            st.write("- Hidrocarburos en agua: 15 ppm")
            st.write("- Sólidos en suspensión: 10 mg/l")
