# Programmer: Anton Strickland
# Self-drawing program

from PIL import Image
from sys import argv
import random
import ga
import vis



# Set the name of the image
name = ''
if len(argv) < 2:
  print("Please specify a file name for the input image.")
  exit()
else:
  name = argv[1]
  
# Set the type of the image
ext = ''
if len(argv) < 3:
  print("Please specify a file type for the image (JPEG, PNG, BMP).")
  exit()
else:
  ext = argv[2]
  
img = Image.open("input/"+name+"."+ext.lower())
target = []
for x in range(0,img.width):
  target.append([])
  for y in range(0,img.height):
    pix = img.getpixel( (x,y) )
    # print("p: " + str(pix))
    #if pix[0] > 33 and pix[1] > 33 and pix[2] > 33:
      #p0 = ga.clamp(pix[0] + random.randint(0, 128), 0, 255)
      #p1 = pix[1]
      #p2 = pix[2]
      # p1 = ga.clamp(pix[1] + random.randint(-64, 64), 0, 255)
      # p2 = ga.clamp(pix[2] + random.randint(-64, 64), 0, 255)
      # print((p0, p1, p2))
      #target[x].append( (p0, p1, p2) )
    #else:
    target[x].append(pix)
  
# new = Image.new("RGBA", (50,50), (128, 128, 128, 128))
'''
for x in range(new.size[0]):
  for y in range(new.size[1]):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    a = random.randint(0, 255)
    new.putpixel((x,y),(r,g,b))
'''
# new.save("output/" + name + "." + ext.lower(), ext.upper())

# Main part of the code begins here
experiment = ga.GeneticAlgorithm()

numGenerations = ((experiment.configInfo.numberOfEvals - experiment.configInfo.mu)/(experiment.configInfo.lamb)) + 1
childList, matingPool, fitnessList, generationList, generationList2 = [], [], [], [], []

print(experiment.configInfo.numberOfEvals, numGenerations)
for k in range(0, int(numGenerations)+3):
  generationList.append([])
  generationList2.append([])
	
#For each run in the range
for run in range(1,experiment.configInfo.numberOfRuns+1):
  experiment.initializeRun(run)
  ga.firstGenerationTree(experiment, generationList, target, img.size)
  
  #The other generations' lambda evaluations
  while(experiment.terminationCondition()):
    experiment.numGen += 1
    # print ("Generation: " + str(experiment.numGen))
    
    # Survival Strategy, if "Plus", empty the population and only use mating pool
    if (experiment.configInfo.strategy == "Plus"):
      del experiment.population[:]
    
    # Calculate probability for parent selection and create children from mating pool
    del childList[:], matingPool[:]
    matingPool = ga.parentSelection(experiment, matingPool)
    childList = ga.createChildrenTree(experiment, childList, matingPool, target, img.size)
    
    #Evaluate the list of children
    for eval in range(0, experiment.configInfo.lamb):
      ga.doEval(experiment, childList[eval], img.size)
      experiment.population.append(childList[eval])
      experiment.numEvals += 1
      # print(experiment.numEvals)
     
    vis.visualize(experiment.numGen, experiment.population, img.size)
		
    # Create the fitness list
    del fitnessList[:]
    for i in experiment.population:
      fitnessList.append(i.fitness)
    # f = ga.displayFitness(experiment.population, "total population")
    
    # Survival Selection
    ga.survivalSelection(experiment)
    
    if experiment.population[0].fitness >= 99:
      print("99%!")
      break
		
    # Write output
    # writeOutput(experiment, generationList, generationList2, numGen, fitnessList)
    ##print len(experiment.population)
		
  if (experiment.bestEvalThisRun > experiment.maxFitnessValue):
        experiment.maxFitnessValue = experiment.bestEvalThisRun
  
  new = Image.new("RGB", (img.width,img.height), (128, 128, 128))

  experiment.population.sort(key=lambda individual: individual.fitness, reverse=True)
  for x in range(new.size[0]):
    for y in range(new.size[1]):
      new.putpixel((x,y),experiment.population[0].solution[x][y])

  new.save("output/" + name + "-run" + str(run) +  "." + ext.lower(), ext.upper())


