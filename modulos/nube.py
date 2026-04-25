import streamlit as st
import json

# Intentamos importar, si falla avisamos qué falta
try:
    from google.cloud import firestore
    from google.oauth2 import service_account
except ModuleNotFoundError:
    st.error("Falta instalar 'google-cloud-firestore'. Agregalo a requirements.txt")
def conectar_db():
    # 1. Convertimos los secretos a un diccionario real de Python
    # Streamlit a veces devuelve un objeto 'AtributeDict', por eso usamos dict()
    key_dict = dict(st.secrets["textkey"])
    
    if "private_key" in key_dict:
        pk = str(key_dict["private_key"])
        
        # --- LIMPIEZA QUIRÚRGICA ---
        # 1. Quitamos los encabezados para limpiar el "corazón" de la llave
        header = "-----BEGIN PRIVATE KEY-----"
        footer = "-----END PRIVATE KEY-----"
        
        if header in pk and footer in pk:
            # Extraemos solo el contenido entre los guiones
            contenido = pk.split(header)[1].split(footer)[0]
            # Borramos: espacios, saltos de línea, tabulaciones y comillas
            contenido = contenido.replace("\\n", "").replace("\n", "").replace(" ", "").replace('"', '').replace("'", "").strip()
            
            # 2. Reconstruimos el PEM con el formato exacto que exige Google
            # El contenido debe ser una sola tira de texto entre los encabezados
            pk_limpia = f"{header}\n{contenido}\n{footer}\n"
            key_dict["private_key"] = pk_limpia

    # 3. Intento de conexión con manejo de error específico
    try:
        creds = service_account.Credentials.from_service_account_info(key_dict)
        return firestore.Client(credentials=creds)
    except Exception as e:
        st.error(f"Error en la llave de Google: {e}")
        st.info("Revisá que en Secrets la 'private_key' no tenga espacios extra.")
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
