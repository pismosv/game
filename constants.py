import pygame


# Константы
FPS = 20
WIDTH, HEIGHT = 500, 500
GRAVITY = 5

# переменные
mouse_pos = None
count = 0
hit = None
CLICK = False

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()
ui_group = pygame.sprite.Group()
menu_group = pygame.sprite.Group()

all_groups = [all_sprites, tiles_group, player_group, wall_group, objects_group,
              items_group, ui_group]
tile_width = tile_height = 50
