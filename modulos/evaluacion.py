import streamlit as st
from modulos.banco_preguntas import CUESTIONARIO_PRODUCCION

def generar_evaluacion():
    st.header("Panel de Evaluación Técnica")
    
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
