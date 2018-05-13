import logging


class GPIO(object):
    INPUT = 1
    OUTPUT = 0
    ALT0 = 4

    HIGH = 1
    LOW = 0

    MODE_UNKNOWN = -1
    BOARD = 10
    BCM = 11
    SERIAL = 40
    SPI = 41
    I2C = 42
    PWM = 43

    @staticmethod
    def setmode(val):
        logging.info('GPIO.setmode: {}'.format(val))

    @staticmethod
    def setup(pin, val):
        logging.info('GPIO.setup: {}/{}'.format(pin, val))

    @staticmethod
    def output(pin, val):
        logging.info('GPIO.output: {}/{}'.format(pin, val))

    @staticmethod
    def cleanup():
        logging.info('GPIO.cleanup')
