import streamlit as st
import pandas as pd

def protocolos_intervencion():
    st.header("🛠️ Protocolos de Intervención (Clase 12)")
    st.info("Operaciones con Tubing, Herramientas de Izaje y Pesca")

    tab1, tab2, tab3 = st.tabs(["🌊 Ahogue de Pozo", "🔧 Herramientas Manuales", "🎣 Maniobras de Pesca"])

    with tab1:
        st.subheader("Protocolo de Ahogue (Kill Procedure)")
        st.write("Según la Clase 12, el procedimiento debe ser ininterrumpido:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Pasos Operativos:**
            1. Mantener tubing conectado a línea para conservar contrapresión.
            2. Conectar bomba en el **casing** (entre columnas).
            3. Iniciar bombeo al máximo caudal sin exceder **1.000 psi**.
            4. Controlar manómetros en salida (tbg) y bomba.
            """)
        
        with col2:
            st.markdown("### 🧮 Cálculo de Volumen")
            st.latex(r"Vol = Vol_{tbg} + Vol_{csg} + 3m^3")
            st.caption("Nota: Se agregan 3m³ adicionales tras ver retorno por el tubing.")
            st.warning("⚠️ Esperar 5 minutos tras el bombeo para verificar el ahogue.")

    with tab2:
        st.subheader("Inspección de Herramientas de Pulling")
        st.markdown("*(Ref: Herramientas Manuales y de Izaje - Clase 12)*")
        
        herramientas = {
            "Elemento": ["Llave Stillson", "Llave de Golpe", "Elevadores", "BOP / Ratigan"],
            "Especificación Técnica": [
                "Longitudes de 14, 18, 24, 36 y 48''. Prohibidas para tubing en boca de pozo.",
                "Para torque en bridas. Verificar estado de caras de impacto.",
                "Verificar seguros, pernos y estado de las amelas.",
                "Cierre hermético obligatorio para cambio de empaquetaduras."
            ]
        }
        st.table(pd.DataFrame(herramientas))

    with tab3:
        st.subheader("Programas de Pesca (1er y 2do Caso)")
        st.markdown("""
        **Puntos Críticos de tus Programas de Pozo:**
        - **Vástago Cortado:** Verificar peso con el *Martin Decker*. Si el peso es total, desclavar bomba.
        - **Pesca de Varilla:** Sacar en **tiros dobles** revisando material y colocar en caballetes.
        - **Finalización:** Probar hermeticidad sobre bomba y realizar prueba de bloqueo.
        """)

    # Bot Guía contextualizado
    st.divider()
    st.markdown("🤖 **Asistente Técnico:** Recordá que según la Clase 12, las llaves Stillson deben estar consignadas y el encargado de turno es el único que autoriza su uso previo chequeo de mordazas.")
