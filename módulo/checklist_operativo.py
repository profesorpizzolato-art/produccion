import streamlit as st

def mostrar_checklist_emergente(titulo_maniobra):
    with st.expander(f"⚠️ PROTOCOLO DE SEGURIDAD: {titulo_maniobra}", expanded=True):
        st.info("Según Clase 11 y 12: Complete los pasos para habilitar comandos.")
        
        col1, col2 = st.columns(2)
        with col1:
            check1 = st.checkbox("Charla de seguridad y medio ambiente realizada (Ref. Clase 11)")
            check2 = st.checkbox("Verificación de presión y descompresión a pileta")
        with col2:
            check3 = st.checkbox("EPP Completo y BOP de varillas inspeccionado")
            check4 = st.checkbox("Área delimitada y kit de derrames en posición")
            
        if check1 and check2 and check3 and check4:
            st.success("✅ Protocolo verificado. Comandos habilitados.")
            return True
        else:
            st.warning("Debe tildar todos los puntos para operar.")
            return False
