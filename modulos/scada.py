import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# --- CONEXIÓN DE DATOS ---
def show():
    st.header("🖥️ SCADA de Producción - Planta MENFA")
    st.write("Instructor: Fabricio Pizzolato")

    # 1. Recuperar Variables Globales (Física y Fallas)
    factor = st.session_state.get('factor_obstruccion', 1.0)
    caudal_nominal = st.session_state.get('caudal_real_scada', 450.0)
    
    # Inicialización de estados de seguridad
    if 'esd_status' not in st.session_state: st.session_state.esd_status = False
    if 'reporte_completado' not in st.session_state: st.session_state.reporte_completado = False

    # --- LÓGICA DE CONTROL DE EMERGENCIA (ESD) ---
    if st.session_state.esd_status:
        st.error("🛑 PLANTA BLOQUEADA POR SISTEMA DE EMERGENCIA (ESD)")
        
        with st.expander("📋 REPORTE DE INCIDENTE OBLIGATORIO", expanded=not st.session_state.reporte_completado):
            st.warning("Debe completar el informe técnico para habilitar el Start-Up.")
            causa = st.selectbox("Causa de la Parada:", [
                "Sobrepresión en Separador", "Falla Instrumental", 
                "Fuga de Hidrocarburo", "Falla de Energía", "Prueba de Seguridad"
            ])
            descripcion = st.text_area("Descripción detallada de la maniobra:")
            
            if st.button("Enviar Reporte y Validar"):
                if len(descripcion) > 10:
                    st.session_state.reporte_completado = True
                    st.success("✅ Reporte archivado. Sistema de seguridad desbloqueado.")
                    st.rerun()
                else:
                    st.error("Por favor, sea más específico en la descripción técnica para el registro de MENFA.")

    # --- BOTONERA DE COMANDO ---
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if not st.session_state.esd_status:
            if st.button("🚨 ACTIVAR ESD", use_container_width=True, type="primary"):
                st.session_state.esd_status = True
                st.session_state.reporte_completado = False 
                st.rerun()
        else:
            st.button("🚨 ESD ACTIVADO", use_container_width=True, disabled=True)

    with col_btn2:
        if st.session_state.esd_status and st.session_state.reporte_completado:
            if st.button("✅ REARMAR PLANTA (START-UP)", use_container_width=True):
                st.session_state.esd_status = False
                st.session_state.reporte_completado = False
                st.balloons()
                st.rerun()
        else:
            st.button("✅ START-UP BLOQUEADO", use_container_width=True, disabled=True)

    # --- PROCESAMIENTO DE DATOS EN TIEMPO REAL ---
    st.divider()
    
    # Si hay ESD el caudal es 0. Si no, es el calculado en IPR/VLP
    caudal_actual = 0.0 if st.session_state.esd_status else caudal_nominal
    
    # Generamos histórico visual (24 hrs) que reacciona a la obstrucción
    datos_historicos = [caudal_actual + np.random.normal(0, 5) for _ in range(24)]
    if st.session_state.esd_status:
        datos_historicos = [0.0] * 24

    # --- GRÁFICO SCADA PROFESIONAL ---
    fig, ax = plt.subplots(figsize=(10, 3))
    # El color cambia a amarillo/naranja si hay mucha obstrucción, o rojo si hay ESD
    color_linea = '#ff4b4b' if st.session_state.esd_status else ('#ffa500' if factor > 1.8 else '#00ff00')
    
    ax.plot(datos_historicos, color=color_linea, linewidth=3, label="Caudal STB/D")
    ax.fill_between(range(len(datos_historicos)), datos_historicos, color=color_linea, alpha=0.1)
    
    # Estética Dark Industrial
    ax.set_facecolor('#1e1e1e')
    fig.patch.set_facecolor('#0e1117')
    ax.tick_params(colors='white')
    ax.grid(True, linestyle='--', alpha=0.2)
    ax.set_title("MONITOR DE FLUJO EN TIEMPO REAL", color='white', loc='left', fontsize=10)
    st.pyplot(fig)

    # --- PANEL DE INSTRUMENTOS (MÉTRICAS) ---
    m1, m2, m3 = st.columns(3)
    
    # La presión sube si el pozo está cerrado (ESD) o si hay parafinas
    p_base = 115.0
    val_presion = 165.0 if st.session_state.esd_status else (p_base * factor)
    
    m1.metric("P. Entrada Separador", f"{val_presion:.1f} psi", 
              delta=f"{val_presion - p_base:.1f}" if val_presion != p_base else None,
              delta_color="inverse")
    
    m2.metric("Caudal de Línea", f"{int(caudal_actual)} STB/D", 
              delta=f"Pérdida por Falla" if factor > 1 and not st.session_state.esd_status else None,
              delta_color="inverse")
    
    m3.metric("Válvula SDV-01", "CERRADA" if st.session_state.esd_status else "ABIERTA")

    # Alerta visual persistente
    if factor > 1.5 and not st.session_state.esd_status:
        st.warning(f"⚠️ Alerta de Eficiencia: Restricción mecánica detectada en línea de flujo (Factor {factor:.1f})")
