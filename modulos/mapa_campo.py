import streamlit as st

def mapa_campo():

    st.title("Mapa del Campo Petrolero")
    st.subheader("Simulador MENFA")

    st.markdown("### Estado de Pozos")

    col1, col2, col3 = st.columns(3)

    p1 = col1.slider("Pozo A1 (BPD)",0,1000,400)
    p2 = col1.slider("Pozo A2 (BPD)",0,1000,350)

    p3 = col2.slider("Pozo B1 (BPD)",0,1000,300)
    p4 = col2.slider("Pozo B2 (BPD)",0,1000,250)

    p5 = col3.slider("Pozo C1 (BPD)",0,1000,200)
    p6 = col3.slider("Pozo C2 (BPD)",0,1000,150)

    st.markdown("---")

    def color_pozo(prod):

        if prod < 100:
            return "red"

        elif prod < 300:
            return "orange"

        else:
            return "green"

    st.markdown("### Mapa del Campo")

    st.markdown(
        f"""
        <div style="text-align:center">

        <div style="display:flex;justify-content:center;gap:40px">

        <div style="background:{color_pozo(p1)};padding:10px;border-radius:10px">Pozo A1</div>
        <div style="background:{color_pozo(p2)};padding:10px;border-radius:10px">Pozo A2</div>

        </div>

        <br>

        <div style="display:flex;justify-content:center;gap:40px">

        <div style="background:{color_pozo(p3)};padding:10px;border-radius:10px">Pozo B1</div>
        <div style="background:{color_pozo(p4)};padding:10px;border-radius:10px">Pozo B2</div>

        </div>

        <br>

        <div style="display:flex;justify-content:center;gap:40px">

        <div style="background:{color_pozo(p5)};padding:10px;border-radius:10px">Pozo C1</div>
        <div style="background:{color_pozo(p6)};padding:10px;border-radius:10px">Pozo C2</div>

        </div>

        <br>

        ↓

        <div style="background:lightblue;padding:12px;border-radius:10px">MANIFOLD</div>

        ↓

        <div style="background:lightgreen;padding:12px;border-radius:10px">SEPARADOR</div>

        ↓

        <div style="background:lightgray;padding:12px;border-radius:10px">TANQUES</div>

        </div>
        """,
        unsafe_allow_html=True
    )
