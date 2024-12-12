import gpiod


class Microphone:
    def __init__(self, digital_pin: int, analog_pin):
        self.chip = gpiod.Chip('gpiochip4')
        self.digital_line = self.chip.get_line(digital_pin)

        self.digital_line_request(
            consumer='Digital', type=gpiod.LINE_REQ_DIR_IN)

    def detect_audio(self) -> bool:
        return self.digital_line.get_value()

    def release_pin(self):
        self.digital_line.release()
