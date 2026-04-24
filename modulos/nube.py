import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json

def conectar_db():
    # Lee las llaves desde la sección Secrets de Streamlit
    key_dict = json.loads(st.secrets["textkey"])
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
