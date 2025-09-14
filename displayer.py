from pololu_3pi_2040_robot import robot

class Displayer:
  def __init__(self):
    self.display = robot.Display()
      
  def show(self, text: str):
    self.display.fill(0)
    self.display.text(text, 0, 0, 1)
    self.display.show()
