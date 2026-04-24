import streamlit as st
import time

def mostrar_equipos_planta():
    st.header("📦 Equipos Críticos de Planta")
    st.write("Monitoreo y control de las unidades principales de la batería.")
    
    # Las 5 pestañas operativas
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌀 Separadores", 
        "📈 Ensayo de Pozos", 
        "🛢️ Tanques", 
        "🚢 Unidad LACT",
        "📊 Puente de Gas"
    ])

    # --- 1. SEPARADORES ---
    with tab1:
        st.subheader("Control de Separación Trifásica (V-01)")
        col_sep1, col_sep2 = st.columns(2)
        presion = col_sep1.slider("Presión de Operación (psi):", 20, 100, 45)
        nivel_crudo = col_sep2.slider("Nivel de Crudo (%):", 0, 100, 50)
        if presion > 80:
            st.error("🚨 Peligro: Presión excedida. Arrastre de líquido a la línea de gas.")
        else:
            st.success("Operación Estable.")

    # --- 2. ENSAYO DE POZOS ---
    with tab2:
        st.subheader("Sistema de Ensayo (Test Header)")
        pozo_test = st.selectbox("Pozo a ensayar:", ["MENFA-001", "MENFA-002", "MENFA-003"])
        if st.button(f"Iniciar Ciclo de Ensayo"):
            with st.status("Midiendo..."):
                time.sleep(1)
                st.metric("Caudal Neto", "42.5 m3/d")

    # --- 3. TANQUES ---
    with tab3:
        st.subheader("Gestión de Almacenamiento")
        col_tk1, col_tk2 = st.columns(2)
        nivel_tk = col_tk1.number_input("Nivel TK-200 (ft):", 0.0, 40.0, 32.5)
        interfase = col_tk2.number_input("Interfase Agua (ft):", 0.0, 10.0, 1.2)
        st.metric("Volumen Neto", f"{(nivel_tk - interfase) * 150:.2f} bbls")

    # --- 4. UNIDAD LACT ---
    with tab4:
        st.subheader("Transferencia de Custodia (LACT)")
        bsw_real = st.slider("BSW Monitor (%):", 0.0, 2.0, 0.4, step=0.1)
        if bsw_real > 1.0:
            st.error(f"RECHAZADO: BSW {bsw_real}% > 1%")
        else:
            st.success("APROBADO PARA VENTA")

    # --- 5. PUENTE DE GAS ---
    with tab5:
        st.subheader("Medición de Gas (Placa de Orificio)")
        c1, c2, c3 = st.columns(3)
        with c1:
            p_est = c1.number_input("Presión Estática (Psia):", value=45.0)
            h_diff = c1.slider("Diferencial (InH2O):", 0, 100, 50)
        with c2:
            d_placa = c2.selectbox("Diámetro Placa (pulg):", [0.5, 1.0, 1.5, 2.0])
            t_gas = c2.number_input("Temp. Gas (°F):", value=75.0)
        
        # Cálculo simplificado Q = C * sqrt(hw * Pf)
        caudal = (d_placa * 12.5) * ((h_diff * p_est)**0.5)
        
        with c3:
            st.metric("Caudal de Gas", f"{caudal:.2f} m3/std")
            if h_diff > 90: st.warning("Cambiar a placa mayor")
            if h_diff < 10: st.warning("Cambiar a placa menor")
