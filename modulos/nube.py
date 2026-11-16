import streamlit as st
import json
import base64
from google.cloud import firestore    
from google.oauth2 import service_account

def conectar_db():
    try:
        # 1. Obtenemos el string Base64 desde los Secrets de Streamlit
        b64_str = st.secrets["gcp_service_account"]["content_b64"]
        
        # 2. Limpiamos cualquier carácter basura (comillas, espacios)
        b64_str = b64_str.strip().replace('"', '').replace("'", "")
        
        # 3. Decodificamos a plano JSON
        bytes_decodificados = base64.b64decode(b64_str)
        json_data = bytes_decodificados.decode("utf-8").strip()
        
        # 4. Convertimos a diccionario
        key_dict = json.loads(json_data)
        
        # 5. Reparamos los saltos de línea de la private_key por si acaso
        if "private_key" in key_dict:
            key_dict["private_key"] = key_dict["private_key"].replace("\\n", "\n")
            
        # Generamos las credenciales y el cliente de Firestore
        credenciales = service_account.Credentials.from_service_account_info(key_dict)
        return firestore.Client(credentials=credenciales)
        
    except Exception as e:
        st.error(f"Error de conexión crítica con Firestore: {e}")
        raise e

def enviar_falla(nombre_falla, descripcion):
    db = conectar_db()
    # Al lanzar una falla nueva, seteamos 'respuesta' vacía para limpiar registros anteriores
    db.collection("simulador").document("sala_emergencia").set({
        "falla": nombre_falla,
        "descripción": descripcion,
        "activo": True,
        "respuesta": "",
        "timestamp": firestore.SERVER_TIMESTAMP
    })

def leer_estado_actual():
    try:
        db = conectar_db()
        doc = db.collection("simulador").document("sala_emergencia").get()
        if doc.exists:
            return doc.to_dict()
        return None
    except Exception:
        return None

def resetear_planta():
    db = conectar_db()
    # Al normalizar, desactivamos la alerta y limpiamos la respuesta vieja
    db.collection("simulador").document("sala_emergencia").set({
        "activo": False,
        "respuesta": ""
    }, merge=True)

def guardar_respuesta_alumno(respuesta_texto):
    try:
        db = conectar_db()
        # Guardamos la respuesta del alumno utilizando merge=True para no pisar la falla activa
        db.collection("simulador").document("sala_emergencia").set({
            "respuesta": respuesta_texto,
            "timestamp_respuesta": firestore.SERVER_TIMESTAMP
        }, merge=True)
        return True
    except Exception as e:
        st.error(f"Error al guardar respuesta del alumno: {e}")
        return False
