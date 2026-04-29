import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from modulos.levantamiento import evaluar_levantamiento
from modulos.diseño_tecnico import calcular_especificaciones_bes, calcular_especificaciones_bm

def pozo_productor():
    st.title("Simulador de Pozo Productor")
    st.subheader("IPCL MENFA - Ingeniería de Producción")

    # --- SIDEBAR: ENTRADA DE DATOS ---
    with st.sidebar:
        st.header("Configuración del Pozo")
        pr = st.slider("Presión Reservorio (psi)", 1000, 5000, 3500)
        pwf = st.slider("Presión Fondo Fluyente (psi)", 100, 4000, 1500)
        pi = st.slider("Índice de Productividad (PI)", 0.1, 5.0, 1.5)
        st.divider()
        gor = st.number_input("GOR (scf/stb)", value=500)
        agua = st.slider("% BSW (Agua y Sedimento)", 0, 100, 10)
        profundidad = st.number_input("Profundidad (ft)", value=8000)

    # --- CÁLCULOS BASE ---
    q = pi * (pr - pwf)
    resultado = evaluar_levantamiento(q, pr, pwf, gor, agua, profundidad)

    # --- ESTRUCTURA DE PESTAÑAS ---
    tab1, tab2, tab3 = st.tabs(["📊 Producción y Nodal", "⚙️ Diseño Técnico", "💰 Análisis Económico"])

    with tab1:
        st.subheader("Rendimiento del Reservorio")
        st.metric("Producción Estimada", f"{round(q, 2)} BPD")
        
        # Gráfico IPR
        pwf_range = np.linspace(0, pr, 50)
        q_ipr = pi * (pr - pwf_range)
        fig_ipr, ax_ipr = plt.subplots(figsize=(7, 3))
        ax_ipr.plot(q_ipr, pwf_range, color='darkred', lw=2)
        ax_ipr.set_xlabel("Caudal (BPD)")
        ax_ipr.set_ylabel("Presión (psi)")
        ax_ipr.invert_yaxis()
        ax_ipr.grid(True, alpha=0.3)
        st.pyplot(fig_ipr)

        if "error" not in resultado:
            st.divider()
            st.write("**Ubicación en Matriz de Productividad**")
            fig_matriz = graficar_matriz(resultado["ip"])
            st.pyplot(fig_matriz)

    with tab2:
        st.subheader("Especificaciones del Sistema Sugerido")
        if "error" in resultado:
            st.error(resultado["error"])
        else:
            sistema = resultado["sistema"]
            st.success(f"✅ Sistema Recomendado: {sistema}")
            st.divider()

            # --- RECUPERACIÓN DE LA LÓGICA DE EXTRACCIÓN ---
            if "ESP" in sistema or "BES" in sistema:
                # Llamamos a tu módulo de diseño técnico para BES
                specs = calcular_especificaciones_bes(q, profundidad, agua)
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Carga (TDH)", f"{specs['tdh']} ft")
                col_b.metric("Etapas Sugeridas", specs['etapas'])
                col_c.metric("Potencia Motor", f"{specs['potencia']} HP")
                st.info("Configuración optimizada para alto caudal y profundidad.")

            elif "Mecánico" in sistema or "Sucker Rod" in sistema:
                # Llamamos a tu módulo de diseño técnico para Mecánico
                specs = calcular_especificaciones_bm(q, profundidad)
                col_a, col_b = st.columns(2)
                col_a.metric("Velocidad", f"{specs['spm']} SPM")
                col_b.metric("Unidad de Superficie", specs['unidad'])
                st.info("Recomendado para pozos de productividad media/baja.")

            else:
                st.warning(f"Diseño detallado para {sistema} aún en desarrollo.")

    with tab3:
        st.subheader("Estimación de Rentabilidad")
        precio_barril = st.number_input("Precio del Crudo (USD/bbl)", value=75)
        costo_op = st.number_input("Costo Operativo Diario (USD)", value=1500)
        
        ingreso_bruto = q * precio_barril
        ganancia_neta = ingreso_bruto - costo_op
        
        c_eco1, c_eco2 = st.columns(2)
        c_eco1.metric("Ingreso Diario", f"USD {round(ingreso_bruto, 2):,}")
        
        delta_color = "normal" if ganancia_neta > 0 else "inverse"
        c_eco2.metric("Ganancia Neta", f"USD {round(ganancia_neta, 2):,}", 
                      delta=f"{round(ganancia_neta, 2)}", delta_color=delta_color)

def graficar_matriz(ip):
    fig, ax = plt.subplots(figsize=(6, 1.5))
    ax.axvspan(0, 0.5, color='red', alpha=0.2)
    ax.axvspan(0.5, 1.5, color='yellow', alpha=0.2)
    ax.axvspan(1.5, 3.0, color='green', alpha=0.2)
    ax.scatter(ip, 0.5, s=150, color='blue', edgecolor='white', zorder=5)
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("Índice de Productividad (IP)")
    plt.tight_layout()
    return fig
