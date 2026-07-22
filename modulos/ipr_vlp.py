import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

def show():
    st.header("📈 Análisis de Nodo: IPR vs VLP")
    st.caption("Optimización de Producción y Control de Restricciones")

    # 1. Garantizamos la presencia del factor de falla en session_state
    if 'factor_obstruccion' not in st.session_state:
        st.session_state.factor_obstruccion = 1.0
    
    factor = st.session_state.factor_obstruccion

    # --- PARÁMETROS DEL RESERVORIO ---
    with st.sidebar.expander("🛠️ Parámetros del Reservorio", expanded=True):
        p_res = st.number_input("Presión de Reservorio (Pr) [psi]", value=3000, step=100)
        pi = st.number_input("Índice de Productividad (IP) [bpd/psi]", value=1.5, step=0.1)
        p_sep = st.number_input("Presión de Separador (Psep) [psi]", value=500, step=10)
        
    # --- CÁLCULO DE IPR (OFERTA) ---
    caudal_max = pi * p_res
    # Generamos un vector denso para mayor precisión en la intersección
    caudales = np.linspace(0.1, caudal_max if caudal_max > 0 else 100.0, 200) 
    pwf = p_res - (caudales / pi)
    pwf = np.maximum(pwf, 0.0)

    # --- CÁLCULO DE VLP (DEMANDA CON OBSTRUCCIÓN) ---
    # La fricción en la tubería se escala según el factor de obstrucción
    vlp = p_sep + (0.05 * factor * (caudales ** 1.8)) 

    # --- CÁLCULO DEL PUNTO DE EQUILIBRIO (INTERSECCIÓN) ---
    indice_cruce = np.argmin(np.abs(pwf - vlp))
    caudal_op = float(caudales[indice_cruce])
    presion_op = float(pwf[indice_cruce])

    # --- VINCULACIÓN EN TIEMPO REAL CON EL SISTEMA SCADA Y MOTOR ---
    st.session_state.caudal_real_scada = caudal_op
    if 'motor' in st.session_state:
        st.session_state.motor.caudal_base = caudal_op
        st.session_state.motor.presion = presion_op

    # --- CÁLCULO VLP IDEAL (Sin Falla) PARA MÉTRICAS ---
    vlp_ideal = p_sep + (0.05 * 1.0 * (caudales ** 1.8))
    idx_ideal = np.argmin(np.abs(pwf - vlp_ideal))
    caudal_ideal = float(caudales[idx_ideal])

    # --- GRÁFICO INTERACTIVO PLOTLY ---
    fig = go.Figure()
    
    # Curva IPR
    fig.add_trace(go.Scatter(
        x=caudales, y=pwf, 
        name="IPR (Oferta Yacimiento)",
        line=dict(color='#00FF90', width=3.5)
    ))
    
    # Curva VLP
    fig.add_trace(go.Scatter(
        x=caudales, y=vlp, 
        name=f"VLP {'(Con Depósito/Parafina)' if factor > 1.0 else '(Línea Limpia)'}",
        line=dict(color='#FF4B4B' if factor > 1.0 else '#00B4D8', width=3.5, dash='dash' if factor > 1.0 else 'solid')
    ))

    # Punto de Operación Activo
    fig.add_trace(go.Scatter(
        x=[caudal_op], y=[presion_op], 
        name="Punto de Operación",
        marker=dict(color='#FFA15A', size=14, symbol='diamond', line=dict(color='white', width=1)),
        text=[f"Q={int(caudal_op)} STB/D<br>Pwf={int(presion_op)} psi"],
        hoverinfo="text"
    ))

    fig.update_layout(
        title=dict(
            text=f"Estado de la Instalación: {'🚨 RESTRICCIÓN POR PARAFINAS/INCRUSTACIÓN' if factor > 1.0 else '✅ TUBERÍA SIN OBSTRUCCIONES'}",
            font=dict(size=16)
        ),
        xaxis_title="Caudal de Líquido (STB/D)",
        yaxis_title="Presión de Fondo Fluyente (Pwf) [psi]",
        template="plotly_dark",
        hovermode="x unified",
        height=480,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- PANEL DE INTERVENCIÓN Y MÉTRICAS DE OPERACIÓN ---
    st.subheader("🛠️ Intervención y Diagnóstico del Pozo")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if factor > 1.0:
            st.warning(f"⚠️ **Daño por Restricción Activo:** Factor de fricción elevado a **{factor:.2f}x**")
            
            if st.button("💉 Inyectar Solvente / Tratamiento Químico", use_container_width=True):
                progreso = st.progress(0)
                status_text = st.empty()
                
                # Proceso dinámico de remediación
                pasos = np.linspace(factor, 1.0, 6)
                for i, f_actual in enumerate(pasos):
                    st.session_state.factor_obstruccion = float(f_actual)
                    p_val = int((i + 1) * (100 / len(pasos)))
                    progreso.progress(p_val)
                    status_text.text(f"🧪 Bombeando agente dispersante... Avance: {p_val}%")
                    time.sleep(0.3) 
                
                status_text.empty()
                progreso.empty()
                st.success("✅ ¡Tratamiento completado! Restricción disuelta.")
                st.rerun()
        else:
            st.success("✅ **Operación Normal:** No se detecta restricción en la tubería de producción.")
            if st.button("🚨 Simular Obstrucción por Parafina (Modo Práctica)", use_container_width=True):
                st.session_state.factor_obstruccion = 2.5
                st.rerun()

    with col2:
        delta_q = caudal_op - caudal_ideal
        st.metric(
            label="Caudal de Operación (Qop)", 
            value=f"{int(caudal_op)} STB/D", 
            delta=f"{int(delta_q)} STB/D vs. Potencial Teórico" if abs(delta_q) > 1 else "Óptimo",
            delta_color="normal"
        )
        st.info(f"📌 **Pwf de Operación:** {int(presion_op)} psi | **Efectividad:** {round((caudal_op / caudal_ideal)*100, 1)}%")

# Para permitir la ejecución directa o importación desde app.py
if __name__ == "__main__":
    show()
