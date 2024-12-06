import paho.mqtt.client as mqtt

BROKER = "broker.emqx.io"
PORT = 1883
KEEPALIVE = 60
TOPIC = "britneyabner/sleepdevice"


class Client:
    def __init__(self, broker, port, keepalive, on_message, on_connect):
        self.broker = broker
        self.port = port
        self.keepalive = keepalive
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.on_connect = on_connect
        self.mqttc.on_message = on_message
        self.mqttc.connect(self.broker, self.port, self.keepalive)

    def subscribe(self, topic: str):
        self.mqttc.subscribe(topic)

    def publish(self, topic: str, msg):
        self.mqttc.publish(topic, msg)

    def loop(self):
        self.mqttc.loop_forever()


def test():
    client = Client(BROKER, PORT, KEEPALIVE)
    client.subscribe(TOPIC)
    client.publish(TOPIC, "hello")
    client.loop()
    client.publish(TOPIC, "test")


if __name__ == "__main__":
    test()
