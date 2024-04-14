from pygame import *
from random import randint
window = display.set_mode((700,500))

background = transform.scale(image.load('galaxy.jpg'),(700,500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

score = 0
lost = 0

font.init()
font2 = font.Font(None, 36)
font3 = font.Font(None, 74)

class GameSprite(sprite.Sprite):
    def __init__(self, image_player, speed, x, y, width , height):
        super().__init__()
        self.image = transform.scale(image.load(image_player), (width,height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        elif keys_pressed[K_d] and self.rect.x < 600:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet('bullet.png', speed = 6 , x = self.rect.centerx,
        y = self.rect.y , width = 15, height = 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -20
            self.rect.x = randint(0,600)
            lost += 1

# class Boss(GameSprite):
    
#     def update(self):
#         self.rect.y += self.speed
#         if self.rect.y > 500:
#             self.rect.y = -20
#             self.rect.x = (0,600)
            


class Bullet(GameSprite):

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

boss = Enemy('ufo.png', speed = 1 ,x= randint (0,600), y = 0, width = 200 , height = 130)
boss.hearts = 25

rocket = Player(image_player = 'rocket.png', speed= 10, x=0, y=390, width = 70, height = 100)  
ufos = sprite.Group()

bullets = sprite.Group()
for i in range(5):
    ufo = Enemy(image_player = 'ufo.png', speed= randint(1,4), x= randint (0,600), y=0, width = 80, height = 50)  
    ufos.add(ufo)

clock = time.Clock()
FPS = 60
game = True
finish = False
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        if i.type == KEYDOWN:
            if i.key == K_SPACE:
                rocket.shoot()    
    if not finish:
        score_text = font2.render('Счёт:'+ str(score),True , (255,255,255))
        miss_text = font2.render('Пропущено:'+ str(lost), True,(255,255,255))
        lose_text = font3.render('YOU LOSE!!!',True , (255,0,0))
        win_text = font3.render('YOU WIN!!!'+ str(score),True , (0,255,255))
        window.blit(background, (0,0))
        window.blit(score_text, (50,30))
        window.blit(miss_text, (50,60))
        rocket.update()
        rocket.reset()
        ufos.update()
        ufos.draw(window)
        bullets.draw(window)
        bullets.update()
        if sprite.spritecollide(rocket, ufos, False):
            finish = True
            window.blit(lose_text, (250,250))
            lose_text = font3.render('YOU LOSE!!!',True , (255,0,0))


        if sprite.groupcollide(ufos, bullets, True , True):
            score += 1
            ufo = Enemy(image_player = 'ufo.png', speed= randint(1,4), x= randint (0,600), y=0, width = 80, height = 50)  
            ufos.add(ufo)
        if score > 10:
            for ufo in ufos:
                ufo.kill()
            boss.reset()
            boss.update()
            if sprite.spritecollide(boss, bullets, True):
                boss.hearts -= 1
                print(boss.hearts)

        
            if boss.hearts <= 0:
                finish = True

                win_text = font3.render('YOU WIN!!!',True , (0,255,0))

    clock.tick(FPS)
    display.update()
