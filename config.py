# Programmer: Anton Strickland
# Self-drawing program

import sys
import json

class ConfigInfo:
  def __init__(self):
  
    # Set config filepath
    self.cfgPath = 'config/default.cfg'
    self.pCrossover = 90
    self.pMutation = 1
    #if len(sys.argv) > 1:
    # self.cfgPath = sys.argv[1]

    # Read config file
    with open(self.cfgPath) as json_data_file:
      self.data = json.load(json_data_file)

    self.randomSeed = self.data["random seed"]
    self.numberOfEvals = self.data["evaluations per run"]
    self.numberOfRuns = self.data["runs"]
    self.logFile = self.data["log file"]
    self.solutionFile = self.data["solution file"]
    self.mu = self.data["mu"]
    self.lamb = self.data["lambda"]
    self.parentSize = self.data["parent selection size"]
    self.survivalSize = self.data["survival selection size"]
    self.parentFPS = self.data["parent select FPS"]
    self.parentKTS = self.data["parent select KTS"]
    self.survivalTrunc = self.data["survival select Trunc"]
    self.survivalKTS = self.data["survival select KTS"]
    # self.survivalFPS = self.data["survival select FPS"]
    self.endByEvals = self.data["end by num evals"]
    self.endByAverage = self.data["end by average fitness"]
    self.endByBest = self.data["end by best fitness"]
    self.endNNum = self.data["n for termination"]
    # self.initParam = self.data["initialization"]
    self.strategy = self.data["survival strategy"]
    # self.recombChance = self.data["recombination chance"]
    # self.mutateChance = self.data["mutation chance"]
    # self.isAdaptiveRecombination = self.data["enable adaptive recomb"]
    # self.isAdaptiveMutation = self.data["enable adaptive mutation"]
    self.maxDepth= self.data["max depth"]
    self.ramped = self.data["ramped"]
    # self.FPS = self.data["pac FPS"]
    # self.overSelection = self.data["over-selection"]
    # self.subtreeCrossover = self.data["sub-tree crossover"]
    # self.subtreeMutation = self.data["sub-tree mutation"]
    # self.truncation = self.data["truncation"]
    # self.ktournament = self.data["k-tournament"]
    # self.parsimonyPressure = self.data["parsimony pressure"]
    # self.parsimonyPressure = self.data["parsimony coefficient"]