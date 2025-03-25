import os
import random
import sys
import pygame


pygame.init()
WIDTH= 1280
HEIGHT = 800
FPS = 60
sc = pygame.display.set_mode((WIDTH,HEIGHT))
clock =pygame.time.Clock()
from load import *



class Bush(pygame.sprite.Sprite):
    def __init__(self,image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect= self.image.get_rect()
        self.rect.x = pos [ 0]
        self.rect.y = pos [ 1]

class Tower_bush(pygame.sprite.Sprite):
    def __init__(self,image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect= self.image.get_rect()
        self.rect.x = pos [ 0]
        self.rect.y = pos [ 1]


class Grass(pygame.sprite.Sprite):
    def __init__(self,image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect= self.image.get_rect()
        self.rect.x = pos [ 0]
        self.rect.y = pos [ 1]

class Right(pygame.sprite.Sprite):
    def __init__(self,image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect= self.image.get_rect()
        self.rect.x = pos [ 0]
        self.rect.y = pos [ 1]

class Left(pygame.sprite.Sprite):
    def __init__(self,image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect= self.image.get_rect()
        self.rect.x = pos [ 0]
        self.rect.y = pos [ 1]
class Bottom(pygame.sprite.Sprite):
    def __init__(self,image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect= self.image.get_rect()
        self.rect.x = pos [ 0]
        self.rect.y = pos [ 1]

class Up(pygame.sprite.Sprite):
    def __init__(self,image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect= self.image.get_rect()
        self.rect.x = pos [ 0]
        self.rect.y = pos [ 1]

class Enemy(pygame.sprite.Sprite):
    def __init__(self,image,pos,dir):
        self.image = image
        self.rect = self.image.get_rect
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = 'right'
        self.speedx= 2
        self.speedy = 0

    def update(self):
        if self.dir == 'right':
            self.speedx = 2
            self.speedy = 0
            self.image = pygame.transform.rotate(enemy_image,90)
        elif self.dir =='top':
             self.speedx = 0
             self.speedy =2
             self.image = pygame.tranform.rotate(enemy_image, 360)
        elif self.dir =='left':
            self.speedx = -2
            self.speedy = 0
            self.image = pygame.transform.rotate(enemy_image, 270)
        elif self.dir =='bottom':
            self.speedx = 0
            self.speedy = -2
            self.image = pygame.transform.rotate(enemy_image, 180)



class Spawner(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.timer_spawn = 1


    def update(self):
        self.spawn()

    def spawn(self):
        if 0< self.rect.centerx <1200 and 0 < self.rect.centery< 800:
            self.timer_spawn += 1
            if self.timer_spawn / FPS > 1:
                enemy = Enemy(enemy_image, self.rect.center)
                enemy_group.add(enemy)
                self.timer_spawn = 0









def game_lvl():
    global pygame
    sc.fill('grey')
    grass_group.update
    grass_group.draw(sc)
    tower_bush_group.update
    tower_bush_group.draw(sc)
    bush_group.update
    bush_group.draw(sc)
    up_group.update
    up_group.draw(sc)
    bottom_group.update
    bottom_group.draw(sc)
    right_group.update
    spawner_group.update
    right_group.draw(sc)
    left_group.update
    left_group.draw(sc)
    enemy_group.update
    enemy_group.draw(sc)
    sc.blit(panel_image,( 0 ,720))


    pygame.display.update()






def restart():
    global grass_group,tower_bush_group,bush_group,enemy_group,spawner_group,up_group,bottom_group,left_group,right_group
    grass_group = pygame.sprite.Group()
    tower_bush_group = pygame.sprite.Group()
    bush_group =pygame.sprite.Group()
    enemy_group= pygame.sprite.Group()
    up_group = pygame.sprite.Group()
    bottom_group = pygame.sprite.Group()
    left_group = pygame.sprite.Group()
    right_group= pygame.sprite.Group()
    spawner_group = pygame.sprite.Group()




def drawmaps(namefile):
    global player
    maps=[]
    source = ''+ str(namefile)
    with open(source, 'r')as file:
        for i in range(0, 10):
            maps.append(file.readline().replace('\n', '').split(',')[0:-1])


        pos = [0, 0]
        for i in range(0, len(maps)):
            pos[1] = i * 80
            for j in range(0, len(maps[0])):
                pos[0] = 80 * j


                if maps [i][j] =='2':
                    bush=Bush(bush_image,pos)
                    bush_group.add(bush)
                elif maps [i][j] =='3':
                    tower_bush=Tower_bush(tower_bush_image,pos)
                    tower_bush_group.add(tower_bush)
                elif maps [i][j] =='4':
                    grass=Grass(grass_image,pos)
                    grass_group.add(grass)
                elif maps [i][j] =='7':
                    right=Right(right_image,pos)
                    right_group.add(right)
                elif maps [i][j] =='8':
                    up=Up(top_image,pos)
                    up_group.add(up)
                elif maps [i][j] =='1':
                    bottom=Bottom(bottom_image,pos)
                    bottom_group.add(bottom)
                elif maps [i][j] =='5':
                    left=Left(left_image,pos)
                    left_group.add(left)


restart()
drawmaps('game lvl')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game_lvl()
        clock.tick(FPS)



