from pololu_3pi_2040_robot import robot
from gyro import Gyro
from timer import Timer
from motor import Motor
from sound_sensor import SoundSensor
from displayer import Displayer
import time

button_a = robot.ButtonA()
displayer: Displayer = Displayer()
gyro: Gyro = Gyro(displayer)
timer: Timer = Timer(gyro)
sound_sensor: SoundSensor = SoundSensor()
motor: Motor = Motor()

displayer.show("Press A to start...")

while True:
    if button_a.check() == True:
      timer.sleep_ms(500)
      displayer.show("start driving ...")
      drive_to_wall()
      
fun drive_to_wall():
  motor.start()
  while sound_sensor.distance_cm() > 10:
    displayer.show(str(sound_sensor.distance_cm()))
    # if the gyro sensor is not right , correct it.
    angle = gyro.degree()
    turn_speed = gyro.turn_speed()
    if  angle < -0.1 && turn_speed > 0:
      motor.turn_left()
      
    if  angle > 0.1  && turn_speed < 0::
      motor.turn_right()
    
  displayer.show("stop driving...")
  motor.stop()


