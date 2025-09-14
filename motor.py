from pololu_3pi_2040_robot import robot
import time

MOTOR_SPEED = 3000

class Motor:
  
  def __init__(self):
    self.motors = robot.Motors()
  
  def start(self):
    self.motors.set_speeds(MOTOR_SPEED, MOTOR_SPEED)

  def stop(self):
    self.motors.off()

  def left(self, degree):
    self.motors.set_speeds(-MOTOR_SPEED, MOTOR_SPEED)

  def right(self, degree):
    self.motors.set_speeds(MOTOR_SPEED, -MOTOR_SPEED)
