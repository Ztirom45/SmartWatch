"""
this program loads a fonts from a string in a python file
code written by Ztirom45
LICENCE: GPL4
"""
CHAR_SPACE = 32
#setup font
from font import *

#import pygame to draw the font
import pygame
pygame.init()
screen = pygame.display.set_mode((1000,1000))


def parse(string,pos,size,color,background_color):
    """
    a function that draws text on screen using the imported font.py file
    """
    char_counter = 0
    for char in string:
        if(ord(char)!=CHAR_SPACE):
            #get x position of the char in the image 
            char_pos = (ord(char)-CHAR_SPACE)*CHAR_W
            if char_pos > IMG_W:char_pos = 0
            #draw char
            for x in range(CHAR_W):
                for y in range(CHAR_H):
                    if(font[y][x+char_pos] == "#"):
                        pygame.draw.rect(screen,color,
                            ((x+char_counter)*size+pos[0],y*size+pos[1],size,size))
                    elif background_color != None:
                        pygame.draw.rect(screen,background_color,
                            ((x+char_counter)*size+pos[0],y*size+pos[1],size,size))
        elif background_color!= None:
            pygame.draw.rect(screen,background_color,
                    (char_counter*size+pos[0],pos[1],CHAR_W*size,CHAR_H*size))
        char_counter += CHAR_W
            

if __name__ == "__main__":
    parse('pos = 1.1234ää',(100,100),4,(255,255,255),(255,0,0))
    pygame.display.update()
    while True:
        pass
