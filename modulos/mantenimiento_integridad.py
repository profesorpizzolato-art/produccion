import streamlit as st
import time

@st.dialog("🛠️ Generación de Orden de Trabajo (OT-AIB-001)")
def modal_reparacion_aib(motor):
    st.write("¿Confirmar inicio de mantenimiento correctivo/preventivo sobre el Motor AIB MENFA-001?")
    st.caption("Esta acción pausará la marcha y reseteará el acumulador a 0.0 hs tras el ciclo de trabajo.")

    if st.button("🔴 Confirmar y Ejecutar OT (45 seg)"):
        motor.reparando_aib = True
        progreso = st.progress(0, text="Iniciando intervención de mantenimiento...")
        
        # Simulación de reparación regresiva/progresiva de 45 segundos
        for i in range(100):
            time.sleep(0.45) # 0.45s * 100 = 45 segundos totales
            progreso.progress(i + 1, text=f"Ejecutando servicio en campo... {i + 1}% (45s total)")

        motor.horas_motor_aib = 0.0
        motor.falla_mecanica_aib = False
        motor.reparando_aib = False
        st.success("✅ OT Finalizada. Motor AIB restablecido a 0.0 hs de marcha.")
        time.sleep(1)
        st.rerun()

def mostrar_mantenimiento_integridad():
    st.title("🛠️ Mantenimiento e Integridad de Activos")

    if 'motor' not in st.session_state:
        st.error("⚠️ Motor no disponible.")
        return

    motor = st.session_state.motor
    motor.actualizar_ciclo()

    st.subheader("⚙️ Monitoreo de Marcha y Desgaste: Motor AIB MENFA-001")

    # Indicadores de Estado
    col1, col2, col3 = st.columns(3)
    col1.metric("Horas de Marcha Acumuladas", f"{round(motor.horas_motor_aib, 2)} hs")
    col2.metric("Régimen de Bombeo (SPM)", f"{motor.spm_aib} SPM")
    
    if motor.falla_mecanica_aib:
        col3.error("💥 CATASTRÓFICO: Falla por Fatiga")
    elif motor.horas_motor_aib > 4800:
        col3.warning("⚠️ ALERTA: Requiere Service")
    else:
        col3.success("🟢 Normal")

    # Bloque de Alerta por Falla Mecánica
    if motor.falla_mecanica_aib:
        st.error("🚨 EL MOTOR SE APAGÓ AUTOMÁTICAMENTE: Se superaron las 4,850 hs operando a más de 10 SPM. Ocurrió corte por fatiga mecánica de cuplas.")

    st.divider()

    # Botón Modal para OT
    if st.button("📋 Generar Orden de Trabajo (OT)"):
        modal_reparacion_aib(motor)
