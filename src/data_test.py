from random import random, randint
from time import sleep
from zlm import *



a = [0]
steps:int = 0

import pygame
pygame.init()
SCREEN_SIZE = 1000
PIXELS_PER_VALUE = int(SCREEN_SIZE/ARRAY_SIZE)
screen = pygame.display.set_mode((SCREEN_SIZE,SCREEN_SIZE))
loop = True
counter:float = 0.0
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
    
    a.append(math.sin(counter)*float(randint(1,3))/2.0)

    screen.fill((0,0,0))
    for i in range(len(a)):
        pygame.draw.rect(screen,
                     (255,255,255),
                     (i*PIXELS_PER_VALUE,SCREEN_SIZE/2-a[i]*SCREEN_SIZE/6,4,4))
    if(get_step(a)):
        steps += 1
        print(steps)
    pygame.display.update()
    counter += 0.2
    sleep(0.02)
