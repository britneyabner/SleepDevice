import gpiod
from gpiod.line import Direction, Value

class Microphone:
    def __init__(self, device_path: str, digital_pin: int):
        self.device_path = device_path
        self.digital_pin = digital_pin

    def detect_sound(self) -> bool:
        value = False
        try:
            def _detect():
                nonlocal value
                with gpiod.request_lines(
                    self.device_path,
                    consumer="_detect",
                    config={
                        self.digital_pin: gpiod.LineSettings(
                            direction=Direction.INPUT
                        )
                    },
                ) as request:
                    value = request.get_value(self.device_path, self.digital_pin)
                    print(value)
        finally:
            return value
