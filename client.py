import paho.mqtt.client as mqtt


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
