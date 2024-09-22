import client

BROKER = "18.118.132.58"
PORT = 1883
KEEPALIVE = 60
TOPIC = "data"

if __name__ == "__main__":
    client.client(BROKER, PORT, KEEPALIVE, TOPIC)
