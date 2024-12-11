import client
import database
import re
import datetime

BROKER = "broker.emqx.io"
PORT = 1883
KEEPALIVE = 60
SUB_TOPIC = "britneyabner/sleepdevice/device"
PUB_TOPIC = "britneyabner/sleepdevice/server"


def name_request(db, msg) -> str:
    patient_id = int(msg)
    fname, lname = db.get_patient_name_from_id(patient_id)
    return_msg = f"Name: {fname} {lname}"

    return return_msg


def add_patient(db, msg):
    name = re.findall(r'[A-Z][A-Za-a]*', msg)
    fname, lname = name[0], name[1]
    db.add_new_patient(fname, lname)


def store_scores(db, msg):
    data = re.findall(r'[0-9]+', msg)
    id, motion, sound = data[0], data[2], data[3]
    time = f"{data[1]} sec"
    date = datetime.today().strftime('%Y-%m-%d')
    db.add_patient_scores(id, date, time, motion, sound)


def run_server():
    db = database.Database("sleepdb", "postgres")

    def _on_connect(mqttc, userdata, flags, reason_code, properties):
        print("Server connected.")

    def _on_message(mqttc, userdata, msg):
        store_scores(db, msg)

    server_client = client.Client(BROKER, PORT, KEEPALIVE, _on_message,
                                  _on_connect)
    server_client.subscribe(SUB_TOPIC)

    server_client.loop()
