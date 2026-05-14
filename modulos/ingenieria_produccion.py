import streamlit as st
import pandas as pd

def mostrar_ingenieria_produccion():
    st.header("⚙️ Ingeniería de Producción y Recuperación")
    st.write("Bienvenido al módulo de optimización de yacimientos. Aquí podrá configurar los métodos de extracción y estrategias de recuperación.")

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
                st.write("- **Ventajas:** Simple, confiable y de fácil mantenimiento.")
                st.write("- **Limitación:** Profundidad limitada por el peso de las varillas y manejo pobre de gas.")
                st.info("💡 Tip: Observe cómo el aumento de SPM (golpes por minuto) eleva la temperatura por fricción en las varillas.")
            with col2:
                st.write("**Calculadora de Producción**")
                spm = st.slider("Emboladas por minuto (SPM):", 1, 15, 8)
                carrera = st.number_input("Longitud de carrera (pulg):", value=100)
                eficiencia = 0.8
                prod = (spm * carrera * eficiencia) * 0.15 
                st.metric("Producción Estimada", f"{prod:.2f} m3/d", "+1.2%")

        elif sistema == "BES (Electrosumergible)":
            with col1:
                st.write("**Bombeo Electrosumergible**")
                st.write("- **Uso:** Pozos de alto caudal (acuíferos fuertes).")
                st.write("- **Componentes:** Motor de fondo, protector y bomba centrífuga multietapa.")
                st.warning("⚠️ Cuidado con la cavitación si la presión de entrada baja del punto de burbuja.")
            with col2:
                hz = st.slider("Frecuencia del VDF (Hz):", 30, 70, 50)
                caudal = hz * 1.8 
                st.metric("Caudal de Bomba", f"{caudal:.1f} m3/d")

        elif sistema == "PCP (Cavidades Progresivas)":
            with col1:
                st.write("**Bombeo por Cavidades Progresivas**")
                st.write("- **Uso:** Crudos pesados y fluidos con alta presencia de arena.")
                st.write("- **Mecánica:** Un rotor metálico gira dentro de un estator de elastómero.")
            with col2:
                rpm = st.slider("Velocidad de Giro (RPM):", 50, 500, 250)
                st.metric("Producción PCP", f"{rpm * 0.12:.2f} m3/d")

        elif sistema == "Gas Lift":
            with col1:
                st.write("**Levantamiento Artificial por Gas**")
                st.write("- **Principio:** Inyectar gas en el anular para alivianar la densidad de la columna.")
                st.write("- **Ventaja:** Ideal para pozos desviados o plataformas offshore.")
            with col2:
                q_gas = st.number_input("Gas Inyectado (kscf/d):", 0, 2000, 500)
                st.metric("Reducción de Gradiente", f"{q_gas * 0.05:.1f} psi/ft")

    # --- TAB 2: RECUPERACIÓN SECUNDARIA ---
    with tab2:
        st.subheader("Inyección de Agua (Waterflooding)")
        st.write("""
        La recuperación secundaria se activa cuando la energía natural del reservorio declina. 
        El agua inyectada tiene dos funciones: **Mantenimiento de presión** y **Barrido mecánico** del crudo.
        """)
        
        col_sec1, col_sec2 = st.columns(2)
        with col_sec1:
            inyectado = st.number_input("Agua Inyectada Total (m3/d):", 0, 2000, 400)
            reemplazo = st.slider("Voidage Replacement Ratio (VRR):", 0.0, 2.0, 1.0)
        
        with col_sec2:
            if reemplazo < 1.0:
                st.error("Presión en declive: Se extrae más fluido del que se inyecta.")
            elif reemplazo == 1.0:
                st.success("Presión Estabilizada: Balance perfecto.")
            else:
                st.warning("Sobrepresión: Riesgo de fractura no deseada en la formación.")

    # --- TAB 3: RECUPERACIÓN TERCIARIA (EOR) ---
    with tab3:
        st.subheader("Enhanced Oil Recovery (EOR)")
        st.write("Métodos avanzados para movilizar el petróleo residual que el agua no pudo desplazar.")
        
        metodo = st.radio("Seleccione Tecnología EOR:", ["Térmico (Vapor)", "Químico (Polímeros)", "Miscible (CO2)"])
        
        if metodo == "Térmico (Vapor)":
            st.info("**Objetivo:** Reducir la viscosidad. Ideal para crudos pesados de la cuenca del Golfo San Jorge.")
            st.slider("Temperatura de Inyección (°C):", 100, 300, 220)
        
        elif metodo == "Químico (Polímeros)":
            st.info("**Objetivo:** Mejorar la relación de movilidad. El polímero 'espesa' el agua para que no se canalice.")
            st.slider("Concentración (ppm):", 500, 3000, 1500)
            
        elif metodo == "Miscible (CO2)":
            st.info("**Objetivo:** El CO2 se mezcla con el petróleo, lo expande y reduce su tensión superficial.")
            st.metric("Incremento Factor de Recobro Est.", "8-15%")

    st.divider()
    st.caption("Módulo desarrollado para la capacitación técnica de IPCL MENFA - 2026")
