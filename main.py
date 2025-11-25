""" electrical vehicle """
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
TARGET_TIME_MS = 15000 # cm CHANGE BOBBY
distance_to_gate = math.sqrt(TARGET_DISTANCE*TARGET_DISTANCE/4 + 90 * 90) - 20
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
        if (target_count -  count) / CM_PER_COUNT < 40:
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

def check_gate():
    """Check the gate. return true if the gate is safe to pass"""
    displayer.show("check gate")
    distance = soundSensor.distance_cm()
    if distance < 50:
        drive(distance - 10, 0)

    turn(10)
    if soundSensor.distance_cm() < 20:
        right(-90)
        drive(5, -90)
    turn(-10)
    if soundSensor.distance_cm() < 20:
        left(90)
        drive(5, 90)
    turn(0)

def aim_gate():
    """Aim the robot to the gate."""
    turn(-90)
    motors.set_speeds(-TURN_SPEED, TURN_SPEED)
    distance = soundSensor.distance_cm()
    angle = gyro.degree()
    while distance > 75:  # look for the inner bottle
        angle = gyro.degree()
        distance = soundSensor.distance_cm()
    motors.off()
    timer.sleep_ms(100)
    if angle > -25: # the bot is outside of the inner bottle
        turn(90)
        drive(distance * math.sin(math.radians(angle)) + 15, 90)

    turn(90)
    motors.set_speeds(TURN_SPEED, -TURN_SPEED)
    distance = soundSensor.distance_cm()
    angle = gyro.degree()
    while distance > 75:  # look for the outer bottle
        angle = gyro.degree()
        distance = soundSensor.distance_cm()
    motors.off()
    timer.sleep_ms(100)

    if angle < 25: # the bot is outside of the outer bottle
        turn(-90)
        drive(distance * math.sin(math.radians(-angle)) + 15, 90)

    turn(0)
    check_gate()

def millis():
    ''' return time in milliseconds '''
    return int(time.time() * 1000)

displayer.show("press B to start.")
while True:
    gyro.degree()
    if button_b.check():
        displayer.show("GOOD LUCK!")
        start = millis()
        timer.sleep_ms(500)  # pylint: disable=no-member
        ############
        drive(distance_to_gate, angle_to_gate)
        timer.sleep_ms(5000)
        aim_gate()
        time_remain = TARGET_TIME_MS - millis() - start
        # calculate wait time assuming 1 second for passing gate and 1 second per meter
        wait_time = max(2500, (time_remain - distance_to_gate / 0.1 - 1000) / 3)
        timer.sleep_ms(wait_time)  # pylint: disable=no-member
        drive(40, 0)
        timer.sleep_ms(wait_time)  # pylint: disable=no-member
        turn(-angle_to_gate)
        timer.sleep_ms(wait_time)  # pylint: disable=no-member
#     drive(distance_to_gate, -angle_to_gate)
