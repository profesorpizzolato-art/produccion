import streamlit as st
def dashboard_principal():
    st.title("SIMULADOR OPERATIVO MENFA")
    st.subheader("Centro de Entrenamiento en Producción Petrolera")

    st.markdown("---")

    st.write("Seleccione un módulo")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button("🛢 Pozo Productor"):
            st.session_state.modulo = "pozo"

        if st.button("🏭 SCADA Planta"):
            st.session_state.modulo = "planta"   
            
        if st.button("🗺 Mapa del Campo"):
            st.session_state.modulo = "mapa"    

    with col2:

        if st.button("📊 Diagrama Planta"):
            st.session_state.modulo = "diagrama"

        if st.button("📈 Fórmulas Producción"):
            st.session_state.modulo = "formulas"
            
        if st.button("📉 IPR - VLP"):
            st.session_state.modulo = "ipr"    

    with col3:

        if st.button("🎓 Evaluación"):
            st.session_state.modulo = "evaluacion"
            
        if st.button("📘 Instrucciones"):
            st.session_state.modulo = "manual"
            
        if st.button("⚠ Entrenamiento"):
            st.session_state.modulo = "entrenamiento"
            
        if st.button("🛢 Campo Petrolero"):
            st.session_state.modulo = "campo"

        # Ejemplo de lo que debe ir dentro de dashboard_principal.py
col1, col2, col3 = st.columns(3)

with col1:
  # Ejemplo de lo que debe ir dentro de dashboard_principal.py
     col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏗️ Ir a Planta"):
        st.session_state.modulo = "planta"

with col2:
    if st.button("📡 Monitor SCADA"):
        st.session_state.modulo = "scada"

with col3:
    if st.button("⚙️ Simular Fallas"):
        st.session_state.modulo = "fallas"

with col2:
    if st.button("📡 Monitor SCADA"):
        st.session_state.modulo = "scada"

with col3:
    if st.button("⚙️ Simular Fallas"):
        st.session_state.modulo = "fallas"
import streamlit as st

def dashboard_principal():

    st.title("Centro de Control MENFA")

    st.markdown("### Simulador de Producción Petrolera")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button("🛢 Pozo Productor", use_container_width=True):
            st.session_state.modulo = "pozo"

        if st.button("🗺 Mapa del Campo", use_container_width=True):
            st.session_state.modulo = "mapa"

        if st.button("📊 Campo Petrolero", use_container_width=True):
            st.session_state.modulo = "campo"

    with col2:

        if st.button("🏭 Planta de Proceso", use_container_width=True):
            st.session_state.modulo = "planta"

        if st.button("📈 Ingeniería Producción", use_container_width=True):
            st.session_state.modulo = "ingenieria"

        if st.button("🧮 Fórmulas Petroleras", use_container_width=True):
            st.session_state.modulo = "formulas"

    with col3:

        if st.button("⚠ Entrenamiento", use_container_width=True):
            st.session_state.modulo = "entrenamiento"

        if st.button("📘 Manual Simulador", use_container_width=True):
            st.session_state.modulo = "manual"

        if st.button("📊 Reporte Producción", use_container_width=True):
            st.session_state.modulo = "reporte"

    st.markdown("---")

    st.subheader("Estado General del Campo")

    colA, colB, colC = st.columns(3)

    colA.metric("Producción Total", "1850 BPD")
    colB.metric("Presión Separador", "120 psi")
    colC.metric("Pozos Activos", "6")
