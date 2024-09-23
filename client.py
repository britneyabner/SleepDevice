import paho.mqtt.client as mqtt

BROKER = "127.0.0.1"
PORT = 1883
KEEPALIVE = 60
TOPIC = "data"


def _on_connect(mqttc, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")


def _on_message(mqttc, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


class MqttClient:
    def __init__(self, broker: str, port: int, keepalive: int, topic: str):
        self.broker = broker
        self.port = port
        self.keepalive = keepalive
        self.topic = topic
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = _on_connect
        self.client.on_message = _on_message

    def connect(self):
        self.client.connect(self.broker, self.port, self.keepalive)
        self.client.subscribe(self.topic)

    def publish(self, message):
        self.client.publish(self.topic, message)


if __name__ == "__main__":
    client = MqttClient(BROKER, PORT, KEEPALIVE, TOPIC)
    client.connect()
    client.client.loop_start()
    client.publish("test")
    client.client.loop_stop()
