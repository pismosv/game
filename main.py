import random
from pygame.locals import *
from constants import *
from animated_sprites import *
from sprites import *

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
    obj_str = "vtbc"
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
            elif level[y][x] in obj_str:
                Tile("ground", x, y)
                items_list.append(Object(level[y][x], x, y))
            elif level[y][x] == "m":
                Tile("ground", x, y)
                items_list.append(Mine(x, y, all_sprites,
                                       items_group))
            elif level[y][x] == "S":
                Tile("ground", x, y)
                c = random.random()
                if c >= 0.5:
                    s = random.random()
                    if s <= 0.25:
                        items_list.append(Stick(x, y, all_sprites,
                                                items_group))
                    elif s <= 0.5:
                        items_list.append(Stone(x, y, all_sprites,
                                                items_group))
                    elif s <= 0.8:
                        items_list.append(Coin(x, y, all_sprites,
                                               items_group))
                    elif s <= 0.95:
                        items_list.append(Jade(x, y, all_sprites,
                                               items_group))
                    elif s <= 1:
                        items_list.append(Diamond(x, y, all_sprites,
                                                  items_group))
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def draw_ui():
    global player, diamonds, stones
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(f"Предметы:{len(player.inventory)}",
                                  True, pygame.Color('yellow'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 10
    intro_rect.y = 30
    screen.blit(string_rendered, intro_rect)
    hp_text = font.render(f"Здоровье:{player.hp}",
                          True, pygame.Color('red'))
    hp_rect = hp_text.get_rect()
    hp_rect.x = 10
    hp_rect.y = 10
    screen.blit(hp_text, hp_rect)
    stone_srt = font.render(f"Камни:{stones_have}",
                            True, pygame.Color('gray'))
    intro_rect1 = string_rendered.get_rect()
    intro_rect1.x = 10
    intro_rect1.y = 50
    screen.blit(stone_srt, intro_rect1)


# функция заставки
def start_screen():
    intro_text = ["", "Давным давно...",
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
    cl = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        cl.tick(FPS)


camera = Camera()
# level = input("Имя уровня:")
lvl = random.choice(["map.txt", "map1.txt", "map2.txt"])
start_screen()
clock = pygame.time.Clock()
player, level_x, level_y = generate_level(load_level(lvl))
MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 600)
a = 0
pos = None
fullscreen = False


# тут главный цикл
def main():
    global player, fullscreen, stones_have
    try:
        inventory_open = False
        while True:
            screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if player.hp > 0:
                        if event.key == pygame.K_a:
                            player.move("left")
                        if event.key == pygame.K_d:
                            player.move("right")
                        if event.key == pygame.K_w:
                            player.move("up")
                        if event.key == pygame.K_s:
                            player.move("down")
                        if event.key == pygame.K_LEFT:
                            player.change_player_sprite("left")
                        if event.key == pygame.K_RIGHT:
                            player.change_player_sprite("right")
                        if event.key == pygame.K_UP:
                            player.change_player_sprite("up")
                        if event.key == pygame.K_DOWN:
                            player.change_player_sprite("down")
                        if event.key == pygame.K_f:
                            if stones_have != 0:
                                stones.append(
                                    FlyingStone(player.looking,
                                                player.x,
                                                player.y, player))
                                stones_have -= 1
                    if event.key == pygame.K_F11:
                        if not fullscreen:
                            pygame.display.set_mode((width, height), FULLSCREEN)
                            fullscreen = True
                    if event.key == pygame.K_F10:
                        if fullscreen:
                            pygame.display.set_mode((width, height))
                            fullscreen = False
                    if event.key == pygame.K_c:
                        if not inventory_open:
                            inventory_open = True
                        else:
                            inventory_open = False
            camera.update(player)
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
            for s in stones:
                s.update()
            if inventory_open:
                Inventory(player)
            pygame.display.flip()
            clock.tick(FPS)
    except Exception as e:
        print("Ошибка:", e)
        terminate()


if __name__ == "__main__":
    main()
