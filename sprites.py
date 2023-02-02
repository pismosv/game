from items import *
from animated_sprites import Boom
from constants import *
from general_functions import load_image

pygame.init()
pygame.key.set_repeat(200, 200)
size = width, height = 500, 500
screen = pygame.display.set_mode(size)

items_list = []

booms = []
stones_have = 3
stones = []

player_image = pygame.transform.scale(load_image("player2.png"),
                                      (50, 50))
player_image_l = pygame.transform.scale(load_image("player2_left.png"),
                                        (50, 50))
player_image_r = pygame.transform.scale(load_image("player2_right.png"),
                                        (50, 50))
player_image_u = pygame.transform.scale(load_image("player2_up.png"),
                                        (50, 50))

tile_images = {
    'wall': pygame.transform.scale(load_image('wall.png'), (50, 50)),
    'ground': pygame.transform.scale(load_image('floor.png'), (50, 50))
}

object_images = {
    'v': pygame.transform.scale(load_image('vase.png'),
                                (50, 50)),
    'c': pygame.transform.scale(load_image('chest.png'),
                                (50, 50)),
    't': pygame.transform.scale(load_image('table.png'),
                                (50, 50)),
    'b': pygame.transform.scale(load_image('table_broken.png'),
                                (50, 50))
}


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
        self.looking = "down"

    def change_player_sprite(self, direction):
        self.looking = direction
        if direction == "left":
            self.image = player_image_l
        elif direction == "right":
            self.image = player_image_r
        elif direction == "down":
            self.image = player_image
        elif direction == "up":
            self.image = player_image_u

    def move(self, direction):
        global stones_have
        self.change_player_sprite(direction)
        if direction == "left":
            self.x -= 1
            self.rect = self.rect.move(
                -tile_width, 0)
        elif direction == "right":
            self.x += 1
            self.rect = self.rect.move(
                tile_width, 0)
        elif direction == "down":
            self.y += 1
            self.rect = self.rect.move(
                0, tile_height)
        elif direction == "up":
            self.y -= 1
            self.rect = self.rect.move(
                0, -tile_height)
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
                    if type(item) == Diamond:
                        item.kill()
                        self.inventory.append(str(item))
                        items_list.remove(item)
                    elif type(item) == Stone:
                        item.kill()
                        stones_have += 1
                        items_list.remove(item)
                    elif type(item) == Mine:
                        item.kill()
                        self.hp -= 10
                        booms.append(Boom(item.rect.x, item.rect.y))
                        items_list.remove(item)
                    else:
                        item.kill()
                        self.inventory.append(str(item))
                        items_list.remove(item)


class FlyingStone(pygame.sprite.Sprite):
    def __init__(self, looking, x, y, main_player):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image("flying_stone.png"),
                                            (50, 50))
        self.look = looking
        self.x, self.y = x, y
        self.rect = self.image.get_rect().move(
            main_player.rect.x,
            main_player.rect.y)

    def update(self):
        if pygame.sprite.spritecollideany(self, wall_group) or \
                pygame.sprite.spritecollideany(self, objects_group):
            self.kill()
            stones.remove(self)
        if self.look == "right":
            self.x -= 1
            self.rect = self.rect.move(
                tile_width, 0)
        elif self.look == "left":
            self.x += 1
            self.rect = self.rect.move(
                -tile_width, 0)
        elif self.look == "up":
            self.y -= 1
            self.rect = self.rect.move(
                0, -tile_height)
        elif self.look == "down":
            self.y += 1
            self.rect = self.rect.move(
                0, tile_height)
        for item in items_list:
            if items_list:
                if pygame.sprite.collide_rect(self, item):
                    if type(item) == Mine:
                        item.kill()
                        booms.append(Boom(item.rect.x, item.rect.y))
                        items_list.remove(item)
                        self.kill()


class Inventory(pygame.sprite.Sprite):
    def __init__(self, main_player):
        super().__init__(ui_group)
        for i in range(10):
            p = pygame.transform.scale(load_image('inventory_background.png'),
                                       (70, 70))
            screen.blit(p, (70 * i, 430))
        for i in range(len(main_player.inventory)):
            it = pygame.transform.scale(load_image(main_player.inventory[i] +
                                                   ".png"), (30, 30))
            screen.blit(it, (30 * i + 30, 450))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, obj_type, pos_x, pos_y):
        super().__init__(objects_group, all_sprites)
        self.image = object_images[obj_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
