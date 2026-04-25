import streamlit as st
import json
import base64
from google.cloud import firestore
from google.oauth2 import service_account

def conectar_db():
    try:
        # 1. Obtenemos el string Base64 desde los Secrets
        b64_str = st.secrets["gcp_service_account"]["content_b64"]
        
        # 2. Limpiamos cualquier carácter basura (comillas, espacios)
        b64_str = b64_str.strip().replace('"', '').replace("'", "")
        
        # 3. Decodificamos a JSON plano
        decoded_bytes = base64.b64decode(b64_str)
        json_data = decoded_bytes.decode("utf-8").strip()
        
        # 4. Convertimos a diccionario
        key_dict = json.loads(json_data)
        
        # 5. Reparamos los saltos de línea de la private_key por si acaso
        if "private_key" in key_dict:
            key_dict["private_key"] = key_dict["private_key"].replace("\\n", "\n")
            
        creds = service_account.Credentials.from_service_account_info(key_dict)
        return firestore.Client(credentials=creds)
    except Exception as e:
        st.error(f"Error de conexión crítica: {e}")
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
    try:
        db = conectar_db()
        doc = db.collection("simulador").document("sala_emergencia").get()
        return doc.to_dict()
    except:
        return None

def resetear_planta():
    db = conectar_db()
    db.collection("simulador").document("sala_emergencia").set({"activo": False}, merge=True)
