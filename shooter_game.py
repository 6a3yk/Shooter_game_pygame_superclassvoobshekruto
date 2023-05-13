from pygame import *
from random import randint
import time as t
init()
mixer.init()
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed,w,h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 5:
            self.kill()

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if (key_pressed[K_LEFT] or key_pressed[K_a]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (key_pressed[K_RIGHT] or key_pressed[K_d]) and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        bullet1 = Bullet('bullet.png', self.rect.centerx,self.rect.top,10,10,30)
        bullets.add(bullet1)
        global last_fire
        last_fire = t.time()
        
        
        
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            global lost
            lost += 1
            self.rect.x = randint(50,650)
            self.rect.y = 0



win_width = 700
win_height = 500
FPS = 30
game = True
finish = False

score = 0
lost = 0

window = display.set_mode((win_width, win_height))
clock = time.Clock()
font0 = font.SysFont('Arial',100)
font1 = font.SysFont('Arial',30)
win_image = font0.render( 'YOU WIN!', True, (0,255,255) )
lose_image = font0.render( 'YOU LOSE!', True, (255,0,0) )

display.set_caption("Shooter")

background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

mixer.music.load('space.ogg')
kick = mixer.Sound('fire.ogg')
mixer.music.play()

player = Player('rocket.png', 20,400,5,65,65)


bullets = sprite.Group()
monsters = sprite.Group()

last_fire = 0
for i in range(5):
    monsters.add(Enemy('ufo.png',randint(50,650),randint(-250,-30),randint(2,8),45,45))


while game:
    clock.tick(FPS)                         #задержка

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN and e.key == K_SPACE:
            if t.time() - last_fire > 0.3 and not(finish):
                player.fire()
    if not(finish): 
        
        player.update()
        monsters.update()
        bullets.update()

        image_score = font1.render('Счёт: '+str(score), True, (255,255,255) )
        image_lost = font1.render('Пропущено: '+str(lost), True, (255,255,255) )
        
        monsters_list = sprite.groupcollide(monsters,bullets,True,True)
        for monst in monsters_list:
            score +=1
            monsters.add(Enemy('ufo.png',randint(50,650),-30,randint(2,8),45,45))
                           
                                                #события и игровая логика




        window.blit(background,(0, 0))          #зачистка экрана
        window.blit(image_score,(3,10))
        window.blit(image_lost,(3,30))
        

        player.reset()
        monsters.draw(window)  
        bullets.draw(window)

        if score >= 10:
            window.blit(win_image, (200,300))
            finish = True

        monsters_list = sprite.spritecollide(player, monsters,False)
        if len(monsters_list) > 0:
            window.blit(lose_image, (200,300))
            finish = True


        display.update()                        #обновление экрана



