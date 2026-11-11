import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def mostrar_modelado_reservorios():
  st.header("📊 Modelado, Análisis Nodal, EOR y Yacimiento 3D")
  st.markdown(
      "Ecosistema integral de simulación y análisis de producción de MenFa"
      " Capacitaciones."
  )

  # Pestañas principales de navegación del módulo
  tabs = st.tabs(
      [
          "🔗 Análisis Nodal (IPR-VLP)",
          "📉 Declinación de Producción",
          "🛢️ Balance de Materia (OOIP)",
          "💧 Recuperación Mejorada (EOR)",
          "🧊 Modelo 3D y Frente de Agua",
      ]
  )

  # ---------------------------------------------------------
  # TAB 1: ANÁLISIS NODAL (IPR vs VLP)
  # ---------------------------------------------------------
  with tabs[0]:
    st.subheader("📈 Análisis Nodal: Curvas IPR vs VLP")
    st.write("Optimización del punto de operación del pozo.")

    col1, col2 = st.columns([1, 2])
    with col1:
      st.subheader("⚙️ Parámetros del Reservorio")
      pr = st.slider("Presión de Reservorio (Pr) [psi]", 1000, 4000, 2500, key="nodal_pr")
      ip = st.slider("Índice de Productividad (IP)", 0.5, 5.0, 1.5, key="nodal_ip")

      st.subheader("🏗️ Parámetros de Instalación")
      p_cabeza = st.slider(
          "Presión de Cabeza (Pwh) [psi]", 50, 500, 150, key="nodal_pwh"
      )

    with col2:
      q_max = pr * ip
      caudal_ipr = np.linspace(0, q_max, 50)
      presion_ipr = pr - (caudal_ipr / ip)

      caudal_vlp = np.linspace(10, q_max, 50)
      presion_vlp = (
          p_cabeza + (0.0005 * caudal_vlp**2) + (0.2 * caudal_vlp)
      )

      fig = go.Figure()
      fig.add_trace(
          go.Scatter(
              x=caudal_ipr,
              y=presion_ipr,
              name="IPR (Yacimiento)",
              line=dict(color="#2ecc71", width=4),
          )
      )
      fig.add_trace(
          go.Scatter(
              x=caudal_vlp,
              y=presion_vlp,
              name="VLP (Instalación)",
              line=dict(color="#e74c3c", width=4),
          )
      )

      fig.update_layout(
          title="Punto de Operación (Intersección IPR-VLP)",
          xaxis_title="Caudal (Q) [bpd]",
          yaxis_title="Presión de Fondo (Pwf) [psi]",
          template="plotly_dark",
          legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
          height=400,
      )
      st.plotly_chart(fig, use_container_width=True)

    idx = np.argwhere(np.diff(np.sign(presion_ipr - presion_vlp))).flatten()
    if len(idx) > 0:
      q_op = round(caudal_ipr[idx[0]], 2)
      pwf_op = round(presion_ipr[idx[0]], 2)

      c1, c2, c3 = st.columns(3)
      c1.metric("Caudal de Operación", f"{q_op} bpd")
      c2.metric("Pwf de Operación", f"{pwf_op} psi")
      c3.metric("Potencial Máximo (AOF)", f"{round(q_max, 1)} bpd")
      st.success(
          f"💡 El pozo está fluyendo a un régimen estable de **{q_op} bpd**."
      )
    else:
      st.error(
          "🚨 Las curvas no se cruzan: El pozo no tiene suficiente energía para"
          " fluir con la configuración actual."
      )

  # ---------------------------------------------------------
  # TAB 2: DECLINACIÓN DE PRODUCCIÓN (Arps)
  # ---------------------------------------------------------
  with tabs[1]:
    st.subheader("📉 Pronóstico por Curvas de Declinación (Arps)")
    c1, c2 = st.columns([1, 2])

    with c1:
      qi = st.number_input("Caudal Inicial ($Q_i$) [bbl/d]", 10, 20000, 1200)
      di = (
          st.slider("Tasa de Declinación ($D_i$) [%/año]", 1.0, 50.0, 15.0)
          / 100.0
      )
      b = st.selectbox(
          "Exponente (b)",
          options=[0.0, 0.5, 1.0],
          format_func=lambda x: (
              "0.0 (Exponencial)"
              if x == 0
              else ("0.5 (Hiperbólica)" if x == 0.5 else "1.0 (Armónica)")
          ),
      )
      anios = st.slider("Período [Años]", 1, 30, 10)

    with c2:
      t = np.linspace(0, anios, anios * 12)
      if b == 0:
        q_t = qi * np.exp(-di * t)
      elif b == 1:
        q_t = qi / (1 + di * t)
      else:
        q_t = qi / ((1 + b * di * t) ** (1 / b))

      fig_dec = go.Figure()
      fig_dec.add_trace(
          go.Scatter(
              x=t,
              y=q_t,
              mode="lines",
              name="Q(t)",
              line=dict(color="#3D405B", width=2.5),
          )
      )
      fig_dec.update_layout(
          title="Pronóstico de Declinación",
          xaxis_title="Tiempo [Años]",
          yaxis_title="Q(t) [bbl/d]",
          template="plotly_white",
          height=400,
      )
      st.plotly_chart(fig_dec, use_container_width=True)
      npv_acum = np.trapz(q_t, t) * 365
      st.metric("Producción Acumulada Estimada", f"{npv_acum/1e6:.2f} MMbbl")

  # ---------------------------------------------------------
  # TAB 3: BALANCE DE MATERIA (OOIP Volumétrico)
  # ---------------------------------------------------------
  with tabs[2]:
    st.subheader("🛢️ Estimación de OOIP (Método Volumétrico)")
    c1, c2, c3 = st.columns(3)
    area = c1.number_input("Área [Acres]", value=500.0)
    espesor = c2.number_input("Espesor Neto [ft]", value=40.0)
    porosidad = c3.number_input("Porosidad", value=0.18, format="%.2f")

    c4, c5 = st.columns(2)
    sw = c4.number_input("Saturación de Agua ($S_{wi}$)", value=0.25, format="%.2f")
    boi = c5.number_input(
        "Factor Volumétrico ($B_{oi}$) [rb/STB]", value=1.25, format="%.2f"
    )

    ooip = (7758 * area * espesor * porosidad * (1 - sw)) / boi
    st.markdown("---")
    st.metric(
        label="Petróleo Original en Sitio (OOIP)", value=f"{ooip/1e6:.2f} MMSTB"
    )

  # ---------------------------------------------------------
  # TAB 4: RECUPERACIÓN MEJORADA (EOR)
  # ---------------------------------------------------------
  with tabs[3]:
    st.subheader("💧 Selección y Evaluación de Métodos EOR")
    c1, c2, c3 = st.columns(3)
    api_oil = c1.number_input("Densidad del Crudo [°API]", value=28.0)
    viscosidad = c2.number_input("Viscosidad del Crudo ($\mu_o$) [cp]", value=3.5)
    perm_med = c3.number_input("Permeabilidad Promedio [md]", value=120.0)

    if api_oil > 30 and viscosidad < 10:
      metodo = "Inyección de Agua Convencional / Secundaria"
      desc = "Adecuado para mantener presión y barrido en crudos livianos."
    elif 15 <= api_oil <= 30 and viscosidad <= 30:
      metodo = "Inyección de Polímeros (EOR Químico)"
      desc = "Mejora la movilidad del agua aumentando su viscosidad."
    else:
      metodo = "Métodos Térmicos (Inyección de Vapor)"
      desc = "Ideal para reducir la alta viscosidad en crudos pesados."

    st.info(f"**Método Sugerido:** {metodo} — {desc}")

    fr_primario = st.slider("Factor de Recuperación Primario [%]", 10.0, 35.0, 20.0)
    incremento_eor = st.slider("Incremento Estimado EOR [%]", 5.0, 25.0, 12.0)
    st.metric(
        "Factor de Recuperación Final Proyectado",
        f"{fr_primario + incremento_eor:.1f}%",
        delta=f"+{incremento_eor}%",
    )

  # ---------------------------------------------------------
  # TAB 5: MODELO 3D CON SLIDER TEMPORAL (Frente de Agua)
  # ---------------------------------------------------------
  with tabs[4]:
    st.subheader("🧊 Modelo 3D y Simulación Dinámica de Frente de Agua")
    st.markdown(
        "Avance del frente de inyección modelado tridimensionalmente año a año."
    )

    c_c1, c_c2, c_c3 = st.columns(3)
    num_pozos_prod = c_c1.number_input("Pozos Productores", 1, 10, 4)
    num_pozos_iny = c_c2.number_input("Pozos Inyectores", 1, 5, 2)
    angulo_buzamiento = c_c3.slider("Ángulo de Buzamiento [°]", 0, 45, 15)

    anio_actual = st.slider("⏱️ Tiempo de Inyección [Años]", 1, 10, 3)

    x_lin = np.linspace(0, 1000, 30)
    y_lin = np.linspace(0, 1000, 30)
    X, Y = np.meshgrid(x_lin, y_lin)
    Z = -(Y * np.tan(np.radians(angulo_buzamiento))) - 200 * np.sin(
        np.pi * X / 1000
    ) * np.sin(np.pi * Y / 1000)

    fig_3d = go.Figure()
    fig_3d.add_trace(
        go.Surface(
            z=Z,
            x=X,
            y=Y,
            colorscale="Viridis",
            name="Tope Yacimiento",
            opacity=0.7,
            showscale=False,
        )
    )

    iny_x = np.array([200, 800])[:num_pozos_iny]
    iny_y = np.array([200, 800])[:num_pozos_iny]
    iny_z = -(iny_y * np.tan(np.radians(angulo_buzamiento))) - 200 * np.sin(
        np.pi * iny_x / 1000
    ) * np.sin(np.pi * iny_y / 1000)

    prod_x = np.array([500, 300, 700, 500])[:num_pozos_prod]
    prod_y = np.array([500, 700, 300, 200])[:num_pozos_prod]
    prod_z = -(prod_y * np.tan(np.radians(angulo_buzamiento))) - 200 * np.sin(
        np.pi * prod_x / 1000
    ) * np.sin(np.pi * prod_y / 1000)

    radio_invacion = 60 * np.sqrt(anio_actual)
    theta = np.linspace(0, 2 * np.pi, 50)
    for i in range(len(iny_x)):
      frente_x = iny_x[i] + radio_invacion * np.cos(theta)
      frente_y = iny_y[i] + radio_invacion * np.sin(theta)
      frente_z = (
          -(frente_y * np.tan(np.radians(angulo_buzamiento)))
          - 200 * np.sin(np.pi * frente_x / 1000) * np.sin(np.pi * frente_y / 1000)
      )

      fig_3d.add_trace(
          go.Scatter3d(
              x=frente_x,
              y=frente_y,
              z=frente_z + 2,
              mode="lines",
              name=f"Frente Año {anio_actual} (Iny {i+1})",
              line=dict(color="cyan", width=4),
          )
      )

    fig_3d.add_trace(
        go.Scatter3d(
            x=iny_x,
            y=iny_y,
            z=iny_z,
            mode="markers+text",
            text=[f"Iny-{i+1}" for i in range(len(iny_x))],
            marker=dict(size=7, color="blue", symbol="diamond"),
            name="Inyectores",
        )
    )
    fig_3d.add_trace(
        go.Scatter3d(
            x=prod_x,
            y=prod_y,
            z=prod_z,
            mode="markers+text",
            text=[f"Prod-{i+1}" for i in range(len(prod_x))],
            marker=dict(size=7, color="red", symbol="circle"),
            name="Productores",
        )
    )

    fig_3d.update_layout(
        title=f"Frente de Barrido - Año {anio_actual}",
        scene=dict(
            xaxis_title="X [m]", yaxis_title="Y [m]", zaxis_title="Z [m]"
        ),
        height=550,
        margin=dict(l=0, r=0, b=0, t=40),
    )
    st.plotly_chart(fig_3d, use_container_width=True)
    st.info(
        f"💧 **Año {anio_actual}:** Radio de avance estimado = **{int(radio_invacion)} m**."
    )
