import streamlit as st
import pandas as pd

def mostrar_ingenieria_produccion():
    st.header("⚙️ Ingeniería de Producción y Recuperación")
    st.write("Optimización de métodos de extracción y estrategias de recuperación de yacimientos.")

    # Inicializamos variables de estado si no existen para evitar errores
    if 'prod_estimada' not in st.session_state: st.session_state.prod_estimada = 80.0
    if 'vrr_sistema' not in st.session_state: st.session_state.vrr_sistema = 1.0

    tab1, tab2, tab3 = st.tabs(["Sistemas S.E.A.", "Recuperación Secundaria", "Recuperación Terciaria (EOR)"])

    # --- TAB 1: SISTEMAS DE EXTRACCIÓN ARTIFICIAL ---
    with tab1:
        st.subheader("Sistemas de Extracción Artificial (S.E.A.)")
        sistema = st.selectbox("Seleccione Sistema a Evaluar:", 
                              ["AIB (Mecánico)", "BES (Electrosumergible)", "PCP (Cavidades Progresivas)", "Gas Lift"])
        
        col1, col2 = st.columns([1, 1])
        
        if sistema == "AIB (Mecánico)":
            with col1:
                st.write("**Aparato de Bombeo Mecánico (Cigüeña)**")
                st.write("- **Ventajas:** Simple y confiable.")
                st.info("💡 Tip: El aumento de SPM eleva la producción pero aumenta la fatiga de varillas.")
            with col2:
                spm = st.slider("Emboladas por minuto (SPM):", 1, 15, 8)
                carrera = st.number_input("Longitud de carrera (pulg):", value=100)
                st.session_state.prod_estimada = (spm * carrera * 0.8) * 0.15 
                st.metric("Producción Calculada", f"{st.session_state.prod_estimada:.2f} m3/d")

        elif sistema == "BES (Electrosumergible)":
            with col1:
                st.write("**Bombeo Electrosumergible**")
                st.warning("⚠️ Cuidado con la cavitación en altas frecuencias.")
            with col2:
                hz = st.slider("Frecuencia del VDF (Hz):", 30, 70, 50)
                st.session_state.prod_estimada = hz * 1.8 
                st.metric("Caudal de Bomba", f"{st.session_state.prod_estimada:.1f} m3/d")

        elif sistema == "PCP (Cavidades Progresivas)":
            with col1:
                st.write("**Bombeo por Cavidades Progresivas**")
                st.write("- **Uso:** Crudos pesados y arenas.")
            with col2:
                rpm = st.slider("Velocidad de Giro (RPM):", 50, 500, 250)
                st.session_state.prod_estimada = rpm * 0.12
                st.metric("Producción PCP", f"{st.session_state.prod_estimada:.2f} m3/d")

        elif sistema == "Gas Lift":
            with col1:
                st.write("**Levantamiento Artificial por Gas**")
            with col2:
                q_gas = st.number_input("Gas Inyectado (kscf/d):", 0, 2000, 500)
                st.metric("Reducción de Gradiente", f"{q_gas * 0.05:.1f} psi/ft")

    # --- TAB 2: RECUPERACIÓN SECUNDARIA ---
    with tab2:
        st.subheader("Inyección de Agua (Waterflooding)")
        col_sec1, col_sec2 = st.columns(2)
        with col_sec1:
            st.session_state.vrr_sistema = st.slider("Voidage Replacement Ratio (VRR):", 0.0, 2.0, 1.0)
        
        with col_sec2:
            if st.session_state.vrr_sistema < 1.0:
                st.error("Presión en declive: VRR < 1.0")
            elif st.session_state.vrr_sistema == 1.0:
                st.success("Presión Estabilizada: VRR = 1.0")
            else:
                st.warning("Sobrepresión: VRR > 1.0")

    # --- TAB 3: RECUPERACIÓN TERCIARIA (EOR) ---
    with tab3:
        st.subheader("Enhanced Oil Recovery (EOR)")
        metodo = st.radio("Seleccione Tecnología EOR:", ["Térmico (Vapor)", "Químico (Polímeros)", "Miscible (CO2)"])
        
        if metodo == "Térmico (Vapor)":
            st.info("Reduce la viscosidad. Ideal para crudos pesados.")
            temp = st.slider("Temperatura de Inyección (°C):", 100, 300, 220)
            # El vapor aumenta la eficiencia un 15% extra
            st.session_state.prod_estimada *= 1.15
        
        elif metodo == "Químico (Polímeros)":
            st.info("Mejora el barrido (eficiencia volumétrica).")
            st.slider("Concentración (ppm):", 500, 3000, 1500)
            st.session_state.prod_estimada *= 1.10
            
    st.divider()
    st.caption("Módulo desarrollado para la capacitación técnica de IPCL MENFA - 2026")
