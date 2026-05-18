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
        
        /* Contenedor adaptativo para el plano interactivo */
        .svg-container {
            width: 100%;
            overflow-x: auto;
            background-color: #0b132b;
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #1e293b;
        }
        </style>
        """,
        unsafe_allow_html=True
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
        st.subheader("Plano de Proceso Interactivo (Gemelo Digital)")
        
        # --- RENDERIZADO DEL DIAGRAMA VECTORIAL (SVG) ---
        # Definición de variables dinámicas y lógicas de alerta para el plano
        p_sep = st.session_state.presion_sep
        t_horno = st.session_state.temp_calentador
        p_gas = p_sep * 0.37
        
        box_sep_color = "#ef4444" if p_sep > 180 else "#22c55e"
        box_horno_color = "#ef4444" if t_horno > 80 else "#f97316"
        
        # Estructura del plano mapeada por coordenadas fijas
        svg_code = f"""
        <div class="svg-container">
        <svg viewBox="0 0 850 500" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="850" height="500" rx="10" fill="#0b1224"/>
            
            <path d="M 50,150 L 150,150" stroke="#38bdf8" stroke-width="3" fill="none" />
            <path d="M 100,150 L 100,320 L 150,320" stroke="#38bdf8" stroke-width="3" fill="none" />
            <path d="M 230,320 L 260,320 L 260,170 L 280,170" stroke="#38bdf8" stroke-width="3" fill="none" />
            
            <path d="M 210,150 L 280,150" stroke="#22c55e" stroke-width="3" fill="none" />
            
            <path d="M 340,130 L 340,100 L 440,100 L 440,120" stroke="#38bdf8" stroke-width="3" fill="none" />
            <path d="M 340,170 L 340,240 L 210,240 L 210,400 L 240,400" stroke="#f97316" stroke-width="3" fill="none" />
            
            <path d="M 500,150 L 660,150 L 660,170" stroke="#38bdf8" stroke-width="3" fill="none" />
            
            <path d="M 340,420 L 480,420 L 480,360 L 510,360" stroke="#f97316" stroke-width="3" fill="none" />
            <path d="M 570,360 L 680,360 L 680,400" stroke="#f97316" stroke-width="3" fill="none" />
            
            <path d="M 720,150 L 780,150 L 780,450" stroke="#22c55e" stroke-width="3" fill="none" />
            <path d="M 680,460 L 680,480 L 780,480" stroke="#3b82f6" stroke-width="3" fill="none" />
            <path d="M 620,240 L 780,240" stroke="#eab308" stroke-width="3" fill="none" stroke-dasharray="5,5" />
            
            <rect x="150" y="125" width="60" height="50" rx="5" fill="#1e293b" stroke="#94a3b8" stroke-width="2"/>
            <text x="180" y="155" fill="white" font-size="11" font-family="Arial" font-weight="bold" text-anchor="middle">Entrada</text>
            
            <rect x="280" y="120" width="120" height="60" rx="8" fill="#1e293b" stroke="{box_sep_color}" stroke-width="3"/>
            <text x="340" y="145" fill="white" font-size="12" font-family="Arial" font-weight="bold" text-anchor="middle">Separador V-01</text>
            <text x="340" y="165" fill="#94a3b8" font-size="11" font-family="Arial" text-anchor="middle">{p_sep} psi</text>
            
            <rect x="420" y="120" width="80" height="55" rx="5" fill="#2d3748" stroke="#38bdf8" stroke-width="2"/>
            <text x="460" y="145" fill="white" font-size="10" font-family="Arial" font-weight="bold" text-anchor="middle">Trampa</text>
            <text x="460" y="160" fill="white" font-size="10" font-family="Arial" text-anchor="middle">Scrubber</text>
            
            <rect x="150" y="295" width="80" height="50" rx="5" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
            <text x="190" y="320" fill="white" font-size="10" font-family="Arial" font-weight="bold" text-anchor="middle">Compresor</text>
            <text x="190" y="335" fill="#38bdf8" font-size="9" font-family="Arial" text-anchor="middle">{p_gas:.1f} psi</text>
            
            <rect x="240" y="385" width="100" height="60" rx="8" fill="#1e293b" stroke="{box_horno_color}" stroke-width="3"/>
            <text x="290" y="415" fill="white" font-size="12" font-family="Arial" font-weight="bold" text-anchor="middle">Horno</text>
            <text x="290" y="435" fill="#f97316" font-size="11" font-family="Arial" text-anchor="middle">{t_horno} °C</text>
            
            <circle cx="540" cy="360" r="25" fill="#1e293b" stroke="#94a3b8" stroke-width="2"/>
            <text x="540" cy="364" fill="white" font-size="11" font-family="Arial" font-weight="bold" text-anchor="middle">Bomba</text>
            
            <rect x="610" y="170" width="100" height="80" rx="15" fill="#2d3748" stroke="#3b82f6" stroke-width="2"/>
            <text x="660" y="215" fill="white" font-size="11" font-family="Arial" font-weight="bold" text-anchor="middle">Desgasificador</text>
            
            <rect x="640" y="380" width="80" height="80" rx="5" fill="#1e293b" stroke="#6366f1" stroke-width="2"/>
            <text x="680" y="415" fill="white" font-size="11" font-family="Arial" font-weight="bold" text-anchor="middle">Columna</text>
            <text x="680" y="435" fill="white" font-size="10" font-family="Arial" text-anchor="middle">Estabilizadora</text>
            
            <text x="50" y="135" fill="#38bdf8" font-size="11" font-family="Arial" font-weight="bold">Entrada de Gas</text>
            <text x="780" y="135" fill="#22c55e" font-size="11" font-family="Arial" font-weight="bold" text-anchor="end">Salida Petróleo</text>
            <text x="780" y="495" fill="#3b82f6" font-size="11" font-family="Arial" font-weight="bold" text-anchor="end">Salida de Agua</text>
            <text x="615" y="270" fill="#eab308" font-size="10" font-family="Arial">Hacia Tanques</text>
        </svg>
        </div>
        """
        st.components.v1.html(svg_code, height=520)
        
        # Línea de proceso resumida (Breadcrumb) abajo para referencia corta
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
            unsafe_allow_html=True
        )

        # Métricas de Proceso estándar abajo
        m1, m2, m3 = st.columns(3)
        m1.metric("Presión Separador", f"{st.session_state.presion_sep} psi", "Normal" if st.session_state.presion_sep <= 180 else "ALTA")
        m2.metric("Temperatura Crudo", f"{st.session_state.temp_calentador} °C", "Óptima")
        m3.metric("Caudal de Entrada", "1850 BPD", "+12 BPD")

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
        
        st.markdown(
            """
            <div class="flow-container" style="padding:10px; margin-bottom:15px;">
                <span class="flow-step" style="font-size:13px;">📥 Manifold</span> <span class="flow-arrow">➔</span>
                <span class="flow-step" style="font-size:14px; color:#06d6a0; background-color:#1e293b; padding:2px 8px; border-radius:4px;">🛢️ Separador Trifásico (Ubicación Actual)</span> <span class="flow-arrow">➔</span>
                <span class="flow-step" style="font-size:13px; opacity:0.5;">🔥 Calentador</span>
            </div>
            """,
            unsafe_allow_html=True
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
