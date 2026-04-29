import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from modulos.levantamiento import evaluar_levantamiento
from modulos.diseño_tecnico import calcular_especificaciones_bes, calcular_especificaciones_bm
from modulos.dinamometro import dinamometro
# Importamos la conexión con la planta
from modulos.equipos_planta import mostrar_equipos_planta

def pozo_productor():
    st.title("Simulador de Pozo Productor")
    st.subheader("IPCL MENFA - Ingeniería de Producción")

    # --- 1. ENTRADAS DE DATOS (CENTRALES) ---
    st.markdown("### Parámetros del Reservorio")
    col1, col2, col3 = st.columns(3)
    with col1:
        pr = st.slider("Presión Reservorio (psi)", 1000, 5000, 3500, key="pr_slider")
    with col2:
        pwf = st.slider("Presión Fondo Fluyente (psi)", 100, 4000, 1500, key="pwf_slider")
    with col3:
        pi = st.slider("Índice de Productividad (PI)", 0.1, 5.0, 1.5, key="pi_slider")

    st.markdown("### Datos de Fluido y Completación")
    c1, c2, c3 = st.columns(3)
    with c1:
        gor = st.number_input("GOR (scf/stb)", value=500, key="gor_input")
    with c2:
        agua = st.slider("% BSW", 0, 100, 10, key="agua_slider")
    with c3:
        profundidad = st.number_input("Profundidad (ft)", value=8000, key="prof_input")

    st.markdown("---")

    # --- 2. CÁLCULOS INMEDIATOS ---
    q = pi * (pr - pwf)
    
    st.subheader("Producción del Pozo")
    st.metric("Producción estimada (BPD)", round(q, 2))

    # --- 3. EVALUACIÓN Y RESULTADOS ---
    resultado = evaluar_levantamiento(q, pr, pwf, gor, agua, profundidad)

    if "error" in resultado:
        st.error(resultado["error"])
    else:
        sistema = resultado["sistema"]
        st.success(f"✅ Sistema recomendado: {sistema}")
        
        g1, g2 = st.columns(2)
        with g1:
            pwf_range = np.linspace(0, pr, 50)
            q_ipr = pi * (pr - pwf_range)
            fig_ipr, ax_ipr = plt.subplots(figsize=(5, 4))
            ax_ipr.plot(q_ipr, pwf_range, color='darkred')
            ax_ipr.set_title("Curva IPR")
            ax_ipr.invert_yaxis()
            st.pyplot(fig_ipr)

        with g2:
            fig_matriz = graficar_matriz(resultado["ip"])
            st.pyplot(fig_matriz)

        # --- 4. ESPECIFICACIONES TÉCNICAS Y DIAGNÓSTICO ---
        st.markdown("---")
        
        if "ESP" in sistema or "BES" in sistema:
            st.subheader("⚙️ Especificaciones Técnicas Detalladas")
            specs = calcular_especificaciones_bes(q, profundidad, agua)
            t1, t2, t3 = st.columns(3)
            t1.metric("Carga (TDH)", f"{specs['tdh']} ft")
            t2.metric("Etapas", specs['etapas'])
            t3.metric("Potencia", f"{specs['potencia']} HP")

        elif "Mecánico" in sistema:
            st.subheader("⚙️ Especificaciones Técnicas Detalladas")
            specs = calcular_especificaciones_bm(q, profundidad)
            t1, t2 = st.columns(2)
            t1.metric("Velocidad", f"{specs['spm']} SPM")
            t2.info(f"**Unidad sugerida:** {specs['unidad']}")
            
            st.markdown("---")
            # Diagnóstico de fondo dinámico
            dinamometro(profundidad, agua, gor, q)

        # --- 5. INTEGRACIÓN CON PLANTA DE TRATAMIENTO ---
        st.markdown("---")
        # Llamamos a la lógica de planta pasando la producción actual
        mostrar_equipos_planta(q_pozo=q, bsw_pozo=agua)

def graficar_matriz(ip):
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.axvspan(0, 0.5, color='red', alpha=0.2)
    ax.axvspan(0.5, 1.5, color='yellow', alpha=0.2)
    ax.axvspan(1.5, 3.0, color='green', alpha=0.2)
    ax.scatter(ip, 0.5, s=200, color='blue', edgecolor='white', zorder=5)
    ax.set_title("Matriz de Productividad")
    ax.set_xlim(0, 3)
    ax.set_yticks([])
    plt.tight_layout()
    return fig
