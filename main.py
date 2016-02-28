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
  print("Please specify a file name for the image.")
  exit()
else:
  name = argv[1]
  
# Set the type of the image
fileType = ''
if len(argv) < 3:
  print("Please specify a file type for the image (JPEG, PNG, BMP).")
  exit()
else:
  fileType = argv[2]
  
new = Image.new("RGBA", (50,50), (128, 128, 128, 128))

for x in range(new.size[0]):
  for y in range(new.size[1]):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    a = random.randint(0, 255)
    new.putpixel((x,y),(r,g,b))

new.save("output/" + name + "." + fileType.lower(), fileType)

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
  ga.firstGeneration(experiment, generationList)
  
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
    childList = ga.createChildren(experiment, childList, matingPool)
    
    #Evaluate the list of children
    for eval in range(0, experiment.configInfo.lamb):
      ga.doEval(experiment, childList[eval])
      experiment.population.append(childList[eval])
      experiment.numEvals += 1
      # print(experiment.numEvals)
     
    vis.visualize(experiment.numGen, experiment.population)
		
    # Create the fitness list
    del fitnessList[:]
    for i in experiment.population:
      fitnessList.append(i.fitness)
    # f = ga.displayFitness(experiment.population, "total population")
    
    # Survival Selection
    ga.survivalSelection(experiment)
		
    # Write output
    # writeOutput(experiment, generationList, generationList2, numGen, fitnessList)
    ##print len(experiment.population)
		
  if (experiment.bestEvalThisRun > experiment.maxFitnessValue):
        experiment.maxFitnessValue = experiment.bestEvalThisRun
  
  new = Image.new("RGB", (50,50), (128, 128, 128))

  experiment.population.sort(key=lambda individual: individual.fitness, reverse=True)
  for x in range(new.size[0]):
    for y in range(new.size[1]):
      new.putpixel((x,y),experiment.population[0].solution[x][y])

  new.save("output/run" + str(run) + "." + fileType.lower(), fileType)


