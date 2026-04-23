import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

def show():
    st.header("📈 Análisis de Nodo: IPR vs VLP")
    st.write("Instructor: Fabricio Pizzolato - Optimización de Producción")

    # 1. Recuperamos el factor de falla del simulador de fallas
    # Si no existe, lo inicializamos en 1.0 (Normal)
    if 'factor_obstruccion' not in st.session_state:
        st.session_state.factor_obstruccion = 1.0
    
    factor = st.session_state.factor_obstruccion

    with st.sidebar.expander("🛠️ Parámetros del Reservorio", expanded=True):
        p_res = st.number_input("Presión de Reservorio (Pr) [psi]", value=3000)
        pi = st.number_input("Índice de Productividad (IP)", value=1.5)
        p_sep = 500 # Presión de llegada/separador fija para este ejemplo
        
    # --- CÁLCULO DE IPR ---
    caudal_max = pi * p_res
    caudales = np.linspace(0.1, caudal_max, 100) # Evitamos el 0 para la potencia de la VLP
    pwf = p_res - (caudales / pi)
    pwf = np.maximum(pwf, 0)

    # --- CÁLCULO DE VLP (Con impacto de falla) ---
    # La VLP sube por fricción (factor) y contrapresión (p_sep)
    vlp = p_sep + (0.05 * factor * caudales**1.8) 

    # --- CÁLCULO DEL PUNTO DE EQUILIBRIO (CRUCE) ---
    # Buscamos donde la diferencia entre oferta y demanda es mínima
    indice_cruce = np.argmin(np.abs(pwf - vlp))
    caudal_op = caudales[indice_cruce]
    presion_op = pwf[indice_cruce]

    # --- GRÁFICO INTERACTIVO ---
    fig = go.Figure()
    
    # Curva IPR
    fig.add_trace(go.Scatter(x=caudales, y=pwf, name="IPR (Oferta)",
                             line=dict(color='#00ff00', width=4)))
    
    # Curva VLP
    fig.add_trace(go.Scatter(x=caudales, y=vlp, name="VLP (Demanda)",
                             line=dict(color='#ff4b4b', width=4, dash='dash')))

    # Punto de Operación
    fig.add_trace(go.Scatter(x=[caudal_op], y=[presion_op], 
                             name="Punto de Operación",
                             marker=dict(color='white', size=12, symbol='diamond')))

    fig.update_layout(
        title=f"Estado del Sistema: {'🚨 RESTRICCIÓN ACTIVA' if factor > 1 else '✅ OPERACIÓN NORMAL'}",
        xaxis_title="Caudal de Líquido (STB/D)",
        yaxis_title="Presión de Fondo Fluyente (Pwf) [psi]",
        template="plotly_dark",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- ACCIONES DE REMEDIACIÓN DINÁMICA ---
    st.subheader("🛠️ Intervención en el Pozo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if factor > 1.0:
            st.warning(f"⚠️ Restricción por Parafinas (Factor: {factor:.2f})")
            
            if st.button("💉 Aplicar Tratamiento Químico / Solvente"):
                progreso = st.progress(0)
                status_text = st.empty()
                
                # Proceso de limpieza simulado
                pasos = np.linspace(factor, 1.0, 5)
                for i, f_actual in enumerate(pasos):
                    st.session_state.factor_obstruccion = float(f_actual)
                    p_val = int((i + 1) * 20)
                    progreso.progress(p_val)
                    status_text.text(f"Bombeando solvente... Limpieza al {p_val}%")
                    time.sleep(0.4) 
                
                st.success("✅ ¡Línea Limpia! La VLP ha vuelto a su estado de diseño.")
                st.rerun()
        else:
            st.success("✅ El pozo fluye sin restricciones mecánicas.")
            if st.button("🚨 Simular Obstrucción (Para Práctica)"):
                st.session_state.factor_obstruccion = 2.5
                st.rerun()

    with col2:
        # Cálculo de Caudal Ideal (con factor = 1.0) para el Delta
        vlp_ideal = p_sep + (0.05 * 1.0 * caudales**1.8)
        idx_ideal = np.argmin(np.abs(pwf - vlp_ideal))
        caudal_ideal = caudales[idx_ideal]
        
        # Métrica comparativa
        st.metric(
            label="Caudal de Operación", 
            value=f"{int(caudal_op)} STB/D", 
            delta=f"{int(caudal_op - caudal_ideal)} STB/D vs. Potencial",
            delta_color="normal"
        )
        st.info(f"Presión de fondo fluyente: {int(presion_op)} psi")
# Dentro de modulos/ipr_vlp.py
st.session_state.caudal_real_scada = float(caudal_op)
