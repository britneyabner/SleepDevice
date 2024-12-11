import camera
import motiondetection
import microphone
import client
import time
import protocol
import sys

DIGITAL_MIC_PIN = 23
ANALOG_MIC_PIN = 24
VIDEO = "test.mp4"
RECORD_TIME = 8 * 60 * 60   # 8 hours, in seconds

BROKER = "broker.emqx.io"
PORT = 1883
KEEPALIVE = 60

SUB_TOPIC = "britneyabner/sleepdevice/server"
PUB_TOPIC = "britneyabner/sleepdevice/device"


def run_device(id: int):
    # Declare callback functions for the microphone that time how long sound is
    # detected for
    sound_start = None
    sound_stop = None
    sound_time = 0

    def _on_sound_detected(pin):
        nonlocal sound_start

        sound_start = time.time()

    def _on_sound_stop(pin):
        nonlocal sound_start
        nonlocal sound_stop
        nonlocal sound_time

        sound_stop = time.time()
        elapsed_time = sound_stop - sound_start
        sound_time += elapsed_time

    # initialize GPIO for sound detection
    _ = microphone.Microphone(6, 7, _on_sound_detected(DIGITAL_MIC_PIN),
                              _on_sound_stop(DIGITAL_MIC_PIN))

    cam = camera.FrameExtracter()
    im1 = cam.capture_frame()
    motion_count = 0
    for i in range(0, 30):
        im2 = cam.capture_frame()
        if motiondetection.detect_motion(im1, im2):
            motion_count += 1
        im1 = im2


    sound_score = int(1 - (sound_time / RECORD_TIME))

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
    motion_score = int((1 - motion_count / frames.count) * 100)

    # format the string for sending to the server via mqtt
    time_str = f"{RECORD_TIME} sec"
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
    run_device(id)
