import client
import database
import re


NAME_REQUEST = r'name request: [0-9]+'
ADD_PATIENT = r'add patient: [A-Z][a-zA-Z]* [A-Z][a-zA-Z]*'


def name_request(db, msg) -> str:
    patient_id = int(msg)
    fname, lname = db.get_patient_name_from_id(patient_id)
    return_msg = f"Name: {fname} {lname}"

    return return_msg


def add_patient(db, msg):
    name = re.findall(r'[A-Z][A-Za-a]*')
    fname, lname = name[0], name[1]
    db.add_new_patient(fname, lname)


def run_server():
    BROKER = "broker.emqx.io"
    PORT = 1883
    KEEPALIVE = 60
    SUB_TOPIC = "britneyabner/sleepdevice/device"
    PUB_TOPIC = "britneyabner/sleepdevice/server"
    db = database.Database("sleepdb", "postgres")

    def _on_connect(mqttc, userdata, flags, reason_code, properties):
        print("Server connected.")

    def _on_message(mqttc, userdata, msg):
        if msg == re.match(NAME_REQUEST, msg):
            name_msg = name_request(db, msg)
            mqttc.publish(PUB_TOPIC, name_msg)
        elif msg == re.match(ADD_PATIENT, msg):
            names = re.findall(r'[A-Z][a-zA-Z]*')
            fname, lname = names[0], names[1]
            db.add_new_patient(fname, lname)

    server_client = client.Client(BROKER, PORT, KEEPALIVE, _on_message,
                                  _on_connect)
    server_client.subscribe(SUB_TOPIC)


