import streamlit as st

def mostrar_checklist_seguridad(modulo_nombre):
    """
    Función de validación basada en la Clase 11 y 12.
    Se asegura de que el alumno cumpla el protocolo antes de operar.
    """
    st.markdown(f"### 🛡️ Protocolo de Seguridad: {modulo_nombre}")
    
    with st.container(border=True):
        st.caption("Referencia: Programa de Mantenimiento de Producción MENFA")
        col1, col2 = st.columns(2)
        
        with col1:
            check1 = st.checkbox("Charla de seguridad y medio ambiente realizada")
            check2 = st.checkbox("Verificación de boca de pozo y descompresión a pileta")
            
        with col2:
            check3 = st.checkbox("Uso de EPP completo y verificación de BOP/Ratigan")
            check4 = st.checkbox("Inspección de herramientas manuales (Stillson/Golpe)")

        if check1 and check2 and check3 and check4:
            st.success("✅ Validación correcta. Acceso habilitado.")
            return True
        else:
            st.warning("🔒 Complete todos los puntos de seguridad para desbloquear los controles.")
            return False
