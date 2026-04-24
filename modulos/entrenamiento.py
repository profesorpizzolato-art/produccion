import streamlit as st
import time

def mostrar_entrenamiento():
    st.header("🎯 Centro de Entrenamiento Operativo")
    st.write("Simulación de escenarios críticos y toma de decisiones en tiempo real.")

    # --- SELECTOR DE ESCENARIO ---
    escenario = st.selectbox(
        "Seleccione el escenario de entrenamiento:",
        ["---", "🚨 Falla de Presión en Manifold", "🔥 Baja Eficiencia en Separación", "🛠️ Parada Programada de Pozo"]
    )

    if escenario == "---":
        st.info("Seleccione un escenario para comenzar la simulación práctica.")
    
    # --- ESCENARIO 1: FALLA DE PRESIÓN ---
    elif escenario == "🚨 Falla de Presión en Manifold":
        st.subheader("Escenario: Alarma PSH-105 Activa")
        st.warning("El SCADA reporta 165 psi en la línea de entrada. El valor máximo es 150 psi.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Datos de Campo:**")
            st.write("- Pozo MENFA-001: Operando a 1200 RPM")
            st.write("- Válvula SDV-101: Abierta")
        
        opcion = st.radio("¿Qué acción operativa toma de inmediato?", [
            "Aumentar la temperatura del calentador",
            "Cerrar válvula de entrada y verificar presión",
            "Ignorar la alarma, puede ser un error del sensor",
            "Activar protocolo ESD (Parada de Emergencia)"
        ])

        if st.button("Ejecutar Acción"):
            if opcion == "Activar protocolo ESD (Parada de Emergencia)":
                st.success("✅ CORRECTO. Ante una sobrepresión no controlada, la seguridad de la planta es prioridad.")
                st.balloons()
            else:
                st.error("❌ INCORRECTO. Esa acción no mitiga el riesgo de ruptura de línea.")

    # --- ESCENARIO 2: EFICIENCIA ---
    elif escenario == "🔥 Baja Eficiencia en Separación":
        st.subheader("Escenario: Crudo Fuera de Especificación")
        st.write("El laboratorio reporta un **BSW de 5%** en el tanque de despacho. El máximo permitido es 1%.")
        
        temp_actual = st.slider("Ajustar Temperatura del Calentador E-01 (°C):", 40, 95, 45)
        
        if st.button("Verificar Resultados"):
            if temp_actual >= 65:
                st.success(f"✅ EFICIENTE. A {temp_actual}°C la viscosidad bajó lo suficiente para separar el agua. BSW actual: 0.8%")
            else:
                st.error(f"⚠️ INSUFICIENTE. A {temp_actual}°C el agua sigue emulsionada. BSW actual: 3.5%")

    # --- SECCIÓN DE CRONÓMETRO ---
    st.divider()
    st.caption("⏱️ El tiempo de respuesta es fundamental en la operación real.")
