import streamlit as st

def show():
    st.title("🖥️ Monitoreo SCADA y Centro de Alarmas")

    if 'motor' not in st.session_state:
        st.error("⚠️ Motor de simulación no encontrado.")
        return

    motor = st.session_state.motor
    motor.actualizar_ciclo()

    # --- MONITOREO DE VARIABLES PRINCIPALES ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("P-Manifold (Dinamica)", f"{motor.p_manifold} psi", delta=f"{round(motor.p_manifold - 145.0, 1)} psi vs Base")
    c2.metric("P-Separador V-01", f"{motor.presion_v01} psi")
    c3.metric("Temp. Horno (TSH-202)", f"{motor.temp_horno} °C")
    c4.metric("BSW Laboratorio", f"{motor.bsw} %")

    st.divider()

    # --- TABLA INTERACTIVA DE ALARMAS (ACK / CLEAR) ---
    st.subheader("🚨 Panel Interactivo de Alarmas de Planta")
    
    for code, info in motor.alarmas.items():
        col_code, col_desc, col_estado, col_accion = st.columns([1, 2, 1, 1])
        
        col_code.write(f"**{code}** ({info['tag']})")
        col_desc.write(info['descripcion'])
        
        # Formato visual según estado de la alarma
        if info['estado'] == "ACTIVA":
            col_estado.error("🔴 ACTIVA")
            if col_accion.button(f"Reconocer ({code})", key=f"btn_{code}"):
                motor.reconocer_alarma(code)
                st.rerun()
        elif info['estado'] == "ACK":
            col_estado.warning("🟡 ACK (Reconocida)")
            col_accion.info("En Observación")
        else:
            col_estado.success("🟢 CLEAR (Normal)")
            col_accion.write("—")
