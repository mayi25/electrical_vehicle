from pololu_3pi_2040_robot import robot
from displayer import Displayer
import time

class Gyro:

  def __init__(self, displayer: Displayer):
    self.imu = robot.IMU()
    self.imu.reset()
    self.imu.enable_default()

    displayer.show("Calibrating...")
    time.sleep_ms(500)
    start_ms = time.ticks_ms()
    self.adjustment_per_second = 0.0
    reading_count = 0
    while time.ticks_diff(time.ticks_ms(), start_ms) < 1000:
      if self.imu.gyro.data_ready():
        self.imu.gyro.read()
        self.adjustment_per_second += self.imu.gyro.last_reading_dps[2]
        reading_count += 1
    self.adjustment_per_second /= reading_count
    self.last_us = time.ticks_us()
    self.last_angle = 0
    self.last_angle_speed = 0
    displayer.show("")

  def degree(self):
    if self.imu.gyro.data_ready():
      self.imu.gyro.read()
      self.last_angle_speed = self.imu.gyro.last_reading_dps[2] - self.adjustment_per_second
      
    now_us = time.ticks_us()
    time_passed = (now_us - self.last_us) / 1000000.0
    angle_moved = self.last_angle_speed * time_passed
    angle = self.last_angle + angle_moved        
    self.last_us = now_us
    self.last_angle = angle
    return angle
