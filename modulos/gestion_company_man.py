import streamlit as st
import pandas as pd

def gestion_company_man():
    st.header("🛠️ Gestión del Company Man (Operaciones)")
    st.subheader("Seguridad en Boca de Pozo y Control de Maniobras")

    tab1, tab2 = st.tabs(["📋 Control de Herramientas", "🏗️ Maniobra de Pesca"])

    with tab1:
        st.markdown("### Verificación de Herramientas (Clase 12)")
        st.write("Antes de iniciar, verifique el estado de las herramientas manuales:")
        
        datos = {
            "Herramienta": ["Llave Stillson", "Llave de Golpe", "Elevadores", "BOP / Ratigan"],
            "Estado": ["Revisar Mordazas", "Verificar Caras", "Seguros de Amelas", "Cierre Hermético"]
        }
        st.table(pd.DataFrame(datos))
        st.caption("⚠️ Prohibido usar Stillson en tubing en boca de pozo (Clase 12).")

    with tab2:
        st.markdown("### Programa de Pozo (Pesca de Vástago)")
        st.markdown("""
        1. **Verificar boca de pozo:** Descomprimir a pileta.
        2. **Montar equipo:** Realizar charla de seguridad.
        3. **Constatar peso:** Usar el *Martin Decker*.
        4. **Acción:** Si el peso es total, proceder a desclavar bomba.
        """)
        if st.button("INICIAR REGISTRO DE MANIOBRA"):
            st.toast("Maniobra iniciada bajo supervisión del Company Man")
