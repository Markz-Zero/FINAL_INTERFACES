import streamlit as st
import paho.mqtt.client as mqtt
import json
import time

# =========================
# CONFIG MQTT
# =========================

BROKER = "broker.mqttdashboard.com"
PORT = 1883
TOPIC = "sg/iot1"

# =========================
# CLIENTE MQTT
# =========================

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION1,
    client_id="streamlit-control"
)

try:
    client.connect(BROKER, PORT)
    client.loop_start()
    mqtt_ok = True
except:
    mqtt_ok = False

# =========================
# INTERFAZ
# =========================

st.title("Control IoT")

if mqtt_ok:
    st.success("MQTT conectado")
else:
    st.error("MQTT desconectado")

# =========================
# BOTONES LED1
# =========================

st.header("LED 1")

col1, col2 = st.columns(2)

with col1:

    if st.button("Encender LED"):

        mensaje = {
            "dispositivo": "led1",
            "estado": "on"
        }

        client.publish(TOPIC, json.dumps(mensaje))

        st.success("LED encendido")

with col2:

    if st.button("Apagar LED"):

        mensaje = {
            "dispositivo": "led1",
            "estado": "off"
        }

        client.publish(TOPIC, json.dumps(mensaje))

        st.warning("LED apagado")
