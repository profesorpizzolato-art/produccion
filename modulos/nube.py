import streamlit as st
import json

# Intentamos importar, si falla avisamos qué falta
try:
    from google.cloud import firestore
    from google.oauth2 import service_account
except ModuleNotFoundError:
    st.error("Falta instalar 'google-cloud-firestore'. Agregalo a requirements.txt")
import streamlit as st
import json
import base64
from google.cloud import firestore
from google.oauth2 import service_account

def conectar_db():
    try:
        # 1. Leemos el bloque codificado desde Secrets
        b64_str = st.secrets["gcp_service_account"]["content_b64"]
        
        # 2. Decodificamos y convertimos a diccionario
        json_data = base64.b64decode(b64_str).decode("utf-8")
        key_dict = json.loads(json_data)
        
        # 3. Conexión oficial
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
