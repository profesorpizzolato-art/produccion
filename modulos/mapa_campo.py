import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def mostrar_mapa():
    st.header("🗺️ Mapa Interactivo de Campo MENFA - Mendoza")
    st.write("Visualización dinámica de activos y alertas operativas.")

    # --- 1. DATOS DE LOS SISTEMAS DE EXTRACCIÓN (Exactos) ---
    conteo_sistemas = {
        'AIB (Mecánico)': 8,
        'ESP (Sumergible)': 3,
        'PCP (Tornillo)': 2,
        'Surgencia': 2
    }

    # Creamos un DataFrame simulado de pozos basado en el conteo
    pozos_data = []
    
    # Coordenadas base simuladas (zona de Malargüe/Llancanelo)
    lat_base = -37.12
    lon_base = -69.72

    for sistema, cantidad in conteo_sistemas.items():
        for i in range(cantidad):
            pozos_data.append({
                'Nombre': f'Pozo {sistema.split(" ")[0]}-{i+1:02d}',
                'Sistema': sistema,
                # Generamos una pequeña variación de ubicación
                'lat': lat_base + np.random.uniform(-0.05, 0.05),
                'lon': lon_base + np.random.uniform(-0.08, 0.08),
                'Estado': 'Normal'
            })

    # Creamos el DataFrame de pozos
    df_pozos = pd.DataFrame(pozos_data)

    # --- 2. GESTIÓN DINÁMICA DE ALERTAS ---
    # Asignamos las alertas específicas que pediste a pozos reales
    # (Usamos .iloc[0] para asegurar que existen)
    if not df_pozos[df_pozos['Sistema'] == 'AIB (Mecánico)'].empty:
        df_pozos.loc[df_pozos['Sistema'] == 'AIB (Mecánico)'].iloc[0]['Nombre'] = 'Pozo MENFA-002'
        idx_menfa2 = df_pozos[df_pozos['Nombre'] == 'Pozo MENFA-002'].index[0]
        df_pozos.at[idx_menfa2, 'Estado'] = '⚠️ Falla Cuplas'

    if not df_pozos[df_pozos['Sistema'] == 'Surgencia'].empty:
        idx_bateria2 = df_pozos[df_pozos['Sistema'] == 'Surgencia'].index[0]
        df_pozos.at[idx_bateria2, 'Nombre'] = 'Línea Batería 2'
        df_pozos.at[idx_bateria2, 'Estado'] = '🚨 Baja Presión'

    # --- 3. INTERFAZ INTERACTIVA ---
    col1, col2 = st.columns([2, 3])

    with col1:
        st.subheader("📊 Resumen de Activos")
        
        # Métrica Interactiva
        total_pozos = len(df_pozos)
        st.metric("Total Pozos Monitoreados", total_pozos, "Cuenca Cuyana")
        
        # Gráfico de Barras Interactivo (0-8)
        fig_bar = px.bar(
            df_pozos['Sistema'].value_counts().reset_index(),
            x='Sistema', 
            y='count',
            labels={'count': 'Cantidad de Pozos'},
            title="Sistemas de Extracción Activos",
            template="plotly_dark",
            range_y=[0, 9] # Escala 0-8 (9 para margen)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("📍 Panel de Alertas en Tiempo Real")
        
        # Filtro interactivo de Alertas
        mostrar_alertas = st.checkbox("Mostrar solo pozos con Alertas", value=False)
        
        # Filtramos los datos para el mapa
        df_mapa = df_pozos
        if mostrar_alertas:
            df_mapa = df_pozos[df_pozos['Estado'] != 'Normal']

        # Mapa Interactivo (Plotly Scatter Mapbox)
        # Necesitas un token de mapbox si quieres vista satelital real, 
        # pero esto usa el mapa base gratuito
        fig_map = px.scatter_mapbox(
            df_mapa, 
            lat="lat", 
            lon="lon", 
            hover_name="Nombre", 
            hover_data=["Sistema", "Estado"],
            color="Estado", # El color cambia según la alerta
            color_discrete_map={
                'Normal': '#2ecc71', # Verde
                '⚠️ Falla Cuplas': '#f1c40f', # Amarillo
                '🚨 Baja Presión': '#e74c3c' # Rojo
            },
            size_mapbox=12, 
            zoom=10,
            mapbox_style="carto-positron", # Mapa base limpio
            title="Ubicación y Estado de Pozos (Campo MENFA)"
        )
        st.plotly_chart(fig_map, use_container_width=True)

    # --- 4. PANEL DE CONTROL DE ALERTAS (Lo que varía) ---
    st.divider()
    st.subheader("🔧 Panel de Control Operativo (Simulación de Fallas)")
    st.write("Variá el estado de los pozos para entrenar la respuesta.")

    with st.expander("Modificar Estado de Pozos"):
        colA, colB, colC = st.columns(3)
        with colA:
            st.selectbox("Seleccionar Pozo:", df_pozos['Nombre'].tolist(), key="select_pozo")
        with colB:
            st.selectbox("Nuevo Estado:", ['Normal', '⚠️ Falla Cuplas', '🚨 Baja Presión', '🔧 Mantenimiento'], key="select_estado")
        with colC:
            if st.button("Aplicar Cambio", use_container_width=True):
                # Lógica para aplicar el cambio (requeriría session_state avanzada, 
                # pero esto muestra cómo funcionaría la interacción)
                st.success(f"Estado de {st.session_state.select_pozo} actualizado a {st.session_state.select_estado}.")
                st.info("Para que la interacción sea permanente, debemos mover la base de datos de pozos a `st.session_state`.")

    # --- 5. ALERTAS OPERATIVAS (Texto Fijo que pediste) ---
    st.divider()
    st.subheader("⚠️ Alertas Operativas Críticas (Mendoza)")
    st.warning("**Pozo MENFA-002:** Requiere cambio de cuplas por fatiga.")
    st.error("**Baja presión** en línea de transferencia hacia Batería 2.")
