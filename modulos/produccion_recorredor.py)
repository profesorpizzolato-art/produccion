import streamlit as st
import pandas as pd
import time

def mostrar_modulo_produccion():
    st.title("🏭 Módulo de Producción Petrolera y Tareas del Recorredor")
    st.caption("Software de Simulación y Capacitación - IPCL MENFA")

    # Pestañas del módulo basándonos en el manual técnico
    tab1, tab2, tab3 = st.tabs([
        "🌿 Proceso en Batería y Recorrida", 
        "🤖 Simulación de Señales SCADA (4-20mA)", 
        "📋 Evaluación de Seguridad y Operación"
    ])

    # ==========================================
    # PESTAÑA 1: PROCESO Y RECORRIDA
    # ==========================================
    with tab1:
        st.header("Flujo del Fluido y Operaciones en Batería")
        st.write(
            "La función principal de una batería es reunir la producción de un grupo de pozos "
            "para separar el gas, el agua y el petróleo, además de almacenar y medir caudales[cite: 1, 11, 12]."
        )
        
        # Simulación visual del Manifold de ingreso
        st.subheader("🎛️ Operación del Manifold de Ingreso (Colector)")
        st.info(
            "**Regla Operativa:** La apertura y cierre de válvulas debe practicarse de forma "
            "simultánea (abrir primero, luego cerrar) de manera gradual para evitar golpes de ariete[cite: 130]."
        )
        
        pozo_seleccionado = st.selectbox("Seleccionar Pozo para Ensayar:", ["Pozo Productor MENFA-01", "Pozo Productor MENFA-02", "Pozo Productor MENFA-03"])
        linea_derivacion = st.radio("Derivar flujo hacia:", ["Línea General (Producción Total) [cite: 131]", "Separador de Ensayo (Control Individual) [cite: 131, 132]"])
        
        if st.button("Ejecutar Maniobra de Válvulas"):
            with st.spinner("Cambiando configuración en el colector..."):
                time.sleep(1.5)
                st.success(f"Maniobra exitosa. El {pozo_seleccionado} ahora está derivado a {linea_derivacion}[cite: 131, 132].")
                st.warning("🔄 Recuerda revisar el circuito de flujo para comprobar la eficacia de la maniobra realizada[cite: 129].")

        st.markdown("---")
        st.subheader("⚙️ Equipos Principales y Línea de Tratamiento")
        
        with st.expander("1. Separadores y Gravitación"):
            st.write("La disociación gas-líquido en el interior del separador se produce principalmente por **efecto de gravitación**, separando los fluidos por diferencia de densidad[cite: 7, 8].")
        
        with st.expander("2. Deshidratación del Gas e Hidratos"):
            st.write("El vapor de agua en el gas disminuye la eficiencia y, en invierno, provoca obstrucciones por congelamiento o formación de **hidratos** (compuestos sólidos con apariencia de hielo)[cite: 202, 203]. Se requiere el uso de torres de absorción a glicol[cite: 19].")

        with st.expander("3. Transferencia de Custodia (Unidad LACT)"):
            st.write("El líquido acondicionado se almacena y transfiere a oleoductos mediante unidades de Transferencia Automática de Producción en Custodia (LACT)[cite: 3].")

    # ==========================================
    # PESTAÑA 2: SIMULACIÓN SCADA
    # ==========================================
    with tab2:
        st.header("Conversión Analógica a Digital (Lógica del PLC/RTU)")
        st.write(
            "Los sistemas SCADA e instrumentos de campo utilizan el estándar industrial de **4-20 miliamperios (mA)** "
            "para transmitir variables físicas de forma eléctrica hacia la RTU o PLC[cite: 26, 45]."
        )
        st.info("💡 **Dato del Manual:** Cuando la variable está en 0, circula un mínimo de 4mA para verificar que el circuito eléctrico esté sano.")

        # Configuración del instrumento simulado
        rango_max_presion = st.number_input("Rango Máximo del Transmisor de Presión (PT) en Kg/cm²:", min_value=1.0, max_value=100.0, value=10.0)
        presion_actual = st.slider("Presión Actual en Campo (Kg/cm²):", min_value=0.0, max_value=float(rango_max_presion), value=float(rango_max_presion*0.4), step=0.1)

        # Cálculos de conversión basados en las fórmulas de cuentas y mA
        # Escala: 0 a Max -> 4mA a 20mA. PLC estándar de 12 bits: 800 a 4000 cuentas
        factor_ma = (presion_actual / rango_max_presion) * 16 + 4
        cuentas_plc = int((presion_actual / rango_max_presion) * (4000 - 800) + 800)

        # Renderizar en tres columnas visuales
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Presión Física", value=f"{presion_actual:.2f} Kg/cm²")
        col2.metric(label="Señal de Corriente", value=f"{factor_ma:.2f} mA")
        col3.metric(label="Cuentas en RTU/PLC", value=f"{cuentas_plc} pts")

        # Gráfico dinámico de simulación de alarma SCADA
        st.subheader("🚨 Lógica de Control de Alarmas (Set Points)")
        set_point_alto = rango_max_presion * 0.8
        
        st.write(f"**Set Point de Alarma Alta:** {set_point_alto:.1f} Kg/cm²")
        
        if presion_actual >= set_point_alto:
            st.error(f"⚠️ CONDICIÓN DE ALARMA: 'Alto Nivel / Presión en Instalación'. Notificando al Servidor SCADA central. Requiere reconocimiento del operador[cite: 42].")
        else:
            st.success("🟢 Operación normal de campo. Variables dentro de parámetros normales[cite: 43].")

    # ==========================================
    # PESTAÑA 3: EVALUACIÓN DE RECORREDOR
    # ==========================================
    with tab3:
        st.header("Examen Técnico de Normas Operativas y de Seguridad")
        st.write("Test de evaluación para personal ingresante y técnicos de producción.")

        puntaje = 0
        
        # Pregunta 1
        p1 = st.radio(
            "1. ¿Qué se deduce si un instrumento de campo reporta una corriente de 0 mA de forma lineal?",
            ["Que la variable medida está exactamente en cero.", 
             "Que existe una anomalía o rotura en el circuito eléctrico (ya que el cero equivale a 4mA)[cite: 52, 53].", 
             "Que el PLC está saturado."]
        )
        if p1 == "Que existe una anomalía o rotura en el circuito eléctrico (ya que el cero equivale a 4mA)[cite: 52, 53].":
            puntaje += 1.0

        # Pregunta 2
        p2 = st.radio(
            "2. Ante una duda en la ejecución de una maniobra operativa compleja en los pozos, ¿cuál es la acción correcta?",
            ["Proceder con cautela basándose en la experiencia previa.",
             "Preguntar la cantidad de veces que sea necesario al supervisor, aunque parezca molesto[cite: 162].",
             "Dejar la maniobra pendiente para el cambio de turno."]
        )
        if p2 == "Preguntar la cantidad de veces que sea necesario al supervisor, aunque parezca molesto[cite: 162].":
            puntaje += 1.0

        # Pregunta 3
        p3 = st.radio(
            "3. Si un recorredor presenta fatiga intensa o somnolencia severa durante su turno de conducción, ¿qué indica el procedimiento?",
            ["Consumir café o energizantes y circular a menor velocidad.",
             "Continuar la marcha para no retrasar el parte diario.",
             "Detener la conducción, hablar de forma franca con el supervisor y solicitar el relevo inmediato del día[cite: 166]."]
        )
        if p3 == "Detener la conducción, hablar de forma franca con el supervisor y solicitar el relevo inmediato del día[cite: 166].":
            puntaje += 1.0

        # Botón de evaluar
        if st.button("Calificar Evaluación Técnico-Operativa"):
            porcentaje = (puntaje / 3.0) * 100
            if porcentaje >= 100:
                st.balloons()
                st.success(f"🎯 Calificación: {porcentaje:.1f}%. ¡Aprobado! El alumno incorpora plenamente los procedimientos de seguridad y cultura operativa[cite: 165].")
            else:
                st.warning(f"⚠️ Calificación: {porcentaje:.1f}%. Se sugiere repasar los capítulos de 'Señales Eléctricas' y 'Normas de Seguridad Humana' del manual[cite: 36, 164, 165].")

# Para integrar este script al menú general de la aplicación "Simulador MENFA":
if __name__ == "__main__":
    st.set_page_config(page_title="Simulador de Producción IPCL", layout="wide")
    mostrar_modulo_produccion()
