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
    # --- NUEVOS CASOS DE SEGURIDAD OPERATIVA ---

# Ejemplo 1: Seguridad en Boca de Pozo
if seleccion == "🛡️ Seguridad: Prensaestopas (AIB)":
    st.subheader("Situación: Fuga en Boca de Pozo")
    st.image("https://img.freepik.com/fotos-premium/primer-plano-fuga-aceite-valvula-tuberias-industriales_1253456-4258.jpg", caption="Inspección visual de fugas")
    st.warning("⚠️ Detectás un goteo constante en el prensaestopas y el vástago pulido levanta temperatura.")
    
    opcion = st.radio("¿Qué acción de seguridad aplicás?", [
        "Apretar las tuercas del prensaestopas al máximo rápidamente",
        "Lubricar el vástago y realizar un ajuste gradual verificando alineación",
        "Parar el equipo y esperar al equipo de mantenimiento de superficie"
    ])
    
    if st.button("Ejecutar Acción"):
        if "gradual" in opcion:
            st.success("✅ ¡Correcto! Evitaste que se quemen las empaquetaduras y controlaste la fuga.")
        else:
            st.error("❌ Incorrecto. Un ajuste brusco sin lubricación dañará definitivamente el sello.")

# Ejemplo 2: Fugas en Líneas de Flujo
elif seleccion == "💧 Fugas: Integridad en Líneas de Flujo":
    st.subheader("Situación: Caída de Presión en Línea de Conducción")
    st.info("El SCADA reporta una caída de 3 psi. Al recorrer, ves burbujeo y humedad en el terreno.")
    
    pasos = st.multiselect("Seleccioná los pasos en el orden correcto de seguridad:", [
        "Delimitar el área (Zona Caliente)", 
        "Detección de Gases (H2S / Explosividad)", 
        "Colocación de grampa de emergencia",
        "Informar al centro de control"
    ])
    
    if st.button("Validar Protocolo"):
        if len(pasos) > 0 and pasos[0] == "Delimitar el área (Zona Caliente)":
            st.success("✅ Protocolo de seguridad iniciado correctamente.")
        else:
            st.warning("⚠️ Recordá que lo primero siempre es delimitar el área para evitar accidentes.")

# Ejemplo 3: Maniobras de Válvulas
elif seleccion == "⚙️ Operativa: Cambio de pozo a Control":
    st.subheader("Situación: Maniobra en Manifold")
    st.write("Debés pasar un pozo de la Línea de Grupo a la Línea de Control para un ensayo.")
    
    maniobra = st.selectbox("¿Cuál es la secuencia correcta de apertura/cierre?", [
        "Cerrar válvula de Grupo y luego abrir la de Control",
        "Abrir válvula de Control y luego cerrar la de Grupo",
        "Cerrar ambas y esperar 5 minutos para despresurizar"
    ])
    
    if st.button("Realizar Maniobra"):
        if "Abrir válvula de Control" in maniobra:
            st.success("✅ ¡Excelente! Seguiste la regla de 'Abrir primero, cerrar después' evitando el Golpe de Ariete.")
        else:
            st.error("❌ ¡Peligro! Generaste un pico de presión que puede dañar la empaquetadura del pozo.")
    st.divider()
    st.caption("⏱️ El tiempo de respuesta es fundamental en la operación real.")
# --- AGREGAR ESTO AL FINAL DE mostrar_entrenamiento() ---
    st.markdown("---")
    st.subheader("🛡️ Simulacros de Seguridad y Emergencias")
    
    caso = st.selectbox("Seleccioná un escenario de emergencia:", [
        "Seleccionar...",
        "Fuga en Prensaestopas (Boca de Pozo)",
        "Pinche/Fuga en Línea de Flujo",
        "Maniobra de Manifold (Evitar Golpe de Ariete)"
    ])

    if caso == "Fuga en Prensaestopas (Boca de Pozo)":
        st.warning("⚠️ El vástago pulido presenta alta temperatura y goteo constante.")
        accion = st.radio("Acción inmediata:", ["Ajustar a fondo", "Lubricar y ajustar gradual", "Parar pozo"])
        if st.button("Validar Maniobra"):
            if "gradual" in accion: st.success("✅ ¡Impecable! Evitaste daños mayores.")
            else: st.error("❌ Error: Podrías quemar las empaquetaduras.")

    elif caso == "Pinche/Fuga en Línea de Flujo":
        st.info("ℹ️ Detectás burbujeo en el suelo sobre la traza del oleoducto.")
        paso1 = st.checkbox("Delimitar zona y medir gases (H2S/Explosividad)")
        paso2 = st.checkbox("Colocar grampa de emergencia")
        if st.button("Verificar Protocolo"):
            if paso1 and paso2: st.success("✅ Protocolo de Integridad aprobado.")
            else: st.warning("⚠️ Falta asegurar el área antes de reparar.")

    elif caso == "Maniobra de Manifold (Evitar Golpe de Ariete)":
        st.write("Debés pasar el pozo de Grupo a Control.")
        maniobra = st.selectbox("Secuencia:", ["Cerrar-Abrir", "Abrir-Cerrar"])
        if st.button("Ejecutar Cambio"):
            if maniobra == "Abrir-Cerrar": st.success("✅ Correcto: Nunca dejaste el pozo cerrado (sin salida).")
            else: st.error("❌ ¡Peligro! El pico de presión dañó la empaquetadura.")
