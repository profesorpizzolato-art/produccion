import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


def mostrar_mapa():
  st.header("🗺️ Mapa Interactivo de Campo MENFA - Yacimiento en Explotación")

  # --- 1. INICIALIZACIÓN DEL ESTADO (Solo ocurre una vez) ---
  if "df_pozos" not in st.session_state:
    # Pozos principales y locaciones críticas
    pozos_iniciales = [
        {
            "Nombre": "Pozo MENFA-001",
            "Sistema": "AIB (Mecánico)",
            "x": 200,
            "y": 250,
            "Estado": "Normal",
        },
        {
            "Nombre": "Pozo MENFA-002",
            "Sistema": "AIB (Mecánico)",
            "x": 350,
            "y": 550,
            "Estado": "⚠️ Falla Cuplas",
        },
        {
            "Nombre": "Pozo MENFA-003",
            "Sistema": "ESP (Sumergible)",
            "x": 500,
            "y": 400,
            "Estado": "Normal",
        },
        {
            "Nombre": "Planta Central Batería 2",
            "Sistema": "Instalación",
            "x": 500,
            "y": 500,
            "Estado": "🚨 Baja Presión",
        },
    ]

    # Generación masiva de pozos distribuidos en el yacimiento (simulando áreas o bloques)
    extras = []
    np.random.seed(42)  # Para que la distribución sea estable al recargar

    # Definimos bloques de desarrollo con sus sistemas de levantamiento típicos
    bloques = [
        {
            "sistema": "AIB (Mecánico)",
            "cant": 14,
            "x_range": (100, 450),
            "y_range": (100, 800),
        },
        {
            "sistema": "ESP (Sumergible)",
            "cant": 8,
            "x_range": (500, 800),
            "y_range": (200, 700),
        },
        {
            "sistema": "PCP (Tornillo)",
            "cant": 6,
            "x_range": (750, 950),
            "y_range": (100, 500),
        },
        {
            "sistema": "Inyector de Agua",
            "cant": 6,
            "x_range": (300, 700),
            "y_range": (150, 850),
        },
    ]

    contador = 10
    for b in bloques:
      sis_nombre = b["sistema"]
      for i in range(b["cant"]):
        # Generar prefijo según sistema
        pref = (
            "AIB"
            if "AIB" in sis_nombre
            else (
                "ESP"
                if "ESP" in sis_nombre
                else "PCP" if "PCP" in sis_nombre else "INY"
            )
        )
        extras.append({
            "Nombre": f"Pozo {pref}-{contador:03d}",
            "Sistema": sis_nombre,
            "x": int(np.random.uniform(b["x_range"][0], b["x_range"][1])),
            "y": int(np.random.uniform(b["y_range"][0], b["y_range"][1])),
            "Estado": (
                "Normal"
                if np.random.rand() > 0.15
                else "🔧 Mantenimiento"
            ),
        })
        contador += 1

    st.session_state.df_pozos = pd.DataFrame(pozos_iniciales + extras)

  # Usamos los datos guardados en la sesión
  df = st.session_state.df_pozos

  # --- 2. VISUALIZACIÓN ---
  col_map, col_ctrl = st.columns([3, 1])

  with col_map:
    # Gráfico de dispersión 2D tipo plano de yacimiento
    fig = px.scatter(
        df,
        x="x",
        y="y",
        color="Estado",
        symbol="Sistema",
        hover_name="Nombre",
        hover_data=["Sistema", "Estado"],
        color_discrete_map={
            "Normal": "#2ecc71",
            "⚠️ Falla Cuplas": "#f1c40f",
            "🚨 Baja Presión": "#e74c3c",
            "🔧 Mantenimiento": "#3498db",
        },
        title=(
            "Disposición Espacial del Yacimiento (Vista en Planta - Más de 30"
            " Activos)"
        ),
        labels={
            "x": "Coordenada Este (X) [m]",
            "y": "Coordenada Norte (Y) [m]",
        },
    )
    fig.update_traces(
        marker=dict(size=13, line=dict(width=1.5, color="White"))
    )
    fig.update_layout(
        template="plotly_dark",
        height=600,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
    )
    st.plotly_chart(fig, use_container_width=True)

  with col_ctrl:
    st.subheader("Panel de Control")
    st.write("Variar estado de activos:")

    target = st.selectbox("Seleccionar Pozo:", df["Nombre"].tolist())
    nuevo_estado = st.selectbox(
        "Nuevo Estado:",
        ["Normal", "⚠️ Falla Cuplas", "🚨 Baja Presión", "🔧 Mantenimiento"],
    )

    if st.button("Actualizar Campo"):
      idx = st.session_state.df_pozos[
          st.session_state.df_pozos["Nombre"] == target
      ].index[0]
      st.session_state.df_pozos.loc[idx, "Estado"] = nuevo_estado
      st.success(f"{target} actualizado correctamente.")
      st.rerun()

    st.markdown("---")
    st.metric("Total Pozos Activos", len(df))

  # --- 3. ALERTAS TÉCNICAS ---
  st.divider()
  st.subheader("⚠️ Reporte de Novedades Críticas en Campo")
  c1, c2 = st.columns(2)
  with c1:
    st.warning(
        "**POZO MENFA-002:** Requiere intervención. Fatiga detectada en cuplas"
        " (AIB)."
    )
  with c2:
    st.error(
        "**PLANTA CENTRAL BATERÍA 2:** Alarma de baja presión enmanifold de"
        " recepción."
    )
