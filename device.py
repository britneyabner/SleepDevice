import pyaudio
import picamera2


def record():
    camera = picamera2.PiCamera2()
    camera.start_preview(picamera2.Preview.QTGL, x=100,
                         y=200, width=800, height=600)
    camera.start()


if __name__ == "__main__":
    record()
