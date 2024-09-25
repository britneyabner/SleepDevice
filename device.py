import time
import picamera2


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


def convert(path: str):
    byte_stream = open("test.mp4", "rb")
    return byte_stream.read()


if __name__ == "__main__":
    record()
    convert("test.mp4")
