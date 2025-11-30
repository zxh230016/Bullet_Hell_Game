import random
import pygame


FPS = 60
WIDTH = 500
HEIGHT = 600

#initializing game and creating window
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 200

all_sprite = pygame.sprite.Group()
player = Player()
all_sprite.add(player)

#game loop
running = True


while running:
    clock.tick(FPS)
    #get input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #update

    #display
    all_sprite.draw(screen)
    pygame.display.update()

pygame.QUIT