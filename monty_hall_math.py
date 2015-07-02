import random

class Car(object):
  """docstring for """
  def __init__(self, id):
    self.id = id

  def __str__(self):
    return "Car"

class Goat(object):
  """docstring for """
  def __init__(self, id):
    self.id = id

  def __str__(self):
    return "Goat"

pack_car = [Car(i) for i in range(1)]
pack_goat = [Goat(i) for i in range(2)]

#print type(pack_car[0])
#print type(pack_car[0]) == type(Car(id))
#print type(Car(id))
#print pack_goat

pack = pack_car + pack_goat
print pack

print random.choice(pack)

def eliminate(pack, elimination):
  print "Length before elimination: %d" % len(pack)
  print "Do %d eliminations." % elimination
  random.shuffle(pack)
  while elimination > 0:
    print "Eliminating...."
    for i in pack:
      if type(i) == type(Goat(id)):
        pack.remove(i)
        elimination -= 1
  print "Length after elimination %d" % len(pack)
  return pack

def pick_after_elimination(pack, TRIAL, elimination):
  pack_copy = pack[:]
  pack_copy = eliminate(pack_copy, elimination)
  picked_car = 0
  for i in range(TRIAL):
    random.shuffle(pack_copy)
    #print pack_copy
    if type(random.choice(pack_copy)) == type(Car(id)):
      picked_car += 1
  print "picked_car: %d" % picked_car
  print "%d elimination" % elimination
  print "%d trials. Probability: %.2f%%" % (TRIAL, 1.0 * picked_car/TRIAL)

def pick(pack, TRIAL=100, elimination=0):
  picked_car = 0
  pack_copy = pack[:]
  for i in range(TRIAL):
    random.shuffle(pack_copy)
    #print pack_copy
    if type(random.choice(pack_copy)) == type(Car(id)):
      picked_car += 1
  print "No elimination"
  print "%d trials. Probability: %.2f%%" % (TRIAL, 1.0 * picked_car/TRIAL)
  if elimination > 0:
    pick_after_elimination(pack, TRIAL, elimination)

pick(pack, TRIAL=100000, elimination=1)
