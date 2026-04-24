import streamlit as st
def mostrar_alerta_seguridad():
    alertas = [
        "🛡️ RES. 148: Verifique que los recintos de tanques estén limpios y con válvulas de drenaje cerradas.",
        "⚠️ CLIMA: Alerta por viento Zonda. Asegure elementos sueltos en locación y suspenda trabajos en altura.",
        "💧 QUÍMICA: Verifique stock de inhibidor de parafina. Las bajas temperaturas aumentan el riesgo de bloqueo.",
        "🔒 LOTO: Recuerde que el candado de seguridad es personal e intransferible."
    ]
    st.sidebar.info(random.choice(alertas))
def dashboard_principal():
    # --- FUNCIÓN AUXILIAR DE NAVEGACIÓN ---
    # Esto asegura que el sidebar y el contenido cambien al mismo tiempo
    def navegar_a(nombre_area):
        st.session_state.area_actual = nombre_area
        st.rerun()

    st.title("Centro de Control MENFA")
    st.markdown("### Simulador de Producción Petrolera 3.0")
    st.markdown("---")

    # --- FILA 1: GESTIÓN DE CAMPO ---
    st.subheader("📍 Gestión de Campo")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🛢️ Pozo Productor", use_container_width=True, key="btn_pozo"):
            navegar_a("🛢️ Pozo Productor")
    with col2:
        if st.button("🗺️ Mapa del Campo", use_container_width=True, key="btn_mapa"):
            navegar_a("🗺️ Mapa del Campo")
    with col3:
        if st.button("📊 Campo Petrolero", use_container_width=True, key="btn_campo"):
            navegar_a("📊 Campo Petrolero")

    # --- FILA 2: PLANTA E INGENIERÍA ---
    st.subheader("🏢 Planta e Ingeniería")
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("🏭 Planta de Proceso", use_container_width=True, key="btn_planta"):
            navegar_a("🏭 Planta de Proceso")
    with col5:
        if st.button("📈 Ingeniería (IPR-VLP)", use_container_width=True, key="btn_ing"):
            navegar_a("📈 Ingeniería")
    with col6:
        if st.button("🧮 Fórmulas Petroleras", use_container_width=True, key="btn_form"):
            navegar_a("🧠 Evaluación")

    # --- FILA 3: ENTRENAMIENTO Y EVALUACIÓN ---
    st.subheader("🧠 Entrenamiento y Evaluación")
    col7, col8, col9 = st.columns(3)
    with col7:
        if st.button("⚠ Entrenamiento Operativo", use_container_width=True, key="btn_entren"):
            navegar_a("🧠 Evaluación")
    with col8:
        if st.button("📘 Manual del Simulador", use_container_width=True, key="btn_manual"):
            st.info("Accediendo al repositorio de documentos técnicos...")
    with col9:
        # Lógica de Seguridad: Botón dinámico según el Rol
        if st.session_state.rol == "instructor":
            if st.button("⚙️ PANEL INSTRUCTOR: Fallas", use_container_width=True, key="btn_fallas"):
                navegar_a("📋 Gestión y Reportes")
        else:
            st.button("✅ Sistema Operativo: OK", use_container_width=True, key="btn_ok_status", disabled=True)

    # --- FILA 4: LIDERAZGO Y SUPERVISIÓN ---
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

    # --- MONITOREO DE MENDOZA ---
    st.subheader("Estado General del Campo (Cuenca Cuyana)")
    mA, mB, mC = st.columns(3)
    mA.metric("Producción Total", "1850 BPD", "+12 BPD")
    mB.metric("Presión de Separador", "120 psi", "-2 psi")
    mC.metric("Pozos en Operación", "6", "Activos")
