import os
import random
import sys
from re import purge

import pygame

pygame.init()
WIDTH = 1280
HEIGHT = 800
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
from load import *
font = pygame.font.SysFont('Aria', 40 )
lvl ='menu'
lvl_game = 1
money = 500000
score = 0


def startMenu():
    sc.fill('grey')
    button_group.draw(sc)
    button_group.update()
    pygame.display.update()

def changelvl():
    sc.fill('grey')
    button2_group.draw(sc)
    button2_group.update()
    pygame.display.update()


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos, next_lvl, text):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.text = text

        self.next_lvl = next_lvl

    def update(self):
        global lvl

        text_render = font.render(self.text, True, 'white')
        sc.blit(text_render, (self.rect.x + 80, self.rect.y + 5))

        click = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.rect.left < click[0] < self.rect.right and self.rect.top < click[1] < self.rect.bottom:
                lvl = self.next_lvl
            if lvl == 'choise':
                button_back = Button(button_image, (540, 270), 'back', 'back')
                button2_group.add(button_back)

                button_lvl1 = Button(button_image, (540, 100), 'lvl_1', 'lvl 1')
                button2_group.add(button_lvl1)
            if lvl == 'game_lvl':
                restart()
            if lvl == 'end':
                exit()


class Bush(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Tower_bush(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    def update(self):
        global money
        if tower_shop_1.buy == True and pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if self.rect.left < pos[0] < self.rect.right \
                    and self.rect.top < pos[1] < self.rect.bottom:
                tower_shots = Tower_shots(tower_1_on, (self.rect.centerx, self.rect.centery - 30))
                tower_shots_group.add(tower_shots)
                tower_shop_1.buy = False
                money -= 100





class Grass(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Right(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = 'right'


class Left(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = 'left'


class Bottom(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = 'bottom'


class Up(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = 'top'


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.dir = 'right'
        self.speedx = 2
        self.speedy = 0
        self.hp = 100


    def update(self):
        global money, score
        self.draw_stats_enemy()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.dir == 'right':
            self.speedx = 2
            self.speedy = 0
            self.image = pygame.transform.rotate(enemy_image, 0)
        elif self.dir == 'top':
            self.speedx = 0
            self.speedy = -2
            self.image = pygame.transform.rotate(enemy_image, 90)
        elif self.dir == 'left':
            self.speedx = -2
            self.speedy = 0
            self.image = pygame.transform.rotate(enemy_image, 180)
        elif self.dir == 'bottom':
            self.speedx = 0
            self.speedy = 2
            self.image = pygame.transform.rotate(enemy_image, 270)

        if pygame.sprite.spritecollide(self, edit_dir_group, False):
            tile = pygame.sprite.spritecollide(self, edit_dir_group, False)[0]
            if abs(self.rect.centerx - tile.rect.centerx) <= 5 and abs(self.rect.centery - tile.rect.centery) <=5:
                self.dir = tile.dir
        if pygame.sprite.spritecollide(self, bullet_group, False):
            bullet = pygame.sprite.spritecollide(self, bullet_group, False)[0]
            self.hp -= bullet.damage
            bullet.kill()
        if self.hp <=0:
            money += 20
            score += 10
            self.kill()




    def draw_stats_enemy(self):
        if self.hp <= 99:
            width_hp = 96 * (self.hp / 100)
            pygame.draw.rect(sc, 'black', (self.rect.x - 30, self.rect.y - 52, 100, 20), 2)
            pygame.draw.rect(sc, 'green', (self.rect.x - 27, self.rect.y - 50, width_hp, 15))



class Edit_dir_tile(pygame.sprite.Sprite):
    def __init__(self, image, pos, dir):
        pygame.sprite.Sprite.__init__(self)
        self.dir = 'right'
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.image = image
        self.dir = dir


class Spawner():
    def __init__(self):
        self.timer_spawn = 1

    def update(self):
        self.spawn()


    def spawn(self):
        self.timer_spawn += 1
        if self.timer_spawn / FPS > 1:
            enemy = Enemy(enemy_image, (0,680))
            enemy_group.add(enemy)
            self.timer_spawn = 0




class Tower_afk(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.buy = False
        self.timer_click = 0

    def update(self):
        pos = pygame.mouse.get_pos()
        if money <= 100:
            self.image = tower_1_of
        elif pygame.mouse.get_pressed()[0] and money >= 100:

            if self.rect.left < pos[0] < self.rect.right\
                    and self.rect.top < pos[1] < self.rect.bottom:

                self.buy = True
        if self.buy:
            sc.blit(tower_1_on, pos)







class Tower_shots(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.lvl = 1
        self.damage = 30
        self.enemy = None
        self.timer_shot = 0
        self.upgrade = False
        self.current_bullet_image = tower_1_bullet

    def update(self):
        self.upgrades()
        self.shot()
        print(self.enemy)

        if self.enemy is None:
            for enemy in enemy_group:
                if ((self.rect.centerx - enemy.rect.centerx) ** 2 + (
                        self.rect.centerx - enemy.rect.centery) ** 2) ** 0.5 <500:
                    self.enemy = enemy
                    break
        if self.enemy not in enemy_group:
            self.enemy = None

        if len(enemy_group) == 0:
            lvl_game += 1
            restart()
            drawMaps(str(lvl_game) + '.txt')

    def upgrades(self):
        global money
        if self.lvl == 1 and money >= 200:

            self.upgrade = True

        if self.upgrade == True:
            sc.blit(upgrade_image, (self.rect.right, self.rect.bottom))

        if self.upgrade == True and pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if self.rect.right< pos[0] < self.rect.right+50\
                     and self.rect.bottom < pos[1] < self.rect.bottom+45:
                self.lvl = 2
                self.damage = 50
                self.image = tower_1_1_image[0]
                Bullet.speed = 15
                self.upgrade = False



    def shot(self):
        self.timer_shot += 1
        if self.enemy != None and self.timer_shot/ FPS > 1:
            x_1 = self.rect.centerx
            y_1 = self.rect.top
            x_2 = self.enemy.rect.centerx
            y_2 = self.enemy.rect.centery
            bullet = Bullet(self.current_bullet_image, (x_1, y_1, x_2, y_2), self.damage, 5*self.lvl)
            bullet_group.add(bullet)
            self.timer_shot = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self,image,pos,damage, speed = 5):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect =self.image.get_rect()
        self.speed = speed
        self.damage = damage
        self.start_pos = pygame.math.Vector2(pos[0],pos[1])
        self.end_pos = pygame.math.Vector2(pos[2], pos[3])
        self.velocity = (self.end_pos - self.start_pos).normalize() *self.speed
        self.rect.center = self.start_pos

    def update(self):

        self.rect.center += self.velocity




def game_lvl():
    global pygame
    sc.fill('grey')
    grass_group.update()
    grass_group.draw(sc)
    tower_bush_group.update()
    tower_bush_group.draw(sc)
    bush_group.update()
    bush_group.draw(sc)
    up_group.update()
    up_group.draw(sc)
    bottom_group.update()
    bottom_group.draw(sc)
    right_group.update()
    right_group.draw(sc)
    left_group.update()
    left_group.draw(sc)



    edit_dir_group.update()
    edit_dir_group.draw(sc)
    sc.blit(panel_image, (0, 720))
    # sc.blit(upgrade_image, (0, 500))
    money_counter = font.render(f'Деньги: {money}', True, 'black')
    score_counter = font.render(f'Score: {score}', True, 'black')
    sc.blit(money_counter, (40, 40))
    sc.blit(score_counter, (40,75))
    tower_afk_group.update()
    tower_afk_group.draw(sc)
    tower_shots_group.update()
    tower_shots_group.draw(sc)
    spawner.update()
    enemy_group.update()
    enemy_group.draw(sc)
    bullet_group.update()
    bullet_group.draw(sc)
    pygame.display.update()


def restart():
    global spawner,tower_shots_group,grass_group,tower_afk_group, tower_bush_group, bush_group, enemy_group, spawner_group, up_group, edit_dir_group, bottom_group, left_group, right_group
    global tower_shop_1, bullet_group,button_group,button2_group



    grass_group = pygame.sprite.Group()
    tower_bush_group = pygame.sprite.Group()
    button_group = pygame.sprite.Group()
    button2_group = pygame.sprite.Group()
    bush_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    edit_dir_group = pygame.sprite.Group()
    up_group = pygame.sprite.Group()
    bottom_group = pygame.sprite.Group()
    left_group = pygame.sprite.Group()
    right_group = pygame.sprite.Group()
    right_group.add(edit_dir_group)
    left_group.add(edit_dir_group)
    bottom_group.add(edit_dir_group)
    up_group.add(edit_dir_group)
    tower_afk_group = pygame.sprite.Group()
    spawner = Spawner()
    bullet_group = pygame.sprite.Group()
    tower_shots_group = pygame.sprite.Group()
    tower_shop_1 = Tower_afk(tower_1_on, (45,765))
    tower_afk_group.add(tower_shop_1)

    button_start = Button(button_image, (540, 100), 'choise', 'start')
    button_group.add(button_start)

    button_score = Button(button_image, (540,180),'score', 'score')
    button_group.add(button_score)

    button_exit = Button(button_image, (540, 270), 'end', 'exit')
    button_group.add(button_exit)

def drawmaps(namefile):
    global player
    maps = []
    source = '' + str(namefile)
    with open(source, 'r') as file:
        for i in range(0, 10):
            maps.append(file.readline().replace('\n', '').split(',')[0:-1])

        pos = [0, 0]
        for i in range(0, len(maps)):
            pos[1] = i * 80
            for j in range(0, len(maps[0])):
                pos[0] = 80 * j

                if maps[i][j] == '2':
                    bush = Bush(bush_image, pos)
                    bush_group.add(bush)
                elif maps[i][j] == '3':
                    tower_bush = Tower_bush(tower_bush_image, pos)
                    tower_bush_group.add(tower_bush)
                elif maps[i][j] == '4':
                    grass = Grass(grass_image, pos)
                    grass_group.add(grass)
                elif maps[i][j] == '7':
                    right = Right(right_image, pos)
                    edit_dir_group.add(right)
                elif maps[i][j] == '8':
                    up = Up(top_image, pos)
                    edit_dir_group.add(up)
                elif maps[i][j] == '1':
                    bottom = Bottom(bottom_image, pos)
                    edit_dir_group.add(bottom)
                elif maps[i][j] == '5':
                    left = Left(left_image, pos)
                    edit_dir_group.add(left)





restart()



drawmaps('game lvl')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if lvl == 'game':
        game_lvl()
    elif lvl == 'menu':
        startMenu()
    elif lvl == 'exit':
        pygame.quit()
        game_lvl()
    elif lvl == 'choise':
        changelvl()
    elif lvl =='back':
        startMenu()
    elif lvl =='lvl_1':
        game_lvl()
    clock.tick(FPS)
