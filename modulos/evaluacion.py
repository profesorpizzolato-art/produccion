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
    
    # 1. Agrupamos las respuestas dentro de un formulario para evitar que la página recargue con cada clic
    with st.form("examen_produccion"):
        for i, item in enumerate(CUESTIONARIO_PRODUCCION):
            # Asignación de categorías según el índice de la pregunta
            if i in [0, 1]: cat = "ING
