import streamlit as st
import paho.mqtt.client as mqtt
import json
import time

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================

st.set_page_config(
    page_title="Sistema IoT",
    page_icon="💡",
    layout="wide"
)

# =====================================================
# MQTT
# =====================================================

BROKER = "broker.mqttdashboard.com"
PORT = 1883
TOPIC = "sg/iot1"

# =====================================================
# CLIENTE MQTT
# =====================================================

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION1,
    client_id="streamlit-control"
)

mqtt_ok = False

try:
    client.connect(BROKER, PORT)
    client.loop_start()
    mqtt_ok = True
except Exception as e:
    mqtt_ok = False
    st.error(f"Error MQTT: {e}")

# =====================================================
# FUNCIONES MQTT
# =====================================================

def enviar_led(dispositivo, estado):

    mensaje = {
        "dispositivo": dispositivo,
        "estado": estado
    }

    client.publish(TOPIC, json.dumps(mensaje))


def enviar_puerta(accion):

    mensaje = {
        "puerta": accion
    }

    client.publish(TOPIC, json.dumps(mensaje))


# =====================================================
# TÍTULO
# =====================================================

st.title("🏠 Sistema IoT")
st.markdown("---")

# =====================================================
# ESTADO MQTT
# =====================================================

if mqtt_ok:
    st.success("✅ Conectado al Broker MQTT")
else:
    st.error("❌ No conectado al Broker MQTT")

# =====================================================
# SECCIÓN LEDS
# =====================================================

st.header("💡 Control de Bombillos LED")

st.write("Control táctil de iluminación")

col1, col2, col3 = st.columns(3)

# =====================================================
# LED 1
# =====================================================

with col1:

    st.subheader("Sala")

    led1 = st.toggle("prender/apagar")

    if led1:

        enviar_led("led1", "on")

        st.success("Bombillo encendido")

    else:

        enviar_led("led1", "off")

        st.warning("Bombillo apagado")

# =====================================================
# LED 2
# =====================================================

with col2:

    st.subheader("Cocina")

    led2 = st.toggle("prender/apagar")

    if led2:

        enviar_led("led2", "on")

        st.success("Bombillo encendido")

    else:

        enviar_led("led2", "off")

        st.warning("Bombillo apagado")

# =====================================================
# LED 3
# =====================================================

with col3:

    st.subheader("Baño")

    led3 = st.toggle("prender/apagar")

    if led3:

        enviar_led("led3", "on")

        st.success("Bombillo encendido")

    else:

        enviar_led("led3", "off")

        st.warning("Bombillo apagado")

# =====================================================
# SEPARADOR
# =====================================================

st.markdown("---")

# =====================================================
# CONTROL DE PUERTA
# =====================================================

st.header("🚪 Sistema Inteligente de Puerta")

st.write(
    """
    Escribe comandos como:

    - abre la puerta
    - abrir puerta
    - cerrar puerta
    - cierra la puerta
    - open door
    - close door
    """
)

comando = st.text_input(
    "Ingrese el comando:",
    placeholder="Ejemplo: abre la puerta"
)

# =====================================================
# BOTÓN ENVÍO
# =====================================================

if st.button("Enviar comando"):

    texto = comando.lower().strip()

    # ==========================================
    # LISTAS DE COMANDOS
    # ==========================================

    comandos_abrir = [

        "abre la puerta",
        "abrir puerta",
        "abrir",
        "open door",
        "open",

    ]

    comandos_cerrar = [

        "cerrar puerta",
        "cierra la puerta",
        "cerrar",
        "close door",
        "close"

    ]

    # ==========================================
    # INTERPRETACIÓN
    # ==========================================

    if texto in comandos_abrir:

        enviar_puerta("abrir")

        st.success("🚪 Puerta Abierta")

    elif texto in comandos_cerrar:

        enviar_puerta("cerrar")

        st.warning("🚪 Puerta Cerrada")

    else:

        st.error("❌ Comando no reconocido")

# =====================================================
# INFORMACIÓN MQTT
# =====================================================

st.markdown("---")

with st.expander("Información del sistema"):

    st.write(f"Broker MQTT: {BROKER}")
    st.write(f"Puerto: {PORT}")
    st.write(f"Topic MQTT: {TOPIC}")

# =====================================================
# PIE DE PÁGINA
# =====================================================

st.markdown("---")

st.caption("Sistema IoT ESP32 + MQTT + Streamlit + Wokwi")
