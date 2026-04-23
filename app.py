import streamlit as st
import sys
import os

# AGREGAR CARPETA MODULOS AL CAMINO DE PYTHON
sys.path.append(os.path.join(os.path.dirname(__file__), "modulos"))

# IMPORTACIONES (Asegúrate de que estos archivos existan en /modulos)
from modulos.dashboard_principal import dashboard_principal
from modulos.pozo_productor import pozo_productor
from modulos.planta_produccion import planta_produccion
from modulos.gestion_supervisor_prod import gestion_supervisor_prod
from modulos import evaluacion as modulo_evaluacion
from modulos.banco_preguntas import CUESTIONARIO_PRODUCCION

def main():
    # Aquí sí va sangría (4 espacios)
    st.title("Simulador de Producción")
    
    # Supongamos que aquí llamas a la evaluación
    if st.sidebar.button("Ir a Evaluación"):
        modulo_evaluacion.evaluacion()

if __name__ == "__main__":
    main()

# CONFIGURACIÓN
st.set_page_config(page_title="IPCL MENFA - Simulador 3.0", layout="wide")

# ESTADO DE SESIÓN
if 'ingresado' not in st.session_state: st.session_state.ingresado = False
if 'rol' not in st.session_state: st.session_state.rol = "alumno"

# --- LOGIN (Simplificado) ---
if not st.session_state.ingresado:
    st.title("🔒 Acceso IPCL MENFA")
    u = st.text_input("Usuario")
    p = st.text_input("Contraseña", type="password")
    if st.button("INGRESAR"):
        if (u == "admin" and p == "menfa2026") or (u == "alumno" and p == "alumno2026"):
            st.session_state.ingresado = True
            st.session_state.rol = "instructor" if u == "admin" else "alumno"
            st.rerun()
    st.stop()

# --- MENÚ LATERAL ORGANIZADO ---
with st.sidebar:
    st.image("assets/logo_menfa.png")
    st.write(f"👤 **Rol:** {st.session_state.rol.upper()}")
    st.divider()
    
    # Agrupamos la info para que no haya botones vacíos
    area = st.radio("Áreas de la Planta:", [
        "🏠 Dashboard", 
        "🛢️ Campo y Pozos", 
        "🏭 Planta de Tratamiento", 
        "📋 Consola de Supervisión",
        "🧠 Evaluación"
    ])
    
    if st.button("🚪 Salir"):
        st.session_state.clear()
        st.rerun()

# --- MOTOR DE EJECUCIÓN (Aquí conectamos toda la info) ---
if area == "🏠 Dashboard":
    dashboard_principal()

elif area == "🛢️ Campo y Pozos":
    # Aquí unimos mapa, estado de pozo y choke control
    tab1, tab2 = st.tabs(["📍 Estado del Pozo", "⚙️ Control de Choke"])
    with tab1: pozo_productor()
    with tab2: st.info("Simulador de presión en cabeza de pozo (Choke Manifold).")

elif area == "🏭 Planta de Tratamiento":
    # Aquí unimos P&ID, SCADA y Proceso
    tab1, tab2 = st.tabs(["🏗️ Operación de Planta", "🖥️ Sistema SCADA"])
    with tab1: planta_produccion()
    with tab2: st.warning("Monitoreo en tiempo real de Tanques de Lavado (13.9 ft).")

elif area == "📋 Consola de Supervisión":
    # Feedback Instructor-Alumno (Toda la info de PDVSA y Gas)
    gestion_supervisor_prod()

elif area == "🧠 Evaluación":
    evaluacion()

def main():
    # --- SIDEBAR: Selector de Módulos ---
    st.sidebar.title("🛠️ Panel de Control")
    st.sidebar.write("Instructor: Fabricio Pizzolato")
    
    categoria = st.sidebar.selectbox(
        "Seleccione Área",
        ["Operaciones de Campo", "Monitoreo SCADA", "Ingeniería y Análisis", "Gestión y Reportes", "Evaluación"]
    )

    # Lógica de navegación dinámica
    if categoria == "Operaciones de Campo":
        modulo = st.sidebar.radio("Módulo", [
            "Campo Petrolero", "Bomba Mecánica", "Manifold Avanzado", 
            "Planta de Producción", "Pozo Productor", "Checklist Operativo"
        ])
        
        if modulo == "Bomba Mecánica":
            import modulos.bomba_mecanica as bm
            bm.show()
        elif modulo == "Manifold Avanzado":
            import modulos.manifold_avanzado as ma
            ma.show()
        # ... seguir con los demás

    elif categoria == "Monitoreo SCADA":
        modulo = st.sidebar.radio("Módulo", ["SCADA Principal", "Alarmas", "Diagrama de Planta"])
        if modulo == "SCADA Principal":
            import modulos.scada as scada
            scada.show()

    elif categoria == "Ingeniería y Análisis":
        modulo = st.sidebar.radio("Módulo", ["IPR/VLP", "Dinamómetro", "Flujo Multifásico", "Fórmulas"])
        if modulo == "Dinamómetro":
            import modulos.dinamometro as din
            din.show()

    elif categoria == "Gestión y Reportes":
        modulo = st.sidebar.radio("Módulo", ["Company Man", "Reporte de Novedades", "Certificado"])
        if modulo == "Reporte de Novedades":
            import modulos.reporte_novedades as rn
            rn.show()

    elif categoria == "Evaluación":
        import modulos.evaluacion as ev
        ev.generar_evaluacion()

if __name__ == "__main__":
    main()
