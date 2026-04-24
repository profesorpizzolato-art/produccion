import streamlit as st
import sys
import os
from modulos.nube import leer_estado_actual
from modulos.nube import leer_estado_actual, enviar_falla, resetear_planta, conectar_db

def verificar_emergencias_remotas():
    estado = leer_estado_actual()
    
    if estado and estado.get("activo"):
        # Bloqueo Visual de Emergencia
        st.markdown("<style>body {background-color: #3e0000 !important;}</style>", unsafe_allow_html=True)
        
        st.error(f"🚨 EMERGENCIA LANZADA POR EL INSTRUCTOR")
        st.header(estado['falla'])
        st.warning(estado['descripcion'])
        
        respuesta = st.text_area("Procedimiento de Maniobra:", placeholder="Ej: Cerrar válvula maestra, abrir bypass...")
        
        if st.button("Enviar Respuesta"):
            # Aquí podrías guardar la respuesta en otra colección de la DB
            st.success("Maniobra reportada. Espere a que el instructor normalice la planta.")
# 1. CONFIGURACIÓN (Debe ser lo primero absoluto)
st.set_page_config(page_title="IPCL MENFA - Simulador 3.0", layout="wide")

# 2. MANEJO DE RUTAS
sys.path.append(os.path.join(os.path.dirname(__file__), "modulos"))
sys.path.append(os.path.join(os.path.dirname(__file__), "motor"))

# 3. ESTADO DE SESIÓN (Inicialización segura)
if 'ingresado' not in st.session_state: 
    st.session_state.ingresado = False
if 'rol' not in st.session_state: 
    st.session_state.rol = "alumno"
if 'area_actual' not in st.session_state: 
    st.session_state.area_actual = "🏠 Dashboard"

# 4. IMPORTACIONES
from modulos.dashboard_principal import dashboard_principal
from modulos.pozo_productor import pozo_productor
from modulos.planta_produccion import planta_produccion
from modulos.gestion_supervisor_prod import gestion_supervisor_prod
from modulos.evaluacion import evaluacion
from modulos.ingenieria import mostrar_ingenieria # Agregá esta importación

# --- SISTEMA DE ACCESO ---
def login():
    st.title("🔒 Acceso IPCL MENFA")
    u = st.text_input("Usuario")
    p = st.text_input("Contraseña", type="password")
    if st.button("INGRESAR"):
        if (u == "admin" and p == "menfa2026") or (u == "alumno" and p == "alumno2026"):
            st.session_state.ingresado = True
            st.session_state.rol = "instructor" if u == "admin" else "alumno"
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

# --- APLICACIÓN PRINCIPAL ---
def main_app():
    opciones = [
        "🏠 Dashboard", 
        "🛢️ Operaciones de Campo",
        "🗺️ Mapa del Campo", 
        "📊 Campo Petrolero",
        "🏭 Planta de Proceso",
        "📦 Equipos de Planta",
        "📈 Ingeniería",
        "🖥️ Monitoreo SCADA",
        "📋 Gestión y Reportes",
        "🛠️ Mantenimiento e Integridad",
        "🧠 Evaluación",
        "🎯 Entrenamiento Operativo",
        "📘 Manual"
    ]

    # --- MENÚ LATERAL ---
    with st.sidebar:
        # Asegúrate de que assets/logo_menfa.png exista
        try:
            st.image("assets/logo_menfa.png") 
        except:
            st.warning("Logo no encontrado en assets/")
            
        st.title("🛠️ Panel de Control")
        st.write(f"👤 **Rol:** {st.session_state.rol.upper()}")
        st.write("Instructor: Fabricio Pizzolato")
        st.divider()
        
        # Sincronización: El radio lee de area_actual
        try:
            indice_actual = opciones.index(st.session_state.area_actual)
        except ValueError:
            indice_actual = 0

        area = st.radio("Navegación:", opciones, index=indice_actual)
        
        # Si el usuario cambia el radio, actualizamos el estado global
        if area != st.session_state.area_actual:
            st.session_state.area_actual = area
            st.rerun()
        
        if st.button("🚪 Salir"):
            st.session_state.clear()
            st.rerun()

 # --- MOTOR DE EJECUCIÓN (Corrección de Rutas) ---
    actual = st.session_state.area_actual

    if actual == "🏠 Dashboard":
        from modulos.dashboard_principal import dashboard_principal
        dashboard_principal()

    elif actual == "🛢️ Operaciones de Campo":
        from modulos.pozo_productor import pozo_productor
        pozo_productor()

    elif actual == "🗺️ Mapa del Campo":
        from modulos.mapa_campo import mostrar_mapa
        mostrar_mapa()

    elif actual == "📊 Campo Petrolero":
        from modulos.campo_petrolero import mostrar_estadisticas
        mostrar_estadisticas()

    elif actual == "🏭 Planta de Proceso":
        from modulos.planta_produccion import planta_produccion
        planta_produccion()
        
    elif actual == "📦 Equipos de Planta":  # <--- Corregido: de 'seleccion' a 'actual'
        from modulos.equipos_planta import mostrar_equipos_planta # <--- Agregamos la importación
        mostrar_equipos_planta() 

    elif actual == "📈 Ingeniería":
        from modulos.ingenieria import mostrar_ingenieria
        mostrar_ingenieria()

    elif actual == "🖥️ Monitoreo SCADA":
        from modulos.scada import show
        show()

    elif actual == "📋 Gestión y Reportes":
        # Corregido: Importamos el nombre correcto del archivo y la función
        from modulos.gestion_supervisor_prod import gestion_supervisor_prod
        gestion_supervisor_prod()
    elif actual == "🛠️ Mantenimiento e Integridad":
        from modulos.mantenimiento_integridad import mostrar_mantenimiento_integridad
        mostrar_mantenimiento_integridad()
    elif actual == "🎯 Entrenamiento Operativo":
        from modulos.entrenamiento import mostrar_entrenamiento
        mostrar_entrenamiento()

    elif actual == "🧠 Evaluación":
        from modulos.evaluacion import evaluacion
        evaluacion()

    elif actual == "📘 Manual":
        from modulos.manual_simulador import mostrar_manual
        mostrar_manual()
    import streamlit as st
# Importamos las funciones que creamos antes
from modulos.nube import enviar_falla, resetear_planta, conectar_db
def modulo_instructor_pizzolato():
    st.title("👨‍🏫 Panel de Control Maestro (Instructor)")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🚀 Inyectar Falla en Tiempo Real")
        falla_nombre = st.selectbox("Seleccione el incidente:", [
            "Fuga de H2S en Manifold",
            "Cavitación en Bomba P-101",
            "BSW Fuera de Especificación",
            "Pérdida de Presión en Línea de Venta",
            "Parada de Emergencia (ESD) Activada"
        ])
        
        detalles = st.text_area("Descripción detallada del síntoma:", 
                                 "El manómetro de entrada muestra una caída de 5 psi y se activa la alarma visual.")
        
        if st.button("🔴 LANZAR FALLA A LOS ALUMNOS"):
            enviar_falla(falla_nombre, detalles)
            st.error(f"FALLA LANZADA: {falla_nombre}")
            st.toast("La planta de los alumnos ha sido alterada.")

    with col2:
        st.subheader("🛡️ Gestión de Planta")
        if st.button("🟢 NORMALIZAR OPERACIÓN"):
            resetear_planta()
            st.success("Planta reseteada a condiciones normales.")
            st.balloons()
            
        st.divider()
        st.write("**Estado de Conexión:**")
        # Aquí podrías consultar quién está conectado
        st.write("📡 Servidor Firebase: Activo")

    # --- SECCIÓN DE MONITOREO DE RESPUESTAS ---
    st.markdown("---")
    st.subheader("📥 Respuestas de Alumnos en Vivo")
    
    db = conectar_db()
    # Leemos la respuesta que el alumno escribió en la DB
    doc = db.collection("simulador").document("sala_emergencia").get().to_dict()
    
    if doc and doc.get("respuesta_alumno"):
        st.info(f"**Última respuesta recibida:**\n\n {doc['respuesta_alumno']}")
        
        # Sistema de calificación rápida
        puntos = st.slider("Calificar maniobra:", 0, 100, 70)
        if st.button("Validar y Calificar"):
            # Aquí podrías guardar la nota en el legajo del alumno
            st.success(f"Nota de {puntos} enviada al historial.")
    else:
        st.write("Esperando respuestas de maniobras...")

if __name__ == "__main__":
    main()
def main():
    st.sidebar.title("Navegación IPCL")
    
    # Selector de Rol para separar las aguas
    rol = st.sidebar.radio("Seleccione su Rol:", ["Alumno", "Instructor"])

    if rol == "Instructor":
        # Ponemos una contraseña simple para que los alumnos no entren
        clave = st.sidebar.text_input("Clave de Acceso:", type="password")
        if clave == "menfa2026": # Podés cambiar esta clave
            modulo_instructor_pizzolato()
        else:
            st.sidebar.warning("Clave incorrecta")
            st.info("Ingrese la clave de instructor para acceder al panel de control.")
    
    else:
        # Aquí va la lógica normal del alumno
        simulador_alumno()    
# --- FLUJO PRINCIPAL ---
if not st.session_state.ingresado:
    login()
else:
    main_app()
