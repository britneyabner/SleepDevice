import pyaudio
import picamera2
import libcamera


def record():
    camera = picamera2.Picamera2()
    camera.start_preview(picamera2.Preview.QTGL, x=100,
                         y=200, width=800, height=600)
    transform = libcamera.Transform(hflip=1)
    camera.start()


if __name__ == "__main__":
    record()
