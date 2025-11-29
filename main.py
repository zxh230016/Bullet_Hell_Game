import random
import pygame


FPS = 60
#initializing game and creating window
pygame.init()
screen = pygame.display.set_mode((500,600))
clock = pygame.time.Clock()

running = True

#game loop
while running:
    clock.tick(FPS)
    #get input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #update

    #display

pygame.QUIT