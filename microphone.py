import RPi.GPIO as GPIO


class Microphone:
    def __init__(self, digital_pin: int, analog_pin: int, rising_callback,
                 falling_callback):
        self.digital_pin = digital_pin
        self.analog_pin = analog_pin

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(digital_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.digital_pin, GPIO.RISING,
                              callback=rising_callback, bouncetime=300)

        GPIO.add_event_detect(self.digital_pin, GPIO.FALLING,
                              callback=falling_callback, bouncetime=300)
