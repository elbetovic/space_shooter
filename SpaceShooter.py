import pygame
import random
import math
import sys
from os import path

assets_dir = path.join(path.dirname(__file__), 'Assets')
sound_dir = path.join(path.dirname(__file__), 'Sound')

#GLOBALNE VARIJABLE

#POSTAVKE PROZORA I BROJ SLIČICA U SEKUNDI
WIDTH = 1024
HEIGHT = 768
FPS = 60

#DEFINIRANJE BOJA
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#INICIJALIZACIJA PYGAME-A I STVARANJE PROZORA
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')


#FUNKCIJE

def show_game_over_screen():
    draw_text(screen, "Space Shooter", 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, "WSAD to move, Mouse Click to fire", 22, WIDTH /2, HEIGHT/2)
    draw_text(screen, "Press any key to begin", 18, WIDTH / 2, HEIGHT *3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGHT = 200
    BAR_HEIGHT = 30
    fill = (pct / 100)  * BAR_LENGHT
    outline_rect = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x+60*i
        img_rect.y = y
        surf.blit(img, img_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

#SPRITES KLASE
#### KLASA PLAYER ####
class Player(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = player_anim[0]
        self.rect = self.image.get_rect()

        self.radius = 50 *1.3
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        self.speedy = 0
        self.frame = 0
        
        self.last_shot = pygame.time.get_ticks()
        self.hide_timer = pygame.time.get_ticks()
        self.last_update = pygame.time.get_ticks()

        self.frame_rate = 100
        self.shield = 100
        self.shoot_delay = 500
        self.shootcount = 1
        self.lives = 3
        self.hidden = False
        
    def update(self):

        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            if self.frame == len(player_anim):
                self.frame = 0
            else:
                center = self.rect.center
                self.image = player_anim[self.frame]
                self.frame += 1
                self.rect = self.image.get_rect()
                self.rect.center = center
                
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 500:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        
        self.speedx = 0
        self.speedy = 0

        mousestate = pygame.mouse.get_pressed()
        keystate = pygame.key.get_pressed()
        
        if keystate[pygame.K_a]:
            self.speedx = -5
        if keystate[pygame.K_d]:
            self.speedx = 5
        if keystate[pygame.K_w]:
            self.speedy = -5
        if keystate[pygame.K_s]:
            self.speedy = 5
        if mousestate[0]:
            self.shoot()

        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.right > WIDTH and not self.hidden:
            self.rect.right = WIDTH
        if self.rect.left < 0 and not self.hidden:
            self.rect.left = 0
        if self.rect.top <0 and not self.hidden:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT and not self.hidden:
            self.rect.bottom = HEIGHT
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            mousepos_x, mousepos_y = pygame.mouse.get_pos()
            if self.shootcount == 1:
                bullet = Bullet(self.rect.centerx, self.rect.centery, mousepos_x, mousepos_y)
                all_sprites.add(bullet)
                bullets.add(bullet)
                random.choice(shoot_sounds).play()
            if self.shootcount == 2:
                bullet1 = Bullet(self.rect.right, self.rect.centery, mousepos_x, mousepos_y)
                bullet2 = Bullet(self.rect.left, self.rect.centery, mousepos_x, mousepos_y)
                all_sprites.add(bullet1, bullet2)
                bullets.add(bullet1, bullet2)
                random.choice(shoot_sounds).play()

    
    def double_shoot():
        pass
    
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (-200, -200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.size = random.choice(('sm', 'med', 'lg'))
        self.image = mob_anim[self.size][0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.radius = int(self.rect.width * 0.70 /2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-200, -150)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

        self.health = 0

        if self.size == 'sm':
            self.health = 1 
        if self.size == 'med':
            self.health = 2 
        if self.size == 'lg':
            self.health = 3 
        
        self.frame_rate = 100
        self.frame = 0
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            if self.frame == len(mob_anim[self.size]):
                self.frame = 0
            else:
                center = self.rect.center
                self.image = mob_anim[self.size][self.frame]
                self.frame += 1
                self.rect = self.image.get_rect()
                self.rect.center = center

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top > HEIGHT + 10 or self.rect.left < -(self.rect.width) \
        or self.rect.right > WIDTH + self.rect.width:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)

class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['armor', 'firepower', 'life'])
        self.image = powerup_img[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed_y = 5

    def update(self):

        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, targetx, targety):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_anim[0]
        self.rect = self.image.get_rect()

        self.rect.centery = y
        self.rect.centerx = x
        self.speed = 10
        angle = math.atan2(targety - y, targetx - x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.frame_rate = 50
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        
    def update(self):

        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            
            if self.frame == len(bullet_anim):
                self.frame = 0
            else:
                center = self.rect.center
                self.image = bullet_anim[self.frame]
                self.frame += 1
                self.rect = self.image.get_rect()
                self.rect.center = center
                
        self.rect.x = self.rect.x + int(self.dx)
        self.rect.y = self.rect.y + int(self.dy)
        
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 20

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

#KLASA POZADINA
class Background():
      def __init__(self):
            self.bgimage = pygame.image.load(path.join(assets_dir, "back.png")).convert()
            self.rectBGimg = self.bgimage.get_rect()
 
            self.bgY1 = 0
            self.bgX1 = 0
 
            self.bgY2 = self.rectBGimg.height
            self.bgX2 = 0
 
            self.moving_speed = 2
         
      def update(self):
        self.bgY1 += self.moving_speed
        self.bgY2 += self.moving_speed
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height
             
      def render(self):
         screen.blit(self.bgimage, (self.bgX1, self.bgY1))
         screen.blit(self.bgimage, (self.bgX2, self.bgY2))

#UČITAVANJE ASSETA

player_img = pygame.image.load(path.join(assets_dir, "player_1.png")).convert()
player_icon = pygame.transform.scale(player_img, ( 50, 50))
player_icon.set_colorkey(BLACK)

player_anim = []
bullet_anim = []
mob_anim = {}
mob_anim['sm'] = []
mob_anim['med'] = []
mob_anim['lg'] = []
powerup_img = {}
powerup_img['armor'] = pygame.image.load(path.join(assets_dir, 'shield0.png')).convert()
powerup_img['firepower'] = pygame.image.load(path.join(assets_dir, 'lightning0.png')).convert()
powerup_img['life'] = pygame.image.load(path.join(assets_dir, 'heart_0.png')).convert()

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['med'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []


for i in range (4):
    filename = 'player_{}.png'.format(i)
    img = pygame.image.load(path.join(assets_dir, filename)).convert()
    img.set_colorkey(BLACK)
    player_anim.append(pygame.transform.scale(img, (320 / 3, 320 / 3)))
    filename = 'projectile_{}.png'.format(i)
    img = pygame.image.load(path.join(assets_dir, filename)).convert()
    img.set_colorkey(BLACK)
    bullet_anim.append(img)
    
for i in range (4):
    filename = 'enemy_{}.png'.format(i)
    img = pygame.image.load(path.join(assets_dir, filename)).convert()
    img.set_colorkey(BLACK)
    mob_anim['sm'].append(pygame.transform.scale(img, (320 / 4, 320 /4)))
    mob_anim['med'].append(pygame.transform.scale(img, (320 / 3, 320 / 3)))
    mob_anim['lg'].append(pygame.transform.scale(img, (320 / 1.5, 320 /1.5)))

    

for i in range(9):
    filename = 'ex{}.png'.format(i)
    img = pygame.image.load(path.join(assets_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (150, 150))
    explosion_anim['lg'].append(img_lg)
    img_med = pygame.transform.scale(img, (100, 100))
    explosion_anim['med'].append(img_med)
    img_sm = pygame.transform.scale(img, (50, 50))
    explosion_anim['sm'].append(img_sm)
    filename = 'pex{}.png'.format(i)
    img = pygame.image.load(path.join(assets_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

#UČITAVANJE ZVUKOVA
explosion_sound = pygame.mixer.Sound(path.join(sound_dir, '8bit_bomb_explosion.wav'))

shoot_sounds = []
powerup_sound_shield = pygame.mixer.Sound(path.join(sound_dir, 'Shield_SFX.wav'))
powerup_sound_firepower = pygame.mixer.Sound(path.join(sound_dir, 'Firepower_SFX.wav'))
powerup_sound_life = pygame.mixer.Sound(path.join(sound_dir, 'Life_SFX.wav'))

for snd in ['sfx_laser1.wav', 'sfx_laser2.wav']:
    shoot_sounds.append(pygame.mixer.Sound(path.join(sound_dir, snd)))

player_death_sound = pygame.mixer.Sound(path.join(sound_dir, 'machinedeath_hq.wav'))
pygame.mixer.music.load(path.join(sound_dir, 'music.wav'))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)



############################################### GAME LOOP ###################################################
game_over = True
running = True
while running:
    if game_over:
        show_game_over_screen()
        pygame.time.delay(500)
        game_over = False
        back_ground = Background()
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        poweups = pygame.sprite.Group()
        player = Player()

        all_sprites.add(player)
        mobcount = 5
        start_ticks = 0
        score = 0
        
        for i in range(mobcount):
            newmob()

    clock.tick(FPS)
    ############################################### EVENTI ###################################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ############################################### UPDATE ###################################################

    back_ground.update()
    back_ground.render()
    all_sprites.update()

    #PROVJERA JE LI PROJEKTIL POGODIO NEPRIJATELJA

    hits = pygame.sprite.groupcollide(mobs, bullets, False, True)
    for hit in hits:
        score += hit.radius
        explosion_sound.play()
        if hit.size == "lg":
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
        if hit.size == "med":
            expl = Explosion(hit.rect.center, 'med')
            all_sprites.add(expl)
        if hit.size == "sm":
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
        
        hit.health -= 1
        if hit.health <= 0:
            if random.random() > 0.9:
                pow = Powerup(hit.rect.center)
                all_sprites.add(pow)
                poweups.add(pow)

            hit.kill()
            newmob()
            
    #PROVJERA JE LI SE NEPRIJATELJ SUDARIO U IGRAČA

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    
    for hit in hits:
        player.shield -= hit.health * 20
        explosion_sound.play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            player_death_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            for hit in hits:
                for mob in mobs:
                    mob.kill()
                    newmob()
            
            player.lives -= 1
            player.shield = 100
    
    #PROVJERA JE LI IGRAČ POKUPIO NADOGRANJU

    hits = pygame.sprite.spritecollide(player, poweups, True)
    for hit in hits:
        if hit.type == 'armor':
            player.shield += 20
            if player.shield >= 100:
                player.shield = 100
            powerup_sound_shield.play()
        if hit.type == 'firepower':
            player.shoot_delay -= 20
            if player.shoot_delay <= 200:
                player.shoot_delay = 200
                player.shootcount = 2
            powerup_sound_firepower.play()
        if hit.type == 'life':
            player.lives +=1
            if player.lives >= 3:
                player.lives = 3
            powerup_sound_life.play()

    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    #DODAVANJE VIŠE NEPRIJATELJA KAKO VRIJEME PROLAZI

    start_ticks += 1
    print(start_ticks)
    if start_ticks % 2700 == 0:
        newmob()
    
    #CRTANJE SVIH SPRITEOVA NA ZASLON I GRAFIČKOG SUČELJA
    all_sprites.draw(screen)
    draw_text(screen, "SCORE: " + str(score), 42, WIDTH/2, 10)
    draw_shield_bar(screen ,5, 5, player.shield)
    draw_lives(screen, WIDTH - 200, 20, player.lives, player_icon)

    #NAKON CRTANJA, "OKRENUTI" ZASLON
    pygame.display.flip()

pygame.quit()
sys.exit()