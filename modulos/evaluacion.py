
import streamlit as st
from modulos.banco_preguntas import CUESTIONARIO_PRODUCCION

def generar_evaluacion():
    st.header("Evaluación Técnica")
    
    # Iteramos sobre los temas del banco de preguntas
    for i, (modulo, datos) in enumerate(CUESTIONARIO_PRODUCCION.items()):
        with st.expander(f"Módulo: {modulo.replace('_', ' ').title()}"):
            
            # Usamos el nombre del modulo e indice para crear IDs únicos
            respuesta = st.radio(
                datos["pregunta"],
                datos["opciones"],
                key=f"radio_{modulo}_{i}"
            )
            
            if st.button("Validar Respuesta", key=f"btn_{modulo}_{i}"):
                if respuesta == datos["correcta"]:
                    st.success("¡Correcto! Conocimiento validado.")
                else:
                    st.error(f"Incorrecto. La respuesta técnica es: {datos['correcta']}")

# Llamada en tu app principal
# generar_evaluacion()
 import streamlit as st

# Aquí iría tu lista de preguntas (o importada desde banco_preguntas)
preguntas = [
    {
        "pregunta": "Función del separador trifásico",
        "opciones": ["Separar petroleo gas agua", "Aumentar presión", "Reducir temperatura"],
        "respuesta": 0 # El índice de la opción correcta
    },
    # Podés seguir agregando más aquí...
]

def evaluacion():
    st.title("📝 Evaluación de Producción")
    
    for i, item in enumerate(preguntas):
        st.subheader(f"Pregunta {i+1}")
        
        # Mostramos la pregunta
        opcion_seleccionada = st.radio(
            item["pregunta"], 
            item["opciones"], 
            key=f"preg_{i}"
        )
        
        if st.button("Validar", key=f"btn_{i}"):
            # Obtenemos el texto de la respuesta correcta usando el índice
            indice_correcto = item["respuesta"]
            texto_correcto = item["opciones"][indice_correcto]
            
            if opcion_seleccionada == texto_correcto:
                st.success("✅ Correcto")
            else:
                st.error(f"❌ Incorrecto. La respuesta era: {texto_correcto}")
        
        st.divider()
