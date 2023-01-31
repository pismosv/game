import random

import pygame
from pygame.locals import *
import pygame_widgets
from pygame_widgets.button import Button

import sprites
from constants import *
from animated_sprites import *
from sprites import *

# старт игры
pygame.init()
pygame.key.set_repeat(200, 200)
size = width, height = 500, 500
screen = pygame.display.set_mode(size)

pygame.mixer.pre_init(44100, 16, 1, 512)
pygame.init()


def load_level(filename):
    filename = 'data/levels/' + filename
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
                Object(level[y][x], x, y)
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
    global player, diamonds, stones_have
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
    stone_srt = font.render(f"Камни:{sprites.stones_have}",
                            True, pygame.Color('gray'))
    intro_rect1 = string_rendered.get_rect()
    intro_rect1.x = 10
    intro_rect1.y = 50
    screen.blit(stone_srt, intro_rect1)


def menu():
    name_of_game = "Picker"
    fon = pygame.transform.scale(load_image('fon_menu.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 200)
    string_rendered = font.render(name_of_game, True, pygame.Color('yellow'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 10
    intro_rect.x = 45
    screen.blit(string_rendered, intro_rect)

    pygame.mixer.music.load(r"data/sounds/menu_theme.mp3")
    pygame.mixer.music.play(-1)
    s = False

    def start():
        global s
        s = True

    button = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        100,  # X-coordinate of top left corner
        150,  # Y-coordinate of top left corner
        300,  # Width
        100,  # Height

        # Optional Parameters
        text='Играть',  # Text to display
        fontSize=50,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(255, 229, 10),
        # Colour of button when not being interacted with
        hoverColour=(255, 234, 61),  # Colour of button when being hovered over
        pressedColour=(255, 204, 8),  # Colour of button when being clicked
        radius=20,  # Radius of border corners (leave empty for not curved)
        onClick=lambda: main()  # Function to call when clicked on
    )

    button1 = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        100,  # X-coordinate of top left corner
        270,  # Y-coordinate of top left corner
        300,  # Width
        100,  # Height

        # Optional Parameters
        text='Выход',  # Text to display
        fontSize=50,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(255, 229, 10),
        # Colour of button when not being interacted with
        hoverColour=(255, 234, 61),  # Colour of button when being hovered over
        pressedColour=(255, 204, 8),  # Colour of button when being clicked
        radius=20,  # Radius of border corners (leave empty for not curved)
        onClick=lambda: exit()  # Function to call when clicked on
    )

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
        if s:
            return "game"
        pygame_widgets.update(events)
        pygame.display.flip()


# функция заставки
def start_screen():
    pygame.mixer.stop()
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
                return
        pygame.display.flip()
        cl.tick(FPS)


def draw_text(tip):
    font = pygame.font.Font(None, 30)
    text_coord = 50
    if tip == 1:
        string_rendered1 = font.render("mission passed!", True,
                                       pygame.Color('gold'))
        intro_rect1 = string_rendered1.get_rect()
        intro_rect1.x = 250 - 70
        intro_rect1.y = 220
        screen.blit(string_rendered1, intro_rect1)
        string_rendered2 = font.render("respect +", True,
                                       pygame.Color('white'))
        intro_rect2 = string_rendered2.get_rect()
        intro_rect2.x = 250 - 45
        intro_rect2.y = 250
        screen.blit(string_rendered2, intro_rect2)


# тут главный цикл
def main():
    global player, fullscreen, stones_have, win, exit_but
    try:
        inventory_open = False
        pygame.mixer.music.load(random.choice([r"data\sounds\alex_f.mp3",
                                               r"data\sounds\tree.mp3",
                                               r"data\sounds\conta_theme.mp3"]))
        pygame.mixer.music.play(-1)
        camera = Camera()
        lvl = random.choice(["map.txt", "map1.txt", "map2.txt"])
        clock = pygame.time.Clock()
        player, level_x, level_y = generate_level(load_level(lvl))
        a = 0
        pos = None
        fullscreen = False
        win = False
        while True:
            screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    if event.button == 1:
                        if exit_but.collidepoint(pos):
                            menu()
                            print(1)
                if event.type == pygame.KEYDOWN:
                    if player.hp > 0 and not win:
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
                            if sprites.stones_have != 0:
                                bip = create_sound04("woo.wav")
                                bip.play()
                                stones.append(
                                    FlyingStone(player.looking,
                                                player.x,
                                                player.y, player))
                                sprites.stones_have -= 1

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
                    if event.key == pygame.K_q:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.pause()
                        return "menu"
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)
            all_sprites.draw(screen)
            player_group.draw(screen)
            draw_ui()
            exit_but = pygame.Rect(0, 0, 40, 40)
            for boom in booms:
                boom.update()
                if boom.cur_frame == 8:
                    booms.remove(boom)
                    boom.kill()
                if boom.cur_frame == 1:
                    b = create_sound04("explosion.wav")
                    b.play()

            for s in stones:
                s.update()

            if inventory_open:
                Inventory(player)

            x = 0
            for elem in items_list:
                if type(elem) == Mine:
                    x += 1
            if x == len(items_list):
                draw_text(1)
                pygame.mixer.music.pause()
                if not win:
                    bip = create_sound04("misson_passed.wav")
                    bip.play()
                    win = True

            if player.hp <= 0:
                pygame.mixer.music.stop()

            pygame.display.flip()
            clock.tick(FPS)
    except Exception as e:
        print("Ошибка:", e)
        terminate()


if __name__ == "__main__":
    while True:
        m = menu()
        if m == "game":
            for group in all_groups:
                group.clear()
            menu_group.clear()
            m = main()
        elif m == "menu":
            all_sprites.clear()
            m = menu()
