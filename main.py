import math
import time
from pololu_3pi_2040_robot import robot
from gyro import Gyro
from displayer import Displayer
from sound_sensor import SoundSensor

#initalizing variables
button_b = robot.ButtonB()
button_c = robot.ButtonC()
displayer: Displayer = Displayer() #display pannel 
gyro: Gyro = Gyro(displayer) 
soundSensor = SoundSensor()
MOTOR_SPEED=3000   # max: 6000
SLOW_MOTOR_SPEED=1000
TURN_SPEED=440
TURN_ANGLE_ADJUST=3.0
ANGLE_OFF_ALLOWED=0.25
SPEED_ADJUST=100  # speed adjustment for angle off
encoders = robot.Encoders() # 0.0287cm/count 
motors = robot.Motors()
distance_to_target = 700 # cm CHANGE
distance_to_gate = math.sqrt(distance_to_target*distance_to_target/4 + 90 * 90) - 20
angle_to_gate = math.degrees(math.atan(180/distance_to_target))  # =(100-10)/(target/2)

def left(target_angle):
  current_angle = gyro.degree()
  motors.set_speeds(-TURN_SPEED, TURN_SPEED)
  while current_angle < target_angle - TURN_ANGLE_ADJUST:
    current_angle = gyro.degree()

  motors.off()
  time.sleep_ms(100)

def right(target_angle):
  current_angle = gyro.degree()
  motors.set_speeds(TURN_SPEED, -TURN_SPEED)
  while current_angle > target_angle + TURN_ANGLE_ADJUST:
    current_angle = gyro.degree()

  motors.off()
  time.sleep_ms(100)

def straight():
  angle = gyro.degree()
  if angle > 1:
    right(0)
  if angle < -1:
    left(0)

def drive(distance, target_angle): #move certain distance at certain angle 
  target_count = distance / 0.0287 
  right_adjusted = 0
  encoders.get_counts(reset = True)
  count = 0
  while count < target_count:
    motors.set_speeds(MOTOR_SPEED, MOTOR_SPEED + right_adjusted) # if the gyro sensor is not right , correct it.
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
  time.sleep_ms(200)

# aim to gate
def aim_gate():
  right(-90)
  motors.set_speeds(-TURN_SPEED, TURN_SPEED)
  distance = soundSensor.distance_cm()
  displayer.show(str(distance))
  while distance > 40:  # look for the inner bottle      
    gyro.degree()
    distance = soundSensor.distance_cm()
    displayer.show(str(distance))

  motors.off()
  time.sleep_ms(100)

  degree = gyro.degree()
  drive(distance - 15, degree)
  left(90)
  if degree > 30:
    drive(15, 90)
  
  motors.set_speeds(TURN_SPEED, -TURN_SPEED)
  distance = soundSensor.distance_cm()
  while distance > 50:  # look for the outer bottle      
    gyro.degree()
    distance = soundSensor.distance_cm()
  motors.off()
  time.sleep_ms(100)
  degree = gyro.degree()
  drive(distance - 17, degree)
  motors.off()
  time.sleep_ms(100)
  straight()
  drive(30, 0)   # pass the gate

right(-90)
  
displayer.show("press B to start.")
while True:
    if button_b.check():
      displayer.show("GOOD LUCK!")
      time.sleep_ms(500)
      ############
      drive(distance_to_gate, angle_to_gate)
      time.sleep_ms(0) # add sleep if needed
      pass_gate()
      time.sleep_ms(0) # add sleep if needed
      right(-angle_to_gate)
      time.sleep_ms(0) # add sleep if needed
#     drive(distance_to_gate, -angle_to_gate)
