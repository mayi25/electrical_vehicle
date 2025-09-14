import time
from machine import Pin

SOUND_SPEED = 34300

class SoundSensor:

  def __init__(self):
    self.trigger = Pin(27, Pin.OUT)
    self.echo = Pin(28, Pin.IN)

  def distance_cm(self):
    self.trigger.value(0)
    time.sleep_ms(10) # settle for 10 ms
    self.trigger.value(1)
    time.sleep_us(10) # Send 10us pulse to trigger
    self.trigger.value(0)
    start_us = time.ticks_us()
    while(self.echo.value() == 0):
      start_us = time.ticks_us()
      continue

    stop_us = time.ticks_us()
    while(self.echo.value() == 1):
      stop_us = time.ticks_us()
      continue

    elapsed = stop_us - start_us
    distance = elapsed * SOUND_SPEED / 1000000.0
    distance = distance / 2
    return distance
  