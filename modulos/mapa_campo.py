import streamlit as st
import pandas as pd

def mostrar_mapa():
    st.header("🗺️ Mapa Georreferenciado del Yacimiento")
    st.write("Ubicación estratégica de activos en la Cuenca Cuyana.")

    # Datos simulados de pozos en zona sur de Mendoza
    df_pozos = pd.DataFrame({
        'lat': [-37.124, -37.145, -37.110, -37.135],
        'lon': [-69.721, -69.702, -69.740, -69.695],
        'Pozo': ['MENFA-001', 'MENFA-002 (Intervenido)', 'MENFA-003', 'MENFA-004'],
        'Estado': ['Activo', 'Parado', 'Activo', 'Activo']
    })

    # Selector de visualización
    capa = st.radio("Capa de datos:", ["Pozos de Producción", "Líneas de Conducción"], horizontal=True)
    
    if capa == "Pozos de Producción":
        st.map(df_pozos, zoom=11)
        st.dataframe(df_pozos, use_container_width=True)
    else:
        st.info("Visualizando trazado de ductos hacia Planta de Tratamiento de Crudo (PTC).")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Oil_and_gas_field_map_icon.svg/1024px-Oil_and_gas_field_map_icon.svg.png", width=200)

    st.success("📍 Sistema de coordenadas: WGS 84 / UTM zone 19S")
