import streamlit as st
import random

def mostrar_troubleshooting():
    st.subheader("🧠 Entrenamiento de Criterio Operativo")
    st.write("Analice los síntomas y determine la causa raíz de la falla.")

    escenarios = [
        {
            "sintoma": "Presión del Separador sube rápido, LSH (Nivel Alto) activado, pero el flujo de gas en el puente marca cero.",
            "opciones": ["Válvula de control de gas trabada cerrada", "Rotura de línea de crudo", "Falla en el suministro eléctrico"],
            "correcta": "Válvula de control de gas trabada cerrada",
            "explicacion": "Al no poder salir el gas, la presión aumenta y 'empuja' el líquido hacia abajo o bloquea el ingreso, activando alarmas por contrapresión."
        },
        {
            "sintoma": "El Monitor de BSW de la Unidad LACT marca 5% constante y la válvula de 3 vías deriva a tanque de reproceso.",
            "opciones": ["Falla en el químico demulsificante", "Gas en la línea de petróleo", "Bomba de transferencia rota"],
            "correcta": "Falla en el químico demulsificante",
            "explicacion": "Un BSW alto indica que la separación agua/petróleo no es efectiva, probablemente por falta de tratamiento químico o bajo tiempo de residencia."
        }
    ]

    if "escenario_actual" not in st.session_state:
        st.session_state.escenario_actual = random.choice(escenarios)

    sc = st.session_state.escenario_actual
    st.warning(f"⚠️ **SÍNTOMA:** {sc['sintoma']}")
    
    respuesta = st.radio("¿Cuál es su diagnóstico?", sc['opciones'])
    
    if st.button("Validar Diagnóstico"):
        if respuesta == sc['correcta']:
            st.success(f"✅ ¡Correcto! {sc['explicacion']}")
            if st.button("Siguiente Desafío"):
                del st.session_state.escenario_actual
                st.rerun()
        else:
            st.error("❌ Diagnóstico errado. Revise las presiones y el flujo del proceso.")
