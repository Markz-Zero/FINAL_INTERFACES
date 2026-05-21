import streamlit as st
import paho.mqtt.client as mqtt
import json
import time

# ===================================
# MQTT
# ===================================

BROKER = "broker.mqttdashboard.com"
PORT = 1883
TOPIC = "casa/control"

client = mqtt.Client("streamlit-client")

try:
    client.connect(BROKER, PORT)
    client.loop_start()
    mqtt_ok = True
except:
    mqtt_ok = False

# ===================================
# FUNCIONES
# ===================================

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


# ===================================
# INTERFAZ
# ===================================

st.title("Casa Inteligente MQTT")

# ==========================
# Estado MQTT
# ==========================

if mqtt_ok:
    st.success("MQTT conectado")
else:
    st.error("MQTT desconectado")

# ==========================
# CONTROL LEDS
# ==========================

st.header("Control de Bombillos LED")

col1, col2 = st.columns(2)

with col1:

    if st.button("Encender LED 1"):
        enviar_led("led1", "on")

    if st.button("Apagar LED 1"):
        enviar_led("led1", "off")

    if st.button("Encender LED 2"):
        enviar_led("led2", "on")

    if st.button("Apagar LED 2"):
        enviar_led("led2", "off")

with col2:

    if st.button("Encender LED 3"):
        enviar_led("led3", "on")

    if st.button("Apagar LED 3"):
        enviar_led("led3", "off")

# ==========================
# CONTROL PUERTA
# ==========================

st.header("Control Inteligente de Puerta")

comando = st.text_input(
    "Escribe un comando",
    placeholder="Ejemplo: abre la puerta"
)

if st.button("Enviar comando"):

    texto = comando.lower()

    # Interpretación inteligente

    abrir = [
        "abre la puerta",
        "abrir puerta",
        "open door",
        "abrir"
    ]

    cerrar = [
        "cerrar puerta",
        "cierra la puerta",
        "close door",
        "cerrar"
    ]

    if texto in abrir:

        enviar_puerta("abrir")

        st.success("Puerta abierta")

    elif texto in cerrar:

        enviar_puerta("cerrar")

        st.success("Puerta cerrada")

    else:

        st.warning("Comando no reconocido")
