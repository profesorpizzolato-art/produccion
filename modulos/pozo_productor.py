import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from modulos.levantamiento import evaluar_levantamiento
from modulos.diseño_tecnico import calcular_especificaciones_bes, calcular_especificaciones_bm

def pozo_productor():
    st.title("Simulador de Pozo Productor")
    st.subheader("IPCL MENFA - Ingeniería de Producción")

    st.markdown("### Parámetros del reservorio")
    col1, col2, col3 = st.columns(3)
    with col1:
        pr = st.slider("Presión Reservorio (psi)", 1000, 5000, 3500)
    with col2:
        pwf = st.slider("Presión Fondo Fluyente (psi)", 100, 4000, 1500)
    with col3:
        pi = st.slider("Índice de Productividad (PI)", 0.1, 5.0, 1.5)

    st.markdown("### Datos de Fluido y Completación")
    c1, c2, c3 = st.columns(3)
    with c1:
        gor = st.number_input("GOR (scf/stb)", value=500)
    with c2:
        agua = st.slider("% Agua y Sedimento", 0, 100, 10)
    with c3:
        profundidad = st.number_input("Profundidad (ft)", value=8000)

    st.markdown("---")

    # Cálculos base
    q = pi * (pr - pwf)
    st.subheader("Producción del Pozo")
    st.metric("Producción estimada (BPD)", round(q, 2))

    # Gráfico IPR
    pwf_range = np.linspace(0, pr, 50)
    q_ipr = pi * (pr - pwf_range)
    fig_ipr, ax_ipr = plt.subplots(figsize=(8, 4))
    ax_ipr.plot(q_ipr, pwf_range, color='darkred', lw=2)
    ax_ipr.set_xlabel("Producción (BPD)")
    ax_ipr.set_ylabel("Presión (psi)")
    ax_ipr.invert_yaxis()
    ax_ipr.grid(True, alpha=0.3)
    st.pyplot(fig_ipr)

    st.markdown("---")
    st.subheader("🧠 Evaluación de Levantamiento Artificial")
    
    resultado = evaluar_levantamiento(q, pr, pwf, gor, agua, profundidad)

    if "error" in resultado:
        st.error(resultado["error"])
    else:
        sistema = resultado["sistema"]
        st.success(f"✅ Sistema recomendado: {sistema}")
        
        # Matriz de productividad
        col_m1, col_m2, col_m3 = st.columns([1, 2, 1])
        with col_m2:
            fig_matriz = graficar_matriz(resultado["ip"])
            st.pyplot(fig_matriz)

        st.markdown("---")
        st.subheader("⚙️ Especificaciones Técnicas Detalladas")

        # Lógica de especificaciones
        if "ESP" in sistema or "BES" in sistema:
            specs = calcular_especificaciones_bes(q, profundidad, agua)
            c1, c2, c3 = st.columns(3)
            c1.metric("Carga (TDH)", f"{specs['tdh']} ft")
            c2.metric("Etapas", specs['etapas'])
            c3.metric("Potencia", f"{specs['potencia']} HP")

        elif "Mecánico" in sistema:
            specs = calcular_especificaciones_bm(q, profundidad)
            c1, c2 = st.columns(2)
            c1.metric("Velocidad", f"{specs['spm']} SPM")
            c2.info(f"**Unidad sugerida:** {specs['unidad']}")

def graficar_matriz(ip):
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.axvspan(0, 0.5, color='red', alpha=0.2)
    ax.axvspan(0.5, 1.5, color='yellow', alpha=0.2)
    ax.axvspan(1.5, 3.0, color='green', alpha=0.2)
    ax.scatter(ip, 0.5, s=150, color='blue', edgecolor='white', zorder=5)
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("IP")
    plt.tight_layout()
    return fig
