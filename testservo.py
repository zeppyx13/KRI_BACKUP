import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for servo
servo_pin = 28

# Set PWM frequency
frequency = 50
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, frequency)

# Define duty cycle range
min_duty = 2.5
max_duty = 12.5

# Function to convert angle to duty cycle
def angle_to_duty_cycle(angle):
    duty_cycle = ((max_duty - min_duty) / 180) * angle + min_duty
    return duty_cycle

# Function to move the servo to a specific angle
def move_servo(angle):
    duty_cycle = angle_to_duty_cycle(angle)
    pwm.start(duty_cycle)
    time.sleep(1)  # Adjust sleep time as needed
    pwm.stop()

# Move servo back and forth
try:
    while True:
        move_servo(0)   # Move to 0 degrees
        time.sleep(1)
        move_servo(90)  # Move to 90 degrees
        time.sleep(1)
        move_servo(180) # Move to 180 degrees
        time.sleep(1)
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
  