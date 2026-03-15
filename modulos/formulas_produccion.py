import streamlit as st

def formulas_produccion():

    st.title("Fórmulas de Producción Petrolera")
    st.subheader("IPCL MENFA - Cálculos Operativos")

    menu = st.selectbox(
        "Seleccionar cálculo",
        [
            "Índice de Productividad (PI)",
            "Corte de Agua",
            "Relación Gas-Petróleo (GOR)",
            "Gradiente Hidrostático",
            "Producción Bombeo Mecánico"
        ]
    )

    # PI

    if menu == "Índice de Productividad (PI)":

        st.write("PI = Q / (Pr - Pwf)")

        q = st.number_input("Producción BPD",100.0)
        pr = st.number_input("Presión reservorio psi",3000.0)
        pwf = st.number_input("Presión fondo fluyente psi",1500.0)

        if st.button("Calcular PI"):

            pi = q / (pr - pwf)

            st.metric("Índice de Productividad",round(pi,3))

    # CORTE DE AGUA

    elif menu == "Corte de Agua":

        st.write("WC = Agua / (Agua + Petróleo)")

        agua = st.number_input("Agua BPD",200.0)
        petroleo = st.number_input("Petróleo BPD",800.0)

        if st.button("Calcular WC"):

            wc = agua / (agua + petroleo)

            st.metric("Corte de Agua (%)",round(wc*100,2))

    # GOR

    elif menu == "Relación Gas-Petróleo (GOR)":

        st.write("GOR = Gas / Petróleo")

        gas = st.number_input("Gas m3/d",5000.0)
        petroleo = st.number_input("Petróleo BPD",1000.0)

        if st.button("Calcular GOR"):

            gor = gas / petroleo

            st.metric("GOR",round(gor,2))

    # GRADIENTE

    elif menu == "Gradiente Hidrostático":

        st.write("Gradiente = 0.433 × densidad")

        densidad = st.number_input("Densidad del fluido (sg)",1.0)

        if st.button("Calcular Gradiente"):

            gradiente = 0.433 * densidad

            st.metric("Gradiente psi/ft",round(gradiente,3))

    # BOMBEO MECANICO

    elif menu == "Producción Bombeo Mecánico":

        st.write("Q = Carrera × SPM × Eficiencia")

        carrera = st.number_input("Carrera pulgadas",80.0)
        spm = st.number_input("Golpes por minuto",8.0)
        eficiencia = st.number_input("Eficiencia %",75.0)

        if st.button("Calcular Producción"):

            q = carrera * spm * (eficiencia/100)

            st.metric("Producción estimada",round(q,2))
