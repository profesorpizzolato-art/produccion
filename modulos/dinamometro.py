import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def dinamometro(profundidad=8000, agua=10, gor=500, q=1000):
    st.markdown("### 📈 Diagnóstico de Fondo")
    
    # --- 1. CÁLCULOS DE CARGA (Libras) ---
    # Peso de las varillas (estático)
    carga_min = profundidad * 1.6 
    # Peso de varillas + peso del fluido (BSW afecta la densidad)
    carga_max = carga_min + (profundidad * 0.433 * (1 + (agua/100)*0.05))
    
    # --- 2. MODELADO DE LA CARTA ---
    # Carrera (0 a 100 pulgadas)
    stroke = 100
    # Efecto de gas: redondea las esquinas superiores e inferiores
    gas_sharpness = max(2, 50 - (gor / 100)) 
    # Llenado: si el caudal es bajo respecto al potencial, hay "golpe de fluido"
    llenado = max(0.4, min(1.0, q / 1500))

    # Generamos los puntos del ciclo (Ascendente y Descendente)
    t = np.linspace(0, 2 * np.pi, 200)
    
    # X es la posición (onda senoidal para suavizar)
    x = (np.cos(t) + 1) * (stroke / 2)
    
    # Y es la carga con lógica de histéresis (forma de paralelogramo)
    y_base = np.sign(np.sin(t))
    y = []
    
    for i in range(len(t)):
        if np.sin(t[i]) > 0: # Carrera ascendente
            val = carga_max - (carga_max - carga_min) * 0.1 * np.exp(-x[i]/10)
        else: # Carrera descendente
            # Aplicamos el "golpe de fluido" si llenado < 1
            if x[i] > (stroke * (1 - llenado)):
                val = carga_min + (carga_max - carga_min) * 0.1
            else:
                val = carga_max - (carga_max - carga_min) * 0.8
        y.append(val)

    # Suavizado técnico para que parezca una carta real de campo
    y = np.convolve(y, np.ones(10)/10, mode='same')

    # --- 3. EL GRÁFICO ESPECTACULAR ---
    fig, ax = plt.subplots(figsize=(7, 5))
    
    # Dibujamos la carta
    ax.plot(x, y, color='#004c6d', lw=3, label="Ciclo de Bombeo")
    ax.fill(x, y, color='#004c6d', alpha=0.1)

    # Formato de ingeniería
    ax.set_title("Carta Dinamométrica de Superficie", fontsize=14, fontweight='bold')
    ax.set_xlabel("Posición (pulgadas)")
    ax.set_ylabel("Carga en la Barra Pulida (lbs)")
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # Añadimos flechas de sentido de giro
    ax.annotate('', xy=(stroke*0.8, carga_max), xytext=(stroke*0.2, carga_max),
                arrowprops=dict(arrowstyle="->", color='gray'))
    
    # Alertas visuales dentro del gráfico
    if gor > 1200:
        ax.text(stroke*0.1, (carga_max + carga_min)/2, "⚠️ Interferencia de Gas", color='orange', fontweight='bold')
    if llenado < 0.7:
        ax.text(stroke*0.5, carga_min - 1000, "❌ GOLPE DE FLUIDO", color='red', fontweight='bold')

    st.pyplot(fig)
    
    # --- 4. CUADRO DE DATOS TÉCNICOS ---
    c1, c2 = st.columns(2)
    c1.metric("Carga Máxima (PPRL)", f"{int(max(y))} lbs")
    c2.metric("Carga Mínima (MPRL)", f"{int(min(y))} lbs")
