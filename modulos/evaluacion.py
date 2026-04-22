import streamlit as st

def evaluacion():
    st.title("Evaluación Producción Petrolera")

    # PREGUNTA 1
    pregunta1 = st.radio(
        "¿Cuál es la función del separador?",
        [
            "Separar fases",
            "Aumentar presión",
            "Reducir viscosidad"
        ],
        key="p1" # Agregamos una clave única para el radio
    )

    if st.button("Responder", key="btn_p1"): # Clave única para el primer botón
        if pregunta1 == "Separar fases":
            st.success("Correcto")
        else:
            st.error("Incorrecto")

    st.divider() # Un separador visual ayuda en la interfaz

    # PREGUNTA 2
    pregunta2 = st.radio(
        "¿Qué indica alta presión en cabeza de pozo?",
        ["Operación normal", "Riesgo de surgencia", "Bajo caudal"],
        key="p2" # Agregamos una clave única para el radio
    )

    if st.button("Responder", key="btn_p2"): # Clave única para el segundo botón
        if pregunta2 == "Riesgo de surgencia":
            st.success("Correcto")
        else:
            st.error("Incorrecto")
