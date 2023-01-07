import os
import random
import sys

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    # if colorkey is not None:
    #     image = image.convert()
    #     if colorkey == -1:
    #         colorkey = image.get_at((0, 0))
    #     image.set_colorkey(colorkey)
    # else:
    #     image = image.convert_alpha()
    return image


items_images = {
    'diamond': pygame.transform.scale(load_image('diamond.png'),
                                      (50, 50)),
    'stick': pygame.transform.scale(load_image('stick.png'),
                                    (50, 50)),
    'mine': pygame.transform.scale(load_image('mine.png'),
                                   (50, 50))
}

tile_width = tile_height = 50


class Item(pygame.sprite.Sprite):
    def __init__(self, item_type, pos_x, pos_y, *groups):
        super().__init__(groups)
        self.image = items_images[item_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Diamond(Item):
    def __init__(self, pos_x, pos_y, *groups):
        super(Diamond, self).__init__("diamond", pos_x, pos_y, groups)
        self.value = random.randint(10, 15)


class Stick(Item):
    def __init__(self, pos_x, pos_y, *groups):
        super(Stick, self).__init__("stick", pos_x, pos_y, groups)
        self.value = random.randint(10, 15)


class Mine(Item):
    def __init__(self, pos_x, pos_y, *groups):
        super(Mine, self).__init__("mine", pos_x, pos_y, groups)
        self.value = random.randint(10, 15)
