import streamlit as st
from modulos.banco_preguntas import CUESTIONARIO_PRODUCCION

def evaluacion():
    st.header("📝 Evaluación de Competencias - IPCL MENFA")
    st.write("Instructor: Fabricio Pizzolato")
    
    if not CUESTIONARIO_PRODUCCION:
        st.warning("El banco de preguntas está vacío.")
        return

    for i, item in enumerate(CUESTIONARIO_PRODUCCION):
        st.subheader(f"Pregunta {i+1}")
        
        # Widget de opción múltiple
        respuesta = st.radio(
            item["pregunta"],
            item["opciones"],
            key=f"preg_{i}"
        )
        
        # Botón de validación individual
        if st.button("Validar Respuesta", key=f"btn_{i}"):
            indice_correcto = item["respuesta"]
            texto_correcto = item["opciones"][indice_correcto]
            
            if respuesta == texto_correcto:
                st.success("✅ ¡Correcto!")
            else:
                st.error(f"❌ Incorrecto. La respuesta técnica es: {texto_correcto}")
        st.divider()

# Si tienes código suelto al final del archivo, asegúrate de borrarlo
# o de que esté pegado al margen izquierdo.
