
#Blayne Hoy
#U1 L1 A very large rat

import random
from random import triangular
from random import shuffle
import time
from rat import Rat

GOAL = 50000                # Target average weight (grams)
NUM_RATS = 20               # Max adult rats in the lab
INITIAL_MIN_WT = 200        # The smallest rat (grams)
INITIAL_MAX_WT = 600        # The chonkiest rat (grams)
INITIAL_MODE_WT = 300       # The most common weight (grams)
MUTATE_ODDS = 0.01          # Liklihood of a mutation
MUTATE_MIN = 0.5            # Scalar mutation - least beneficial
MUTATE_MAX = 1.2            # Scalar mutation - most beneficial
LITTER_SIZE = 8             # Pups per litter (1 mating pair)
GENERATIONS_PER_YEAR = 10   # How many generations are created each year
GENERATION_LIMIT = 500      # Generational cutoff - stop breeded no matter what
MUTATE_ODDS = 0.01
MUTATE_MIN = 0.5
MUTATE_MAX = 1.2

def initial_population():
  '''Create the initial set of rats based on constants'''
  rats = [[],[]]
  mother = Rat("F", INITIAL_MIN_WT)
  father = Rat("M", INITIAL_MAX_WT)
  
  for r in range(NUM_RATS):
    if r < 10:
      sex = "M"
      ind = 0
    else:
      sex = "F"
      ind = 1
  
    wt = calculate_weight(sex, mother, father)
    R = Rat(sex, wt)
    rats[ind].append(R)
  
  return rats

def calculate_weight(sex, mother, father):

  min = mother.getWeight()
  max = father.getWeight()  
  
  if sex == "M":
    wt = int(triangular(min, max, max))
  else:
    wt = int(triangular(min, max, min))
  return wt


def mutate(pups):
  for a in pups:
    for b in a:
      if random.random() < MUTATE_ODDS:
        mutation_factor = random.triangular(MUTATE_MIN, MUTATE_MAX, 1.0)
        mutated_weight = int(b.getWeight() * mutation_factor)
        b.weight = mutated_weight

  return pups  


def breed(rats):
  """Create mating pairs, create LITTER_SIZE children per pair"""
  random.shuffle(rats[0])
  random.shuffle(rats[1])
  pups = [[],[]]
  flag = 0
  for a in range(10):
    mother = rats[1][a]
    father = rats[0][a]
    for b in range(8):
      if flag < 40:
        wt = calculate_weight("M", mother, father)
        children = Rat("M", wt) 
        pups[0].append(children)
      else:
        wt = calculate_weight("F", mother, father)
        children = Rat("F", wt)
        pups[1].append(children)
      flag += 1

  

  return pups

def select(rats, pups):
  largest = []
  newRats = [[],[]]
  rats[0].extend(pups[0])
  rats[1].extend(pups[1])
  rats[0].sort(reverse=True)
  rats[1].sort(reverse=True)
  largestmale = rats[0][0]
  largestfemale = rats[1][0]
  newRats[0].extend(rats[0][:10])
  newRats[1].extend(rats[1][:10])
  rats = newRats

  if largestmale >= largestfemale:
    largest.append(largestmale)
  else:
    largest.append(largestfemale)




  return rats, largest[0]

def calculate_mean(rats):
  total_weight_males = sum(r.getWeight() for r in rats[0])
  total_weight_females = sum(r.getWeight() for r in rats[1])
  total_weight = total_weight_males + total_weight_females
  num_males = len(rats[0])
  num_females = len(rats[1])
  numRats = num_males + num_females

  return total_weight // numRats

def fitness(mean_weight):
  """Determine if the target average matches the current population's average"""

  
  return mean_weight >= GOAL


def main():
  rats = initial_population()
  generation = 0
  largest_rat_ever = None
  average_weights = []
  start_time = time.time()

  generation_data = []

  while generation < GENERATION_LIMIT:
    mean_weight = calculate_mean(rats)
    average_weights.append(mean_weight)
    generation_data.append(f"Gen {generation}: {mean_weight}G")

    if fitness(mean_weight):
      print(f"Goal reached in {generation}.")
      break
    
    pups = breed(rats)
    pups = mutate(pups)
    rats, largest_rat = select(rats, pups)
    if largest_rat_ever is None or largest_rat.getWeight() > largest_rat_ever.getWeight():
      largest_rat_ever = largest_rat
    
    generation += 1

  end_time = time.time()
  time_elapsed = end_time - start_time
  years_taken = generation / GENERATIONS_PER_YEAR

  print("\n --------------FINAL REPORT--------------")
  print(f"Number of generations bred: {generation}.")
  print(f"Average weight for every generation: {average_weights}.")
  print(f"Number of years taken: {years_taken} years.")
  print(f"Weight of largest rat ever: {largest_rat_ever.getWeight()} grams")
  if time_elapsed < 60:
    print(f"Total time: {time_elapsed} seconds")
  else:
    print(f"Total time: {time_elapsed} minutes")

  

if __name__ == "__main__":
  main()