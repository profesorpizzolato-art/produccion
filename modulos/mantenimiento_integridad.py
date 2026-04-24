import streamlit as st
import pandas as pd
import random

def mostrar_mantenimiento_integridad():
    st.header("🛠️ Gestión de Mantenimiento e Integridad")
    
    tab1, tab2 = st.tabs(["🔧 Mantenimiento Mecánico", "🧪 Control Químico e Integridad"])

    with tab1:
        st.subheader("Estado de Equipos Críticos")
        # Simulación de estado de mantenimiento
        equipos = {
            "Equipo": ["Bomba de Transferencia P-101", "Motor AIB MENFA-001", "Compresor K-200", "Separador V-01"],
            "Horas de Marcha": [1250, 4800, 850, 15000],
            "Estado": ["Normal", "⚠️ Requiere Service", "Normal", "Inspección Visual OK"]
        }
        df_equipos = pd.DataFrame(equipos)
        
        def color_estado(val):
            color = 'red' if 'Requiere' in val else 'green'
            return f'color: {color}'

        st.table(df_equipos.style.applymap(color_estado, subset=['Estado']))
        
        if st.button("📝 Generar Orden de Trabajo (OT)"):
            st.success("Orden de Trabajo enviada al equipo de mantenimiento para MENFA-001.")

    with tab2:
        st.subheader("Tratamiento Químico y Corrosión")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Dosificación de Productos:**")
            d_dem = st.slider("Desemulsionante (ppm):", 0, 100, 25)
            d_inh = st.slider("Inhibidor de Corrosión (ppm):", 0, 50, 15)
            
            if st.button("Aplicar Ajuste Químico"):
                st.toast("Caudal de bombas dosificadoras actualizado.")

        with col2:
            st.write("**Estado de Integridad (Líneas):**")
            presion_linea = st.number_input("Presión de Línea de Venta (psi):", value=110)
            
            if presion_linea > 130:
                st.error("🚨 ALERTA DE INTEGRIDAD: Posible taponamiento por parafinas.")
                if st.button("🔥 Programar Hot Oil"):
                    st.warning("Maniobra de limpieza térmica programada.")
            else:
                st.success("Integridad de línea dentro de parámetros normales.")

        st.divider()
        st.info("💡 **Dato del Instructor:** El control de parafinas es vital en invierno en la Cuenca Cuyana para evitar sobrepresiones en las líneas de conducción.")
