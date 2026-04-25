import streamlit as st
import json

# Intentamos importar, si falla avisamos qué falta
try:
    from google.cloud import firestore
    from google.oauth2 import service_account
except ModuleNotFoundError:
    st.error("Falta instalar 'google-cloud-firestore'. Agregalo a requirements.txt")
def conectar_db():
    # 1. Leemos el diccionario desde los secrets
    key_dict = dict(st.secrets["textkey"])
    
    # 2. LIMPIEZA PROFUNDA DE LA LLAVE
    if "private_key" in key_dict:
        pk = key_dict["private_key"]
        
        # Eliminamos espacios accidentales al inicio y al final
        pk = pk.strip()
        
        # Corregimos los saltos de línea literales que a veces mete TOML
        pk = pk.replace("\\n", "\n")
        
        # Si por error se pegaron comillas extras, las sacamos
        pk = pk.replace('"', '').replace("'", "")
        
        # Aseguramos que los encabezados PEM sean correctos
        if "-----BEGIN PRIVATE KEY-----" not in pk:
            pk = "-----BEGIN PRIVATE KEY-----\n" + pk
        if "-----END PRIVATE KEY-----" not in pk:
            pk = pk + "\n-----END PRIVATE KEY-----"
            
        key_dict["private_key"] = pk

    # 3. Conexión
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
