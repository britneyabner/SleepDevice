import paho.mqtt.client as mqtt

BROKER = "broker.emqx.io"
PORT = 1883
KEEPALIVE = 60
TOPIC = "britneyabner/sleepdevice"


def _on_connect(mqttc, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")


def _on_message(mqttc, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


if __name__ == "__main__":
    server = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    server.on_connect = _on_connect
    server.on_message = _on_message
    server.connect(BROKER, PORT, KEEPALIVE)
    server.subscribe(TOPIC)
    server.loop_forever()
