class Rat:
  def __init__(self, sex, weight):
    self.sex = sex
    self.weight = weight
    self.litters = 0
  
  def __str__(self):
    return f"Sex - {self.sex}, Weight - {self.weight}, Litters - {self.litters}"

  def __repr__(self):
    return f"{self.sex} - {self.weight}"
  
  def __lt__(self, other):
    return self.weight < other
  
  def getWeight(self):
    return self.weight
  
  def getSex(self):
    return self.sex

  def canBreed(self):
    return self.litters <= 5

  def __gt__(self, other):
    return self.weight > other


  def __le__(self, other):
    return self.weight <= other

  def __ge__(self, other):
    return self.weight >= other

  def __eq__(self, other):
    return self.weight == other
