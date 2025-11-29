import random
import pygame

#initializing game and creating window
pygame.init()
screen = pygame.display.set_mode((500,600))

running = True

#game loop
while running:
    #get input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #update

    #display

pygame.QUIT