import streamlit as st

def instrucciones_simulador():

    st.title("Manual de Uso del Simulador MENFA")

    st.markdown("---")

    st.header("Objetivo del Simulador")

    st.write("""
Este simulador fue diseñado para entrenamiento en operaciones de producción petrolera.

Permite al usuario comprender el comportamiento operativo de:

• Pozos productores  
• Sistemas de flujo  
• Planta de separación  
• Variables de producción  
• Ingeniería de producción
""")

    st.markdown("---")

    st.header("Cómo usar el simulador")

    st.write("""
1. Ingresar al módulo Pozo Productor.
2. Ajustar las variables de presión y temperatura.
3. Observar la producción estimada.
4. Analizar el comportamiento del sistema en el módulo SCADA.
5. Revisar el diagrama de flujo de la planta.
6. Utilizar las fórmulas para validar cálculos.
""")

    st.markdown("---")

    st.header("Ejercicios de entrenamiento")

    st.subheader("Ejercicio 1")

    st.write("""
El pozo presenta las siguientes condiciones:

Presión de reservorio: 3000 psi  
Presión fondo fluyente: 1200 psi  

Pregunta:

Calcule el Índice de Productividad (PI).
""")

    respuesta1 = st.number_input("Respuesta PI")

    if st.button("Verificar ejercicio 1"):

        if 0.4 < respuesta1 < 0.9:
            st.success("Respuesta correcta aproximada")
        else:
            st.error("Revisar cálculo")

    st.markdown("---")

    st.subheader("Ejercicio 2")

    st.write("""
Producción total: 1000 BPD  
Producción de agua: 300 BPD  

Pregunta:

Calcular el corte de agua.
""")

    respuesta2 = st.number_input("Respuesta Corte Agua (%)")

    if st.button("Verificar ejercicio 2"):

        if 28 < respuesta2 < 32:
            st.success("Correcto")
        else:
            st.error("Revisar cálculo")

    st.markdown("---")

    st.info("Estos ejercicios permiten entrenar el análisis operativo de producción.")
