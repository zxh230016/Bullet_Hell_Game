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
#bgm
pygame.mixer.init()
menu_bgm = "StartPageBGM.mp3"
game_bgm = "GameBGM.mp3"
#sfx
select_sfx = pygame.mixer.Sound("Select.mp3")
quit_sfx = pygame.mixer.Sound("Quit.mp3")

def start_menu():
    play_music(menu_bgm)  # play menu music
    menu_running = True
    font = pygame.font.Font('ScienceGothic.ttf', 40)

    while menu_running:
        screen.fill((0, 0, 0))
        start_text = font.render("Press S to Start", True, (0, 255, 0))
        quit_text = font.render("Press Q to Quit", True, (255, 0, 0))

        screen.blit(start_text, (WIDTH/2 - start_text.get_width()/2, HEIGHT/2))
        screen.blit(quit_text, (WIDTH/2 - quit_text.get_width()/2, HEIGHT/2 + 60))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                quit_sfx.play()
                pygame.time.delay(300)
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    flash_text(screen, start_text, (WIDTH/2 - start_text.get_width()/2, HEIGHT/2), sfx=select_sfx)
                    menu_running = False  # exit menu
                    play_music(game_bgm)
                elif event.key == pygame.K_q:
                    flash_text(screen, start_text, (200, 200))
                    quit_sfx.play()
                    pygame.time.delay(250)
                    pygame.quit()
                    exit()

def flash_text(surface, text_surf, pos, flashes=2, speed=150, bg_color=(0, 0, 0), sfx=None):
    if sfx:
        sfx.play()

    rect = text_surf.get_rect(topleft=pos)

    for i in range(flashes):
        #hide text
        surface.fill(bg_color, rect)
        pygame.display.update(rect)
        pygame.time.delay(speed)

        #show text
        surface.blit(text_surf, pos)
        pygame.display.update(rect)
        pygame.time.delay(speed)

def play_music(bgm_file, loop=-1, volume=0.5, fadeout_ms=1000, fadein_ms=1000):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(fadeout_ms)
    pygame.mixer.music.load(bgm_file)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops=loop, fade_ms=fadein_ms)

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

        #health
        self.health = 5

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

        #collision check with enemy bullets
        hits = pygame.sprite.spritecollide(self, bullets, True)
        if hits:
            self.health -= 1
            if self.health <= 0:
                game_over_screen()


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

def game_over_screen():
    screen.fill((0, 0, 0))
    pygame.mixer.music.stop()
    font_big = pygame.font.Font('ScienceGothic.ttf', 50)
    font_small = pygame.font.Font('ScienceGothic.ttf', 30)

    #display YOU DIED
    text = font_big.render("YOU DIED", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
    screen.blit(text, text_rect)

    #display options
    retry_text = font_small.render("Press R to Try Again", True, (255, 255, 255))
    quit_text = font_small.render("Press Q to Quit", True, (255, 255, 255))
    screen.blit(retry_text, (WIDTH/2 - retry_text.get_width()/2, HEIGHT/2 + 20))
    screen.blit(quit_text, (WIDTH/2 - quit_text.get_width()/2, HEIGHT/2 + 60))

    #pause loop
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_sfx.play()
                pygame.time.delay(250)
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    flash_text(screen, retry_text, (WIDTH/2 - retry_text.get_width()/2, HEIGHT/2 + 20), sfx=select_sfx)
                    waiting = False
                    reset_game()
                elif event.key == pygame.K_q:
                    quit_sfx.play()
                    pygame.time.delay(300)
                    pygame.quit()
                    exit()
        pygame.display.update()

def reset_game():
    global all_sprite, player, bullets
    all_sprite.empty()
    bullets.empty()
    
    player = Player()
    all_sprite.add(player)
    play_music(game_bgm)

font = pygame.font.Font('ScienceGothic.ttf', 20)

#display menu
start_menu()

#game loop
running = True

while running:
    clock.tick(FPS)
    #get input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            quit_sfx.play()
            pygame.time.delay(300)
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
    health_text = font.render(f'Life: {player.health}', True, (255, 255, 255))
    screen.blit(health_text, (WIDTH - 80, 10))

    pygame.display.update()


pygame.QUIT