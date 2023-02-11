#Создай собственный Шутер!
from pygame import *
from random import randint
win_width = 1400
win_height = 800
max_lost = 15
lost = 0
score = 0
live = 9
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 100)
mixer.init()
lol = mixer.Sound('fire.ogg')
window = display.set_mode((win_width, win_height))
display.set_caption('draganoid')
image_jpg = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width -80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('rocket.png', self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)
        lol.play()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost        
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width -80)
            self.rect.y = 0
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width -80)
            self.rect.y = 0



class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()


player = Player('bullet.png', win_width/2, win_height - 80, 15)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 5):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, randint(2,9))
    monsters.add(monster)

for i in range(1, 2):
    asteroid = Asteroid('asteroid.png', randint(80, win_width - 80), -40, randint(1,5))
    asteroids.add(asteroid)


game = True
finish = False
clock = time.Clock()
FPS = 90
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()


    if not finish:
        window.blit(image_jpg, (0,0))        
        text_check = font1.render('убито: ' + str(score), 1, (255, 255, 255))
        window.blit(text_check, (10, 40))
        text_lose = font1.render('пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 75))
        text_live = font2.render(str(live), 1, (255, 0, 0))
        window.blit(text_live, (1340, 40))
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()


        for c in sprite.groupcollide(monsters, bullets, True, True):
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, randint(1,9))
            monsters.add(monster)

        if  lost >= max_lost or live <= 0:
            loses = font2.render('пройгрыш', 1, (255, 255, 255))
            window.blit(loses, (550, 400))
            finish = True

        if score >= 35:
            loses = font2.render('выйгрыш', 1, (255, 255, 255))
            window.blit(loses, (550, 400))
            finish = True

        if sprite.spritecollide(player, monsters, False):
            sprite.spritecollide(player, monsters, True)
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, randint(1,9))
            monsters.add(monster)
            live -= 1

        if  sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, asteroids, True)
            asteroid = Asteroid('asteroid.png', randint(80, win_width - 80), -40, randint(1,5))
            asteroids.add(asteroid)
            live -= 1 



    display.update()
    clock.tick(FPS)



#pyinstaller shooter_game.py



