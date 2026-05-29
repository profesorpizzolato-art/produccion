import streamlit as st
import pandas as pd
import plotly.express as px
import random

def mostrar_alerta_seguridad():
    alertas = [
        "🛡️ RES. 148: Verifique que los recintos de tanques estén limpios y con válvulas de drenaje cerradas.",
        "⚠️ CLIMA: Alerta por viento Zonda. Asegure elementos sueltos en locación y suspenda trabajos en altura.",
        "💧 QUÍMICA: Verifique stock de inhibidor de parafina. Las bajas temperaturas aumentan el riesgo de bloqueo.",
        "🔒 LOTO: Recuerde que el candado de seguridad es personal e intransferible."
    ]
    st.sidebar.info(random.choice(alertas))

def dashboard_principal():
    # --- INICIALIZACIÓN DE ALERTAS ---
    mostrar_alerta_seguridad()

    # --- FUNCIÓN AUXILIAR DE NAVEGACIÓN ---
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
        if st.button("🛢️ operaciones de campo", use_container_width=True, key="btn_pozo"):
            navegar_a("🛢️ Operaciones de Campo")
    with col2:
        if st.button("🗺️ Mapa del Campo", use_container_width=True, key="btn_mapa"):
            navegar_a("🗺️ Mapa del Campo") # <-- Corregido: Removida asignación fantasma
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
        # 🎯 ¡VINCULACIÓN LOGRADA! Apunta al nuevo módulo de extracción artificial
        if st.button("🧮 Fórmulas Petroleras", use_container_width=True, key="btn_form"):
            navegar_a("🧮 Fórmulas de Producción Petrolera")

    # --- FILA 3: ENTRENAMIENTO Y EVALUACIÓN ---
    st.subheader("🧠 Entrenamiento y Evaluación")
    col7, col8, col9 = st.columns(3)
    with col7:
        if st.button("⚠ Entrenamiento Operativo", use_container_width=True, key="btn_entren"):
            navegar_a("🎯 Entrenamiento Operativo")
    with col8:
        if st.button("📘 Manual del Simulador", use_container_width=True, key="btn_manual"):
            navegar_a("📘 Manual")
    with col9:
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

    # --- NUEVA SECCIÓN: ANÁLISIS DE PARTICIPACIÓN ---
    st.subheader("📊 Análisis de Producción del Yacimiento")
    
    prod_alumno = st.session_state.get('prod_estimada', 150.0)
    vrr = st.session_state.get('vrr_sistema', 1.0)
    
    df_part = pd.DataFrame({
        "Sistema": ["AIB (Mecánico)", "BES (Control Alumno)", "PCP", "Gas Lift", "Surgencia"],
        "Producción": [450, prod_alumno, 300, 250, 400]
    })
    
    c_chart, c_metrics = st.columns([2, 1])
    
    with c_chart:
        fig = px.pie(df_part, values='Producción', names='Sistema', hole=0.4,
                     color_discrete_sequence=["#FF8C00", "#5A5A5A", "#A9A9A9", "#FFA500", "#2F4F4F"])
        fig.update_layout(showlegend=True, height=350, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        
    with c_metrics:
        total_m3 = df_part["Producción"].sum()
        st.metric("Total Yacimiento", f"{total_m3:,.1f} m3/d", delta=f"{vrr:.2f} VRR")
        st.write("**Estado de Inyección:**")
        if vrr < 1.0:
            st.warning("⚠️ VRR Insuficiente")
        else:
            st.success("✅ VRR Óptimo")

    # --- MONITOREO DE MENDOZA (CUENCA CUYANA) ---
    st.subheader("Estado General del Campo")
    mA, mB, mC = st.columns(3)
    
    mA.metric("Producción Total", f"{total_m3:,.1f} m3/d", f"{total_m3 * 6.29:,.0f} BPD")
    mB.metric("Presión de Separador", f"{120 * vrr:.1f} psi", f"{vrr - 1.0:.2f} Delta")
    mC.metric("Pozos en Operación", "6", "Activos")
