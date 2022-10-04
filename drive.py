from tlc5947 import TLC5947
import time
from pyftdi import spi
# Instantiate a SPI controller
spi = spi.SpiController()


# AD0 should be connected to SCLK

# AD1 should be connected to MOSI (master out, slave in)

# AD4 should be connected to the second slave /CS, i

# Blank is tied to ground

# Configure the first interface (IF/1) of the first FTDI device as a
# SPI master
spi.configure('ftdi://::/1')

# Get a SPI port to a SPI slave w/ /CS on A*BUS3 and SPI mode 0 @ 12MHz
slave = spi.get_port(cs=0, freq=12E6, mode=0)

# Get GPIO port to manage extra pins, use A*BUS4 as GPO, A*BUS4 as GPI
gpio = spi.get_gpio()

# Assert GPO pin


class FakeGPIO(object):

    def __init__(self, gpio):
        self.g = gpio
        self._value = False

    def switch_to_output(self, value):
        self.g.set_direction(0x30, 0x10)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value == 0:
            self.g.write(0x00)
            self._value = False
        else:
            self.g.write(0x10)
            self._value = True


tlc = TLC5947(slave, FakeGPIO(gpio))


def mkled(pin):
    return tlc.create_pwm_out(pin)


leds = list(map(mkled, range(8)))
o = 5

while True:

    leds[o].duty_cycle = 65535
    time.sleep(1)

    leds[o].duty_cycle = 0
    time.sleep(1)


