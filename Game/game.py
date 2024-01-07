import pygame
import sys
import os

pygame.init()
pygame.key.set_repeat(10, 100)
size = WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((size), pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 60


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


def start_screen():
    intro_text = ["Меню", "Управление: W A S D",
                  "Чтобы начать нажмите: Пробел",
                  "Правила игры:"
                  ]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    font1 = pygame.font.Font("data/Ustroke-Regular.ttf", 50)
    text_coord = 50
    horrortextstart = font1.render('НЕ ДАЙ СЕБЯ ПОЙМАТЬ', 1, ('red'))
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 100
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    screen.blit(horrortextstart, (100, 700))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if event.key == pygame.K_SPACE:
                    return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'normgrass': load_image('Grass100.png'),
    'rockgrass': load_image('RG100.png'),
    'rockgrasszab': load_image('RGw100.png'),
    'wall': load_image('Wall100.png'),
    'wallh': load_image('WallH100.png'),
    'Wfloor': load_image('Wfloor100.png'),
    'WallHwP1': load_image('WallHwP1-100.png'),
    'WallHwP2': load_image('WallHwP2-100.png'),
    'RG90': load_image('RG100R90.png'),
    'RG180': load_image('RG100R180.png'),
    'src': load_image('src.png')
}
player_image = load_image('mainch.png')

tile_width = tile_height = 100


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        if tile_type == 'rockgrasszab':
            self.add(wall_group)
        if tile_type == 'RG90':
            self.add(wall_group)
        if tile_type == 'wall':
            self.add(wall_group)
        if tile_type == 'wallh':
            self.add(wall_group)
        if tile_type == 'WallHwP1':
            self.add(wall_group)
        if tile_type == 'WallHwP2':
            self.add(wall_group)
        if tile_type == 'RG180':
            self.add(wall_group)
        if tile_type == 'src':
            self.add(wall_group)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, dx, dy):
        self.rect = self.rect.move(dx, dy)
        if pygame.sprite.spritecollideany(self, wall_group):
            self.rect = self.rect.move(-dx, -dy)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('rockgrass', x, y)
            elif level[y][x] == '/':
                Tile('rockgrasszab', x, y)
            elif level[y][x] == ',':
                Tile('normgrass', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '+':
                Tile('wallh', x, y)
            elif level[y][x] == '=':
                Tile('Wfloor', x, y)
            elif level[y][x] == '-':
                Tile('WallHwP1', x, y)
            elif level[y][x] == '_':
                Tile('WallHwP2', x, y)
            elif level[y][x] == ')':
                Tile('RG90', x, y)
            elif level[y][x] == '(':
                Tile('RG180', x, y)
            elif level[y][x] == ']':
                Tile('src', x, y)
            elif level[y][x] == '@':
                Tile('normgrass', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


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
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


if __name__ == '__main__':
    start_screen()
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    # основной персонаж
    player, level_x, level_y = generate_level(load_level('2.txt'))
    camera = Camera()

    ten = pygame.sprite.Sprite(player_group)
    ten.image = load_image('t.png')
    ten.rect = ten.image.get_rect()
    ten.rect.x = 0
    ten.rect.y = 0

    fps = 60
    running = True
    STEP = 10  # 10 tile_width
    keys = pygame.key.get_pressed()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if event.key == pygame.K_a:
                    dx, dy = -STEP, 0
                if event.key == pygame.K_a and (event.mod & pygame.KMOD_SHIFT):
                    dx, dy = -STEP - 15, 0
                if event.key == pygame.K_d:
                    dx, dy = STEP, 0
                if event.key == pygame.K_d and (event.mod & pygame.KMOD_SHIFT):
                    dx, dy = STEP + 15, 0
                if event.key == pygame.K_w:
                    dx, dy = 0, -STEP
                if event.key == pygame.K_w and (event.mod & pygame.KMOD_SHIFT):
                    dx, dy = 0, -STEP - 15
                if event.key == pygame.K_s:
                    dx, dy = 0, STEP
                if event.key == pygame.K_s and (event.mod & pygame.KMOD_SHIFT):
                    dx, dy = 0, STEP + 15
                player.update(dx, dy)

        screen.fill('black')
        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
