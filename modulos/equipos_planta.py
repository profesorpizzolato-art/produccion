import streamlit as st
import time

def mostrar_equipos_planta(q_pozo=100.0, bsw_pozo=1.0):
    st.header("📦 Equipos Críticos de Planta")
    st.write(f"Monitoreo en tiempo real basado en la producción actual: **{round(q_pozo, 2)} BPD**")
    
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
        presion = col_sep1.slider("Presión de Operación (psi):", 20, 200, 45)
        
        # Lógica técnica: A mayor caudal de pozo, más difícil es mantener el nivel
        nivel_sugerido = min(100.0, (q_pozo / 5000) * 100)
        nivel_crudo = col_sep2.slider("Nivel de Crudo (%):", 0.0, 100.0, nivel_sugerido)
        
        if presion > 150:
            st.error("🚨 Peligro: Presión excedida. Arrastre de líquido a la línea de gas.")
        elif q_pozo > 4500:
            st.warning("⚠️ Alerta: Caudal cercano al límite de diseño del separador.")
        else:
            st.success("Operación Estable.")

    # --- 2. ENSAYO DE POZOS ---
    with tab2:
        st.subheader("Sistema de Ensayo (Test Header)")
        pozo_test = st.selectbox("Pozo a ensayar:", ["MENFA-001 (Actual)", "MENFA-002", "MENFA-003"])
        if st.button(f"Iniciar Ciclo de Ensayo"):
            with st.status("Midiendo flujo multifásico..."):
                time.sleep(1.5)
                st.metric("Caudal Neto Medido", f"{round(q_pozo, 2)} BPD")
                st.metric("BSW Medido", f"{bsw_pozo} %")

    # --- 3. TANQUES ---
    with tab3:
        st.subheader("Gestión de Almacenamiento")
        col_tk1, col_tk2 = st.columns(2)
        # El nivel del tanque ahora se ve influenciado por el caudal del pozo
        nivel_tk = col_tk1.number_input("Nivel TK-200 (ft):", 0.0, 40.0, 32.5)
        interfase = col_tk2.number_input("Interfase Agua (ft):", 0.0, 10.0, 1.2)
        
        vol_neto = (nivel_tk - interfase) * 150
        st.metric("Volumen Neto Disponible", f"{vol_neto:.2f} bbls")
        st.caption(f"Tiempo de llenado estimado: {round(vol_neto/max(1, q_pozo), 2)} días")

    # --- 4. UNIDAD LACT ---
    with tab4:
        st.subheader("Transferencia de Custodia (LACT)")
        # El monitor de BSW toma el valor del pozo por defecto
        bsw_real = st.slider("BSW Monitor (%):", 0.0, 5.0, float(bsw_pozo), step=0.1)
        
        if bsw_real > 1.0:
            st.error(f"RECHAZADO: BSW {bsw_real}% > 1.0% (Fuera de norma comercial)")
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
        
        caudal_gas = (d_placa * 12.5) * ((h_diff * p_est)**0.5)
        
        with c3:
            st.metric("Caudal de Gas", f"{caudal_gas:.2f} m3/std")
            if h_diff > 90: st.warning("Cambiar a placa mayor")
            elif h_diff < 10: st.warning("Cambiar a placa menor")

    # --- OPERACIÓN DE EQUIPOS CRÍTICOS ---
    st.markdown("---")
    st.header("🎮 Operación de Equipos Críticos")
    
    op_equipo = st.radio("Seleccioná equipo para operar:", ["Separador/Calentador", "Unidad LACT (Despacho)"], horizontal=True)

    if op_equipo == "Separador/Calentador":
        st.subheader("🔥 Control de Temperatura y Calidad (BSW)")
        t_cal = st.slider("Ajustar Temperatura Calentador (°C)", 30, 90, 50)
        
        # Simulación: A más temperatura, mejor separación de agua (baja el BSW)
        # Usamos el BSW del pozo como base para la reducción
        bsw_salida = max(0.2, bsw_pozo - (t_cal * 0.05))
        
        st.metric("Calidad de Salida (BSW)", f"{round(bsw_salida, 2)} %")
        if bsw_salida > 1.0: 
            st.error("❌ Crudo fuera de norma (BSW > 1%)")
        else: 
            st.success("✅ Crudo listo para despacho.")

    elif op_equipo == "Unidad LACT (Despacho)":
        st.subheader("📏 Transferencia de Custodia (Venta)")
        # Traemos el volumen del pozo como sugerencia
        vol_bruto = st.number_input("Volumen Bruto a Despachar (m3)", value=float(q_pozo/6.28)) # conversion bbl a m3 aprox
        bsw_final = st.slider("BSW Medido Final (%)", 0.0, 2.0, float(bsw_pozo))
        
        neto = vol_bruto * (1 - (bsw_final/100))
        
        if st.button("Generar Ticket de Medición"):
            st.code(f"""
            IPCL MENFA - CERTIFICADO DE DESPACHO
            ------------------------------------
            Origen: Batería Central Mendoza
            Volumen Bruto: {round(vol_bruto, 2)} m3
            BSW Final: {bsw_final} %
            Petróleo Neto: {round(neto, 3)} m3
            Estado: APROBADO PARA VENTA
            Responsable: Fabricio Pizzolato
            """, language="text")
