import streamlit as st

def evaluacion():
    st.header("🧠 Evaluación de Competencias Operativas")
    st.write("Examen técnico para la certificación en Operaciones de Campo y Planta.")

    # --- 1. DATOS DEL ALUMNO ---
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre Completo del Alumno:")
        with col2:
            dni = st.text_input("DNI:")

    # --- 2. EXAMEN (Banco de Preguntas) ---
    st.divider()
    score = 0

    # Pregunta 1
    st.markdown("### 1. Sistema de Extracción")
    p1 = st.radio(
        "Si observamos que un pozo tiene un **AIB (Aparato Independiente de Bombeo)**, ¿a qué sistema de extracción pertenece?",
        ["Surgencia Natural", "Bombeo Mecánico", "Bombeo Electrosumergible (ESP)", "Plunger Lift"],
        index=None
    )
    if p1 == "Bombeo Mecánico": score += 25

    # Pregunta 2
    st.markdown("### 2. Control de Planta")
    p2 = st.radio(
        "¿Cuál es el objetivo principal del Separador Trifásico en la PTC?",
        ["Aumentar la presión del gas", "Separar el gas, el crudo y el agua de formación", "Calentar el petróleo para reducir viscosidad"],
        index=None
    )
    if p2 == "Separar el gas, el crudo y el agua de formación": score += 25

    # Pregunta 3
    st.markdown("### 3. Ingeniería y Producción")
    p3 = st.radio(
        "En el análisis nodal, si la curva VLP se desplaza hacia arriba (aumento de contrapresión), ¿qué sucede con el caudal de producción?",
        ["El caudal aumenta", "El caudal disminuye", "El caudal se mantiene constante"],
        index=None
    )
    if p3 == "El caudal disminuye": score += 25

    # Pregunta 4
    st.markdown("### 4. Seguridad Operativa")
    p4 = st.radio(
        "¿Qué significan las siglas **ESD** en una sala de control de planta?",
        ["Electric System Data", "Emergency Shutdown (Parada de Emergencia)", "Every Single Day"],
        index=None
    )
    if p4 == "Emergency Shutdown (Parada de Emergencia)": score += 25

    # --- 3. RESULTADOS ---
    st.divider()
    if st.button("Finalizar y Calificar", use_container_width=True):
        if not nombre or not dni:
            st.error("Por favor, ingrese sus datos antes de calificar.")
        else:
            st.subheader(f"Resultado para {nombre}")
            if score >= 75:
                st.balloons()
                st.success(f"✅ APROBADO - Calificación: {score}/100")
                st.info("Puede solicitar su certificado de asistencia a Menfa Capacitaciones.")
            else:
                st.error(f"❌ REPROBADO - Calificación: {score}/100")
                st.warning("Se recomienda repasar los módulos de Planta e Ingeniería.")
            
            # Opción para "Imprimir" o guardar
            st.button("Descargar Reporte de Examen (PDF)", disabled=True)
            st.caption("Función de exportación PDF disponible en la versión Pro.")
