import picamera2

def record_video(video_name: str, recording_time: int):
    camera = picamera2.PiCamera()
    camera.resolution = (640, 480)

    video_file = video_name + ".h264"

    camera.start_recording(video_file)
    camera.wait_recording(recording_time)
    camera.stop_recording
