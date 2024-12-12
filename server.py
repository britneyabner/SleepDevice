import client
import database
import re
import datetime
import json
import protocol

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


def run_server():
    db = database.Database("sleepdb", "postgres")

    def _on_connect(mqttc, userdata, flags, reason_code, properties):
        print("Server connected.")

    def _on_message(mqttc, userdata, msg):
        data = json.loads(msg.payload)
        if data["request"] == "send_scores":
            db.add_patient_scores(
                data["id"],
                data["date"],
                data["time"],
                data["motion_score"],
                data["sound_score"]
            )
        elif data["request"] == "request_scores_on_date":
            id = data["id"]
            date = data["date"]
            motion = db.get_motion_score_on_date(id, date)
            sound = db.get_sound_score_on_date(id, date)
            message = protocol.msg_send_scores_on_date(motion, sound)
            server_client.publish(PUB_TOPIC, message)

    server_client = client.Client(BROKER, PORT, KEEPALIVE, _on_connect, _on_message)
    server_client.subscribe(SUB_TOPIC)

    server_client.loop()

if __name__ == "__main__":
    run_server()
