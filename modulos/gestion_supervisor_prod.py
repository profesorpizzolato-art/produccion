import streamlit as st

def gestion_supervisor_prod():
    st.title("📋 Gestión del Supervisor - Checklist de Turno")

    if 'motor' not in st.session_state:
        st.error("⚠️ Motor no disponible.")
        return

    motor = st.session_state.motor

    st.subheader("✔️ Validación de Seguridad y Operación de Campo")

    # CHECK 1: PERMISOS DE TRABAJO EN CALIENTE
    motor.permiso_trabajo_caliente = st.checkbox(
        "🔥 Permisos de trabajo en caliente validados y firmados",
        value=motor.permiso_trabajo_caliente
    )

    # CHECK 2: REVISIÓN DE INYECCIÓN QUÍMICA
    motor.revision_quimica = st.checkbox(
        "🧪 Revisión de parámetros de inyección de química en pozo/manifold",
        value=motor.revision_quimica
    )

    st.divider()

    # --- CONTROL DEL HORNO/CALENTADOR (BLOQUEADO SI NO HAY PERMISO) ---
    st.subheader("🔥 Operación de Calentador de Proceso")
    
    if not motor.permiso_trabajo_caliente:
        st.error("🔒 SLIDERS BLOQUEADOS: Se requiere validar 'Permisos de trabajo en caliente' para operar el horno.")
        st.slider("Temperatura Objetivo Horno (°C)", 30.0, 110.0, float(motor.temp_horno), disabled=True)
    else:
        st.success("🔓 Operación del Horno Habilitada")
        motor.temp_horno = st.slider(
            "Temperatura Objetivo Horno (°C)", 
            30.0, 110.0, float(motor.temp_horno), step=0.5
        )

    # ESTADO DE QUÍMICA Y PENALIZACIÓN EN TIEMPO REAL
    if not motor.revision_quimica:
        tiempo_restante = max(0, int(120 - motor.tiempo_sin_quimica))
        if tiempo_restante > 0:
            st.warning(f"⚠️ Alerta: Inyección de química no validada. Penalización de BSW (5.5%) en **{tiempo_restante} segundos**.")
        else:
            st.error("🚨 CRÍTICO: Inyección de química omitida. BSW disparado al 5.5% en Laboratorio por emulsión no tratada.")
