import os
import random
import sys
import pygame

pygame.init()
WIDTH = 1280
HEIGHT = 800
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
from load import *
font = pygame.font.SysFont('Aria', 40 )
money = 500


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


    def update(self):
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
            print(1)
            tile = pygame.sprite.spritecollide(self, edit_dir_group, False)[0]
            if abs(self.rect.centerx - tile.rect.centerx) <= 5 and abs(self.rect.centery - tile.rect.centery) <=5:
                self.dir = tile.dir


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
                    and self.rect.top < pos[0] < self.rect.bottom:
                self.buy = True
        if self.buy:
            sc.blit(tower_1_on, pos)







class tower(pygame.sprite.Sprite):
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


    def update(self):






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
    money_counter = font.render(f'Деньги: {money}', True, 'black')
    sc.blit(money_counter, (40, 40))
    tower_afk_group.update()
    tower_afk_group.draw(sc)
    spawner.update()
    enemy_group.update()
    enemy_group.draw(sc)
    pygame.display.update()


def restart():
    global spawner,grass_group,tower_afk_group, tower_bush_group, bush_group, enemy_group, spawner_group, up_group, edit_dir_group, bottom_group, left_group, right_group
    grass_group = pygame.sprite.Group()
    tower_bush_group = pygame.sprite.Group()
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
    tower_shop_1 = Tower_afk(tower_1_on, (45,765))
    tower_afk_group.add(tower_shop_1)

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
    game_lvl()
    clock.tick(FPS)
