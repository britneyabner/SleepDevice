import pyaudio
import time
import picamera2
import libcamera


def record():
    camera = picamera2.Picamera2()
    video_config = camera.create_video_configuration()
    camera.configure(video_config)
    encoder = picamera2.encoders.H264Encoder(bitrate=10000000)
    output = "test.h264"

    camera.start_recording(encoder, output)
    time.sleep(10)
    camera.stop_recording()


if __name__ == "__main__":
    record()
