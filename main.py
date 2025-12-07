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
player_hitted_sfx = pygame.mixer.Sound("player_hitted.mp3")
#bullet image
IMG_DANNMAKU = pygame.image.load("red_bullet.png").convert_alpha()
IMG_DANNMAKU = pygame.transform.scale(IMG_DANNMAKU, (16, 16))
IMG_ENEMY_BULLET = pygame.image.load("blue_bullet.png").convert_alpha()
IMG_ENEMY_BULLET = pygame.transform.scale(IMG_ENEMY_BULLET, (20, 20))

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
        pygame.time.delay(250)

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
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 4
        self.speedy = 4

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
        hits = pygame.sprite.spritecollide(self, enemy_bullet, True)
        if hits:
            player_hitted_sfx.play()
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
            player_bullet.add(bullet1, bullet2)

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((6, 15))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom <0:
            self.kill()

all_sprite = pygame.sprite.Group()
player = Player()
all_sprite.add(player)
player_bullet = pygame.sprite.Group()

class Dannmaku:
    def __init__(self, enemy, bullet_group, all_sprites):
        self.enemy = enemy
        self.bullet_group = bullet_group
        self.all_sprites = all_sprites

        self.angle = 0
        self.spin_speed = 0.03
        self.bullet_speed = 2
        self.bullet_count = 16
        self.shoot_delay = 6
        self.timer = 0

    def update(self):
        self.angle += self.spin_speed  
        if self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi

        self.timer += 1
        if self.timer >= self.shoot_delay:
            self.timer = 0
            cx, cy = self.enemy.rect.center

            for i in range(self.bullet_count):
                bullet_angle = self.angle + (i * (2 * math.pi / self.bullet_count))
                bullet = DannmakuBullet(start_x=cx, start_y=cy, angle=bullet_angle, radius_speed=0.3, spread_scale=5)
                self.bullet_group.add(bullet)
                self.all_sprites.add(bullet)

class DannmakuBullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, angle, radius_speed=0.3, spread_scale=5):
        super().__init__()
        self.start_x = start_x
        self.start_y = start_y
        self.angle = angle
        self.radius = 8
        self.radius_speed = radius_speed
        self.spread_scale = spread_scale

        self.image = IMG_DANNMAKU
        self.rect = self.image.get_rect()

    def update(self):
        self.radius += self.radius_speed
        offset = self.radius * self.spread_scale
        self.rect.centerx = self.start_x + math.cos(self.angle) * offset
        self.rect.centery = self.start_y + math.sin(self.angle) * offset

        # remove bullets far off-screen
        if (self.rect.x < -50 or self.rect.x > 850 or 
            self.rect.y < -50 or self.rect.y > 650):
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = IMG_ENEMY_BULLET
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

enemy_bullet = pygame.sprite.Group()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(50, WIDTH - 50),
            random.randint(50, HEIGHT // 3)
        )

        self.speed = 3
        self.target_pos = self.get_new_target()
        self.pause_time = 0
        self.pause_duration = 10000  # 10 seconds
        self.health = 200

        self.danmaku = Dannmaku(self, enemy_bullet, all_sprite)

    def get_new_target(self):
        return pygame.Vector2(
            random.randint(50, WIDTH - 50),
            random.randint(50, HEIGHT // 2)
        )

    def update(self):
        global player_bullet
        global score

        enemy_pos = pygame.Vector2(self.rect.center)

        #Movement
        if self.pause_time <= 0:
            direction = self.target_pos - enemy_pos
            distance = direction.length()

            if distance < self.speed:
                self.rect.center = (int(self.target_pos.x), int(self.target_pos.y))
                self.pause_time = self.pause_duration
                self.target_pos = self.get_new_target()
            else:
                move_vector = direction.normalize() * self.speed
                self.rect.centerx += move_vector.x
                self.rect.centery += move_vector.y
        else:
            self.pause_time -= clock.get_time()

        #Collision check
        hits = pygame.sprite.spritecollide(self, player_bullet, True)
        if hits:
            score += 1
            self.health -= 2
            if self.health <= 0:
                game_clear_screen()

        self.danmaku.update()

enemy = Enemy()
all_sprite.add(enemy)

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
    global all_sprite, player, player_bullet, enemy_bullet, enemy, enemy_life, game_cleared, score
    game_cleared = False
    score = 0
    all_sprite.empty()
    player_bullet.empty()
    enemy_bullet.empty()
    
    player = Player()
    all_sprite.add(player)

    enemy_life = 500
    enemy = Enemy()
    all_sprite.add(enemy)

    play_music(game_bgm)

def game_clear_screen():
    global game_cleared
    game_cleared = True
    pygame.mixer.music.stop()

    screen.fill((0, 0, 0))
    font_big = pygame.font.Font('ScienceGothic.ttf', 50)
    font_small = pygame.font.Font('ScienceGothic.ttf', 30)

    #display GAME CLEAR!
    text = font_big.render("GAME CLEAR!", True, (0, 255, 0))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
    screen.blit(text, text_rect)

    #display option
    retry_text = font_small.render("Press R to Try Again", True, (255, 255, 255))
    quit_text = font_small.render("Press Q to Quit", True, (255, 255, 255))
    screen.blit(retry_text, (WIDTH/2 - retry_text.get_width()/2, HEIGHT/2 + 20))
    screen.blit(quit_text, (WIDTH/2 - quit_text.get_width()/2, HEIGHT/2 + 60))

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


font = pygame.font.Font('ScienceGothic.ttf', 20)
score = 0

#display menu
start_menu()

#game loop
running = True
game_cleared = False

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
    if random.random() < 0.1:
        b = EnemyBullet()
        all_sprite.add(b)
        enemy_bullet.add(b)   
    
    #update
    all_sprite.update()

    #display
    screen.fill((0, 0, 0))
    all_sprite.draw(screen)
    health_text = font.render(f'Life: {player.health}', True, (255, 255, 255))
    score_text = font.render(f'Score:{score}', True, (255, 255, 255))
    screen.blit(health_text, (WIDTH - 120, 10))
    screen.blit(score_text, (WIDTH - 120, 30))

    pygame.display.update()

pygame.QUIT