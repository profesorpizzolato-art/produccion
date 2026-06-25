import streamlit as st

def simular_destilacion_astm_d86(api):
    """Cálculo estimado del rendimiento según grados API"""
    factor_livianos = api / 50.0
    nafta = round(35 * factor_livianos, 1)
    kerosene = round(15 * factor_livianos, 1)
    gasoil = round(25 * (1 - (factor_livianos * 0.2)), 1)
    residuo = round(100 - (nafta + kerosene + gasoil), 1)
    return {"Nafta": nafta, "Kerosene": kerosene, "Gasoil": gasoil, "Residuo Pesado": residuo}

def mostrar_laboratorio_crudo():
    """Función principal que renderiza la interfaz en Streamlit"""
    st.header("🔬 Laboratorio de Control de Crudo (Res. 35/2021)")
    st.write("Ensayos clave y especificaciones comerciales antes del transporte o envío a refinería.")
    
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
        else:
            api_sugerido, visc_sugerida = 34.2, 12.0
            
        api = st.number_input("Gravedad API (°API) - ASTM D1298:", value=api_sugerido, step=0.1)
        viscosidad = st.number_input("Viscosidad (cSt) - ASTM D445:", value=visc_sugerida, step=0.5)
        pour_point = st.slider("Punto de Escurrimiento (°C) - ASTM D97:", -25, 10, -15)
        
    with col_param2:
        st.subheader("2. Impurezas Críticas")
        agua_sedimentos = st.number_input("Agua y Sedimentos BS&W (%) - ASTM D4007:", value=0.4, step=0.05)
        sal = st.number_input("Contenido de Sal (g/m³) - ASTM D3230:", value=45.0, step=5.0)
        
    with col_param3:
        st.subheader("3. Volatilidad")
        presion_reid = st.number_input("Presión de Vapor Reid (kPa a 37.8°C) - ASTM D323:", value=65.0, step=1.0)
        
    # Clasificación de Crudo según API
    tipo_crudo = "Pesado" if api < 22 else "Mediano" if api <= 31.1 else "Ligero"
    
    # Evaluación contra los límites estrictos de la Res. 35/2021
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
        
    # Alertas de desviaciones
    if not chk_agua: st.warning(f"⚠️ BS&W Fuera de especificación comercial (> 1.0%)")
    if not chk_sal: st.warning(f"⚠️ Contenido de Sal supera el máximo permitido (> 100 g/m³)")
    if not chk_reid: st.warning(f"⚠️ Presión de vapor Reid excede la seguridad normativa (> 103.42 kPa)")

    # Rendimiento de destilación estimado
    with st.expander("📊 Rendimiento Estimado de Refinación (Curva de Ebullición - ASTM D86)"):
        rendimiento = simular_destilacion_astm_d86(api)
        for prod, pct in rendimiento.items():
            st.progress(pct/100, text=f"{prod}: {pct}%")
