""" electrical vehicle """
# !pylint main.py
import math
import time
from pololu_3pi_2040_robot import robot
from gyro import Gyro
from displayer import Displayer
from sound_sensor import SoundSensor
from timer import Timer

#initalizing variables
button_b = robot.ButtonB()
button_c = robot.ButtonC()
displayer: Displayer = Displayer() #display pannel
gyro: Gyro = Gyro(displayer)
soundSensor = SoundSensor()
timer = Timer(gyro)
MOTOR_SPEED=3000   # max: 6000
SLOW_MOTOR_SPEED=1000
TURN_SPEED=500
TURN_ANGLE_ADJUST=3.0
ANGLE_OFF_ALLOWED=0.25
SPEED_ADJUST=200  # speed adjustment for angle off
encoders = robot.Encoders() # 0.0287cm/count
motors = robot.Motors()
CM_PER_COUNT = 0.0287
TARGET_DISTANCE = 700 # cm CHANGE BOBBY
TARGET_TIME_MS = 10000 # cm CHANGE BOBBY
distance_to_gate = math.sqrt(TARGET_DISTANCE*TARGET_DISTANCE/4 + 90 * 90) - 8
angle_to_gate = math.degrees(math.atan(180/TARGET_DISTANCE))  # =(100-10)/(target/2)

def left(target_angle):
    """Turn left to the target angle."""
    current_angle = gyro.degree()
    motors.set_speeds(-TURN_SPEED, TURN_SPEED)
    while current_angle < target_angle - TURN_ANGLE_ADJUST:
        current_angle = gyro.degree()

    motors.off()
    timer.sleep_ms(100)

def right(target_angle):
    """Turn right to the target angle."""
    current_angle = gyro.degree()
    motors.set_speeds(TURN_SPEED, -TURN_SPEED)
    while current_angle > target_angle + TURN_ANGLE_ADJUST:
        current_angle = gyro.degree()

    motors.off()
    timer.sleep_ms(100)  # pylint: disable=no-member

def turn(target_angle):
    """Turn the robot into the target angle."""
    current_angle = gyro.degree()
    if target_angle > current_angle:
        left(target_angle)
    else:
        right(target_angle)

def drive(distance, target_angle): #move certain distance at certain angle
    """Drive the robot for a certain distance at a certain angle."""
    if distance <= 1:
        return
    target_count = distance / CM_PER_COUNT
    right_adjusted = 0
    encoders.get_counts(reset = True)
    count = 0
    while count < target_count:
        if (target_count -  count) * CM_PER_COUNT < 30:
            motors.set_speeds(SLOW_MOTOR_SPEED, SLOW_MOTOR_SPEED + right_adjusted)
        else:
            motors.set_speeds(MOTOR_SPEED,
                              MOTOR_SPEED + right_adjusted) # adjust speed based on gyro.
        angle = gyro.degree()
        if angle < target_angle - ANGLE_OFF_ALLOWED:
            right_adjusted = SPEED_ADJUST
        elif angle > target_angle + ANGLE_OFF_ALLOWED:
            right_adjusted = -SPEED_ADJUST
        else:
            right_adjusted = 0

        counts = encoders.get_counts()
        count = (counts[0] + counts[1]) / 2

    motors.off()
    timer.sleep_ms(100)  # pylint: disable=no-member

def pass_gate():
    """Slow pass the gate assuming it is in the middle of the gate"""
    displayer.show("pass gate!")

    # check the outer bottle
    turn(10)
    distance = soundSensor.distance_cm()
    if distance < 50:
        right(-90)
        drive(7 - distance * math.sin(math.radians(10)), -90)

    # check the inner bottle
    turn(-10)
    distance = soundSensor.distance_cm()
    if distance < 50:
        left(90)
        drive(7 - distance * math.sin(math.radians(10)), 90)
    turn(0)

def aim_gate():
    """Aim the robot to the gate."""
    turn(0)
    distance = soundSensor.distance_cm()
    if 15 < distance < 50:
        drive(distance - 15, 0)
    # if see the inner bottle, move left 3cm, try 3 times maximum
    count = 0
    while distance < 50 and count < 3:
        turn(90)
        drive(3, 90)
        turn(0)
        distance = soundSensor.distance_cm()
        count = count + 1
    pass_gate()

def millis():
    ''' return time in milliseconds '''
    return int(time.time() * 1000)

displayer.show("press B to start.")

while True:
    if abs(gyro.degree()) > 1:
        displayer.show("Gyro off, reset!")
        break
    if button_c.check():
        while True:
            displayer.show("distance:" + str(soundSensor.distance_cm()))
    if button_b.check():
        displayer.show("GOOD LUCK!")
        start = millis()
        timer.sleep_ms(500)
        ############
        drive(distance_to_gate, angle_to_gate)
        aim_gate()
        time_remain = TARGET_TIME_MS - millis() + start
        # calculate wait time assuming 1 second for passing gate and 1 second per meter
        wait_time = min(2500, (time_remain - distance_to_gate * 15 - 1000) / 3)
        timer.sleep_ms(wait_time)
        drive(26, 0) # cross the gate
        timer.sleep_ms(wait_time)
        turn(-angle_to_gate)
        timer.sleep_ms(wait_time)
        drive(distance_to_gate, -angle_to_gate - 1.5)
