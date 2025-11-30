import random
import pygame
import math

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
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.speedy = 8
        self.shoot_delay = 200   # milliseconds between bullets
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_w]:
            self.rect.y -= self.speedy
        if key_pressed[pygame.K_s]:
            self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet1 = PlayerBullet(self.rect.centerx - 10, self.rect.top)
            bullet2 = PlayerBullet(self.rect.centerx + 10, self.rect.top)
            all_sprite.add(bullet1, bullet2)
            bullets.add(bullet1, bullet2)
  

all_sprite = pygame.sprite.Group()
player = Player()
all_sprite.add(player)

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = 0

        # give random angle
        angle = random.uniform(-60, 60)
        speed = random.randint(3, 6)

        # movement
        self.speedx = speed * math.sin(math.radians(angle))
        self.speedy = speed * math.cos(math.radians(angle))

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()

bullets = pygame.sprite.Group()
all_sprite.add(bullets)

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 25))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom <0:
            self.kill()


#game loop
running = True

while running:
    clock.tick(FPS)
    #get input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player.shoot() #continuous shooting

    # randomly spawn bullets
    if random.random() < 0.15:
        b = EnemyBullet()
        all_sprite.add(b)
        bullets.add(b)   
    
    #update
    all_sprite.update()

    #display
    screen.fill((0, 0, 0))
    all_sprite.draw(screen)
    pygame.display.update()

pygame.QUIT