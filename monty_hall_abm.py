'''
Author: Seyoung Park
E-mail: seyoung.park@aalto.fi
Date: 2015.July.2nd

++++++++++++++++++++++++++
+++ Monty Hall Paradox +++
++++++++++++++++++++++++++

Purpose: Solve the paradox by ABM(Agent Based Modeling)
Tested on Python 2.7.9 (Mac OS X 10.10.3)
Reference:
https://en.wikipedia.org/wiki/Monty_Hall_problem
http://arxiv.org/ftp/arxiv/papers/1208/1208.2638.pdf
http://math.stackexchange.com/questions/608957/monty-hall-problem-extended

++++++ Example 1. ++++++
http://web.mit.edu/rsi/www/2013/files/MiniSamples/MontyHall/montymain.pdf
3 Doors = 1 Car + 2 Goats
choose_original(DOORS, 1000000) ===> 33.326%
choose_switched(DOORS, 1000000) ===> 66.708%

++++++ Example 2. ++++++
http://web.mit.edu/rsi/www/2013/files/MiniSamples/MontyHall/montymain.pdf
13 Doors = 1 Car + 12 Goats
choose_original(DOORS, 1000000) ===> 7.68%
choose_switched(DOORS, 1000000) ===> 8.39%

++++++ Example 3. ++++++
http://math.stackexchange.com/questions/1032661/monty-hall-problem-with-five-doors
5 Doors = 1 Car + 4 Goats
choose_original(DOORS, 1000000) ===> 20.00%
choose_switched(DOORS, 1000000) ===> 26.67%

Note:
The probability values will differ everytime you run the simulation.
That is very natural - that's the point of simulations ;)
The probabilistic error bound of the simulation decreases as 1/sqrt(TRIAL)
i.e., if you want accuracy of first decimal, run at least 100 simulations.
'''

from datetime import datetime
from functools import wraps
import random, itertools

class Door(object):
  ''' Lots of Door objects will be created with many same contents.
  I wasn't sure how the hashing will work with default mode.
  So I defined __eq__ and __hash__.
  When a new Door object is created, id is incremented by 1 '''
  newid = itertools.count().next
  def __init__(self, content):
    self.id = Door.newid()
    self.content = content

  def __eq__(self, other):
    ''' This is necessary for user defined __hash__ '''
    return self.id == other.id

  def __hash__(self):
    return self.id.__hash__()



def timed(func):
  ''' Benchmarking wrapper '''
  @wraps(func)
  def decorated(*args, **kwargs):
    pre_t = datetime.utcnow()
    result = func(*args, **kwargs)
    post_t = datetime.utcnow()
    duration = (post_t - pre_t).total_seconds()
    print "\t%s: %.2f sec" % (func, duration)
    return result
  return decorated


def generate_doors(car_num, goat_num):
  ''' First use List when generating but return a Tuple
      I do it so that one doesn't accidentally modify the original. '''
  doors = [Door('car') for i in range(car_num)]
  doors += [Door('goat') for i in range(goat_num)]
  return tuple(doors)


def eliminate(doors, elimination):
  ''' Monty opens num(elimination) doors for the challenger.
  e.g. eliminate([Door(), Door(), Door()], 1)
  ==>  [Door(), Door()]'''
  while elimination > 0:
    r = random.choice(doors)
    if r.content == 'goat':
      doors.remove(r)
      elimination -= 1
  return doors


@timed
def choose_original(doors, TRIAL=100):
  ''' Challenger is determined with his first choice.
  Calculate the probability how many times he wins out of
  num(TRIAL) times. '''
  picked_car = 0
  doors = list(doors)    # doors was a tuple

  for i in range(TRIAL):
    ## At every trial, the order of the contents should be "unique"
    random.shuffle(doors)
    if (random.choice(doors)).content == 'car':
      picked_car += 1

  probability = 1.0 * picked_car/TRIAL
  return probability, picked_car


@timed
def choose_switched(doors_original, TRIAL=100, elimination=1):
  ''' Challenger is indecisive. He switches the door to another.
  Note:
  What many people do wrong is that, they try to count also the times
  when the challenger didn't change his decision. That is calculated
  in choose_original(.....). Do separately. It's easier and simpler.'''
  if elimination == 0:
    print "You are not opening any door.\nThis is the same as just choosing the first choice."
    return choose_original(doors, TRIAL)

  elif elimination < 0:
    raise  ArithmeticError("Elimination can't be negative! Give a positive integer!")

  else:
    picked_car = 0
    for i in range(TRIAL):
      doors = list(doors_original)
      random.shuffle(doors)
      ## Challenger makes his first choice
      ## e.g. doors = [car, goat, goat] ===> [car, goat]
      first_choice = doors.pop()
      ## Monty opens one door which has a goat behind the door
      ## e.g. eliminate([car, goat], 1) ===> [car]
      doors = eliminate(doors, elimination)

      second_choice = random.choice(doors)
      if second_choice.content == 'car':
        picked_car += 1

    probability = 1.0 * picked_car/TRIAL
    return probability, picked_car

DOORS = generate_doors(1, 4)
TRIAL = 1000000

(original_pr, original_win) = choose_original(DOORS, TRIAL)
(switched_pr, switched_win) = choose_switched(DOORS, TRIAL, elimination=1)
print "%d trials | original win: %d cars, probability: %.2f%%" % (TRIAL, original_win, 100 * original_pr)
print "%d trials | switched win: %d cars, probability: %.2f%%" % (TRIAL, switched_win, 100 * switched_pr)
