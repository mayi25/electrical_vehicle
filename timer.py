from gyro import Gyro
import time

class Timer:
    def __init__(self, gyro: Gyro):
        self.gyro = gyro
    
    def sleep_ms(self, ms: int):
        start_ms = time.ticks_ms()
        now_ms = start_ms
        while now_ms - start_ms < ms:
          self.gyro.degree()
          time.sleep_ms(1)
          now_ms = time.ticks_ms()
