import os
import random
import sys
import pygame
from pygame.locals import *
import items
from constants import *
from general_functions import *
from animated_sprites import *

# старт игры
pygame.init()
pygame.key.set_repeat(200, 200)
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '~'), level_map))


# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()

# словари с картинками

tile_images = {
    'wall': pygame.transform.scale(load_image('wall.png'), (50, 50)),
    'ground': pygame.transform.scale(load_image('floor.png'), (50, 50))
}

object_images = {
    'vase': pygame.transform.scale(load_image('vase.png'),
                                   (50, 50)),
}

items_images = {
    'diamond': pygame.transform.scale(load_image('diamond.png'),
                                      (50, 50))
}

# разные картинки игрока
player_image = pygame.transform.scale(load_image("player2.png"),
                                      (50, 50))
player_image_l = pygame.transform.scale(load_image("player2_left.png"),
                                        (50, 50))
player_image_r = pygame.transform.scale(load_image("player2_right.png"),
                                        (50, 50))
player_image_u = pygame.transform.scale(load_image("player2_up.png"),
                                        (50, 50))

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == "wall":
            self.add(wall_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Object(pygame.sprite.Sprite):
    def __init__(self, obj_type, pos_x, pos_y):
        super().__init__(objects_group, all_sprites)
        self.image = object_images[obj_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(player_image, (50, 50))
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.hp = 20
        self.inventory = []

    def move(self, direction):
        global diamonds
        if direction == "left":
            self.x -= 1
            self.rect = self.rect.move(
                -tile_width, 0)
            self.image = player_image_l
        elif direction == "right":
            self.x += 1
            self.rect = self.rect.move(
                tile_width, 0)
            self.image = player_image_r
        elif direction == "down":
            self.y += 1
            self.rect = self.rect.move(
                0, tile_height)
            self.image = player_image
        elif direction == "up":
            self.y -= 1
            self.rect = self.rect.move(
                0, -tile_height)
            self.image = player_image_u
        else:
            print("неизвестное направление")
        if pygame.sprite.spritecollideany(self, wall_group) or \
                pygame.sprite.spritecollideany(self, objects_group):
            if direction == "left":
                self.x += 1
                self.rect = self.rect.move(
                    tile_width, 0)
            elif direction == "right":
                self.x -= 1
                self.rect = self.rect.move(
                    -tile_width, 0)
            elif direction == "down":
                self.y -= 1
                self.rect = self.rect.move(
                    0, -tile_height)
            elif direction == "up":
                self.y += 1
                self.rect = self.rect.move(
                    0, tile_height)
        for item in items_list:
            if items_list:
                if pygame.sprite.collide_rect(self, item):
                    if type(item) == items.Diamond:
                        item.kill()
                        diamonds += 1
                        self.inventory.append(str(item))
                        items_list.remove(item)
                    elif type(item) == items.Mine:
                        item.kill()
                        self.hp -= 15
                        booms.append(Boom(item.rect.x, item.rect.y))
                        items_list.remove(item)
                    else:
                        item.kill()
                        self.inventory.append(str(item))
                        items_list.remove(item)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Boom(AnimatedSprite):
    def __init__(self, x, y):
        super(Boom, self).__init__(
            pygame.transform.scale(load_image("boom.png"),
                                   (450, 50)), 9, 1, x, y, all_sprites)

    def update(self):
        super(Boom, self).update()


items_list = []


# генерация уровня
def generate_level(level):
    global items_list
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('ground', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('ground', x, y)
                new_player = Player(x, y)
            elif level[y][x] == "v":
                Tile("ground", x, y)
                items_list.append(Object("vase", x, y))
            elif level[y][x] == "m":
                Tile("ground", x, y)
                items_list.append(items.Mine(x, y, all_sprites,
                                             items_group))
            elif level[y][x] == "S":
                Tile("ground", x, y)
                s = random.random()
                if s <= 0.25:
                    items_list.append(items.Stick(x, y, all_sprites,
                                                  items_group))
                elif s <= 0.5:
                    items_list.append(items.Stone(x, y, all_sprites,
                                                  items_group))
                elif s <= 0.8:
                    items_list.append(items.Coin(x, y, all_sprites,
                                                 items_group))
                elif s <= 0.95:
                    items_list.append(items.Jade(x, y, all_sprites,
                                                 items_group))
                elif s <= 1:
                    items_list.append(items.Diamond(x, y, all_sprites,
                                                    items_group))
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def draw_ui():
    global main_player, diamonds
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(f"Алмазы:{diamonds}",
                                  True, pygame.Color('cyan'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 10
    intro_rect.y = 30
    screen.blit(string_rendered, intro_rect)
    hp_text = font.render(f"Здоровье:{main_player.hp}",
                          True, pygame.Color('white'))
    hp_rect = hp_text.get_rect()
    hp_rect.x = 10
    hp_rect.y = 10
    screen.blit(hp_text, hp_rect)


# функция заставки
def start_screen():
    intro_text = ["Давным давно...", "",
                  "Древняя раса людей создала",
                  "Магические камни",
                  "Но после 4 тысяч лет, предки",
                  "Этих могущественных людей начали воевать",
                  "Из-за этих камней. После войны",
                  "камни остались в древних руинах.",
                  "И наш герой решил их собрать,",
                  "Чтобы вернуть могущество своего народа"]

    fon = pygame.transform.scale(load_image('fon_level.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:  # тут отрисовываем все строчки одна за одной
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


camera = Camera()
# level = input("Имя уровня:")
level = "map.txt"
start_screen()
clock = pygame.time.Clock()
main_player, level_x, level_y = generate_level(load_level(level))
MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 600)
a = 0
pos = None
fullscreen = False
diamonds = 0
booms = []


# тут главный цикл
def main():
    global main_player, fullscreen
    try:
        while True:
            screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if main_player.hp > 0:
                        if event.key == pygame.K_a:
                            main_player.move("left")
                        if event.key == pygame.K_d:
                            main_player.move("right")
                        if event.key == pygame.K_w:
                            main_player.move("up")
                        if event.key == pygame.K_s:
                            main_player.move("down")
                    if event.key == pygame.K_F11:
                        if not fullscreen:
                            pygame.display.set_mode((width, height), FULLSCREEN)
                            fullscreen = True
                    if event.key == pygame.K_F10:
                        if fullscreen:
                            pygame.display.set_mode((width, height))
                            fullscreen = False
                    if event.key == pygame.K_c:
                        print(main_player.inventory)
            camera.update(main_player)
            for sprite in all_sprites:
                camera.apply(sprite)
            all_sprites.draw(screen)
            player_group.draw(screen)
            draw_ui()
            for boom in booms:
                boom.update()
                if boom.cur_frame == 8:
                    booms.remove(boom)
                    boom.kill()
            pygame.display.flip()
            clock.tick(FPS)
    except Exception as e:
        print("Ошибка:", e)
        terminate()


if __name__ == "__main__":
    main()
