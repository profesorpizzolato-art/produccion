import streamlit as st

def render_pozo():
    st.title("🛢️ Operaciones de Pozo - MENFA-02")
    motor = st.session_state.motor
    
    # El alumno modifica el estrangulador
    nuevo_choke = st.slider("Apertura de Choke (%)", 0.0, 100.0, float(motor.estado["pozo"]["choke_pct"]))
    
    # Impacto inmediato en el motor técnico
    if nuevo_choke != motor.estado["pozo"]["choke_pct"]:
        motor.ajustar_choke(nuevo_choke)
        st.success(f"Choke ajustado a {nuevo_choke}%")
        
    # Mostrar datos calculados en tiempo real por el motor
    st.metric("Caudal Bruto actual", f"{motor.estado['pozo']['caudal_bruto']:.2f} bbl/d")
