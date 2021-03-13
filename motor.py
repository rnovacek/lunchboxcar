import machine
import time

class _Motor:

    def __init__(self, dir_pin, speed_pin):
        self.dir_pin = machine.Pin(dir_pin, machine.Pin.OUT)
        self.speed_pwm = machine.PWM(
            machine.Pin(speed_pin, machine.Pin.OUT), freq=500)

    def set_speed(self, speed):
        self.dir_pin.value(0 if speed < 0 else 1)
        self.speed_pwm.duty(abs(speed))


motor_a = _Motor(dir_pin=0, speed_pin=5)
motor_b = _Motor(dir_pin=2, speed_pin=4)
