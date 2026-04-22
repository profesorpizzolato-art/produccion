import streamlit as st

def seguridad_y_checklist():
    st.header("🛡️ Control de Seguridad y Medio Ambiente")
    st.subheader("Checklist Obligatorio de Pre-Operación")

    st.warning("De acuerdo a los Programas de Pulling (Casos 1 y 2), debe verificar la locación antes de intervenir.")

    with st.container(border=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏗️ Estado del Equipo")
            c1 = st.checkbox("Charla de seguridad y medio ambiente realizada")
            c2 = st.checkbox("Verificación de estado de boca de pozo")
            c3 = st.checkbox("Descompresión a pileta verificada")
            c4 = st.checkbox("Equipo de Pulling/Guinche correctamente montado")

        with col2:
            st.markdown("### 🧤 Elementos de Protección")
            c5 = st.checkbox("EPP Completo (Casco, calzado, guantes, protección visual)")
            c6 = st.checkbox("BOP de varillas instalado y operativo")
            c7 = st.checkbox("Herramientas manuales inspeccionadas (Stillson, llaves de golpe)")
            c8 = st.checkbox("Extintores y kit de derrames en posición")

    # Lógica de validación
    total_checks = sum([c1, c2, c3, c4, c5, c6, c7, c8])
    
    if total_checks < 8:
        st.error(f"Faltan {8 - total_checks} puntos de seguridad por verificar. El simulador permanece bloqueado.")
        st.session_state.seguridad_aprobada = False
    else:
        st.success("✅ Protocolo de seguridad completado. Sistema habilitado para operación.")
        st.session_state.seguridad_aprobada = True
        if st.button("ACCEDER AL SIMULADOR DE PRODUCCIÓN"):
            st.session_state.modulo = "dashboard"
            st.rerun()
