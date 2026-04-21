import streamlit as st

def dashboard_principal():
    st.title("Centro de Control MENFA")
    st.markdown("### Simulador de Producción Petrolera")
    st.markdown("---")

    # Fila 1: Operaciones de Pozo y Campo
    st.subheader("📍 Gestión de Campo")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🛢 Pozo Productor", use_container_width=True, key="btn_pozo"):
            st.session_state.modulo = "pozo"
    with col2:
        if st.button("🗺 Mapa del Campo", use_container_width=True, key="btn_mapa"):
            st.session_state.modulo = "mapa"
    with col3:
        if st.button("📊 Campo Petrolero", use_container_width=True, key="btn_campo"):
            st.session_state.modulo = "campo"

    # Fila 2: Planta e Ingeniería
    st.subheader("🏢 Planta e Ingeniería")
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("🏭 Planta de Proceso", use_container_width=True, key="btn_planta"):
            st.session_state.modulo = "planta"
    with col5:
        if st.button("📈 Ingeniería (IPR-VLP)", use_container_width=True, key="btn_ing"):
            st.session_state.modulo = "ipr"
    with col6:
        if st.button("🧮 Fórmulas Petroleras", use_container_width=True, key="btn_form"):
            st.session_state.modulo = "formulas"

    # Fila 3: Entrenamiento y Soporte
    st.subheader("🧠 Entrenamiento y Soporte")
    col7, col8, col9 = st.columns(3)
    with col7:
        if st.button("⚠ Entrenamiento", use_container_width=True, key="btn_entren"):
            st.session_state.modulo = "entrenamiento"
    with col8:
        if st.button("📘 Manual Simulador", use_container_width=True, key="btn_manual"):
            st.session_state.modulo = "manual"
    with col9:
        if st.button("⚙️ Simular Fallas", use_container_width=True, key="btn_fallas"):
            st.session_state.modulo = "fallas"

    # Fila 4: GESTIÓN DE SUPERVISOR (Basado en Clase 8)
    st.subheader("📋 Liderazgo y Supervisión")
    col10, col11, col12 = st.columns(3)
    
    with col10:
        if st.button("🔍 Acciones Supervisor", use_container_width=True, key="btn_super"):
            st.session_state.modulo = "supervisor"
    
    with col11:
        # Habilitado: Reporte de variaciones diarias y novedades de campo
        if st.button("📝 Reporte de Novedades", use_container_width=True, key="btn_novedades"):
            st.session_state.modulo = "reporte_novedades"
            
    with col12:
        # Habilitado: Seguimiento de performance y prevención de declinación
        if st.button("💵 Control de Pérdidas", use_container_width=True, key="btn_perdidas"):
            st.session_state.modulo = "control_perdidas"

    st.markdown("---")

    # Métricas en tiempo real
    st.subheader("Estado General del Campo")
    colA, colB, colC = st.columns(3)
    colA.metric("Producción Total", "1850 BPD")
    colB.metric("Presión Separador", "120 psi")
    colC.metric("Pozos Activos", "6")
