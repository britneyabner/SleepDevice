import paho.mqtt.client as mqtt

BROKER = "127.0.0.1"
PORT = 1883
KEEPALIVE = 60
TOPIC = "data"


def run_client(broker, port, keepalive, topic):
    def on_connect(mqttc, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        mqttc.subscribe(topic)

    def on_message(mqttc, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port, keepalive)
    client.publish("data", "test")
    client.loop_forever()


if __name__ == "__main__":
    run_client(BROKER, PORT, KEEPALIVE, TOPIC)
