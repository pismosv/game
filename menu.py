import os
import sys

import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.key.set_repeat(200, 200)
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.flip()

    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image


    fon = pygame.transform.scale(load_image('fon_menu.png'), (width, height))
    screen.blit(fon, (0, 0))
