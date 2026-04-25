import streamlit as st
import json

# Intentamos importar, si falla avisamos qué falta
try:
    from google.cloud import firestore
    from google.oauth2 import service_account
except ModuleNotFoundError:
    st.error("Falta instalar 'google-cloud-firestore'. Agregalo a requirements.txt")

def conectar_db():
    # 1. Obtenemos el secreto
    secret_data = st.secrets["textkey"]
    
    # 2. Verificamos si es un string o ya es un diccionario
    if isinstance(secret_data, str):
        # Si es texto (string), lo cargamos como JSON
        key_dict = json.loads(secret_data)
    else:
        # Si ya es un diccionario (dict), lo usamos directo
        key_dict = secret_data
        
    # 3. Conectamos con las credenciales
    creds = service_account.Credentials.from_service_account_info(key_dict)
    return firestore.Client(credentials=creds)

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
