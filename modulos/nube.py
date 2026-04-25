import streamlit as st
import json

# Intentamos importar, si falla avisamos qué falta
try:
    from google.cloud import firestore
    from google.oauth2 import service_account
except ModuleNotFoundError:
    st.error("Falta instalar 'google-cloud-firestore'. Agregalo a requirements.txt")
def conectar_db():
    import json
    # Buscamos el secreto que crearemos en el paso siguiente
    try:
        # Intentamos leerlo como un diccionario directo (Streamlit lo hace si el formato es correcto)
        key_dict = dict(st.secrets["gcp_service_account"])
        
        # Corregimos los saltos de línea que son el 99% del problema
        if "private_key" in key_dict:
            key_dict["private_key"] = key_dict["private_key"].replace("\\n", "\n")
            
        creds = service_account.Credentials.from_service_account_info(key_dict)
        return firestore.Client(credentials=creds)
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        raise e

def enviar_falla(nombre_falla, descripcion):
    db = conectar_db()
    # Escribimos en un documento fijo para que el alumno lo lea
    db.collection("simulador").document("sala_emergencia").set({
        "falla": nombre_falla,
        "descripcion": descripcion,
        "activo": True,
        "timestamp": firestore.SERVER_TIMESTAMP
    })

def leer_estado_actual():
    db = conectar_db()
    doc = db.collection("simulador").document("sala_emergencia").get()
    return doc.to_dict()

def resetear_planta():
    db = conectar_db()
    db.collection("simulador").document("sala_emergencia").update({"activo": False})
