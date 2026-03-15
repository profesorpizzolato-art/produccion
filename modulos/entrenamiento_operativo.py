import streamlit as st
import random

def entrenamiento_operativo():

    st.title("Modo Entrenamiento Operativo")
    st.subheader("Simulador MENFA")

    st.markdown("---")

    escenarios = [

        {
            "problema": "Alta presión en separador",
            "opciones": [
                "Abrir válvula de alivio",
                "Aumentar caudal",
                "Cerrar el pozo"
            ],
            "correcta": "Abrir válvula de alivio"
        },

        {
            "problema": "Producción baja en pozo",
            "opciones": [
                "Revisar presión fondo fluyente",
                "Cerrar manifold",
                "Apagar separador"
            ],
            "correcta": "Revisar presión fondo fluyente"
        },

        {
            "problema": "Alto corte de agua",
            "opciones": [
                "Ajustar choke",
                "Cerrar tanque",
                "Aumentar presión en separador"
            ],
            "correcta": "Ajustar choke"
        }

    ]

    escenario = random.choice(escenarios)

    st.warning(f"Escenario: {escenario['problema']}")

    respuesta = st.radio(
        "¿Qué acción tomaría?",
        escenario["opciones"]
    )

    if st.button("Verificar respuesta"):

        if respuesta == escenario["correcta"]:

            st.success("Decisión correcta")

        else:

            st.error("Decisión incorrecta")
