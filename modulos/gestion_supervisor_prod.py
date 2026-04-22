import streamlit as st

def gestion_supervisor_prod():
    st.title("🎓 Consola de Instrucción: Supervisor de Producción")

    # --- LÓGICA DE ROLES: INSTRUCTOR ---
    if st.session_state.rol == "instructor":
        st.sidebar.success("MODO INSTRUCTOR: Configurando Escenario")
        with st.expander("🚩 Panel de Control del Instructor", expanded=True):
            st.markdown("### Definir Desafío para el Alumno")
            escenario = st.selectbox("Seleccione el problema a simular:", [
                "Bajo tiempo de residencia en Tanque de Lavado",
                "Arrastre de agua en crudo Mesa 30",
                "Contaminación por Gas Ácido (H2S)"
            ])
            
            # Guardamos el escenario en la sesión para que el alumno lo vea
            st.session_state.mensaje_instructor = st.text_area("Indicaciones para el alumno:", 
                value=f"Atención: Se reportan problemas de {escenario.lower()}. Verifique niveles y tiempos de residencia.")
            
            if st.button("Lanzar Escenario al Simulador"):
                st.toast("Escenario enviado al panel del alumno")

    # --- LÓGICA DE ROLES: ALUMNO / PANEL DE OPERACIÓN ---
    st.divider()
    
    col_izq, col_der = st.columns([2, 1])

    with col_izq:
        st.subheader("🛠️ Panel de Operación y Toma de Acciones")
        
        # Pestañas integradas con la info técnica de tus documentos
        tab1, tab2, tab3 = st.tabs(["📊 KPI y Optimización", "📐 Ingeniería de Niveles", "⛽ Tratamiento de Gas"])

        with tab1:
            st.markdown("### Eficiencia Operativa (Ref. Clase 11)")
            st.info("El tratamiento consiste principalmente en la **deshidratación del petróleo** mediante métodos químicos y térmicos.")
            c1, c2 = st.columns(2)
            c1.metric("Tiempo de Residencia", "2.5 Horas", "Requerido")
            c2.metric("Costo de Intervención", "30%", "Límite OPEX")

        with tab2:
            st.markdown("### Cálculos de Operación (PDVSA Monagas)")
            st.write("Ajuste los parámetros del **Tanque de Lavado** para crudo Mesa 30:")
            
            with st.container(border=True):
                st.markdown("**Valores de Diseño:**")
                st.write("- Altura del distribuidor: **6 ft**")
                st.write("- Succión de bomba (P-01C): **17 ft**")
                
                # El alumno toma la acción aquí
                nivel_ingresado = st.slider("Nivel de Interfaz Agua/Crudo (ft):", 0.0, 20.0, 12.0)
                
                if nivel_ingresado < 13.9:
                    st.error("⚠️ Nivel insuficiente (Menor a 13.9 ft). Riesgo inminente de arrastre de agua y sedimentación incompleta.")
                else:
                    st.success("✅ Nivel de lavado óptimo. Se garantiza la desestabilización de la emulsión y coalescencia.")

        with tab3:
            st.markdown("### Separación de Gas Natural")
            st.write("Gestión de contaminantes (H2S y CO2) según protocolos.")
            
            opcion_gas = st.radio("Seleccione tecnología de separación:", ["Mallas Moleculares", "Membranas"])
            
            if opcion_gas == "Mallas Moleculares":
                st.help("Uso de lechos fijos para absorción física y deshidratación.")
            else:
                st.warning("La separación por membranas (afinidad/difusividad) puede generar pérdidas de hidrocarburos.")

    with col_der:
        st.markdown("### 📢 Feedback Educativo")
        # Mostramos lo que el instructor escribió
        if 'mensaje_instructor' in st.session_state:
            with st.chat_message("assistant"):
                st.write(st.session_state.mensaje_instructor)
        else:
            st.info("Esperando instrucciones del supervisor de guardia...")

        # Botón para que el alumno entregue su tarea
        if st.button("Enviar Reporte de Acciones"):
            st.balloons()
            st.success("Reporte enviado para evaluación del instructor.")

    st.divider()
    st.caption("MENFA 3.0 | Datos técnicos extraídos de PDVSA Distrito Norte y Operación de Gas Natural.")
