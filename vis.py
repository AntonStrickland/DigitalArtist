# Programmer: Anton Strickland
# Self-drawing program

import pygame
import sys

screen = pygame.display.set_mode((1024,480))
pygame.init()
myfont = pygame.font.SysFont("monospace", 15)
headerFont = pygame.font.SysFont("monospace", 30)

def checkInput():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
        
def visualize(gen, pics):
  screen.fill( (0,0,0) )
  
  bigX = 25
  bigY = 100
  bigWidth = 50
  
  smallX = 25
  smallY = bigY
  
  picsPerColumn = 4
  picsPerGen = 29
  index = 0
  
  delayTime = 0

  # render text
  label = headerFont.render("Generation: " + str(gen), 1, (255,255,0))
  screen.blit(label, (bigX, bigY-30))
  
  pics.sort(key=lambda individual: individual.fitness, reverse=True)
  nodeIndex = 0
  
  for individual in pics:
    if nodeIndex > picsPerGen:
      break
    if (index > picsPerColumn):
      index = 0
      smallX = smallX + 125
      smallY = 100
      
    for i in range(50):
      for j in range(50):
        screen.set_at((smallX+i, smallY+j), individual.solution[i][j])
        
    label = myfont.render(str(int(individual.fitness)), 1, (255,255,0))
    screen.blit(label, (smallX+60, smallY))
    
    smallY = smallY + 75
    index = index + 1
    nodeIndex = nodeIndex + 1
    checkInput()
    
  pygame.display.update()
  pygame.time.delay(delayTime)
    
  

