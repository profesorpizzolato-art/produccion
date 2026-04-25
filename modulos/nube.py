import streamlit as st
import json
import base64
from google.cloud import firestore
from google.oauth2 import service_account

def conectar_db():
    try:
        # Recupera el bloque codificado desde Secrets
        b64_str = st.secrets["gcp_service_account"]["content_b64"]
        b64_str = b64_str.strip().replace('"', '').replace("'", "")
        
        # Decodifica y limpia
        json_data = base64.b64decode(b64_str).decode("utf-8").strip()
        key_dict = json.loads(json_data)
        
        # Repara saltos de línea de la private_key
        if "private_key" in key_dict:
            key_dict["private_key"] = key_dict["private_key"].replace("\\n", "\n")
            
        creds = service_account.Credentials.from_service_account_info(key_dict)
        return firestore.Client(credentials=creds)
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        raise e

def enviar_falla(nombre_falla, descripcion):
    db = conectar_db()
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
    db.collection("simulador").document("sala_emergencia").set({"activo": False}, merge=True)
