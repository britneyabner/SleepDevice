import client

BROKER = "127.0.0.1"
PORT = 1883
KEEPALIVE = 60
TOPIC = "data"

if __name__ == "__main__":
    client.run_client(BROKER, PORT, KEEPALIVE, TOPIC)
