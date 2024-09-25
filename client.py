import paho.mqtt.client as mqtt
import device

BROKER = "broker.emqx.io"
PORT = 1883
KEEPALIVE = 60
TOPIC = "britneyabner/sleepdevice"


def _on_connect(mqttc, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")


def _on_message(mqttc, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = _on_connect
    client.on_message = _on_message
    client.connect(BROKER, PORT, KEEPALIVE)
    client.subscribe(TOPIC)

    device.record()
    byte_stream = device.convert("test.mp4")
    client.publish(TOPIC, byte_stream)
    client.loop_forever()
