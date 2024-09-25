import pyaudio
import time
import picamera2
import libcamera


def record():
    camera = picamera2.Picamera2()
    video_config = camera.create_video_configuration()
    camera.configure(video_config)
    encoder = picamera2.encoders.H264Encoder(bitrate=10000000)
    output = picamera2.outputs.FfmpegOutput("test.mp4", audio=True)

    camera.start_recording(encoder, output)
    time.sleep(10)
    camera.stop_recording()

    return output


if __name__ == "__main__":
    record()
