import streamlit as st
import time

def mostrar_entrenamiento():
    st.header("🎯 Centro de Entrenamiento Operativo")
    st.write("Simulación de escenarios críticos y toma de decisiones en tiempo real.")

    # --- SELECTOR DE ESCENARIO ÚNICO ---
    # He unido todas las opciones en un solo menú para que sea fácil de navegar
   opciones = [
        "---", 
        "🚨 Falla de Presión en Manifold", 
        "🔥 Baja Eficiencia en Separación", 
        "🛡️ Seguridad: Prensaestopas (AIB)",
        "💧 Fugas: Integridad en Líneas de Flujo",
        "⚙️ Operativa: Cambio de pozo a Control",
        "🔊 Diagnóstico: Cavitación en Bomba B-201",
        "🧪 Química: Emulsión Crítica (Pad de Tanques)",
        "💨 Gas Lift: Inestabilidad de Flujo"
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

    st.divider()
    st.caption("⏱️ El tiempo de respuesta es fundamental en la operación real.")

elif seleccion == "🔊 Diagnóstico: Cavitación en Bomba B-201":
        st.subheader("Escenario: Ruidos anormales en Planta de Inyección")
        st.warning("La bomba de inyección de agua de formación emite un sonido similar a 'bombear piedras' y vibra intensamente.")
        
        causa = st.radio("¿Cuál es el diagnóstico probable y la acción inmediata?", [
            "Alta presión en la descarga - Abrir válvula de alivio",
            "Baja presión en la succión (Cavitación) - Limpiar filtro de entrada y verificar nivel de tanque",
            "Falla de rodamientos - Engrasar y seguir operando",
            "Aire en la línea - Purgar la bomba en marcha"
        ])
        
        if st.button("Confirmar Diagnóstico"):
            if "Cavitación" in causa:
                st.success("✅ ¡Correcto! Identificaste el fenómeno de cavitación. La caída de presión en la succión genera burbujas de vapor que dañan el impulsor.")
            else:
                st.error("❌ Incorrecto. Ese sonido es característico de la cavitación por falta de NPSH (carga neta de succión positiva).")

elif seleccion == "🧪 Química: Emulsión Crítica (Pad de Tanques)":
        st.subheader("Situación: El crudo no separa a pesar de la temperatura")
        st.info("Tenés el calentador a 75°C (máximo operativo), pero el BSW sigue en 4%.")
        
        accion_quimica = st.selectbox("¿Qué ajuste realizas en la dosificación?", [
            "Seleccionar...",
            "Aumentar la inyección de desemulsionante y verificar punto de aplicación",
            "Bajar la temperatura para que el agua pese más",
            "Aumentar el tiempo de residencia cerrando la salida de planta"
        ])
        
        if st.button("Aplicar Cambio Químico"):
            if "desemulsionante" in accion_quimica:
                st.success("✅ Correcto. A veces la temperatura sola no rompe la tensión interfacial. Un ajuste en las ppm de química es la clave.")
            else:
                st.error("❌ Fallaste. Bajar la temperatura solo empeorará la viscosidad y el BSW subirá.")

elif seleccion == "💨 Gas Lift: Inestabilidad de Flujo":
        st.subheader("Situación: Pozo MENFA-005 con Flujo Intermitente (Slugging)")
        st.write("La presión de inyección de gas oscila violentamente y el pozo entrega 'burbujones' de crudo.")
        
        maniobra_gas = st.radio("¿Cómo estabilizas el pozo?", [
            "Cerrar la inyección de gas de golpe",
            "Incrementar la presión de inyección de forma gradual para barrer el líquido",
            "Abrir el pozo a la atmósfera (venteo)",
            "Reducir el orificio de la válvula de producción"
        ])
        
        if st.button("Estabilizar Pozo"):
            if "Incrementar" in maniobra_gas:
                st.success("✅ ¡Muy bien! Incrementaste la velocidad de flujo para pasar de flujo intermitente a flujo anular continuo.")
            else:
                st.error("❌ Error operativo. Cerrar el gas de golpe podría 'ahogar' el pozo definitivamente.")

elif seleccion == "🔥 Operación: Encendido de Calentador E-102":
        st.subheader("Maniobra: Puesta en servicio de Calentador de Fuego Directo")
        st.info("El equipo estuvo parado por mantenimiento. Debés iniciar el ciclo de encendido.")
        
        paso = st.radio("¿Cuál es el primer paso crítico antes de encender el piloto?", [
            "Abrir el paso de gas principal",
            "Realizar el barrido de aire (Purge) de la cámara de combustión",
            "Aumentar el setpoint de temperatura",
            "Cerrar la chimenea para conservar calor"
        ])
        
        if st.button("Iniciar Encendido"):
            if "barrido" in paso:
                st.success("✅ ¡Correcto! El barrido elimina gases remanentes evitando una explosión al encender el piloto (Pre-purge).")
            else:
                st.error("❌ ¡PELIGRO! Encender sin barrido previo puede causar una explosión en la cámara por acumulación de gases.")

elif seleccion == "🧼 Mantenimiento: Cambio de Filtro de Entrada":
        st.subheader("Maniobra: Limpieza de Filtro Dúplex en Operación")
        st.warning("El diferencial de presión en el filtro A es alto. Debés pasar al filtro B sin detener la producción.")
        
        secuencia = st.selectbox("¿Cuál es la secuencia operativa segura?", [
            "Seleccionar...",
            "Cerrar A y luego abrir B rápidamente",
            "Abrir válvula de equilibrio, llenar filtro B, abrir B y cerrar A",
            "Pedir parada de planta para cambiar filtros",
            "Abrir B y dejar los dos abiertos permanentemente"
        ])
        
        if st.button("Ejecutar Cambio"):
            if "equilibrio" in secuencia:
                st.success("✅ ¡Impecable! El uso de la línea de equilibrio evita el golpe de presión y garantiza que el filtro nuevo no tenga aire.")
            else:
                st.error("❌ Incorrecto. Si no equilibrás presiones primero, podés dañar las mallas o causar una caída de presión que dispare la parada de planta.")

elif seleccion == "⚡ Recuperación: Arranque de Pozo (Post-Corte)":
        st.subheader("Maniobra: Normalización de Pozo con AIB tras falla eléctrica")
        st.write("La energía volvió. El pozo estuvo parado 4 horas y el fluido se enfrió en la línea.")
        
        accion_aib = st.radio("¿Cómo procedés con el arranque?", [
            "Arrancar el motor a máxima velocidad inmediatamente",
            "Verificar nivel de aceite, realizar giros manuales/breves y arrancar con bypass de presión",
            "Abrir la purga al suelo y arrancar",
            "Esperar a que salga el sol para que caliente la línea"
        ])
        
        if st.button("Normalizar Pozo"):
            if "bypass" in accion_aib or "breves" in accion_aib:
                st.success("✅ ¡Excelente! Los arranques intermitentes 'despegan' la bomba suavemente evitando la rotura del vástago por carga de fluido estático.")
            else:
                st.error("❌ ¡Peligro! Un arranque brusco con la columna de fluido fría puede cortar el vástago o dañar los pernos del equipo.")
