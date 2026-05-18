import streamlit as st
import pandas as pd
import time

# ==========================================
# 0. ESTILOS CSS PERSONALIZADOS (UI INDUSTRIAL)
# ==========================================
def aplicar_estilos_industriales():
    st.markdown(
        """
        <style>
        /* Contenedor del P&ID Simplificado (Línea de Proceso) */
        .flow-container {
            background-color: #0b132b; /* Azul noche oscuro */
            border-radius: 10px;
            padding: 18px;
            border: 1px solid #1c2541;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 20px;
        }
        .flow-step {
            color: #48cae4; /* Azul brillante */
            font-weight: bold;
            font-size: 15px;
            display: flex;
            align-items: center;
        }
        .flow-arrow {
            color: #06d6a0; /* Verde agua para dirección del flujo */
            font-weight: bold;
            margin: 0 4px;
        }
        
        /* Tarjetas de Equipos de la Planta */
        .equipo-card {
            background-color: #1e293b;
            padding: 15px;
            border-radius: 8px;
            min-height: 110px;
        }
        </style>
        """,
        unsafe_allowed_html=True
    )


# ==========================================
# 1. MÓDULO: PLANTA DE PRODUCCIÓN (PTC)
# ==========================================
def planta_produccion():
    aplicar_estilos_industriales()
    
    st.header("🏭 Planta de Tratamiento de Crudo (PTC) - Control Central")
    st.write("Monitoreo de Tren de Separación, Calentamiento y Deshidratación.")

    # --- Session State para interactividad ---
    if 'presion_sep' not in st.session_state:
        st.session_state.presion_sep = 120.0
    if 'temp_calentador' not in st.session_state:
        st.session_state.temp_calentador = 65.0

    # --- LAYOUT PRINCIPAL ---
    col_proceso, col_control = st.columns([3, 1])

    with col_proceso:
        st.subheader("Esquema de Flujo (P&ID Simplificado)")
        
        # REPLICACIÓN DE LA IMAGEN 2: Línea de proceso estilizada
        st.markdown(
            """
            <div class="flow-container">
                <span class="flow-step">🕹️ Manifold de Entrada</span>
                <span class="flow-arrow">➔</span>
                <span class="flow-step">🛢️ Separador Trifásico</span>
                <span class="flow-arrow">➔</span>
                <span class="flow-step">🔥 Calentador</span>
                <span class="flow-arrow">➔</span>
                <span class="flow-step">💧 Tanque Cortador</span>
                <span class="flow-arrow">➔</span>
                <span class="flow-step">🚛 Despacho</span>
            </div>
            """,
            unsafe_allowed_html=True
        )
        
        # REPLICACIÓN DE LA IMAGEN 1: Bloques visuales de planta dinámica
        st.write("**Simulación de Planta de Proceso en Tiempo Real**")
        p1, p2, p3 = st.columns(3)
        
        with p1:
            st.markdown(
                f"""<div class="equipo-card" style="border-left: 5px solid #eab308;">
                <h5 style="margin:0; color:white;">Entrada de Gas 💨</h5>
                <p style="color:#94a3b8; font-size:13px; margin-top:8px;">Presión: {st.session_state.presion_sep * 0.37:.1f} psi<br>Válvula: Abierta</p>
                </div>""", unsafe_allowed_html=True
            )
            
        with p2:
            # Color de borde dinámico según nivel de alarma
            sep_color = "#ef4444" if st.session_state.presion_sep > 180 else "#22c55e"
            st.markdown(
                f"""<div class="equipo-card" style="border-left: 5px solid {sep_color};">
                <h5 style="margin:0; color:white;">Separador V-01 🛢️</h5>
                <p style="color:#94a3b8; font-size:13px; margin-top:8px;">Presión: {st.session_state.presion_sep} psi<br>Eficiencia: 98.4%</p>
                </div>""", unsafe_allowed_html=True
            )
            
        with p3:
            st.markdown(
                f"""<div class="equipo-card" style="border-left: 5px solid #3b82f6;">
                <h5 style="margin:0; color:white;">Desgasificador 🧪</h5>
                <p style="color:#94a3b8; font-size:13px; margin-top:8px;">Temp Crudo: {st.session_state.temp_calentador} °C<br>Vacío: -2.1 psi</p>
                </div>""", unsafe_allowed_html=True
            )
            
        st.write("") # Espaciador

        # Métricas de Proceso estándar abajo
        m1, m2, m3 = st.columns(3)
        m1.metric("Presión Separador", f"{st.session_state.presion_sep} psi", "Normal" if st.session_state.presion_sep <= 180 else "ALTA")
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

    # --- SECCIÓN TÉCNICA ---
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


# ==========================================
# 2. MÓDULO: CENTRO DE CONTROL (PLANTAS MULTIPESTAÑA)
# ==========================================
def mostrar_plantas_proceso():
    aplicar_estilos_industriales()
    
    st.header("🏭 Centro de Control: Plantas de Proceso")
    st.write("Gestión integral de los equipos de separación, tratamiento y despacho.")

    # Pestañas principales
    tabs = st.tabs([
        "🌀 Separación", 
        "📊 Puente de Gas",
        "📈 Ensayo de Pozos", 
        "🛢️ Tanques", 
        "🚢 Unidad LACT"
    ])

    # --- PESTAÑA 1: SEPARADORES ---
    with tabs[0]:
        st.subheader("Separador Trifásico V-01")
        
        # Inyectamos el flujo resumido también acá para contexto del alumno
        st.markdown(
            """
            <div class="flow-container" style="padding:10px; margin-bottom:15px;">
                <span class="flow-step" style="font-size:13px;">📥 Manifold</span> <span class="flow-arrow">➔</span>
                <span class="flow-step" style="font-size:14px; color:#06d6a0; background-color:#1e293b; padding:2px 8px; border-radius:4px;">🛢️ Separador Trifásico (Ubicación Actual)</span> <span class="flow-arrow">➔</span>
                <span class="flow-step" style="font-size:13px; opacity:0.5;">🔥 Calentador</span>
            </div>
            """,
            unsafe_allowed_html=True
        )
        
        c1, c2 = st.columns(2)
        presion = c1.slider("Presión de Control (psi):", 20, 100, 45, key="sep_p")
        nivel = c2.slider("Nivel de Interfase (%):", 0, 100, 50, key="sep_n")
        
        if presion > 85:
            st.error("🚨 ALERTA: Alta presión. Riesgo de apertura de PSV (Válvula de Seguridad).")
        else:
            st.success("Estado: Operación estable.")

    # --- PESTAÑA 2: PUENTE DE GAS ---
    with tabs[1]:
        st.subheader("Medición Fiscal de Gas")
        col_g1, col_g2 = st.columns(2)
        h_diff = col_g1.number_input("Presión Diferencial (InH2O):", 0, 100, 40)
        p_est = col_g2.number_input("Presión Estática (psia):", 20, 200, 50)
        
        caudal_gas = (h_diff * p_est)**0.5 * 15.5
        st.metric("Caudal de Gas Calculado", f"{caudal_gas:.2f} m3/std")
        
        if h_diff > 90: st.warning("⚠️ Cambiar a una placa de orificio de mayor diámetro.")

    # --- PESTAÑA 3: ENSAYO DE POZOS ---
    with tabs[2]:
        st.subheader("Control de Producción (Test Header)")
        pozo = st.selectbox("Seleccionar pozo para ensayo:", ["MENFA-001", "MENFA-002", "MENFA-003"])
        if st.button("▶️ Iniciar Ensayo de 12hs"):
            with st.status("Recibiendo datos de separador de ensayo..."):
                time.sleep(1.5)
                st.metric("Producción Neta", "48.2 m3/d", "+2.5%")

    # --- PESTAÑA 4: TANQUES ---
    with tabs[3]:
        st.subheader("Parque de Tanques (Almacenamiento)")
        tk_nivel = st.number_input("Nivel de Tanque TK-200 (ft):", 0.0, 40.0, 28.5)
        if tk_nivel > 36:
            st.error("🚨 NIVEL CRÍTICO: Riesgo de rebalse. Detener bombeo de entrada.")
        
        if st.button("💧 Drenar Agua de Formación"):
            st.info("Operación iniciada. Verificando calidad de agua de salida...")

    # --- PESTAÑA 5: UNIDAD LACT ---
    with tabs[4]:
        st.subheader("Venta y Transferencia de Custodia")
        bsw = st.slider("Corte de Agua (BSW %):", 0.0, 5.0, 0.4, step=0.1)
        
        if bsw > 1.0:
            st.markdown("### 🔴 SALIDA BLOQUEADA")
            st.error("El crudo no cumple especificación comercial (>1% BSW).")
        else:
            st.markdown("### 🟢 DESPACHO ACTIVO")
            st.success("Enviando crudo a Oleoducto Principal.")
