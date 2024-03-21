CHARS =  95
CHAR_W = 5
CHAR_H = 7
CHAR_PER_BIT = 6

from PIL import Image

rgb_2_1bit = lambda rgb: rgb[0]+rgb[1]+rgb[2]>383

with Image.open("7x5Font.png") as img:
    data = img.load()

new_data = []
bit_image = []
for t in range(CHARS):
    new_data.append([])
    bits = [0]*CHAR_PER_BIT
    bit_counter = 0
    for y in range(CHAR_H):
        new_data[t].append([])
        for x in range(CHAR_W):
            new_data[t][y].append(not(rgb_2_1bit(data[x+t*CHAR_W,y])))
            if(not(rgb_2_1bit(data[x+t*CHAR_W,y]))):
                byte = int(bit_counter/8)
                bit_offset = bit_counter-byte*8
                bits[byte] += 2**bit_offset
            bit_counter += 1
    bit_image+=bits

print(bit_image)

import pygame
pygame.init()
screen = pygame.display.set_mode((1000,3000))
RECT_SIZE = 3

image_str = ""

print(img.size)

for y in range(CHAR_H): 
    image_str += "\n"
    for t in range(CHARS):
        for x in range(CHAR_W):
            if(new_data[t][y][x]):
                image_str += "#"
                pygame.draw.rect(screen,(255,255,255),
                    (x*RECT_SIZE+100,(y+t*CHAR_H)*RECT_SIZE,RECT_SIZE,RECT_SIZE))
            else:
                image_str += " "

pygame.display.update()

with open("font.py","w") as file:
    file.write(image_str)
while True:pass
