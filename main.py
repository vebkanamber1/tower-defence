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

font = pygame.font.SysFont('Aria', 40)
lvl = 'menu'
lvl_game = 1
money = 500
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


# def score():
#     sc.fill('grey')
#     button_group.draw(sc)
#     button_group.update()
#     pygame.display.update()


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos, next_lvl, text):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.text = text

        self.next_lvl = next_lvl
        self.timer_click = 0

    def update(self):
        global lvl, money
        self.timer_click += 1
        text_render = font.render(self.text, True, 'white')
        sc.blit(text_render, (self.rect.x + 80, self.rect.y + 5))

        click = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.timer_click / FPS > 0.3:
            if self.rect.left < click[0] < self.rect.right and self.rect.top < click[1] < self.rect.bottom:
                lvl = self.next_lvl
            if lvl == 'choise':
                button_back = Button(button_image, (540, 350), 'menu', 'back')
                button2_group.add(button_back)

                button_lvl1 = Button(button_image, (540, 100), 'lvl 1', 'lvl 1')
                button2_group.add(button_lvl1)

                button_lvl2 = Button(button_image, (540, 180), 'lvl 2', 'lvl 2')
                button2_group.add(button_lvl2)

                button_lvl3 = Button(button_image, (540, 270), 'lvl 3', 'lvl 3')
                button2_group.add(button_lvl3)

            if lvl == 'lvl 1':
                money = 500
                restart()
                drawmaps('game_lvl1')

            if lvl == 'lvl 2':
                money = 400
                restart()

                drawmaps('game_lvl2')

            if lvl == 'lvl 3':
                money = 500
                restart()

                drawmaps('game_lvl3')
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
        if tower_shop_2.buy == True and pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if self.rect.left < pos[0] < self.rect.right \
                    and self.rect.top < pos[1] < self.rect.bottom:
                tower_shots2 = Tower_shots2(tower_2_on, (self.rect.centerx, self.rect.centery - 30))
                tower_shots2_group.add(tower_shots2)
                tower_shop_2.buy = False
                money -= 200
        if tower_shop_3.buy == True and pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if self.rect.left < pos[0] < self.rect.right \
                    and self.rect.top < pos[1] < self.rect.bottom:
                tower_shots3 = Tower_shots3(tower_3_on, (self.rect.centerx, self.rect.centery - 30))
                tower_shots3_group.add(tower_shots3)
                tower_shop_3.buy = False
                money -= 200

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
        self.default_image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.dir = 'right'
        self.speedx = 2
        self.speedy = 0
        self.max_hp = 100
        self.hp = self.max_hp

        if lvl =='lvl 2':
            self.max_hp = 120
            self.hp = self.max_hp

        if lvl =='lvl 3':
            self.max_hp = 180
            self.hp = self.max_hp


    def update(self):
        global money, score,lvl
        self.draw_stats_enemy()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.dir == 'right':
            self.speedx = 2
            self.speedy = 0
            self.image = pygame.transform.rotate(self.default_image, 0)
        elif self.dir == 'top':
            self.speedx = 0
            self.speedy = -2
            self.image = pygame.transform.rotate(self.default_image, 90)
        elif self.dir == 'left':
            self.speedx = -2
            self.speedy = 0
            self.image = pygame.transform.rotate(self.default_image, 180)
        elif self.dir == 'bottom':
            self.speedx = 0
            self.speedy = 2
            self.image = pygame.transform.rotate(self.default_image, 270)

        if pygame.sprite.spritecollide(self, edit_dir_group, False):
            tile = pygame.sprite.spritecollide(self, edit_dir_group, False)[0]
            if abs(self.rect.centerx - tile.rect.centerx) <= 5 and abs(self.rect.centery - tile.rect.centery) <= 5:
                self.dir = tile.dir
        if pygame.sprite.spritecollide(self, bullet_group, False):
            bullet = pygame.sprite.spritecollide(self, bullet_group, False)[0]
            self.hp -= bullet.damage

        if pygame.sprite.spritecollide(self, bullet2_group, False):
            bullet2 = pygame.sprite.spritecollide(self, bullet2_group, False)[0]
            self.hp -= bullet2.damage
            bullet2.death = True

        if pygame.sprite.spritecollide(self, bullet3_group, False):
            bullet3 = pygame.sprite.spritecollide(self, bullet3_group, False)[0]
            self.hp -= bullet3.damage

        if self.hp <= 0:
            money += 20
            score += 10
            self.kill()
        if lvl =='lvl 2':
            self.max_hp = 120



        if lvl =='lvl 3':
            self.max_hp= 180






    def draw_stats_enemy(self):
        if self.hp < self.max_hp:
            width_hp = 96 * (self.hp / self.max_hp)
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
        global lvl
        if lvl =='lvl 1':
            self.timer_spawn += 1
            if self.timer_spawn / FPS > 1:
                enemy = Enemy(enemy_image, (0, 680))
                enemy_group.add(enemy)
                self.timer_spawn = 0
        elif lvl == 'lvl 2':
            self.timer_spawn += 1
            if self.timer_spawn / FPS > 1:
                enemy = Enemy(enemy2_image, (0, 360))
                enemy_group.add(enemy)
                self.timer_spawn = 0
        elif lvl =='lvl 3':
            self.timer_spawn += 1
            if self.timer_spawn / FPS > 1.8:
                enemy = Enemy(enemy3_image, (0, 360))
                enemy_group.add(enemy)
                self.timer_spawn = 0
                enemy = Enemy(enemy3_image, (200, 0))
                enemy_group.add(enemy)
                enemy.dir = 'bottom'
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
        if money < 100:
            self.image = tower_1_of
        elif pygame.mouse.get_pressed()[0] and money >= 100:

            if self.rect.left < pos[0] < self.rect.right \
                    and self.rect.top < pos[1] < self.rect.bottom:
                self.buy = True
        if self.buy:
            sc.blit(tower_1_on, pos)

class Tower_afk2(pygame.sprite.Sprite):
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
        if money < 200:
            self.image = tower_2_of
        elif pygame.mouse.get_pressed()[0] and money >= 200:

            if self.rect.left < pos[0] < self.rect.right \
                    and self.rect.top < pos[1] < self.rect.bottom:
                self.buy = True
        if self.buy:
            sc.blit(tower_2_on, pos)

class Tower_afk3(pygame.sprite.Sprite):
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
        if money < 200:
            self.image = tower_3_of
        elif pygame.mouse.get_pressed()[0] and money >= 200:

            if self.rect.left < pos[0] < self.rect.right \
                    and self.rect.top < pos[1] < self.rect.bottom:
                self.buy = True
        if self.buy:
            sc.blit(tower_3_on, pos)



class Tower_shots(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.current_image_list = tower_1_image
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.lvl = 1
        self.damage = 30
        self.enemy = None
        self.timer_shot = 0
        self.upgrade = False
        self.current_bullet_image = tower_1_bullet
        self.frame = 0
        self.timer_anime = 0
        self.anime = True

    def update(self):
        self.upgrades()
        self.shot()
        self.animation()


        if self.enemy is None:
            for enemy in enemy_group:
                if ((self.rect.centerx - enemy.rect.centerx) ** 2 + (
                        self.rect.centerx - enemy.rect.centery) ** 2) ** 0.5 < 500:
                    self.enemy = enemy
                    break
        if self.enemy not in enemy_group:
            self.enemy = None

    def upgrades(self):
        global money
        if self.lvl == 1 and money >= 200:
            self.upgrade = True

        if self.upgrade == True:
            sc.blit(upgrade_image, (self.rect.right, self.rect.bottom))

        if self.upgrade == True and pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if self.rect.right < pos[0] < self.rect.right + 50 \
                    and self.rect.bottom < pos[1] < self.rect.bottom + 45:
                money -=200
                self.lvl = 2
                self.damage = 50
                self.image = tower_1_1_image[0]
                Bullet.speed = 15
                self.upgrade = False
                self.current_image_list = tower_1_1_image


    def shot(self):
        self.timer_shot += 1
        if self.enemy != None and self.timer_shot / FPS > 2.5:
            x_1 = self.rect.centerx
            y_1 = self.rect.top
            x_2 = self.enemy.rect.centerx
            y_2 = self.enemy.rect.centery
            bullet = Bullet(self.current_bullet_image, (x_1, y_1, x_2, y_2), self.damage, 5 * self.lvl)
            bullet_group.add(bullet)
            self.timer_shot = 0

    def animation(self):
        if self.anime:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(self.current_image_list) - 1:
                    self.frame = 0
                else:
                    self.frame += 1
                self.timer_anime = 0
        self.image = self.current_image_list[self.frame]

class Tower_shots2(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.current_image_list = tower_2_image
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.lvl = 1
        self.damage = 50
        self.enemy = None
        self.timer_shot = 0
        self.upgrade = False
        self.current_bullet_image = tower_2_bullet
        self.frame = 0
        self.timer_anime = 0
        self.anime = True

    def update(self):
        self.upgrades()
        self.shot()
        self.animation()






        if self.enemy is None:
            for enemy in enemy_group:
                if ((self.rect.centerx - enemy.rect.centerx) ** 2 + (
                        self.rect.centerx - enemy.rect.centery) ** 2) ** 0.5 < 500:
                    self.enemy = enemy
                    break
        if self.enemy not in enemy_group:
            self.enemy = None

    def upgrades(self):
        global money
        if self.lvl == 1 and money >= 250:
            self.upgrade = True

        if self.upgrade == True:
            sc.blit(upgrade_image, (self.rect.right, self.rect.bottom))

        if self.upgrade == True and pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if self.rect.right < pos[0] < self.rect.right + 50 \
                    and self.rect.bottom < pos[1] < self.rect.bottom + 45:
                money -=250
                self.lvl = 2
                self.damage = 75
                self.image = tower_2_1_image[2]

                self.upgrade = False
                self.current_image_list = tower_2_1_image

    def shot(self):
        self.timer_shot += 1
        if self.enemy != None and self.timer_shot / FPS > 4:
            x_1 = self.rect.centerx
            y_1 = self.rect.top
            x_2 = self.enemy.rect.centerx
            y_2 = self.enemy.rect.centery
            bullet2 = Bullet2(self.current_bullet_image, (x_1, y_1, x_2, y_2), self.damage, 5 * self.lvl)
            bullet2_group.add(bullet2)
            self.timer_shot = 0





    def animation(self):
        if self.anime:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.11:
                if self.frame == len(self.current_image_list) - 1:
                    self.frame = 0
                else:
                    self.frame += 1
                self.timer_anime = 0
        self.image = self.current_image_list[self.frame]



class Tower_shots3(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.current_image_list = tower_3_image
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.lvl = 1
        self.damage = 50
        self.enemy = None
        self.timer_shot = 0
        self.upgrade = False
        self.current_bullet_image = tower_3_bullet
        self.frame = 0
        self.timer_anime = 0
        self.anime = True

    def update(self):
        self.upgrades()
        self.shot()
        self.animation()






        if self.enemy is None:
            for enemy in enemy_group:
                if ((self.rect.centerx - enemy.rect.centerx) ** 2 + (
                        self.rect.centerx - enemy.rect.centery) ** 2) ** 0.5 < 500:
                    self.enemy = enemy
                    break
        if self.enemy not in enemy_group:
            self.enemy = None

    def upgrades(self):
        global money
        if self.lvl == 1 and money >= 300:
            self.upgrade = True

        if self.upgrade == True:
            sc.blit(upgrade_image, (self.rect.right, self.rect.bottom))

        if self.upgrade == True and pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if self.rect.right < pos[0] < self.rect.right + 50 \
                    and self.rect.bottom < pos[1] < self.rect.bottom + 45:
                money -=300
                self.lvl = 2
                self.damage = 75
                self.image = tower_3_1_image[2]

                self.upgrade = False
                self.current_image_list = tower_3_1_image

    def shot(self):
        self.timer_shot += 1
        if self.enemy != None and self.timer_shot / FPS > 3:
            x_1 = self.rect.centerx
            y_1 = self.rect.top
            x_2 = self.enemy.rect.centerx
            y_2 = self.enemy.rect.centery
            bullet3 = Bullet3(self.current_bullet_image, (x_1, y_1, x_2, y_2), self.damage, 5 * self.lvl)
            bullet3_group.add(bullet3)
            self.timer_shot = 0





    def animation(self):
        if self.anime:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.11:
                if self.frame == len(self.current_image_list) - 1:
                    self.frame = 0
                else:
                    self.frame += 1
                self.timer_anime = 0
        self.image = self.current_image_list[self.frame]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, pos, damage, speed=5):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = speed
        self.damage = damage
        self.start_pos = pygame.math.Vector2(pos[0], pos[1])
        self.end_pos = pygame.math.Vector2(pos[2], pos[3])
        self.velocity = (self.end_pos - self.start_pos).normalize() * self.speed
        self.rect.center = self.start_pos
        self.death = False
        self.timer = 0
        self.frame = 0
        self.timer_anime = 0
        self.anime = False





    def update(self):
        self.animation()
        self.rect.center += self.velocity
        if self.death:
            self.timer += 1
            if self.timer / FPS > 0.3:
                self.kill()
        if pygame.sprite.spritecollide(self, enemy_group, True):
            self.anime = True
            self.speed = 0

    def animation(self):
        if self.anime:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(tower_bullet_anime) - 1:
                    self.frame = 0
                    self.kill()
                else:
                    self.frame += 1
                self.timer_anime = 0
        self.image = tower_bullet_anime[self.frame]

class Bullet2(pygame.sprite.Sprite):
    def __init__(self, image, pos, damage, speed=5):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = speed
        self.damage = damage
        self.start_pos = pygame.math.Vector2(pos[0], pos[1])
        self.end_pos = pygame.math.Vector2(pos[2], pos[3])
        self.velocity = (self.end_pos - self.start_pos).normalize() * self.speed
        self.rect.center = self.start_pos
        self.death = False
        self.timer = 0
        self.frame = 0
        self.timer_anime = 0
        self.anime = False





    def update(self):
        self.animation()
        self.rect.center += self.velocity
        if self.death:
            self.timer += 1
            if self.timer / FPS > 0.3:
                self.kill()
        if pygame.sprite.spritecollide(self, enemy_group, True):
            self.anime = True
            self.speed = 0

    def animation(self):
        if self.anime:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(tower_bullet_2anime) - 1:
                    self.frame = 0
                    self.kill()
                else:
                    self.frame += 1
                self.timer_anime = 0
        self.image = tower_bullet_2anime[self.frame]

class Bullet3(pygame.sprite.Sprite):
    def __init__(self, image, pos, damage, speed=5):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = speed
        self.damage = damage
        self.start_pos = pygame.math.Vector2(pos[0], pos[1])
        self.end_pos = pygame.math.Vector2(pos[2], pos[3])
        self.velocity = (self.end_pos - self.start_pos).normalize() * self.speed
        self.rect.center = self.start_pos
        self.death = False
        self.timer = 0
        self.frame = 0
        self.timer_anime = 0
        self.anime = False





    def update(self):
        self.animation()
        self.rect.center += self.velocity
        if self.death:
            self.timer += 1
            if self.timer / FPS > 0.3:
                self.kill()
        if pygame.sprite.spritecollide(self, enemy_group, True):
            self.anime = True
            self.speed = 0

    def animation(self):
        if self.anime:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.05:
                if self.frame == len(tower_bullet_3anime) - 1:
                    self.frame = 0
                    self.kill()
                else:
                    self.frame += 1
                self.timer_anime = 0
        self.image = tower_bullet_3anime[self.frame]




def game_lvl1():
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
    score_counter = font.render(f'Score: {score}', True, 'black')
    sc.blit(money_counter, (40, 40))
    sc.blit(score_counter, (40, 75))
    tower_afk_group.update()
    tower_afk_group.draw(sc)
    tower_shots_group.update()
    tower_shots_group.draw(sc)
    tower_afk2_group.update()
    tower_afk2_group.draw(sc)
    tower_shots2_group.update()
    tower_shots2_group.draw(sc)
    tower_afk3_group.update()
    tower_afk3_group.draw(sc)
    tower_shots3_group.update()
    tower_shots3_group.draw(sc)
    bullet3_group.update()
    bullet3_group.draw(sc)
    spawner.update()
    enemy_group.update()
    enemy_group.draw(sc)
    bullet_group.update()
    bullet_group.draw(sc)
    bullet2_group.update()
    bullet2_group.draw(sc)
    pygame.display.update()


def game_lvl2():
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
    score_counter = font.render(f'Score: {score}', True, 'black')
    sc.blit(money_counter, (40, 40))
    sc.blit(score_counter, (40, 75))
    tower_afk_group.update()
    tower_afk_group.draw(sc)
    tower_shots_group.update()
    tower_shots_group.draw(sc)
    tower_afk2_group.update()
    tower_afk2_group.draw(sc)
    tower_shots2_group.update()
    tower_shots2_group.draw(sc)
    tower_afk3_group.update()
    tower_afk3_group.draw(sc)
    tower_shots3_group.update()
    tower_shots3_group.draw(sc)
    bullet3_group.update()
    bullet3_group.draw(sc)
    spawner.update()
    enemy_group.update()
    enemy_group.draw(sc)
    bullet_group.update()
    bullet_group.draw(sc)
    bullet2_group.update()
    bullet2_group.draw(sc)
    pygame.display.update()


def game_lvl3():
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
    score_counter = font.render(f'Score: {score}', True, 'black')
    sc.blit(money_counter, (40, 40))
    sc.blit(score_counter, (40, 75))
    tower_afk_group.update()
    tower_afk_group.draw(sc)
    tower_afk2_group.update()
    tower_afk2_group.draw(sc)
    tower_shots2_group.update()
    tower_shots2_group.draw(sc)
    tower_shots_group.update()
    tower_shots_group.draw(sc)
    tower_afk3_group.update()
    tower_afk3_group.draw(sc)
    tower_shots3_group.update()
    tower_shots3_group.draw(sc)
    bullet3_group.update()
    bullet3_group.draw(sc)
    spawner.update()
    enemy_group.update()
    enemy_group.draw(sc)
    bullet_group.update()
    bullet_group.draw(sc)
    bullet2_group.update()
    bullet2_group.draw(sc)
    pygame.display.update()


def restart():
    global spawner, tower_shots_group, grass_group, tower_afk_group, tower_bush_group, bush_group, enemy_group, spawner_group, up_group, edit_dir_group, bottom_group, left_group, right_group
    global tower_shop_1, bullet_group, button_group, button2_group,tower_shop_2,tower_afk2_group,tower_shots2_group,bullet2_group,tower_shop_3,bullet3_group,tower_afk3_group,tower_shots3_group
    # global

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
    tower_afk2_group = pygame.sprite.Group()
    spawner = Spawner()
    bullet_group = pygame.sprite.Group()
    bullet2_group = pygame.sprite.Group()


    bullet3_group = pygame.sprite.Group()
    tower_afk3_group = pygame.sprite.Group()
    tower_shots3_group = pygame.sprite.Group()
    tower_shots_group = pygame.sprite.Group()
    tower_shots2_group = pygame.sprite.Group()
    tower_shop_1 = Tower_afk(tower_1_on, (45, 765))
    tower_afk_group.add(tower_shop_1)
    tower_shop_2 = Tower_afk2(tower_2_on, (127, 762))
    tower_afk_group.add(tower_shop_2)
    tower_shop_3 = Tower_afk3(tower_3_on, (205, 761))
    tower_afk_group.add(tower_shop_3)

    button_start = Button(button_image, (540, 100), 'choise', 'start')
    button_group.add(button_start)

    button_score = Button(button_image, (540, 180), 'score', 'score')
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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if lvl == 'game':
        game_lvl1()
    elif lvl == 'menu':
        startMenu()
    elif lvl == 'exit':
        pygame.quit()
        game_lvl1()
    elif lvl == 'choise':
        changelvl()
    elif lvl == 'back':
        startMenu()
    elif lvl == 'lvl 1':
        game_lvl1()
    elif lvl == 'lvl 2':
        game_lvl2()
    elif lvl == 'lvl 3':
        game_lvl3()
    clock.tick(FPS)
