from typing import Union, List
from adafruit_servokit import ServoKit, Servo as AdafruitServo

class Servo:
    servo: AdafruitServo
    min: int
    max: int
    state: int  ## 0 = off, 1 = on

    def __init__(self, servo: AdafruitServo, min=0, max=90):
        self.servo = servo
        self.min = min
        self.max = max

    def set_on(self):
        if self.state != 1:
            self.servo.angle = self.max
            self.state = 1

    def set_off(self):
        if self.state != 0:
            self.servo.angle = self.min
            self.state = 0


class Digit:
    servos: List[Servo]
    state: Union[int, None]  # current number active or None if reset

    def __init__(self, servos: [Servo, Servo, Servo, Servo, Servo, Servo, Servo]):
        """
        Segment numbering shown below
            (0)>>>  ---
            (3)>> |     | <<(5)
            (1)>>>  ---
            (4)>> |     | <<(6)
            (2)>>>  ---
        """
        self.servos = servos
        self.reset()

    def reset(self):
        for servo in self.servos:
            servo.set_off()
            self.state = None

    def set_digit(self, number: int):
        config = {
            # Values for shown (1) or sideways (0)
            0: [1, 0, 1, 1, 1, 1, 1],
            1: [0, 0, 0, 0, 0, 1, 1],
            2: [1, 1, 1, 0, 1, 1, 0],
            3: [1, 1, 1, 0, 0, 1, 1],
            4: [0, 1, 0, 1, 0, 1, 1],
            5: [1, 1, 1, 0, 1, 0, 1],
            6: [0, 1, 1, 1, 1, 0, 1],
            7: [1, 0, 0, 0, 0, 1, 1],
            8: [1, 1, 1, 1, 1, 1, 1],
            9: [1, 1, 0, 1, 0, 1, 1],
        }
        for servo, servo_state in zip(self.servos, config.get(number)):
            servo: Servo
            if servo_state == 1:
                servo.set_on()
            else:
                servo.set_off()


