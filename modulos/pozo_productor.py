import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from modulos.levantamiento import evaluar_levantamiento
from modulos.diseño_tecnico import calcular_especificaciones_bes, calcular_especificaciones_bm

def pozo_productor():
    st.title("Simulador de Pozo Productor")
    st.subheader("IPCL MENFA - Ingeniería de Producción")

    # --- SECCIÓN 1: PARÁMETROS ---
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

    # --- SECCIÓN 2: PRODUCCIÓN e IPR ---
    q = pi * (pr - pwf)
    st.subheader("Producción del Pozo")
    st.metric("Producción estimada (BPD)", round(q, 2))

    st.subheader("Curva IPR")
    pwf_range = np.linspace(0, pr, 50)
    q_ipr = pi * (pr - pwf_range)
    fig, ax = plt.subplots()
    ax.plot(q_ipr, pwf_range)
    ax.set_xlabel("Producción (BPD)")
    ax.set_ylabel("Presión fondo fluyente (psi)")
    ax.invert_yaxis()
    st.pyplot(fig)

    # --- SECCIÓN 3: LEVANTAMIENTO ARTIFICIAL ---
    st.markdown("---")
    st.subheader("🧠 Evaluación de Levantamiento Artificial")
    resultado = evaluar_levantamiento(q, pr, pwf, gor, agua, profundidad)

    if "error" in resultado:
        st.error(resultado["error"])
    else:
        sistema = resultado["sistema"]
        st.success(f"Sistema recomendado: {sistema}")
        
        # Gráfico de la Matriz
        fig_matriz = graficar_matriz(resultado["ip"], sistema)
        st.pyplot(fig_matriz)

        # --- SECCIÓN 4: ESPECIFICACIONES TÉCNICAS (Lo nuevo) ---
        st.markdown("---")
        st.subheader("⚙️ Especificaciones Técnicas Detalladas")

        if "BES" in sistema:
            specs = calcular_especificaciones_bes(q, profundidad, agua)
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Carga (TDH)", f"{specs['tdh']} ft")
            col_b.metric("Etapas", specs['etapas'])
            col_c.metric("Potencia", f"{specs['potencia']} HP")

        elif "Mecánico" in sistema:
            specs = calcular_especificaciones_bm(q, profundidad)
            col_a, col_b = st.columns(2)
            col_a.metric("Velocidad", f"{specs['spm']} SPM")
            col_b.info(f"**Unidad sugerida:** {specs['unidad']}")

def graficar_matriz(ip, sistema_nombre):
    fig, ax = plt.subplots()
    ax.axvspan(0, 0.5, color='red', alpha=0.2)
    ax.axvspan(0.5, 1.5, color='yellow', alpha=0.2)
    ax.axvspan(1.5, 3, color='green', alpha=0.2)
    ax.scatter(ip, 0.5, s=200, color='blue', edgecolor='white', zorder=5)
    ax.set_title("Matriz de Selección")
    ax.set_xlim(0, 3)
    ax.set_yticks([])
    ax.text(ip, 0.3, f"IP={ip:.2f}", ha='center', fontweight='bold')
    return fig
