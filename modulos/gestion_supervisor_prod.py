import streamlit as st

def gestion_supervisor_prod():
    st.title("🎓 Consola de Supervisión: Misión de Planta")

    # --- LÓGICA DE ROLES: INSTRUCTOR (Indicaciones) ---
    if st.session_state.rol == "instructor":
        st.sidebar.success("MODO INSTRUCTOR: Configurando Desafío")
        with st.expander("🚩 Panel de Control del Instructor", expanded=True):
            st.markdown("### Definir Misión Técnica")
            escenario = st.selectbox("Seleccione el problema a simular:", [
                "Exceso de sales en crudo (Desalado)",
                "Baja temperatura de tratamiento (Viscosidad)",
                "Rotura de emulsión ineficiente"
            ])
            
            # El instructor define la guía pedagógica
            st.session_state.guia_pedagogica = st.text_area("Indicaciones para el alumno:", 
                value=f"Instructor: El crudo presenta problemas de {escenario.lower()}. "
                      "Recuerde aplicar los criterios de la Clase 11 sobre deshidratación.")
            
            if st.button("Enviar Desafío al Alumno"):
                st.toast("Misión actualizada")

    # --- LÓGICA DE ROLES: ALUMNO (Acciones) ---
    st.divider()
    
    col_izq, col_der = st.columns([2, 1])

    with col_izq:
        st.subheader("🛠️ Toma de Acciones del Operador")
        
        tab_desalado, tab_termico, tab_separadores = st.tabs([
            "🧂 Desalado", "🔥 Tratamiento Térmico", "📐 Separadores"
        ])

        with tab_desalado:
            st.markdown("#### Programa de Desalado (Ref: Planta de Tratamiento.pptx)")
            st.write("El objetivo es remover las sales hasta los valores de especificación comercial.")
            fase = st.radio("Acción de control:", ["Inyección de agua de lavado", "Ajuste de desemulsificante"])
            
            if fase == "Inyección de agua de lavado":
                st.success("✅ Correcto: El agua de lavado ayuda a disolver y arrastrar las sales del crudo.")
            else:
                st.info("El desemulsificante ayuda a la coalescencia, pero la remoción de sal requiere agua de lavado.")

        with tab_termico:
            st.markdown("#### Control de Viscosidad y Temperatura")
            st.write("Según tus archivos, el calor reduce la viscosidad y rompe la resistencia de la película en las gotas.")
            temp = st.slider("Ajustar Temperatura de Operación (°F):", 100, 300, 150)
            
            # Datos de la Tabla Nº 2 de separadores.docx
            if temp < 150:
                st.warning("⚠️ Velocidad de sedimentación muy baja (1,5. 10^-7 cm/seg). La separación será lenta.")
            elif temp >= 250:
                st.success(f"✅ Velocidad optimizada (1,6. 10^-2 cm/seg). Sedimentación eficiente para gotas de 500μ.")
            
            

        with tab_separadores:
            st.markdown("#### Dimensionamiento y Residencia")
            st.write("Garantice que el **Tanque Lavador** opere bajo los parámetros de PDVSA.")
            residencia = st.number_input("Tiempo de Residencia (Horas):", 1.0, 5.0, 2.5)
            
            if residencia < 2.5:
                st.error("❌ Tiempo insuficiente. Se requiere un mínimo de 2.5h para la desestabilización de la emulsión.")
            else:
                st.success("✅ Tiempo de residencia adecuado para el crudo Mesa 30.")

    with col_der:
        st.markdown("### 📢 Canal de Instrucción")
        # Visualización de las órdenes del instructor
        if 'guia_pedagogica' in st.session_state:
            with st.chat_message("assistant"):
                st.write(st.session_state.guia_pedagogica)
        else:
            st.info("Esperando que el instructor configure la planta...")

        st.divider()
        st.markdown("#### Estado de la Planta")
        st.progress(0.75, text="Calidad del Crudo (API/Sal)")
        
        if st.button("Cerrar Turno y Enviar Informe"):
            st.balloons()
            st.success("Informe de gestión enviado satisfactoriamente.")

    st.title("📋 Supervisión")

    st.text_area("Observaciones del instructor")

    if st.button("Guardar reporte"):
        st.success("Reporte guardado")
    st.divider()
    st.caption("Módulos actualizados con datos de: Separadores.docx, Plantas de Tratamiento.pptx y PDVSA Monagas.")
