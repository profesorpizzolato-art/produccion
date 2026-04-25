import streamlit as st
import time

def mostrar_entrenamiento():
    st.header("🎯 Centro de Entrenamiento Operativo")
    st.write("Simulación de escenarios críticos y toma de decisiones en tiempo real.")

    # --- SELECTOR DE ESCENARIO ÚNICO ---
    opciones = [
        "---", 
        "🚨 Falla de Presión en Manifold", 
        "🔥 Baja Eficiencia en Separación", 
        "🛡️ Seguridad: Prensaestopas (AIB)",
        "💧 Fugas: Integridad en Líneas de Flujo",
        "⚙️ Operativa: Cambio de pozo a Control",
        "🔊 Diagnóstico: Cavitación en Bomba B-201",
        "🧪 Química: Emulsión Crítica (Pad de Tanques)",
        "💨 Gas Lift: Inestabilidad de Flujo", # Agregué la coma que faltaba
        "🔥 Operación: Encendido de Calentador E-102",      
        "🧼 Mantenimiento: Cambio de Filtro de Entrada",  
        "⚡ Recuperación: Arranque de Pozo (Post-Corte)"
    ]
    
    seleccion = st.selectbox("Seleccione el escenario de entrenamiento:", opciones)

    if seleccion == "---":
        st.info("Seleccione un escenario para comenzar la simulación práctica.")
    
    # --- ESCENARIO 1: FALLA DE PRESIÓN ---
    elif seleccion == "🚨 Falla de Presión en Manifold":
        st.subheader("Escenario: Alarma PSH-105 Activa")
        st.warning("El SCADA reporta 165 psi en la línea de entrada. El valor máximo es 150 psi.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Datos de Campo:**")
            st.write("- Pozo MENFA-001: Operando a 1200 RPM")
            st.write("- Válvula SDV-101: Abierta")
        
        opcion_p = st.radio("¿Qué acción operativa toma de inmediato?", [
            "Aumentar la temperatura del calentador",
            "Cerrar válvula de entrada y verificar presión",
            "Ignorar la alarma, puede ser un error del sensor",
            "Activar protocolo ESD (Parada de Emergencia)"
        ])

        if st.button("Ejecutar Acción"):
            if opcion_p == "Activar protocolo ESD (Parada de Emergencia)":
                st.success("✅ CORRECTO. Ante una sobrepresión no controlada, la seguridad de la planta es prioridad.")
                st.balloons()
            else:
                st.error("❌ INCORRECTO. Esa acción no mitiga el riesgo de ruptura de línea.")

    # --- ESCENARIO 2: EFICIENCIA ---
    elif seleccion == "🔥 Baja Eficiencia en Separación":
        st.subheader("Escenario: Crudo Fuera de Especificación")
        st.write("El laboratorio reporta un **BSW de 5%** en el tanque de despacho. El máximo permitido es 1%.")
        
        temp_actual = st.slider("Ajustar Temperatura del Calentador E-01 (°C):", 40, 95, 45)
        
        if st.button("Verificar Resultados"):
            if temp_actual >= 65:
                st.success(f"✅ EFICIENTE. A {temp_actual}°C la viscosidad bajó lo suficiente para separar el agua. BSW actual: 0.8%")
            else:
                st.error(f"⚠️ INSUFICIENTE. A {temp_actual}°C el agua sigue emulsionada. BSW actual: 3.5%")

    # --- ESCENARIO 3: PRENSAESTOPAS ---
    elif seleccion == "🛡️ Seguridad: Prensaestopas (AIB)":
        st.subheader("Situación: Fuga en Boca de Pozo")
        st.image("https://img.freepik.com/fotos-premium/primer-plano-fuga-aceite-valvula-tuberias-industriales_1253456-4258.jpg", caption="Inspección visual de fugas")
        st.warning("⚠️ Detectás un goteo constante en el prensaestopas y el vástago pulido levanta temperatura.")
        
        opcion_s = st.radio("¿Qué acción de seguridad aplicás?", [
            "Apretar las tuercas del prensaestopas al máximo rápidamente",
            "Lubricar el vástago y realizar un ajuste gradual verificando alineación",
            "Parar el equipo y esperar al equipo de mantenimiento de superficie"
        ], key="radio_aib")
        
        if st.button("Validar Maniobra"):
            if "gradual" in opcion_s:
                st.success("✅ ¡Correcto! Evitaste que se quemen las empaquetaduras y controlaste la fuga.")
            else:
                st.error("❌ Incorrecto. Un ajuste brusco sin lubricación dañará definitivamente el sello.")

    # --- ESCENARIO 4: FUGAS ---
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

    # --- ESCENARIO 5: MANIOBRA VÁLVULAS ---
    elif seleccion == "⚙️ Operativa: Cambio de pozo a Control":
        st.subheader("Situación: Maniobra en Manifold")
        st.write("Debés pasar un pozo de la Línea de Grupo a la Línea de Control para un ensayo.")
        
        maniobra = st.selectbox("¿Cuál es la secuencia correcta de apertura/cierre?", [
            "Seleccionar...",
            "Cerrar válvula de Grupo y luego abrir la de Control",
            "Abrir válvula de Control y luego cerrar la de Grupo",
            "Cerrar ambas y esperar 5 minutos para despresurizar"
        ])
        
        if st.button("Realizar Maniobra"):
            if "Abrir válvula de Control" in maniobra:
                st.success("✅ ¡Excelente! Seguiste la regla de 'Abrir primero, cerrar después' evitando el Golpe de Ariete.")
            else:
                st.error("❌ ¡Peligro! Generaste un pico de presión que puede dañar la empaquetadura del pozo.")

    # --- ESCENARIO 6: CAVITACIÓN ---
    elif seleccion == "🔊 Diagnóstico: Cavitación en Bomba B-201":
        st.subheader("Escenario: Ruidos anormales en Planta de Inyección")
        st.warning("La bomba emite un sonido similar a 'bombear piedras' y vibra intensamente.")
        
        causa = st.radio("¿Diagnóstico y acción inmediata?", [
            "Alta presión en la descarga - Abrir válvula de alivio",
            "Baja presión en la succión (Cavitación) - Limpiar filtro de entrada",
            "Falla de rodamientos - Engrasar",
            "Aire en la línea - Purgar"
        ])
        
        if st.button("Confirmar Diagnóstico"):
            if "Cavitación" in causa:
                st.success("✅ ¡Correcto! La caída de presión en succión genera burbujas de vapor que dañan el impulsor.")
            else:
                st.error("❌ Incorrecto. Ese sonido es cavitación por falta de NPSH.")

    # --- ESCENARIO 7: QUÍMICA ---
    elif seleccion == "🧪 Química: Emulsión Crítica (Pad de Tanques)":
        st.subheader("Situación: El crudo no separa a pesar de la temperatura")
        st.info("Calentador a 75°C, pero el BSW sigue en 4%.")
        
        accion_quimica = st.selectbox("¿Qué ajuste realizas?", [
            "Seleccionar...",
            "Aumentar la inyección de desemulsionante",
            "Bajar la temperatura",
            "Aumentar el tiempo de residencia"
        ])
        
        if st.button("Aplicar Cambio"):
            if "desemulsionante" in accion_quimica:
                st.success("✅ Correcto. Un ajuste en las ppm de química es la clave cuando el calor no basta.")
            else:
                st.error("❌ Fallaste. Bajar la temperatura empeorará la separación.")

    # --- ESCENARIO 8: GAS LIFT ---
    elif seleccion == "💨 Gas Lift: Inestabilidad de Flujo":
        st.subheader("Situación: Pozo con Flujo Intermitente (Slugging)")
        st.write("La presión de inyección oscila y el pozo entrega 'burbujones'.")
        
        maniobra_gas = st.radio("¿Cómo estabilizas el pozo?", [
            "Cerrar la inyección de gas",
            "Incrementar la presión de inyección gradualmente",
            "Abrir el pozo a la atmósfera",
            "Reducir el orificio de producción"
        ])
        
        if st.button("Estabilizar"):
            if "Incrementar" in maniobra_gas:
                st.success("✅ ¡Muy bien! Barriste el líquido acumulado hacia un flujo continuo.")
            else:
                st.error("❌ Error operativo. Cerrar el gas podría ahogar el pozo.")

    # --- ESCENARIO 9: CALENTADOR ---
    elif seleccion == "🔥 Operación: Encendido de Calentador E-102":
        st.subheader("Maniobra: Puesta en servicio de Calentador")
        st.info("Iniciando ciclo de encendido post-mantenimiento.")
        
        paso_cal = st.radio("¿Paso crítico antes del piloto?", [
            "Abrir gas principal",
            "Realizar el barrido de aire (Purge) de la cámara",
            "Aumentar temperatura",
            "Cerrar chimenea"
        ])
        
        if st.button("Iniciar"):
            if "barrido" in paso_cal:
                st.success("✅ ¡Correcto! Barrido finalizado (Pre-purge). Área segura.")
            else:
                st.error("❌ ¡PELIGRO! Explosión por acumulación de gases remanentes.")

    # --- ESCENARIO 10: FILTROS ---
    elif seleccion == "🧼 Mantenimiento: Cambio de Filtro de Entrada":
        st.subheader("Maniobra: Limpieza de Filtro Dúplex")
        st.warning("Diferencial alto en filtro A. Pasar a filtro B.")
        
        secuencia_f = st.selectbox("¿Secuencia segura?", [
            "Seleccionar...",
            "Cerrar A y abrir B",
            "Abrir válvula de equilibrio, llenar B, abrir B y cerrar A",
            "Abrir B y dejar ambos abiertos"
        ])
        
        if st.button("Ejecutar"):
            if "equilibrio" in secuencia_f:
                st.success("✅ ¡Impecable! Sin golpe de presión ni entrada de aire al sistema.")
            else:
                st.error("❌ Incorrecto. Podés disparar una parada de planta por transitorio de presión.")

    # --- ESCENARIO 11: ARRANQUE POST-CORTE ---
    elif seleccion == "⚡ Recuperación: Arranque de Pozo (Post-Corte)":
        st.subheader("Maniobra: Arranque de AIB post-falla eléctrica")
        st.write("Pozo parado 4 horas, fluido frío.")
        
        accion_aib = st.radio("¿Cómo arrancás?", [
            "Arranque directo",
            "Verificar aceite, giros breves/intermitentes y bypass",
            "Abrir purga al suelo"
        ])
        
        if st.button("Normalizar"):
            if "breves" in accion_aib:
                st.success("✅ ¡Excelente! Evitaste el corte del vástago por carga estática.")
            else:
                st.error("❌ ¡Peligro! Esfuerzo excesivo en los pernos y el vástago.")

    st.divider()
    st.caption("⏱️ IPCL MENFA - Entrenamiento Operativo Avanzado")
