import streamlit as st

def protocolos_intervencion():
    st.header("🛠️ Protocolos de Intervención y Pulling")
    
    opcion = st.selectbox("Seleccione el Escenario de Falla:", [
        "Seleccionar...",
        "1ER CASO: Pesca de Vástago Cortado",
        "2DO CASO: Pesca de Varilla de Bombeo",
        "Operación de Ahogue de Pozo",
        "Checklist de Seguridad (Pre-Montaje)"
    ])

    if opcion == "1ER CASO: Pesca de Vástago Cortado":
        st.subheader("📋 Programa Operativo: Vástago Cortado")
        with st.container(border=True):
            st.write("**Pasos Críticos:**")
            st.markdown("""
            1. **Seguridad:** Verificar estado de boca de pozo. Descomprimir a pileta.
            2. **Maniobra:** Preparar pescador. Bajar y realizar pesca de vástago.
            3. **Validación:** Constatar peso de herramienta y recorrido de pistón.
            4. **Cierre:** Clavar bomba en anclaje mecánico y probar hermeticidad.
            """)
            st.info("💡 **Dato Técnico:** El peso total debe coincidir con el peso teórico de las varillas de bombeo.")

    elif opcion == "Operación de Ahogue de Pozo":
        st.subheader("🌊 Protocolo de Ahogue (Kill Procedure)")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Acciones:**")
            st.markdown("- Detener equipo de bombeo.\n- Conectar bomba en el casing.\n- Bombear al máximo caudal sin exceder 1000 psi.")
        with col2:
            st.write("**Cálculo de Volumen:**")
            st.latex(r"Vol_{total} = Vol_{tbg} + Vol_{csg} + 50\%")
            st.caption("Referencia: Clase 12 - Operaciones con Tubing")
