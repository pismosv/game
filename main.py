import csv
import random

import pygame
from pygame.locals import *
import pygame_menu
from pygame_menu import themes

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
    # string_rendered = font.render(f"Предметы:{len(player.inventory)}",
    #                               True, pygame.Color('yellow'))
    # intro_rect = string_rendered.get_rect()
    # intro_rect.x = 10
    # intro_rect.y = 30
    # screen.blit(string_rendered, intro_rect)
    hp_text = font.render(f"Здоровье:{player.hp}",
                          True, pygame.Color('red'))
    hp_rect = hp_text.get_rect()
    hp_rect.x = 10
    hp_rect.y = 10
    screen.blit(hp_text, hp_rect)
    stone_srt = font.render(f"Камни:{sprites.stones_have}",
                            True, pygame.Color('gray'))
    intro_rect1 = stone_srt.get_rect()
    intro_rect1.x = 10
    intro_rect1.y = 30
    screen.blit(stone_srt, intro_rect1)


# функция заставки
def start_screen():
    pygame.mixer.stop()
    intro_text = ["", "", "Когда-то планета Вулкан была цветущим миром.",
                  "Народы этой планеты возводили странные строения",
                  "и хранили там свои сокровища, но они придумывали",
                  "хитроумные ловушки, чтобы ни кто не смог",
                  "их забрать. Но что же случилось? Не осталось ни ",
                  "кого на этой планете, кто бы мог рассказать, куда",
                  "делись все обитатели? Мы теперь оказались здесь,",
                  "чтобы разобраться и найти все тайники и сокровища."]

    fon = pygame.transform.scale(load_image('fon_level.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 25)
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
        string_rendered3 = font.render("нажми Q чтобы выйти в меню", True,
                                       pygame.Color('red'))
        intro_rect3 = string_rendered3.get_rect()
        intro_rect3.x = 250 - 140
        intro_rect3.y = 350
        screen.blit(string_rendered3, intro_rect3)
    elif tip == 2:
        string_rendered1 = font.render("mission failed!", True,
                                       pygame.Color('red'))
        intro_rect1 = string_rendered1.get_rect()
        intro_rect1.x = 250 - 70
        intro_rect1.y = 220
        screen.blit(string_rendered1, intro_rect1)
        string_rendered2 = font.render("хорошая попытка!",
                                       True,
                                       pygame.Color('white'))
        intro_rect2 = string_rendered2.get_rect()
        intro_rect2.x = 250 - 85
        intro_rect2.y = 250
        screen.blit(string_rendered2, intro_rect2)
        string_rendered3 = font.render("нажми Q чтобы выйти в меню", True,
                                       pygame.Color('red'))
        intro_rect3 = string_rendered3.get_rect()
        intro_rect3.x = 250 - 140
        intro_rect3.y = 350
        screen.blit(string_rendered3, intro_rect3)


pygame.init()
surface = pygame.display.set_mode((600, 400))

inventory_open = camera = lvl = clock = player = level_x = \
    level_y = fullscreen = win = game_over = None

background = pygame.Surface(size)


def initstate():
    global inventory_open, camera, lvl, clock, player, level_x, level_y, \
        fullscreen, win, game_over
    inventory_open = False
    camera = Camera()
    lvl = random.choice(["map.txt", "map1.txt", "map2.txt"])
    clock = pygame.time.Clock()
    player, level_x, level_y = generate_level(load_level(lvl))
    fullscreen = False
    win = False
    game_over = False


# тут главный цикл
def main():
    global inventory_open, camera, lvl, clock, player, level_x, level_y, \
        fullscreen, win, first_start, stones_have, game_over
    j = 0
    try:
        initstate()
        pygame.display.set_mode((500, 500))
        pygame.mixer.music.load(random.choice([r"data\sounds\alex_f.mp3",
                                               r"data\sounds\tree.mp3",
                                               r"data\sounds\conta_theme.mp3"]))
        pygame.mixer.music.play(-1)
        start_screen()
        while True:
            screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
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
                        else:
                            pygame.display.set_mode((width, height))
                            fullscreen = False
                    if event.key == pygame.K_c:  # open inventory
                        if not inventory_open:
                            inventory_open = True
                        else:
                            inventory_open = False
                    if event.key == pygame.K_q:  # button to leave from game
                        global all_sprites, tiles_group, player_group, \
                            wall_group, objects_group, items_group, ui_group, \
                            menu_group
                        for group in all_groups:
                            for item in group:
                                item.kill()
                        screen.fill((0, 0, 0))
                        pygame.mixer.music.stop()
                        pygame.mixer.stop()
                        pygame.display.set_mode((600, 400))
                        items_list.clear()
                        pygame.mixer.music.load(r"data\sounds\menu_theme.mp3")

                        pygame.mixer.music.play(-1)
                        sprites.stones_have = 3
                        if win:
                            count_money_for_wining()
                        update_csv()

                        return
                    if event.key == pygame.K_TAB:  # turn on/off music
                        j += 1
                        if j % 2 != 0:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                    if sv_cheats:  # if cheats true
                        if event.key == pygame.K_l:
                            items_list.clear()
                        if event.key == pygame.K_m:
                            player.hp = 0

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
                player.hp = 0
                draw_text(2)
                if not game_over:
                    bip = create_sound04("game_over.wav")
                    bip.play()
                    game_over = True
            pygame.display.flip()
            clock.tick(FPS)
    except Exception as e:
        print("Ошибка:", e)
        terminate()


def start_the_game():
    if root_to_play:
        main()
    else:
        return


def update_csv():
    filename = "tops.csv"
    f = open(filename, "w+")
    f.close()
    with open('tops.csv', 'w', newline='',
              encoding="utf8") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for elem in top_data:
            writer.writerow(elem)


def change_value_in_list(name, value):
    global top_data
    names = [x[0] for x in top_data]
    if name in names:
        for i in range(len(top_data)):
            if top_data[i][0] == name:
                top_data[i][1] = value
                break
        top_data.sort(key=lambda x: int(x[1]), reverse=True)
    else:
        top_data.append([name, value])
        top_data.sort(key=lambda x: int(x[1]), reverse=True)


def count_money_for_wining():
    money = 0
    cost = {
        'diamond': 30,
        'stick': 5,

        'coin': 10,
        'jade': 15
    }
    for elem in player.inventory:
        money += cost[elem]
    change_value_in_list(username_text.get_value(), money)


def read_csv():
    info = []
    with open('tops.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for index, row in enumerate(reader):
            info.append(row)
    info.sort(key=lambda x: x[1])
    return sorted(info, key=lambda x: int(x[1]), reverse=True)


def level_menu():
    global top_data
    global level, table, rows_in_table
    for elem in rows_in_table:
        table.remove_row(elem)
    rows_in_table = []
    for row in top_data:
        i = table.add_row(row, cell_align=pygame_menu.locals.ALIGN_CENTER)
        rows_in_table.append(i)
    mainmenu._open(level)


def check_name():
    global root_to_play
    cur = username_text.get_value()
    if cur:
        if len(cur) >= 4:
            for s in cur:
                if s in "&$%@#*:;":
                    root_to_play = False
                    return
            root_to_play = True
            return
    root_to_play = False
    return


root_to_play = False

top_data = read_csv()
local_name = "username"

learning = pygame_menu.Menu('Обучение', 600, 400,
                            theme=themes.THEME_DARK)
help_ = """Клавиши:
    -Кнопки W/A/S/D чтобы ходить во все стороны
    -Кнопки верх/вниз/влево/вправо чтобы крутить
    головой персонажа(чтобы удобней кидать камни)
    -Кнопка F для бросания камня(камень полетит туда
    куда вы смотрите в данный момент)
    -Кнопка Q чтобы покинуть игру
    -Кнопка TAB для выключения и включения
    фоновой музыки
    -Кнопка C включает/выключает отображение 
    инвенторя
       
Перед тем как играть вам нужно придумать
себе имя и ввести его в окно. Если вы будете
играть под другим именем то все 
выигранные очки уйдут на то имя.
Критерии имени:
    -использовать буквы  и цифры
    -длина больше 3 букв/цифр
    -не использовать пробелы
    -не использовать спец символы &$%@#*:;"""

learning.add.label(help_, font_size=20, label_id="1")

a = learning.get_widgets()
for elem in a:
    elem.set_alignment(pygame_menu.locals.ALIGN_LEFT)



update_loading = pygame.USEREVENT + 0

mainmenu = pygame_menu.Menu('Picker', 600, 400, theme=themes.THEME_ORANGE)
username_text = mainmenu.add.text_input('Name: ', default='username')

# print(name_text.get_value())

mainmenu.add.button('Игра', start_the_game)
mainmenu.add.button('Топ игроков', level_menu)
mainmenu.add.button('Обучение', learning)

level = pygame_menu.Menu('Top player money', 600, 400,
                         theme=themes.THEME_BLUE)
table = level.add.table(table_id='my_table', font_size=25)
table.default_cell_padding = 15
table.default_row_background_color = 'white'
table.add_row(['Имя игрока', 'кол-во кредитов'],
              cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)
rows_in_table = []
for row in top_data:
    i = table.add_row(row, cell_align=pygame_menu.locals.ALIGN_CENTER)
    rows_in_table.append(i)

arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10, 15))

pygame.mixer.music.load(r"data\sounds\menu_theme.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)

music_on = True
if __name__ == "__main__":
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                update_csv()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    if music_on:
                        music_on = False
                    else:
                        music_on = True

                    if not music_on:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

        if local_name != username_text.get_value():
            local_name = username_text.get_value()
            check_name()

        if mainmenu.is_enabled():
            mainmenu.update(events)
            mainmenu.draw(surface)
            if (mainmenu.get_current().get_selected_widget()):
                arrow.draw(surface,
                           mainmenu.get_current().get_selected_widget())

        pygame.display.update()
