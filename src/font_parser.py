CHARS =  95
CHAR_W = 5
IMG_W = 475
CHAR_H = 7
CHAR_PER_BIT = 6
from font import *

import pygame
pygame.init()
screen = pygame.display.set_mode((1000,1000))

font = font.split("\n")
def parse(string,size):
    char_counter = 0
    for char in string:
        if(ord(char)!=32):
            char_pos = (ord(char)-32)*5
            if char_pos > IMG_W:char_pos = 0
            print(ord(char))
            for x in range(CHAR_W):
                for y in range(1,8):
                    if(font[y][x+char_pos] == "#"):
                        pygame.draw.rect(screen,(255,255,255),((x+char_counter)*size,y*size,size,size))
                    else:
                        pygame.draw.rect(screen,(255,0,0),((x+char_counter)*size,y*size,size,size))
        char_counter += CHAR_W
            
parse('pos = 1.1234ää',4)
pygame.display.update()


while True:
    pass
