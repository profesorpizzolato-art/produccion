import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from modulos.levantamiento import evaluar_levantamiento

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

    # Parámetros adicionales necesarios para la función evaluar_levantamiento
    st.markdown("### Datos de Fluido y Completación")
    c1, c2, c3 = st.columns(3)
    with c1:
        gor = st.number_input("GOR (scf/stb)", value=500)
    with c2:
        agua = st.slider("% Agua y Sedimento", 0, 100, 10)
    with c3:
        profundidad = st.number_input("Profundidad (ft)", value=8000)

    st.markdown("---")

    # Cálculo producción
    q = pi * (pr - pwf)
    st.subheader("Producción del Pozo")
    st.metric("Producción estimada (BPD)", round(q, 2))

    # Gráfico IPR
    st.subheader("Curva IPR")
    pwf_range = np.linspace(0, pr, 50)
    q_ipr = pi * (pr - pwf_range)
    
    fig, ax = plt.subplots()
    ax.plot(q_ipr, pwf_range)
    ax.set_xlabel("Producción (BPD)")
    ax.set_ylabel("Presión fondo fluyente (psi)")
    ax.set_title("Curva IPR del pozo")
    ax.invert_yaxis()
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("Estado del pozo")

    if q > 3000:
        st.success("Pozo de alta productividad")
    elif q > 1000:
        st.warning("Producción media")
    else:
        st.error("Producción baja")

    st.subheader("🧠 Evaluación de Levantamiento Artificial")

    # --- AQUÍ ESTABA EL ERROR DE INDENTACIÓN ---
    # Todo esto debe estar dentro de pozo_productor()
    resultado = evaluar_levantamiento(q, pr, pwf, gor, agua, profundidad)

    if "error" in resultado:
        st.error(resultado["error"])
    else:
        st.metric("Índice de Productividad (IP)", round(resultado["ip"], 2))
        st.info(f"Zona: {resultado['zona']}")
        st.success(f"Sistema recomendado: {resultado['sistema']}")
        
        # Llamamos a la función de la matriz aquí mismo
        fig_matriz = graficar_matriz(resultado["ip"], resultado["sistema"])
        st.pyplot(fig_matriz)

def graficar_matriz(ip, sistema_nombre):
    fig, ax = plt.subplots()

    # ZONAS (tipo matriz) con colores
    ax.axvspan(0, 0.5, color='red', alpha=0.2)
    ax.axvspan(0.5, 1.5, color='yellow', alpha=0.2)
    ax.axvspan(1.5, 3, color='green', alpha=0.2)

    # Líneas divisorias
    ax.axvline(0.5, color='gray', linestyle='--')
    ax.axvline(1.5, color='gray', linestyle='--')

    # Punto del pozo
    ax.scatter(ip, 0.5, s=200, color='blue', edgecolor='white', zorder=5)

    # Etiquetas
    ax.set_title("Matriz de Selección de Levantamiento Artificial")
    ax.set_xlabel("Índice de Productividad (IP)")
    ax.set_yticks([])
    ax.set_xlim(0, 3)

    # Texto en zonas y datos
    ax.text(0.25, 0.9, "Baja", ha='center')
    ax.text(1.0, 0.9, "Media", ha='center')
    ax.text(2.25, 0.9, "Alta", ha='center')
    
    ax.text(ip, 0.3, f"IP={ip:.2f}", ha='center', fontweight='bold')
    ax.text(ip, 0.7, sistema_nombre, ha='center', color='darkblue')

    return fig
