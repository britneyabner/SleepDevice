import camera
import motiondetection
import microphone
import client
import time
import protocol
import sys
import datetime
import json

DEVICE_PATH = "dev/gpiochip4"
DIGITAL_MIC_PIN = 23

BROKER = "broker.emqx.io"
PORT = 1883
KEEPALIVE = 60

SUB_TOPIC = "britneyabner/sleepdevice/server"
PUB_TOPIC = "britneyabner/sleepdevice/device"


def record_data(id: int, record_time: int):
    sound_time = 0

    cam = camera.Camera()
    im1 = cam.capture_frame()
    frame_count = 1
    motion_count = 0
    for i in range(0, record_time):
        im2 = cam.capture_frame()
        frame_count += 1
        if motiondetection.detect_motion(im1, im2):
            motion_count += 1
        im1 = im2
        if microphone.detect_sound():
            sound_time += 1
        time.sleep(1)

    motion_score = int(1 - (motion_count / frame_count))
    sound_score = int(1 - (sound_time / record_time))

    # use the number of motions to calculate sound score
    motion_score = int((1 - motion_count / frame_count) * 100)

    # format the string for sending to the server via mqtt
    date_str = datetime.date.today().strftime('%Y-%m-%d')
    time_str = f"{record_time} sec"
    score_message = protocol.msg_send_scores(id, date_str, time_str, motion_score,
                                             sound_score)

    print(score_message)

    # initialize the mqtt client
    def _on_connect(mqttc, userdata, flags, reasone_code, properties):
        print("Device connected")

    def _on_message(mqttc, userdata, msg):
        data = json.loads(msg.payload)
        if data["request"] == "send_scores_on_date":
            motion = data["motion_score"]
            sound = data["sound_score"]
            print(f"motion: {motion}, sound: {sound}")

    mqttc = client.Client(BROKER, PORT, KEEPALIVE, _on_connect, _on_message)
    mqttc.subscribe(SUB_TOPIC)

    # publish the recorded scores to the server
    mqttc.publish(PUB_TOPIC, score_message)


def get_score(id: int, date: str):
    def _on_connect(mqttc, userdata, flags, reason_code, properties):
        print("Device connected")

    def _on_message(mqttc, userdata, msg):
        data = json.loads(msg.payload)
        if data["request"] == "send_scores_on_date":
            motion = data["motion_score"]
            sound = data["sound_score"]
            print(f"motion: {motion}, sound: {sound}")

    request = protocol.msg_request_scores_on_date(id, date)
    mqttc = client.Client(BROKER, PORT, KEEPALIVE, _on_connect, _on_message)
    mqttc.publish(PUB_TOPIC, request)
