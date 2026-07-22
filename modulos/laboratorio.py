import streamlit as st

def simular_destilacion_astm_d86(api):
    """Cálculo estimado del rendimiento según grados API"""
    factor_livianos = api / 50.0
    nafta = round(35 * factor_livianos, 1)
    kerosene = round(15 * factor_livianos, 1)
    gasoil = round(25 * (1 - (factor_livianos * 0.2)), 1)
    residuo = round(max(0.0, 100.0 - (nafta + kerosene + gasoil)), 1)
    return {"Nafta": nafta, "Kerosene": kerosene, "Gasoil": gasoil, "Residuo Pesado": residuo}

def calcular_dosis_quimico(caudal_bpd, ppm_objetivo, densidad_quimico_g_ml=0.92):
    """
    Cálculo de Inyección de Químico Desemulsionante / Antiemulsionante.
    - Caudal en BPD (Barreles per day)
    - Dosis en ppm (partes por millón)
    - Retorna el caudal de inyección en L/día y cm3/min (GPD / LPD)
    """
    # 1 BBL = 158.987 Litros
    caudal_litros_dia = caudal_bpd * 158.987
    # Litros de químico puro = (L_crudo * ppm) / 1,000,000
    litros_quimico_dia = (caudal_litros_dia * ppm_objetivo) / 1_000_000
    cm3_minuto = (litros_quimico_dia * 1000) / 1440  # 1440 min/día
    
    return round(litros_quimico_dia, 2), round(cm3_minuto, 2)

def mostrar_laboratorio_crudo(bsw_motor=None, rvp_motor=None, caudal_motor=450.0):
    """
    Función principal del Laboratorio de Crudo + Tratamiento Químico.
    """
    st.header("🔬 Laboratorio de Control de Crudo & Dosificación Química")
    st.write("Ensayos bajo Res. 35/2021 y optimización de inyección de aditivos upstream.")

    tab_lab, tab_quimico = st.tabs(["🧪 Ensayos de Calidad (ASTM)", "🧪 Dosificación de Químicos Upstream"])

    # Valores base por defecto
    bsw_def = float(bsw_motor) if bsw_motor is not None else 0.4
    rvp_def = float(rvp_motor) if rvp_motor is not None else 65.0

    # -------------------------------------------------------------------------
    # TAB 1: ENSAYOS DE LABORATORIO
    # -------------------------------------------------------------------------
    with tab_lab:
        cuenca = st.selectbox("Seleccionar Procedencia del Crudo:", [
            "Cuenca Neuquina (Medanito)", 
            "Cuenca Golfo San Jorge (Escalante)", 
            "Cuenca Austral", 
            "Cuenca Cuyana"
        ])
        
        col_param1, col_param2, col_param3 = st.columns(3)
        with col_param1:
            st.subheader("1. Propiedades Físicas")
            if "Golfo" in cuenca:
                api_sugerido, visc_sugerida = 24.5, 45.0
            elif "Cuyana" in cuenca:
                api_sugerido, visc_sugerida = 31.0, 22.0
            else:
                api_sugerido, visc_sugerida = 34.2, 12.0
                
            api = st.number_input("Gravedad API (°API) - ASTM D1298:", value=api_sugerido, step=0.1)
            viscosidad = st.number_input("Viscosidad (cSt) - ASTM D445:", value=visc_sugerida, step=0.5)
            pour_point = st.slider("Punto de Escurrimiento (°C) - ASTM D97:", -25, 10, -15)
            
        with col_param2:
            st.subheader("2. Impurezas Críticas")
            agua_sedimentos = st.number_input("Agua y Sedimentos BS&W (%) - ASTM D4007:", value=bsw_def, step=0.05)
            sal = st.number_input("Contenido de Sal (g/m³) - ASTM D3230:", value=45.0, step=5.0)
            
        with col_param3:
            st.subheader("3. Volatilidad")
            presion_reid = st.number_input("Presión de Vapor Reid (kPa a 37.8°C) - ASTM D323:", value=rvp_def, step=1.0)
            
        # Clasificación de Crudo según API
        tipo_crudo = "Pesado" if api < 22 else "Mediano" if api <= 31.1 else "Ligero"
        
        # Evaluación contra la Res. 35/2021
        chk_agua = agua_sedimentos <= 1.0
        chk_sal = sal <= 100.0
        chk_reid = presion_reid <= 103.42
        apto = chk_agua and chk_sal and chk_reid
        
        st.markdown("---")
        st.subheader("📋 Dictamen Técnico Final")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Clasificación por Densidad", f"Crudo {tipo_crudo}", f"{api} °API")
        
        if apto:
            c2.success("✅ APTO PARA TRANSPORTE")
        else:
            c2.error("❌ RECHAZADO / TRATAMIENTO")
            
        c3.metric("Viscosidad Cinemática", f"{viscosidad} cSt")
            
        if not chk_agua: st.warning("⚠️ BS&W Fuera de especificación comercial (> 1.0%)")
        if not chk_sal: st.warning("⚠️ Contenido de Sal supera el máximo permitido (> 100 g/m³)")
        if not chk_reid: st.warning("⚠️ Presión de vapor Reid excede la seguridad normativa (> 103.42 kPa)")

        with st.expander("📊 Rendimiento Estimado de Refinación (ASTM D86)"):
            rendimiento = simular_destilacion_astm_d86(api)
            for prod, pct in rendimiento.items():
                val_progress = max(0.0, min(1.0, pct / 100.0))
                st.progress(val_progress, text=f"{prod}: {pct}%")

    # -------------------------------------------------------------------------
    # TAB 2: DOSIFICACIÓN DE QUÍMICOS UPSTREAM
    # -------------------------------------------------------------------------
    with tab_quimico:
        st.subheader("🧪 Sistema de Inyección de Químicos (Tratamiento Superficial)")
        st.write("Ajuste del programa quimico para rompimiento de emulsión Agua en Petróleo (W/O).")

        col_q1, col_q2 = st.columns(2)

        with col_q1:
            tipo_quimico = st.selectbox("Seleccionar Aditivo Químico:", [
                "Desemulsionante Principal (Rompimiento Base)",
                "Clarificante de Agua (Tratamiento de Secundaria)",
                "Antincrustante (Inhibidor de Incrustaciones)",
                "Secuestrante de H2S (Triazina)"
            ])

            caudal_tratar = st.number_input("Caudal de Crudo a Tratar (BPD):", value=float(caudal_motor), step=50.0)
            ppm_dosis = st.slider("Dosis Objetivo (ppm):", min_value=5, max_value=150, value=30, step=5)

            litros_dia, cm3_min = calcular_dosis_quimico(caudal_tratar, ppm_dosis)

        with col_q2:
            st.markdown("### 📊 Consumo Calculado")
            st.metric("Tasa de Inyección Diaria", f"{litros_dia} L/día")
            st.metric("Caudal de Inyección Calibrado", f"{cm3_min} cm³/min")

            # Diagnóstico técnico de la dosis
            st.markdown("---")
            if ppm_dosis < 20:
                st.error("🚨 **Subdosificación crítica:** Riesgo de emulsión dura. El BS&W en separadores aumentará por encima del 1.0%.")
            elif 20 <= ppm_dosis <= 50:
                st.success("🟢 **Dosis Óptima de Operación:** Eficiencia de separación ideal sin sobredimensionar costos quimicos.")
            else:
                st.warning("⚠️ **Sobredosificación (Efecto Inverso):** Exceso de tensioactivo. Puede saturar la fase acuosa y encarecer el OPEX.")

        st.info(f"💡 **Regla Operativa:** Para {caudal_tratar} BPD con {ppm_dosis} ppm de {tipo_quimico.split('(')[0].strip()}, ajustá la bomba dosificadora a **{cm3_min} cm³/min** en la cabeza de pozo o manifold de entrada.")
