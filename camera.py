import time
import cv2


"""
def record_video(file_name: str, record_time: int):
    camera = picamera2.Picamera2()
    video_config = camera.create_video_configuration()
    camera.configure(video_config)
    encoder = picamera2.encoders.H264Encoder(bitrate=10000000)
    output = picamera2.outputs.FfmpegOutput(file_name, audio=False)

    camera.start_recording(encoder, output)
    time.sleep(record_time)
    camera.stop_recording()
"""


class FrameExtracter:
    def __init__(self):
        self.vidcap = cv2.VideoCapture(0)
        self.count = 0
        self.success = True

    def extract_frame(self):
        if not self.success:
            return None

        self.vidcap.set(cv2.CAP_PROP_POS_MSEC, (self.count*1000))
        self.success, image = self.vidcap.read()
        self.count += 1

        return image
    
    def capture_frame(self):
        ret, frame = self.vidcap.read()
        if ret:
            cv2.imshow('Frame', frame)


def test_record_video():
    pass

def test_frame_extractor():
    frame_extractor = FrameExtracter("test.mp4")

    while True:
        frame1 = frame_extractor.extract_frame()
        frame2 = frame_extractor.extract_frame()

        if frame1 is None or frame2 is None:
            break


if __name__ == "__main__":
    test_frame_extractor()
