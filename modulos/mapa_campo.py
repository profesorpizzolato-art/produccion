import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def mostrar_mapa():
    st.header("🗺️ Mapa Interactivo de Campo MENFA")

    # --- 1. INICIALIZACIÓN DEL ESTADO (Solo ocurre una vez) ---
    if 'df_pozos' not in st.session_state:
        # Definimos los pozos base de Mendoza
        pozos_iniciales = [
            {'Nombre': 'Pozo MENFA-001', 'Sistema': 'AIB (Mecánico)', 'lat': -37.12, 'lon': -69.72, 'Estado': 'Normal'},
            {'Nombre': 'Pozo MENFA-002', 'Sistema': 'AIB (Mecánico)', 'lat': -37.13, 'lon': -69.71, 'Estado': '⚠️ Falla Cuplas'},
            {'Nombre': 'Pozo MENFA-003', 'Sistema': 'ESP (Sumergible)', 'lat': -37.11, 'lon': -69.73, 'Estado': 'Normal'},
            {'Nombre': 'Línea Batería 2', 'Sistema': 'Surgencia', 'lat': -37.15, 'lon': -69.70, 'Estado': '🚨 Baja Presión'},
        ]
        
        # Generamos el resto de los pozos para completar tu esquema (8 AIB, 3 ESP, etc.)
        extras = []
        sistemas = {'AIB (Mecánico)': 6, 'ESP (Sumergible)': 2, 'PCP (Tornillo)': 2, 'Surgencia': 1}
        for sis, cant in sistemas.items():
            for i in range(cant):
                extras.append({
                    'Nombre': f'Pozo {sis[:3]}-{i+10}', 
                    'Sistema': sis, 
                    'lat': -37.12 + np.random.uniform(-0.04, 0.04), 
                    'lon': -69.72 + np.random.uniform(-0.04, 0.04), 
                    'Estado': 'Normal'
                })
        
        st.session_state.df_pozos = pd.DataFrame(pozos_iniciales + extras)

    # Usamos los datos guardados en la sesión
    df = st.session_state.df_pozos

    # --- 2. VISUALIZACIÓN ---
    col_map, col_ctrl = st.columns([3, 1])

    with col_map:
        fig = px.scatter_mapbox(
            df, lat="lat", lon="lon", color="Estado",
            hover_name="Nombre", hover_data=["Sistema"],
            color_discrete_map={
                'Normal': '#2ecc71',
                '⚠️ Falla Cuplas': '#f1c40f',
                '🚨 Baja Presión': '#e74c3c',
                '🔧 Mantenimiento': '#3498db'
            },
            zoom=10, height=550, mapbox_style="carto-positron"
        )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)

    with col_ctrl:
        st.subheader("Panel de Control")
        st.write("Variar estado de activos:")
        
        target = st.selectbox("Seleccionar:", df['Nombre'].tolist())
        nuevo_estado = st.selectbox("Nuevo Estado:", ["Normal", "⚠️ Falla Cuplas", "🚨 Baja Presión", "🔧 Mantenimiento"])
        
        if st.button("Actualizar Campo"):
            # Actualizamos el DataFrame en la sesión
            idx = st.session_state.df_pozos[st.session_state.df_pozos['Nombre'] == target].index[0]
            st.session_state.df_pozos.at[idx, 'Estado'] = nuevo_estado
            st.success(f"{target} actualizado.")
            st.rerun()

    # --- 3. ALERTAS TÉCNICAS (Fijas) ---
    st.divider()
    st.subheader("⚠️ Reporte de Novedades Críticas")
    c1, c2 = st.columns(2)
    with c1:
        st.warning("**POZO MENFA-002:** Requiere intervención. Fatiga detectada en cuplas (AIB).")
    with c2:
        st.error("**BATERÍA 2:** Alarma de baja presión en línea de transferencia.")
