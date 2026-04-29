import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from modulos.levantamiento import evaluar_levantamiento
from modulos.diseño_tecnico import calcular_especificaciones_bes, calcular_especificaciones_bm

def pozo_productor():
    st.title("Simulador de Pozo Productor")
    st.subheader("IPCL MENFA - Ingeniería de Producción")

    # --- ENTRADAS DE DATOS (Sidebar para dejar limpia la pantalla principal) ---
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
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Producción Estimada", f"{round(q, 2)} BPD")
        
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
            st.write("**Matriz de Selección de Levantamiento**")
            fig_matriz = graficar_matriz(resultado["ip"])
            st.pyplot(fig_matriz)

    with tab2:
        st.subheader("Especificaciones del Sistema Sugerido")
        if "error" in resultado:
            st.error(resultado["error"])
        else:
            sistema = resultado["sistema"]
            st.success(f"✅ Sistema Recomendado: {sistema}")
            
            if "ESP" in sistema or "BES" in sistema:
                specs = calcular_especificaciones_bes(q, profundidad, agua)
                c1, c2, c3 = st.columns(3)
                c1.metric("Carga (TDH)", f"{specs['tdh']} ft")
                c2.metric("Etapas Bomba", specs['etapas'])
                c3.metric("Potencia", f"{specs['potencia']} HP")
            
            elif "Mecánico" in sistema:
                specs = calcular_especificaciones_bm(q, profundidad)
                c1, c2 = st.columns(2)
                c1.metric("Velocidad", f"{specs['spm']} SPM")
                c2.info(f"**Unidad:** {specs['unidad']}")

    with tab3:
        st.subheader("Estimación de Rentabilidad")
        precio_barril = st.number_input("Precio del Crudo (USD/bbl)", value=75)
        costo_op = st.number_input("Costo Operativo Diario (USD)", value=1500)
        
        ingreso_bruto = q * precio_barril
        ganancia_neta = ingreso_bruto - costo_op
        
        c_eco1, c_eco2 = st.columns(2)
        c_eco1.metric("Ingreso Diario", f"USD {round(ingreso_bruto, 2):,}")
        
        # Color dinámico para la ganancia
        delta_color = "normal" if ganancia_neta > 0 else "inverse"
        c_eco2.metric("Ganancia Neta", f"USD {round(ganancia_neta, 2):,}", 
                      delta=f"{round(ganancia_neta, 2)}", delta_color=delta_color)

        if ganancia_neta < 0:
            st.error("⚠️ El pozo no es rentable bajo estas condiciones.")
        else:
            st.success("✔️ Operación rentable.")

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
