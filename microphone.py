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


DEVICE_PATH = "/dev/gpiochip0"
DIGIATL_PIN = 23


def _get_line_value(chip_path, line_offset):
    with gpiod.request_lines(
        chip_path,
        consumer="get-line-value",
        config={line_offset: gpiod.LineSettings(direction=Direction.INPUT)},
    ) as request:
        value = request.get_value(line_offset)
        print(value)


if __name__ == "__main__":
    try:
        _get_line_value(DEVICE_PATH, DIGIATL_PIN)
    finally:
        pass
