import camera
import motiondetection
import microphone
import client
import time
import protocol
import sys

DEVICE_PATH = "dev/gpiochip0"
DIGITAL_MIC_PIN = 23

BROKER = "broker.emqx.io"
PORT = 1883
KEEPALIVE = 60

SUB_TOPIC = "britneyabner/sleepdevice/server"
PUB_TOPIC = "britneyabner/sleepdevice/device"


def run_device(id: int, record_time: int):
    sound_time = 0

    # initialize GPIO for sound detection
    mic = microphone.Microphone(DEVICE_PATH, DIGITAL_MIC_PIN)
    cam = camera.FrameExtracter()

    im1 = cam.capture_frame()
    frame_count = 1
    motion_count = 0
    for i in range(0, record_time):
        #im2 = cam.capture_frame()
        frame_count += 1
        #if motiondetection.detect_motion(im1, im2):
            #motion_count += 1
        #im1 = im2
        if mic.detect_sound():
            sound_time += 1
        time.sleep(1)

    motion_score = int(1 - (motion_count / frame_count))
    sound_score = int(1 - (sound_time / record_time))

    '''
    # iterate through the frames of the video to detect motions
    frames = camera.FrameExtracter(VIDEO)
    motion_count = 0
    image1 = frames.extract_frame()
    image2 = frames.extract_frame()
    while image1 is not None and image2 is not None:
        if motiondetection.detect_motion(image1, image2):
            motion_count += 1
    '''
    # use the number of motions to calculate sound score
    motion_score = int((1 - motion_count / frame_count) * 100)

    # format the string for sending to the server via mqtt
    time_str = f"{record_time} sec"
    score_message = protocol.send_scores(id, time_str, motion_score,
                                         sound_score)

    # initialize the mqtt client
    def _on_connect(mqttc, userdata, flags, reasone_code, properties):
        print("Device connected")

    def _on_message(mqttc, userdata, msg):
        pass

    mqttc = client.Client(BROKER, PORT, KEEPALIVE, _on_connect, _on_message)
    mqttc.subscribe(SUB_TOPIC)

    # publish the recorded scores to the server
    mqttc.publish(PUB_TOPIC, score_message)

    # loop, waiting for messages
    mqttc.loop()


if __name__ == "__main__":
    id = sys.argv[1]
    record_time = int(sys.argv[2])
    run_device(id, record_time)
