# Programmer: Anton Strickland
# Self-drawing program

import random
import collections
import sys
from datetime import datetime
import time
import config
import gp

# Define classes and functions

palette = [ (255,1,1), (1,255,1), (1,1,255) ] # (255, 255, 1), (255, 1, 255), (1, 255, 255), (255, 255, 255), (1, 1, 1) ]

def clamp(n, smallest, largest): 
  return int(max(smallest, min(n, largest)))

class Individual:
  
  def __init__(self, treeR, treeG, treeB, solution=[], target=None, fitness=-1):
    self.solution = solution
    self.fitness = fitness
    self.pSelection = 0
    self.evaluated = False
    self.target = target
    self.gpTreeR = treeR
    self.gpTreeG = treeG
    self.gpTreeB = treeB
      
  def evaluate(self, x, y):
    r = self.gpTreeR.evaluate(x, y)
    g = self.gpTreeG.evaluate(x, y)
    b = self.gpTreeB.evaluate(x, y)
    return (r,g,b)
    
    
class GeneticAlgorithm:
  
  # Initialize the empty lists
  population = []
  elitistPool = []

  def __init__(self):
    self.bestEvalThisRun = 0
    self.maxFitnessValue = 0
    self.averageFitness = 0
    self.previousAverageFitness = [0]
    self.previousBestThisRun = [0]
    self.avgCounter = 0
    self.bestCounter = 0
    self.configInfo = config.ConfigInfo()
    # self.configInfo.config()
    self.lastRestartNum = 0
    self.gpTree = gp.GPTree(self.configInfo.maxDepth)
          
  def outputResults(self):
    # Write to the output file
    with open(self.configInfo.solutionFile,'w+') as output:
      output.write("c Solution for: " + self.configInfo.cnfFile + '\n')
      output.write("c MAXSAT fitness value: " + str(self.maxFitnessValue) + '\nv ')
      solutionOutput = []
      for i in range(0, len(self.solutionVarList)):
        if (self.solutionVarList[i] == False):
          solutionOutput.append(-1*i)
        else:
          solutionOutput.append(i)
      for i in range(1, len(solutionOutput)):
          output.write(str(solutionOutput[i]) + " ")

  def initializeRun(self, run):
    #Write the current run number to the output file
    with open(self.configInfo.logFile,'a') as output:
      output.write("\nRun " + str(run) + '\n')
    print ("Run: " + str(run))
    
    del self.population[:]
    
    #Reset the best fitness value for this run to zero
    self.bestEvalThisRun = 0
    self.lastRestartNum = 0
    self.numEvals = 0
    self.numGen = 0
  
    return
    
  # initializes a picture of n x n with RGB pixels
  def initializeUniformRandom(self, size):
    sol = []
    for x in range(0,size[0]):
      sol.append([])
      for y in range(0,size[1]):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        sol[x].append( (r,g,b) )
    return sol
      
  def rouletteWheel(self):
    mating_pool = []
    a = []
    for i in range(0, len(self.population)):
      avalue = 0
      for j in range(0, i+1):
        avalue += self.population[j].pSelection
      a.append(avalue)
    
    current_member = 1
    while(current_member <= self.configInfo.lamb+1):
      r = random.random()
      i = 0
      ##print "r: " + str(r)
      while(a[i] < r):
        i = i + 1
      mating_pool.append(self.population[i])
      current_member = current_member + 1
    return mating_pool
  
  def tournamentWithReplacement(self):
    mating_pool = []
    current_member = 1
    k = self.configInfo.parentSize
    #pick k individuals randomly, with or without replacement
    #select the best of these k comparing their fitness
    #denote this individual as i
    # #print "kt: " + str(len(self.population))
    while(current_member <= self.configInfo.mu+1):
      select = []
      
      while(len(select) < k):
        r = random.random()
        
        index = random.randint(0, len(self.population)-1)
        if (r > 0.5):
          select.append(self.population[index])
      best = 0
      bestIndex = 0
      for s in range (0, k):
        if select[s].fitness >= best:
          best = select[s].fitness
          bestIndex = s

      mating_pool.append(select[bestIndex])
      current_member = current_member + 1
    return mating_pool
    
    
  def truncation(self):

    #print_sorted(population, "Truncation Before:")
    
    sortedPopulation = []
    sortedPopulation = self.population
    sortedPopulation.sort(key=lambda x: x.fitness, reverse=True)
    
    newPopulation = []
    for i in range (self.configInfo.mu):
      #print i
      newPopulation.append(sortedPopulation[i])

    del self.population[:]
    
    for i in newPopulation:
      self.population.append(i)
      
    #print_sorted(population, "Truncation After:")
        
    return
    
  def tournamentWithoutReplacement(self):
    current_member = 1
    k = self.configInfo.survivalSize
    #pick k individuals randomly, with or without replacement
    #select the best of these k comparing their fitness
    #denote this individual as i
    while(len(self.population) > self.configInfo.mu):
      select = []
      while(len(select) < k):
        r = random.random()
        index = random.randint(0, len(self.population)-1)
        if r > 0.5:
          select.append(self.population[index])
          self.population.pop(index)
        
      worst = sys.maxsize
      worstIndex = 0
      for s in range (0, k):
        # #print "tourney " + str(select[s].fitness)
        if select[s].fitness <= worst:
          worst = select[s].fitness
          worstIndex = s
      
      # #print "removing " + str(select[worstIndex].fitness)
      select.pop(worstIndex)
      
      for s in select:
        self.population.append(s)
      
      current_member = current_member + 1
    return
        
  def terminationCondition(self):
    ##print self.averageFitness
    ##print self.previousAverageFitness
    if (self.configInfo.endByEvals == "True"):
      if (self.numEvals > self.configInfo.numberOfEvals):
        return False
        
    if (self.configInfo.endByAverage == "True"):
      ##print self.averageFitness
      ##print self.previousAverageFitness
      ##print numGen
      deltaAverageFitness = abs(self.averageFitness - self.previousAverageFitness[0])

      ##print deltaAverageFitness
      if (deltaAverageFitness < 1):
        self.avgCounter += 1
        ##print self.avgCounter
        if (self.avgCounter >= self.configInfo.endNNum):
          if (self.configInfo.elitist != 0):
            self.restart()
            return True
          else:
            return False
        else:
          return True
      else:
        self.avgCounter = 0
        return True
          
    if (self.configInfo.endByBest == "True"):
      deltaBestFitness = abs(self.bestEvalThisRun - self.previousBestThisRun[0])
      if (deltaBestFitness < 1):
        self.bestCounter += 1
        if (self.bestCounter >= self.configInfo.endNNum):
          if (self.configInfo.elitist != 0):
            self.restart()
          return True
        else:
          return False
      else:
        self.bestCounter = 0
        return True
        
    return True

    
def swap_mutation(parent):

  index1 = random.randint(0, len(parent)-1)
  index2 = index1
  while (index2 == index1):
    index2 = random.randint(0, len(parent)-1)
    
  temp = parent[index2]
  
  parent[index2] = parent[index1]
  parent[index1] = temp
  
  return parent
  
# uniform crossover for binary representation
def uniformCrossover(parent1, parent2):
  child1 = []
  child2 = []
  
  for i in range(0, len(parent1)):
    p = random.random()
    if p > 0.5:
      child1.append(parent1[i])
    else:
      child1.append(parent2[i])
  
  for i in range(0, len(child1)):
    child2.append(not child1[i])

  return child1
  
def firstGeneration(exp, generationList, initialTarget, size):
  # Fill the population with mu individuals
  for i in range (0, exp.configInfo.mu):
    individual = Individual(exp.initializeUniformRandom(size), initialTarget)
    exp.population.append(individual)

  #The first generation's mu evaluations
  for eval in range(0, exp.configInfo.mu):
    doEval(exp, exp.population[eval], size)
    exp.numEvals = exp.numEvals + 1
        
  fitnessList = []
  for i in range (0, len(exp.population)):
    fitnessList.append(exp.population[i].fitness)
      
  # Write to the output file
  with open(exp.configInfo.logFile,'a') as output:
    exp.averageFitness = sum(fitnessList) / float(len(fitnessList))
    generationList[exp.numGen].append(exp.averageFitness)
    output.write(str("%04d" % (exp.configInfo.mu)) + '\t' + str("{0:.4f}".format(exp.averageFitness)) + '\t' + str(exp.bestEvalThisRun) + '\n')
    
  return

def parentSelection(exp, matingPool):
  if (exp.configInfo.parentFPS == "True"):
    totalFitness = 0
    for i in range(0, len(exp.population)):
      totalFitness += exp.population[i].fitness
    for i in range(0, len(exp.population)):
      exp.population[i].pSelection = exp.population[i].fitness / (totalFitness*1.0)
    ##print "pop size: " + str(len(exp.population))
    matingPool = exp.rouletteWheel()
  elif (exp.configInfo.parentKTS == "True"):
    matingPool = exp.tournamentWithReplacement()
  else:
    #If neither is true, assume Uniform Random Parent Selection
    while(len(matingPool) < len(experiment.configInfo.lamb)):
      r = random.randint(0, len(experiment.population)-1)
      matingPool.append(experiment.population[r])
  return matingPool
  
def createChildren(exp, childList, matingPool, size):

  recombinationRate = 1
  mutationRate = 1
  mutateChance = 0.75
  
  width, height = size[0], size[1]

  for s in range (0, len(matingPool)-1):
  
    childSolution = []
    # childTarget = matingPool[s].target
    
    # Crosses over two pixels to make a new pixel for each pixel
    # for i in range(0, recombinationRate):
    for x in range(0, width):
      childSolution.append([])
      for y in range(0, height):
        # Cross the two individual pixels
        childPixel = uniformCrossover(matingPool[s].solution[x][y], matingPool[s+1].solution[x][y])
        targetPixel = uniformCrossover(childTarget[x][y], childTarget[x][y])

        for k in range(0,3):
              
          if (random.random() > mutateChance):
             # childPixel = random.choice(palette)
             # target[x][y] = childPixel
             
          
            if childTarget[x][y][k] > childPixel[k]:
              childPixel[k] += random.randint(0, 24)
            else:
              childPixel[k] -= random.randint(0, 24)
              
            childPixel[k] = clamp(childPixel[k], 0, 255)

        childSolution[x].append( (childPixel[0], childPixel[1], childPixel[2] ))
    
    # Add finalized child to the list of children
    childList.append(Individual(childSolution, childTarget))
        
  return childList
      
def displayFitness(pop, string=""):
  fitnessList = []
  #print string
  for i in range (len(pop)):
    fitnessList.append(pop[i].fitness)
    # #print fitnessList[i]
    fitnessList.sort()
  print (fitnessList)
  #print len(pop)
   
  return fitnessList

def survivalSelection(exp):
  if (exp.configInfo.survivalTrunc == "True"):
    exp.truncation()
  elif (exp.configInfo.survivalKTS == "True"):
    exp.tournamentWithoutReplacement()
  elif (exp.configInfo.survivalFPS == "True"):
    totalFitness = 0
    for i in range(0, len(exp.population)):
      totalFitness += exp.population[i].fitness
    for i in range(0, len(exp.population)):
      exp.population[i].pSelection = exp.population[i].fitness / (totalFitness*1.0)
    selection = exp.rouletteWheel()
    for s in selection:
      exp.population.remove(Individual(s))
  else:
    #If neither is true, assume Uniform Random Survival Selection
    while(len(exp.population) > exp.configInfo.mu):
      exp.population.pop(random.randint(0, len(exp.population)-1))
  
def writeOutput(exp, genList1, genList2, genNum, fitnessList):
  # Write to the output file
      with open(exp.configInfo.logFile,'a') as output:
        exp.averageFitness = sum(fitnessList) / float(len(fitnessList))
        
        ##print genNum
        ##print len(generationList)
        # Keep track of the average fitness and previous average fitness
        genList1[genNum].append(exp.averageFitness)
        exp.previousAverageFitness = genList1[genNum-1]
        
        # Keep track of the best fitness and previous best fitness
        genList2[genNum].append(exp.bestEvalThisRun)
        exp.previousBestThisRun = genList2[genNum-1]
        
        output.write(str("%04d" % (numEvals)) + '\t' + str("{0:.4f}".format(exp.averageFitness)) + '\t' + str(exp.bestEvalThisRun) + '\n')
#------------------------------------


def writeFinalOutput(exp):
  # print experiment.solutionVarList
  # Write to a file the average average and the average best fitness values
  with open("out/averages-" + exp.configInfo.cnfFile[5] + ".txt",'w+') as output:
    for i in range(0, len(generationList)):
    
        if (len(generationList[i]) > 0):
          avgAvgFitness = sum(generationList[i]) / float(len(generationList[i]))
        if len(generationList2[i]) > 0:
          avgBestFitness = sum(generationList2[i]) / float(len(generationList2[i]))
        else:
          avgBestFitness = 0
        eval = exp.configInfo.mu + exp.configInfo.lamb * i
        output.write(str("%04d" % (eval)) + '\t' + str("{0:.4f}".format(avgAvgFitness)) + '\t'  + str("{0:.4f}".format(avgBestFitness)) + '\n')
  exp.outputResults()
    
def doEval(exp, individual, size):

  diffList = []
  # Get difference between each RGB value 
  width, height = size[0], size[1]
  for x in range(width):
    for y in range(height):
      eval = individual.evaluate(x,y)
      individual.solution[x][y] = ( clamp(eval[0],0,255), clamp(eval[1],0,255), clamp(eval[2],0,255) )
      diffR = abs(individual.solution[x][y][0] - individual.target[x][y][0])/255
      diffG = abs(individual.solution[x][y][1] - individual.target[x][y][1])/255
      diffB = abs(individual.solution[x][y][2] - individual.target[x][y][2])/255
      # print(diffR, diffG, diffB)
      diffTotal = (diffR + diffG + diffB)/3
      # print(diffTotal)
      diffList.append(diffTotal)

    # Save the solution and its fitness for this individual
    individual.fitness = 100 - (100 * sum(diffList)/(width*height))
    # print(individual.fitness)
    individual.evaluated = True

    # print(individual.fitness, exp.bestEvalThisRun)
    # Save the best fitness value for this run
    if (individual.fitness > exp.bestEvalThisRun):
      exp.bestEvalThisRun = individual.fitness
    
def firstGenerationTree(exp, generationList, initialTarget, size):

  # Fill the population with mu individuals
  for i in range (0, exp.configInfo.mu):
    
    if exp.configInfo.ramped == "True":
      if i < exp.configInfo.mu / 2:
        treeR = gp.GPTree(exp.configInfo.maxDepth, "Full")
        treeG = gp.GPTree(exp.configInfo.maxDepth, "Full")
        treeB = gp.GPTree(exp.configInfo.maxDepth, "Full")
      else:
        treeR = gp.GPTree(exp.configInfo.maxDepth, "Full")
        treeG = gp.GPTree(exp.configInfo.maxDepth, "Full")
        treeB = gp.GPTree(exp.configInfo.maxDepth, "Full")
    else:
      treeR = gp.GPTree(exp.configInfo.maxDepth)
      treeG = gp.GPTree(exp.configInfo.maxDepth)
      treeB = gp.GPTree(exp.configInfo.maxDepth)
      
    exp.population.append(Individual(treeR, treeG, treeB, exp.initializeUniformRandom(size), initialTarget))
    
  # The first generation's mu evaluations
  for eval in range(0, exp.configInfo.mu):
    doEval(exp, exp.population[eval], size)
    exp.numEvals = exp.numEvals + 1
        
  fitnessList = []
  for i in range (0, len(exp.population)):
    fitnessList.append(exp.population[i].fitness)
    

def createChildrenTree(exp, childList, matingPool, initialTarget, imgSize):

  size = 0
  while(size < len(matingPool)):
    # print size
    
    r = random.randint(0, 100)
    
    if r <= exp.configInfo.pCrossover and size+1 < len(matingPool):
      # print "Do crossover!"
      treeR = gp.subTreeCrossover(matingPool[size].gpTreeR, matingPool[size+1].gpTreeR)
      treeG = gp.subTreeCrossover(matingPool[size].gpTreeG, matingPool[size+1].gpTreeG)
      treeB = gp.subTreeCrossover(matingPool[size].gpTreeB, matingPool[size+1].gpTreeB)
      size = size + 2
      #print matingPool[s].solution
      
      # Add finalized children to the list of children
      childList.append(Individual(treeR[0], treeG[0], treeB[0], exp.initializeUniformRandom(imgSize), initialTarget))
      childList.append(Individual(treeR[1], treeG[1], treeB[1], exp.initializeUniformRandom(imgSize), initialTarget))
    
    elif r > exp.configInfo.pCrossover and r < exp.configInfo.pCrossover + exp.configInfo.pMutation:
      # print "Do mutation!"
      treeR = gp.subTreeMutation(matingPool[size].gpTreeR, matingPool[size].gpTreeR.root)
      treeG = gp.subTreeMutation(matingPool[size].gpTreeG, matingPool[size].gpTreeG.root)
      treeB = gp.subTreeMutation(matingPool[size].gpTreeB, matingPool[size].gpTreeB.root)
      
      childList.append(Individual(treeR, treeG, treeB, exp.initializeUniformRandom(imgSize), initialTarget))
      size = size + 1
    else:
      # print "Do replication!"
      # Select individual based on fitness
      # Insert copy of it into next gen
      childList.append(Individual(matingPool[size].gpTreeR, matingPool[size].gpTreeG, matingPool[size].gpTreeB, exp.initializeUniformRandom(imgSize), initialTarget))
      size = size + 1
        
  return childList