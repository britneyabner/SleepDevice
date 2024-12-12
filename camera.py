import cv2
import picamera2


class Camera:
    def __init__(self):
        self.picam = picamera2.Picamera2()
        self.picam.configure(self.picam.create_video_configuration(
            main={"format": 'XRGB8888', "size": (300, 300)}))
        self.picam.start()

    def capture_frame(self):
        return self.picam.capture_array()
