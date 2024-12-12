import gpiod
from gpiod.line import Direction, Value

DEVICE_PATH = "/dev/gpiochip0"
DIGIATL_PIN = 23


def _get_line_value(chip_path, line_offset):
    with gpiod.request_lines(
        chip_path,
        consumer="get-line-value",
        config={line_offset: gpiod.LineSettings(direction=Direction.INPUT)},
    ) as request:
        value = request.get_value(line_offset)
        return value


def detect_sound():
    try:
        if _get_line_value(DEVICE_PATH, DIGIATL_PIN) == Value.ACTIVE:
            return True
        else:
            return False
    except Exception:
        return False
