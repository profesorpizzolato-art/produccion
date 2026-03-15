import streamlit as st
import pandas as pd
import numpy as np

def campo_petrolero():

    st.title("Simulador de Campo Petrolero")
    st.subheader("Simulador MENFA - Producción de Campo")

    st.markdown("---")

    st.write("Ajuste la producción de cada pozo")

    col1, col2, col3 = st.columns(3)

    pozo1 = col1.slider("Pozo A1 (BPD)", 0, 1000, 400)
    pozo2 = col1.slider("Pozo A2 (BPD)", 0, 1000, 350)

    pozo3 = col2.slider("Pozo B1 (BPD)", 0, 1000, 300)
    pozo4 = col2.slider("Pozo B2 (BPD)", 0, 1000, 250)

    pozo5 = col3.slider("Pozo C1 (BPD)", 0, 1000, 200)
    pozo6 = col3.slider("Pozo C2 (BPD)", 0, 1000, 150)

    st.markdown("---")

    produccion_total = pozo1 + pozo2 + pozo3 + pozo4 + pozo5 + pozo6

    st.metric("Producción total del campo", f"{produccion_total} BPD")

    st.markdown("---")

    datos = pd.DataFrame({
        "Pozo": ["A1","A2","B1","B2","C1","C2"],
        "Producción": [pozo1,pozo2,pozo3,pozo4,pozo5,pozo6]
    })

    st.bar_chart(datos.set_index("Pozo"))

    st.markdown("---")

    if produccion_total > 3500:

        st.warning("Producción muy alta para capacidad de planta")

    elif produccion_total < 1000:

        st.error("Producción de campo muy baja")

    else:

        st.success("Producción dentro del rango operativo")
