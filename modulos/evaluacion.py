import streamlit as st
from modulos.banco_preguntas import CUESTIONARIO_PRODUCCION

def evaluacion():
    st.header("📋 Centro de Evaluación Técnica - IPCL MENFA")
    st.write("Instructor: Fabricio Pizzolato")
    
    # 1. Inicializamos el estado del examen si no existe
    if 'examen_enviado' not in st.session_state:
        st.session_state.examen_enviado = False

    # 2. Creamos el Formulario de Examen
    with st.form("form_evaluacion"):
        respuestas_alumno = []
        
        for i, item in enumerate(CUESTIONARIO_PRODUCCION):
            st.subheader(f"Pregunta {i+1}")
            
            if item["tipo"] == "TAREA":
                st.info(f"🛠️ **DESAFÍO PRÁCTICO:** {item['pregunta']}")
            else:
                st.write(item["pregunta"])
            
            # Guardamos la opción elegida en una lista
            opcion = st.radio(
                "Seleccione la respuesta técnica:", 
                item["opciones"], 
                key=f"preg_{i}", 
                index=None
            )
            respuestas_alumno.append(opcion)
            st.divider()

        # Botón de envío dentro del formulario
        enviado = st.form_submit_button("📊 FINALIZAR Y GENERAR PERFIL DE COMPETENCIAS")

    # 3. Lógica de Calificación (se ejecuta al presionar el botón)
    if enviado:
        categorias = {
            "INGENIERÍA DE NODOS": {"correctas": 0, "total": 0},
            "PROCESAMIENTO": {"correctas": 0, "total": 0},
            "SEGURIDAD / ESD": {"correctas": 0, "total": 0},
            "DIAGNÓSTICO": {"correctas": 0, "total": 0}
        }

        # Procesamos cada respuesta
        for i, res in enumerate(respuestas_alumno):
            # Asignación de categorías por índice
            if i in [0, 1]: cat = "INGENIERÍA DE NODOS"
            elif i in [2, 3, 5, 8]: cat = "PROCESAMIENTO"
            elif i in [6, 7]: cat = "SEGURIDAD / ESD"
            else: cat = "DIAGNÓSTICO"
            
            categorias[cat]["total"] += 1
            
            # Verificamos si la respuesta es correcta
            if res == CUESTIONARIO_PRODUCCION[i]["opciones"][CUESTIONARIO_PRODUCCION[i]["respuesta"]]:
                categorias[cat]["correctas"] += 1

        # --- MOSTRAR RESULTADOS ---
        st.session_state.examen_enviado = True
        total_bien = sum(c["correctas"] for c in categorias.values())
        porcentaje = (total_bien / len(CUESTIONARIO_PRODUCCION)) * 100
        st.session_state.puntaje_alumno = porcentaje

        st.header("🎯 Resultado del Perfil Profesional")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Puntaje General", f"{porcentaje}%")
            if porcentaje >= 70:
                st.success("APTO PARA OPERACIÓN")
                st.balloons()
            else:
                st.error("NO APTO - RECAPACITAR")

        with col2:
            for cat, datos in categorias.items():
                rend = (datos["correctas"] / datos["total"]) * 100
                st.write(f"**{cat}:** {rend}%")
                st.progress(rend / 100)

        # Feedback de seguridad
        if categorias["SEGURIDAD / ESD"]["correctas"] < categorias["SEGURIDAD / ESD"]["total"]:
            st.warning("⚠️ Reforzar protocolos de seguridad y válvulas SDV.")
