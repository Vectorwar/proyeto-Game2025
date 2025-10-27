"""This is a pilot test file for the juego package.
create by Jose juan Padilla"""

import pygame
import random 

pygame.init()
#Screen dimensions
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space rain game")

#Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

#player properties
player_width = 50
player_height = 60
player = pygame.Rect(width // 2 - player_width // 2,
                     height - player_height - 10,
                     player_width,
                     player_height)

# main loop of the game
running = True # game is running
while running: # this is a loop that keeps the game running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()