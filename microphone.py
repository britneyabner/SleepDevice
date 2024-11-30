import RPi.GPIO as GPIO


class Microphone:
    def __init__(self, digital_pin: int, analog_pin: int, callback_function):
        self.digital_pin = digital_pin
        self.analog_pin = analog_pin
        self.callback_function = callback_function

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(digital_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(digital_pin, GPIO.RISING)
        GPIO.add_event_callback(digital_pin, self.callback_function)

    def detect_audio(self) -> bool:
        return GPIO.input(self.digital_pin)
