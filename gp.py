#Name: Anton Strickland
#CS5401 Assignment 2C

import random
import collections

functionLength = 4
terminalLength = 2


class GPTree():
  def __init__(self, maxDepth, type="None"):

    self.maxDepth = maxDepth
    self.root = None
    self.makeNewRoot(type)
    
    
  def makeNewRoot(self, type="None"):
    if (type == "None"):
      self.root = self.populate_tree(self.maxDepth)
    elif (type == "Full"):
      self.root = self.populate_full(-1, self.maxDepth)
    elif (type == "Grow"):
      self.root = self.populate_grow(-1, self.maxDepth)
    
  def evaluate(self, x, y):
    return self.root.evaluate(x, y)
    
  def print_tree_indented(self, tree, level=0):
    if tree is None:
      return
    self.print_tree_indented(tree.right, level+1)
    print (' ' * level + str(tree.value))
    self.print_tree_indented(tree.left, level+1)
    return

  def output_tree_indented(self, output, tree, level=0):
    if tree is None:
      return ""
    output = self.output_tree_indented(output, tree.right, level+1)
    output =  ' ' * level + str(tree.value) + "\n"
    # print output
    output = self.output_tree_indented(output, tree.left, level+1)
    return output
    
  def getFromTerminalSet(self, num):
    if num is 0:
      return 'x'
    elif num is 1:
      return 'y'
    else:
      return random.random()

  def getFromFunctionSet(self, num):
    if num is 0:
      return '+'
    elif num is 1:
      return '-'
    elif num is 2:
      return '*'
    elif num is 3:
      return '/'
    else:
      return 'r'

  def populate_tree(self, maxDepth):
    
    r = random.randint(0,functionLength)
    startFunction = self.getFromFunctionSet(r)
    
    tree = GPNode(startFunction, self, self, None)
    self.populate_recursive(tree, 0, maxDepth)
    # self.print_tree_indented(tree)
    
    return tree
    
  def populate_recursive(self, currentNode, currentDepth, maxDepth):
  
    if (random.random() > 0.5 and currentDepth < maxDepth):
      r = random.randint(0,functionLength)
      currentNode.left = GPNode(self.getFromFunctionSet(r), self, currentNode, currentDepth)
      currentNode.left.branch = "Left"
      self.populate_recursive(currentNode.left, currentDepth+1, maxDepth)
    else:
      r = random.randint(0,terminalLength)
      currentNode.left = GPNode(self.getFromTerminalSet(r), self, currentNode, currentDepth)
      currentNode.left.branch = "Left"
      
    if (random.random() > 0.5 and currentDepth < maxDepth):
      r = random.randint(0,functionLength)
      currentNode.right = GPNode(self.getFromFunctionSet(r), self, currentNode, currentDepth)
      currentNode.right.branch = "Right"
      self.populate_recursive(currentNode.right, currentDepth+1, maxDepth)
    else:
      r = random.randint(0,terminalLength)
      currentNode.right = GPNode(self.getFromTerminalSet(r), self, currentNode, currentDepth)
      currentNode.right.branch = "Right"
    return

  def populate_full(self, currentDepth, maxDepth, currentNode=None):
  
    if currentDepth == -1:
      r = random.randint(0,2)
      startFunction = self.getFromFunctionSet(r)
    
      root = GPNode(startFunction, self, 0, None) 
      self.populate_full(currentDepth+1, maxDepth, root)
      return root
    
    # If we are not at the max depth, choose a function  
    if(currentDepth < maxDepth):
      r = random.randint(0,functionLength)
      currentNode.left = GPNode(self.getFromFunctionSet(r), self, currentNode, currentDepth)
      currentNode.left.branch = "Left"
      self.populate_full(currentDepth+1, maxDepth, currentNode.left)
      r = random.randint(0,functionLength)
      currentNode.right = GPNode(self.getFromFunctionSet(r), self, currentNode, currentDepth)
      currentNode.right.branch = "Right"
      self.populate_full(currentDepth+1, maxDepth, currentNode.right)
        
    # Otherwise, choose a terminal  
    else:
      r = random.randint(0,terminalLength)
      currentNode.left = GPNode(self.getFromTerminalSet(r), self, currentNode, currentDepth)
      currentNode.left.branch = "Left"
      r = random.randint(0,terminalLength)
      currentNode.right = GPNode(self.getFromTerminalSet(r), self, currentNode, currentDepth)
      currentNode.right.branch = "Right"
    
    return currentNode
    
  def populate_grow(self, currentDepth, maxDepth, currentNode=None):
    if currentDepth == -1:
      r = random.randint(0,2)
      startFunction = self.getFromFunctionSet(r)
      
      root = GPNode(startFunction, self, 0, None) 
      self.populate_grow(currentDepth+1, maxDepth, root)
      return root
    
    # Choose between a function and a terminal if not at max depth
    if(currentDepth < maxDepth):
      if (random.random() > 0.5):
        r = random.randint(0,functionLength)
        currentNode.left = GPNode(self.getFromFunctionSet(r), self, currentNode, currentDepth)
        currentNode.left.branch = "Left"
        self.populate_grow(currentDepth+1, maxDepth, currentNode.left)
      else:
        r = random.randint(0,terminalLength)
        currentNode.left = GPNode(self.getFromTerminalSet(r), self, currentNode, currentDepth)
        currentNode.left.branch = "Left"
        
      if (random.random() > 0.5):
        r = random.randint(0,functionLength)
        currentNode.right = GPNode(self.getFromFunctionSet(r), self, currentNode, currentDepth)
        currentNode.right.branch = "Right"
        self.populate_grow(currentDepth+1, maxDepth, currentNode.right)
      else:
        r = random.randint(0,terminalLength)
        currentNode.right = GPNode(self.getFromTerminalSet(r), self, currentNode, currentDepth)
        currentNode.right.branch = "Right"
        
    # If we are at the max depth, choose a terminal  
    else:
      r = random.randint(0,terminalLength)
      currentNode.left = GPNode(self.getFromTerminalSet(r), self, currentNode, currentDepth)
      currentNode.left.branch = "Left"
      r = random.randint(0,terminalLength)
      currentNode.right = GPNode(self.getFromTerminalSet(r), self, currentNode, currentDepth)
      currentNode.right.branch = "Right"
      
    return currentNode
  
  
    
class GPNode():
  def __init__(self, value, evaluator, parent, depth):
    self.left = None
    self.right = None
    self.value = value
    self.evaluator = evaluator
    self.id = None
    self.depth = depth
    self.parent = parent
    self.branch = None
    
    
  def evaluate(self, x, y):
    # print "value: " + str(self.value)
    if self.value == '+':
      return self.left.evaluate(x, y) + self.right.evaluate(x, y)
    elif self.value == '-':
      return self.left.evaluate(x, y) - self.right.evaluate(x, y)
    elif self.value == '*':
      return self.left.evaluate(x, y) * self.right.evaluate(x, y)
    elif self.value == '/':
    
      left = self.left.evaluate(x, y)
      right = self.right.evaluate(x, y)
      
      if right == 0:
        return 0
      else:
        return left / right
    elif self.value == 'r':
      #print self.left.evaluate()
      #print self.right.evaluate()
      
      left = self.left.evaluate(x, y)
      right = self.right.evaluate(x, y)
      
      if left == right:
        return left
        
      if left < right:
        return random.uniform(left, right)
      else:
        return random.uniform(right, left)
    
    elif self.value == 'x':
      return x
    elif self.value == 'y':
      return y
    else:
      return self.value
      



  
def assignNode(node, id):
  if node is None:
    return
    
  node.id = id
  id = id + 1
  # print str(node.value) + " " + str(node.id)
  
  if node.left is not None:
    node.left.id = id
    #print "left"
    id = assignNode(node.left, id)
  if node.right is not None:
    node.right.id = id
    #print "right"
    id = assignNode(node.right, id)
    
  return id
  
def checkRoot(node):

  id = 0
  node.id = id
  id = id + 1
  
  # print "\n\nROOT"
  # print str(node.value) + " " + str(node.id)
  
  if node.left is not None:
    # print "\nLEFT"
    id = id + 1
    node.left.id = id
    id = assignNode(node.left, id)
  if node.right is not None:
    # print "\nRIGHT"
    node.right.id = assignNode(node.right, id)  
    
  return id
  
  
def findRandomNode(node, id):
  if node is None:
    return None
  
  # We have found the randomly selected node
  if node.id == id:
    return node
  
  if node.left is not None:
    node = findRandomNode(node.left, id+1)
  if node.right is not None:
    node = findRandomNode(node.right, id+1)
    
  return node

  
def subTreeCrossover(tree1, tree2, gptree=None):

  # print "Tree A Before:"
  # gptree.print_tree_indented(root1)
  # print "Tree B Before:"
  # gptree.print_tree_indented(root2)
  
  root1 = tree1.root
  root2 = tree2.root
  
  # Give an id to each node in each tree
  numNodes1 = checkRoot(root1)
  numNodes2 = checkRoot(root2)
  r1 = random.randint(1, numNodes1)
  r2 = random.randint(1, numNodes2)
  
  # Check the id of each node in each tree to find the right ones
  node1 = findRandomNode(root1, r1)
  node2 = findRandomNode(root2, r2)
  
  # print "Node1 Value: " + str(node1.value) + " " + str(node1.id)
  # print "Node2 Value: " + str(node2.value) + " " + str(node2.id)
  
  # Swap the two subtrees
  # swapSubtrees(node1, root1, node2.parent)
  # swapSubtrees(node2, root2, node1.parent)
  
  temp1 = node1.parent
  temp2 = node2.parent
  
  node1.parent = temp2
  node2.parent = temp1
  
  if node1.branch == "Left":
    temp2.left = node1
  else:
    temp2.right = node1
    
  if node2.branch == "Left":
    temp1.left = node2
  else:
    temp1.right = node1
  
  # print "Tree A After:"
  # gptree.print_tree_indented(root1)
  # print "Tree B After:"
  # gptree.print_tree_indented(root2)
  
  tree1.root,tree2.root = root1,root2

  return tree1,tree2

def subTreeMutation(gptree, root):
  
  #gptree.print_tree_indented(root)
  
  # Give an id to each node in each tree
  numNodes = assignRootID(root)
  #print numNodes
  r = random.randint(1, numNodes)
  
  # Check the id of each node in each tree to find the right ones
  node = findRandomNode(root, r)
  
  root.left = None
  root.right = None
  root.totalDepth = numNodes
  
  gptree.populate_recursive(node, node.depth, gptree.maxDepth)

  return

def overSelection(population, lamb):

  mating_pool = []
  x = 1

  if len(population) > 1000:
    x = 0.32
  if len(population) > 2000:
    x = 0.16
  if len(population) > 4000:
    x = 0.8
  if len(population) > 8000:
    x = 0.4
    
  population.sort(key=lambda x: x.score, reverse=True)
  
  group1 = []
  group2 = []
  
  length = (int) (len(population) * x)
  
  for i in xrange(length):
    group1.append(population[i])
    population.remove(population[i])
    
  for p in population:
    group2.append(population[p])
    population.remove(population[p])
    
  j = (int) (lamb * 0.80)
  
  for k in xrange(j):
    mating_pool.append(group1[k])
    
  i = 0
  while(len(mating_pool) < lamb):
    mating_pool.append(group2[j+i])
    i = i + 1
    
  return mating_pool
    
