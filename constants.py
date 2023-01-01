import pygame


# Константы
<<<<<<< HEAD
FPS = 20
=======
FPS = 50
>>>>>>> a60ae16 (dev 0.1.a)
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
enemy_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
tile_width = tile_height = 50
