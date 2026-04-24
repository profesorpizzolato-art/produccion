import streamlit as st

def dashboard_principal():
    st.title("Centro de Control MENFA")
    st.markdown("### Simulador de Producción Petrolera 3.0")
    st.markdown("---")

    # --- FUNCIÓN AUXILIAR PARA NAVEGAR ---
    def navegar_a(nombre_area):
        st.session_state.area_actual = nombre_area
        st.rerun()

    # Fila 1: Operaciones de Pozo y Campo
    st.subheader("📍 Gestión de Campo")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🛢 Pozo Productor", use_container_width=True, key="btn_pozo"):
            navegar_a("🛢️ Operaciones de Campo")
    with col2:
        if st.button("🗺 Mapa del Campo", use_container_width=True, key="btn_mapa"):
            # Si no tenés esta área en el radio, podés mandarlo a una genérica
            navegar_a("🛢️ Operaciones de Campo") 
    with col3:
        if st.button("📊 Campo Petrolero", use_container_width=True, key="btn_campo"):
            navegar_a("🛢️ Operaciones de Campo")

    # Fila 2: Planta e Ingeniería
    st.subheader("🏢 Planta e Ingeniería")
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("🏭 Planta de Proceso", use_container_width=True, key="btn_planta"):
            navegar_a("🏭 Planta de Tratamiento")
    # En la Fila 2 de tu dashboard_principal.py
    with col5:
        if st.button("📈 Ingeniería (IPR-VLP)", use_container_width=True, key="btn_ing"):
           st.session_state.area_actual = "📈 Ingeniería" # <--- Corregido
           st.rerun()
    with col6:
        if st.button("🧮 Fórmulas Petroleras", use_container_width=True, key="btn_form"):
            navegar_a("🧠 Evaluación")

    # Fila 3: Entrenamiento y Soporte
    st.subheader("🧠 Entrenamiento y Evaluación")
    col7, col8, col9 = st.columns(3)
    with col7:
        if st.button("⚠ Entrenamiento Operativo", use_container_width=True, key="btn_entren"):
            navegar_a("🧠 Evaluación")
    with col8:
        if st.button("📘 Manual del Simulador", use_container_width=True, key="btn_manual"):
            st.info("Abriendo Manual de Usuario...")
    with col9:
        if st.session_state.rol == "instructor":
            if st.button("⚙️ PANEL INSTRUCTOR: Fallas", use_container_width=True, key="btn_fallas"):
                navegar_a("📋 Gestión y Reportes")
        else:
            st.button("⚙️ Sistema Operativo: OK", use_container_width=True, key="btn_fallas_dis", disabled=True)

    # Fila 4: Liderazgo y Supervisión
    st.subheader("📋 Liderazgo y Supervisión")
    col10, col11, col12 = st.columns(3)
    with col10:
        if st.button("🔍 Acciones Supervisor", use_container_width=True, key="btn_super"):
            navegar_a("📋 Gestión y Reportes")
    with col11:
        if st.button("📝 Reporte de Novedades", use_container_width=True, key="btn_novedades"):
            navegar_a("📋 Gestión y Reportes")
    with col12:
        if st.button("💵 Control de Pérdidas", use_container_width=True, key="btn_perdidas"):
            navegar_a("📋 Gestión y Reportes")

    st.markdown("---")

    # Métricas en tiempo real
    st.subheader("Estado General del Campo (Mendoza)")
    colA, colB, colC = st.columns(3)
    colA.metric("Producción Total", "1850 BPD", "+12 BPD")
    colB.metric("Presión de Separador", "120 psi", "-2 psi")
    colC.metric("Pozos en Operación", "6", "Activos")
