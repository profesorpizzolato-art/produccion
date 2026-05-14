import streamlit as st
import pandas as pd

def mostrar_ingenieria_produccion():
    st.header("⚙️ Ingeniería de Producción y Recuperación")
    
    tab1, tab2, tab3 = st.tabs(["Sistemas S.E.A.", "Recuperación Secundaria", "Recuperación Terciaria (EOR)"])

    with tab1:
        st.subheader("Sistemas de Extracción Artificial")
        sistema = st.selectbox("Seleccione Sistema:", ["AIB (Mecánico)", "BES (Electrosumergible)", "PCP (Cavidades Progresivas)", "Gas Lift"])
        
        col1, col2 = st.columns([1, 1])
        
        if sistema == "AIB (Mecánico)":
            with col1:
                st.write("**Características:** Ideal para pozos de bajo caudal y profundidades medias. Muy robusto y fácil de supervisar visualmente.")
                st.info("Concepto Clave: Transformación de movimiento rotativo a alternativo.")
            with col2:
                # Simulador práctico simple
                st.write("**Calculadora de Producción Estimada**")
                emboladas = st.slider("Emboladas por minuto (SPM):", 1, 15, 8)
                carrera = st.number_input("Longitud de carrera (pulg):", value=100)
                eficiencia = 0.8
                prod = (emboladas * carrera * eficiencia) * 0.15 # Factor simplificado
                st.metric("Producción Estimada (m3/d)", f"{prod:.2f}")

        elif sistema == "BES (Electrosumergible)":
            with col1:
                st.write("**Características:** Maneja grandes caudales. Requiere energía eléctrica de alta potencia. Sensible a la presencia de gas.")
            with col2:
                hz = st.slider("Frecuencia (Hz):", 30, 70, 50)
                caudal = hz * 1.5 # Relación lineal simplificada
                st.metric("Caudal de Bomba", f"{caudal} m3/d")

    with tab2:
        st.subheader("Recuperación Secundaria: Inyección de Agua")
        st.write("El objetivo es mantener la presión del reservorio y desplazar el petróleo hacia los pozos productores.")
        
        # Práctica de eficiencia de barrido
        inyectado = st.number_input("Agua Inyectada (m3/dia):", 0, 500, 100)
        reemplazo = st.slider("Factor de Reemplazo (Voidage Replacement Ratio):", 0.5, 1.5, 1.0)
        st.write(f"Con un factor de {reemplazo}, la presión del yacimiento tiende a {'estabilizarse' if reemplazo == 1.0 else 'variar'}.")

    with tab3:
        st.subheader("Recuperación Terciaria (EOR)")
        metodo = st.radio("Método EOR:", ["Térmico (Vapor)", "Químico (Polímeros/Surfactantes)", "Gaseoso (CO2)"])
        if metodo == "Térmico (Vapor)":
            st.write("Reduce la **viscosidad** del crudo pesado para facilitar su flujo.")
