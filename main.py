import os
import sys
import pygame

# старт игры
pygame.init()
pygame.key.set_repeat(200, 100)
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


# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
tile_images = {
    'wall': pygame.transform.scale(load_image('wall.png'), (50, 50)),
    'ground': pygame.transform.scale(load_image('floor.png'), (50, 50))
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


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(player_image, (50, 50))
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def move(self, direction):
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
        if pygame.sprite.spritecollideany(self, wall_group):
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
        # print(self.x, self.y)


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


# генерация уровня
def generate_level(level):
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
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


# функция заставки
def start_screen():
    intro_text = ["Давным давно...", "",
                  "Существовали две расы -",
                  "Люди и монстры,",
                  "Но люди загнали их в подземелье,",
                  "И сейчас монстры хотят ",
                  "вернуться на поверхность...",
                  "Но наш герой им этого не даст."]

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:  # тут отрисовываем все строчки одна за одной
        string_rendered = font.render(line, True, pygame.Color('black'))
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


# тут главный цикл
def main():
    try:
        camera = Camera()
        # level = input("Имя уровня:")
        level = "map.txt"
        start_screen()
        clock = pygame.time.Clock()
        player, level_x, level_y = generate_level(load_level(level))
        while True:
            screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.move("left")
                    if event.key == pygame.K_RIGHT:
                        player.move("right")
                    if event.key == pygame.K_UP:
                        player.move("up")
                    if event.key == pygame.K_DOWN:
                        player.move("down")
            # изменяем ракурс камеры
            camera.update(player)
            # обновляем положение всех спрайтов
            for sprite in all_sprites:
                camera.apply(sprite)
            all_sprites.draw(screen)
            player_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
    except Exception as e:
        print("Ошибка:", e)
        terminate()


if __name__ == "__main__":
    main()
