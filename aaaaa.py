from gpiozero import Servo, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Set up pigpio pin factory
factory = PiGPIOFactory()

# Use the pigpio pin factory
Device.pin_factory = factory

# Create servo object
servo = Servo(17)

while True:
    servo.min()
    sleep(1)
    servo.mid()
    sleep(1)
    servo.max()
    sleep(1)
