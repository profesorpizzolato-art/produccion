import streamlit as st

def show():
    st.header("⚠️ Panel de Simulación de Fallas")
    st.write("Instructor: Fabricio Pizzolato")
    st.write("Simula condiciones adversas para observar el impacto en las curvas de producción.")

    # 1. INICIALIZACIÓN DE VARIABLES GLOBALES DE FALLA
    if 'factor_obstruccion' not in st.session_state:
        st.session_state.factor_obstruccion = 1.0
    if 'factor_densidad' not in st.session_state:
        st.session_state.factor_densidad = 1.0
    if 'tipo_falla_actual' not in st.session_state:
        st.session_state.tipo_falla_actual = "Operación Normal"

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Seleccionar Evento")
        
        # Usamos el estado guardado para que el selectbox no se resetee solo
        falla = st.selectbox(
            "Tipo de Falla", 
            [
                "Operación Normal",
                "Obstrucción en Línea de Flujo (Parafinas)",
                "Aumento de Contrapresión en Separador",
                "Incremento de Corte de Agua (Aumento de Densidad)"
            ],
            index=[
                "Operación Normal",
                "Obstrucción en Línea de Flujo (Parafinas)",
                "Aumento de Contrapresión en Separador",
                "Incremento de Corte de Agua (Aumento de Densidad)"
            ].index(st.session_state.tipo_falla_actual)
        )

        # 2. LÓGICA DE ACTUALIZACIÓN DE VARIABLES
        if falla != st.session_state.tipo_falla_actual:
            st.session_state.tipo_falla_actual = falla
            
            if falla == "Operación Normal":
                st.session_state.factor_obstruccion = 1.0
                st.session_state.factor_densidad = 1.0
                st.success("Sistema normalizado.")
            
            elif falla == "Obstrucción en Línea de Flujo (Parafinas)":
                st.session_state.factor_obstruccion = 2.5 # Aumenta fricción
                st.session_state.factor_densidad = 1.0
                st.warning("Restricción por parafinas activa.")

            elif falla == "Aumento de Contrapresión en Separador":
                st.session_state.factor_obstruccion = 1.8 # Sube la presión de llegada
                st.session_state.factor_densidad = 1.0
                
            elif falla == "Incremento de Corte de Agua (Aumento de Densidad)":
                st.session_state.factor_obstruccion = 1.2
                st.session_state.factor_densidad = 1.4 # Impacto en gradiente estático
            
            st.rerun() # Forzamos recarga para que el SCADA se entere al instante

    with col2:
        st.info("💡 **Dato Técnico IPCL MENFA:**")
        if st.session_state.factor_obstruccion > 1.0:
            st.error(f"Efecto actual: Pendiente VLP incrementada x{st.session_state.factor_obstruccion}")
        
        st.write("""
        En la cuenca cuyana, la deposición de parafinas desplaza la curva VLP hacia la izquierda. 
        Esto reduce el caudal de aporte y aumenta la presión de fondo fluyente necesaria.
        """)

    # 3. BOTÓN DE ACCIÓN RÁPIDA (REPARACIÓN)
    if st.session_state.factor_obstruccion > 1.0:
        if st.button("🛠️ Realizar Limpieza (Pigging / Hot Oil)"):
            st.session_state.factor_obstruccion = 1.0
            st.session_state.factor_densidad = 1.0
            st.session_state.tipo_falla_actual = "Operación Normal"
            st.success("Limpieza exitosa. Planta en condiciones de diseño.")
            st.rerun()
