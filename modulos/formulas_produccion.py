import streamlit as st
import math

def formulas_produccion():
    st.title("🧮 Fórmulas de Producción Petrolera")
    st.subheader("IPCL MENFA - Cálculos Operativos de Extracción")
    st.markdown("---")

    menu = st.selectbox(
        "Seleccionar cálculo / Sistema de Extracción:",
        [
            "Índice de Productividad (PI)",
            "Corte de Agua (BSW / WC)",
            "Gradiente Hidrostático",
            "Producción Teórica Bombeo Mecánico (AIB)",
            "Producción por Bombeo Electrosumergible (BES)",
            "Producción por Cavidades Progresivas (PCP)",
            "Inyección de Gas Lift (Cálculo de Tasa)"
        ]
    )

    # ---------------------------------------------------------
    # ÍNDICE DE PRODUCTIVIDAD (PI)
    # ---------------------------------------------------------
    if menu == "Índice de Productividad (PI)":
        st.markdown("#### Fórmula de IP (Vogel Lineal / Darcy)")
        st.latex(r"PI = \frac{Q}{P_r - P_{wf}}")

        col1, col2, col3 = st.columns(3)
        with col1:
            q = st.number_input("Producción Actual (Q) [BPD]", min_value=0.0, value=150.0, step=10.0)
        with col2:
            pr = st.number_input("Presión de Reservorio (Pr) [psi]", min_value=0.0, value=3000.0, step=100.0)
        with col3:
            pwf = st.number_input("Presión Fondo Fluyente (Pwf) [psi]", min_value=0.0, value=1500.0, step=100.0)

        if st.button("Calcular PI", use_container_width=True):
            if pr - pwf <= 0:
                st.error("⚠️ La Presión de Reservorio debe ser estrictamente mayor a la Presión Fluyente (Pwf).")
            else:
                pi = q / (pr - pwf)
                st.metric("Índice de Productividad", f"{round(pi, 3)} BPD/psi")

    # ---------------------------------------------------------
    # CORTE DE AGUA (WC)
    # ---------------------------------------------------------
    elif menu == "Corte de Agua (BSW / WC)":
        st.markdown("#### Fórmula de Corte de Agua (Water Cut)")
        st.latex(r"WC = \frac{Q_{agua}}{Q_{agua} + Q_{petróleo}} \times 100")

        col1, col2 = st.columns(2)
        with col1:
            agua = st.number_input("Producción de Agua [BPD]", min_value=0.0, value=200.0, step=10.0)
        with col2:
            petroleo = st.number_input("Producción de Petróleo [BPD]", min_value=0.0, value=800.0, step=10.0)

        if st.button("Calcular WC", use_container_width=True):
            total_fluido = agua + petroleo
            if total_fluido == 0:
                st.error("⚠️ La producción total (Agua + Petróleo) no puede ser cero.")
            else:
                wc = agua / total_fluido
                st.metric("Corte de Agua (WC / BSW)", f"{round(wc * 100, 2)} %")

    # ---------------------------------------------------------
    # GRADIENTE HIDROSTÁTICO
    # ---------------------------------------------------------
    elif menu == "Gradiente Hidrostático":
        st.markdown("#### Gradiente de Presión por Densidad")
        st.latex(r"\text{Gradiente (psi/ft)} = 0.433 \times \gamma_{\text{fluido}} \text{ (sg)}")

        densidad = st.number_input("Densidad Relativa del Fluido (sg) [Agua = 1.0]", min_value=0.0, value=1.0, step=0.05)

        if st.button("Calcular Gradiente", use_container_width=True):
            gradiente = 0.433 * densidad
            st.metric("Gradiente Hidrostático", f"{round(gradiente, 3)} psi/ft")

    # ---------------------------------------------------------
    # PRODUCCIÓN BOMBEO MECÁNICO (AIB)
    # ---------------------------------------------------------
    elif menu == "Producción Teórica Bombeo Mecánico (AIB)":
        st.markdown("#### Ecuación de Rendimiento de Bombeo Mecánico")
        st.latex(r"Q_{\text{teor}} = 0.1166 \times D^2 \times S \times N \times \eta")

        col1, col2 = st.columns(2)
        with col1:
            diametro = st.number_input("Diámetro del Pistón [pulgadas]", min_value=0.5, value=1.5, step=0.25)
            carrera = st.number_input("Longitud de Carrera (S) [pulgadas]", min_value=0.0, value=80.0, step=5.0)
        with col2:
            spm = st.number_input("Velocidad de Bombeo (N) [SPM / Golpes por min]", min_value=0.0, value=8.0, step=1.0)
            eficiencia = st.number_input("Eficiencia Volumétrica ($\eta$) [%]", min_value=0.0, max_value=100.0, value=75.0, step=5.0)

        if st.button("Calcular Producción AIB", use_container_width=True):
            q_teorica = 0.1166 * (diametro ** 2) * carrera * spm * (eficiencia / 100.0)
            st.metric("Producción Estimada Real", f"{round(q_teorica, 1)} BPD")

    # ---------------------------------------------------------
    # BOMBEO ELECTROSUMERGIBLE (BES)
    # ---------------------------------------------------------
    elif menu == "Producción por Bombeo Electrosumergible (BES)":
        st.markdown("#### Estimación de Frecuencia vs Caudal BES")
        st.write("La tasa de flujo en una bomba BES varía linealmente con la frecuencia eléctrica (Hz).")
        st.latex(r"Q_{\text{actual}} = Q_{\text{diseño}} \times \left( \frac{f_{\text{actual}}}{f_{\text{diseño}}} \right) \times \eta")

        col1, col2 = st.columns(2)
        with col1:
            q_diseno = st.number_input("Caudal nominal a 50 Hz [BPD]", min_value=0.0, value=1000.0, step=100.0)
            f_actual = st.number_input("Frecuencia actual del Variador (VSD) [Hz]", min_value=30.0, max_value=70.0, value=45.0, step=1.0)
        with col2:
            f_diseno = st.number_input("Frecuencia de diseño base [Hz]", min_value=50.0, max_value=60.0, value=50.0, step=10.0)
            eficiencia = st.number_input("Eficiencia de las etapas de la bomba [%]", min_value=0.0, max_value=100.0, value=85.0, step=5.0)

        if st.button("Calcular Producción BES", use_container_width=True):
            q_bes = q_diseno * (f_actual / f_diseno) * (eficiencia / 100.0)
            st.metric("Producción Estimada BES", f"{round(q_bes, 1)} BPD")

    # ---------------------------------------------------------
    # BOMBEO POR CAVIDADES PROGRESIVAS (PCP)
    # ---------------------------------------------------------
    elif menu == "Producción por Cavidades Progresivas (PCP)":
        st.markdown("#### Ecuación Volumétrica de Bomba PCP")
        st.latex(r"Q_{\text{teor}} = \Delta V \times N \times 0.00905 \times \eta")
        st.caption("Donde $\Delta V$ es el desplazamiento de la bomba (cm³/rev) y $N$ son las RPM del cabezal.")

        col1, col2 = st.columns(2)
        with col1:
            desplazamiento = st.number_input("Desplazamiento de la bomba [cm³/rev]", min_value=0.0, value=120.0, step=10.0)
            rpm = st.number_input("Velocidad de giro del Cabezal [RPM]", min_value=0.0, value=250.0, step=10.0)
        with col2:
            eficiencia = st.number_input("Eficiencia Volumétrica (pérdida por slip) [%]", min_value=0.0, max_value=100.0, value=80.0, step=5.0)

        if st.button("Calcular Producción PCP", use_container_width=True):
            # Conversión cinemática estándar de cm3/rev y RPM a BPD:
            q_pcp = desplazamiento * rpm * 0.00905 * (eficiencia / 100.0)
            st.metric("Producción Estimada PCP", f"{round(q_pcp, 1)} BPD")

    # ---------------------------------------------------------
    # GAS LIFT
    # ---------------------------------------------------------
    elif menu == "Inyección de Gas Lift (Cálculo de Tasa)":
        st.markdown("#### Relación de Inyección de Gas (GLR Mínima Requerida)")
        st.latex(r"Q_{\text{gas requerido}} = Q_{\text{fluido}} \times GLR_{\text{objetivo}}")

        col1, col2 = st.columns(2)
        with col1:
            q_fluido = st.number_input("Producción total de líquido esperada [BPD]", min_value=0.0, value=600.0, step=50.0)
        with col2:
            glr_target = st.number_input("GLR Objetivo de Inyección [SCF/STB]", min_value=0.0, value=400.0, step=50.0)

        if st.button("Calcular Requerimiento de Gas", use_container_width=True):
            total_gas_scf = q_fluido * glr_target
            total_gas_m3 = total_gas_scf * 0.0283168 # Conversión a m3 standard
            
            st.metric("Volumen de Inyección Diario", f"{round(total_gas_m3, 1)} std m³/d", 
                      delta=f"{round(total_gas_scf, 0):,.0f} SCF/d")
