import streamlit as st
from modulos.banco_preguntas import CUESTIONARIO_PRODUCCION

def evaluacion():
    st.header("📋 Centro de Evaluación Técnica - IPCL MENFA")
    st.write("Instructor: Fabricio Pizzolato")
    
    # Diccionarios para trackear categorías
    categorias = {
        "INGENIERÍA DE NODOS": {"correctas": 0, "total": 0},
        "PROCESAMIENTO": {"correctas": 0, "total": 0},
        "SEGURIDAD / ESD": {"correctas": 0, "total": 0},
        "DIAGNÓSTICO": {"correctas": 0, "total": 0}
    }
    
    respuestas_usuario = []

    for i, item in enumerate(CUESTIONARIO_PRODUCCION):
        # Mapeo de categorías basado en los bloques que definimos
        cat = ""
        if i in [0, 1]: cat = "INGENIERÍA DE NODOS"
        elif i in [2, 3, 5, 8]: cat = "PROCESAMIENTO"
        elif i in [6, 7]: cat = "SEGURIDAD / ESD"
        else: cat = "DIAGNÓSTICO"
        
        categorias[cat]["total"] += 1
        
        st.subheader(f"Pregunta {i+1} [{cat}]")
        if item["tipo"] == "TAREA":
            st.info(f"🛠️ **DESAFÍO PRÁCTICO:** {item['pregunta']}")
        else:
            st.write(item["pregunta"])
            
    res = st.radio(
    "Seleccione opción:", 
    item["opciones"],  # <--- Cambiado de 'options' a 'opciones'
    key=f"eval_{i}", 
    index=None
)

if res == item["opciones"][item["respuesta"]]: # <--- También cambiar aquí
    categorias[cat]["correctas"] += 1

    if st.button("📊 FINALIZAR Y GENERAR PERFIL DE COMPETENCIAS"):
        st.header("🎯 Resultado del Perfil Profesional")
        
        total_bien = sum(c["correctas"] for c in categorias.values())
        porcentaje_total = (total_bien / len(CUESTIONARIO_PRODUCCION)) * 100
        st.session_state.puntaje_alumno = porcentaje_total
        
        # --- DASHBOARD DE MÉTRICAS ---
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric("Puntaje General", f"{porcentaje_total}%")
            if porcentaje_total >= 70:
                st.success("APTO PARA OPERACIÓN")
            else:
                st.error("NO APTO - RECAPACITAR")

        with col2:
            # Mostramos el desglose por área
            for cat, datos in categorias.items():
                rendimiento = (datos["correctas"] / datos["total"]) * 100
                color = "green" if rendimiento >= 70 else "red"
                st.write(f"**{cat}:** {rendimiento}%")
                st.progress(rendimiento / 100)

        # --- RECOMENDACIÓN TÉCNICA ---
        st.subheader("💡 Feedback del Instructor")
        if categorias["SEGURIDAD / ESD"]["correctas"] < categorias["SEGURIDAD / ESD"]["total"]:
            st.warning("⚠️ Atención: Debes reforzar protocolos de seguridad. La operación de válvulas SDV es crítica.")
        if categorias["INGENIERÍA DE NODOS"]["correctas"] == categorias["INGENIERÍA DE NODOS"]["total"]:
            st.info("✅ Excelente comprensión de curvas IPR/VLP.")
            
        st.balloons()
