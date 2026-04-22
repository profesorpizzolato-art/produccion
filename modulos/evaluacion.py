import streamlit as st

def evaluacion():

    st.title("Evaluación Producción Petrolera")

    pregunta = st.radio(
        "¿Cuál es la función del separador?",
        [
            "Separar fases",
            "Aumentar presión",
            "Reducir viscosidad"
        ]
    )

    if st.button("Responder"):

        if pregunta == "Separar fases":
            st.success("Correcto")
        else:
            st.error("Incorrecto")

    pregunta = st.radio(
        "¿Qué indica alta presión en cabeza de pozo?",
        ["Operación normal", "Riesgo de surgencia", "Bajo caudal"]
    )

    if st.button("Responder"):
        if pregunta == "Riesgo de surgencia":
            st.success("Correcto")
        else:
            st.error("Incorrecto")
