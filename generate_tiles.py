from PIL import Image, ImageDraw
import os

TILE_SIZE = 32

def create_tile():
    return Image.new('RGB', (TILE_SIZE, TILE_SIZE), (0, 0, 0))

def set_pixel(img, x, y, color):
    if 0 <= x < TILE_SIZE and 0 <= y < TILE_SIZE:
        img.putpixel((x, y), color)

def draw_rect(img, x, y, w, h, color):
    for i in range(x, x + w):
        for j in range(y, y + h):
            set_pixel(img, i, j, color)

def draw_tile(name, draw_fn):
    os.makedirs('tiles', exist_ok=True)
    img = create_tile()
    draw_fn(img)
    img.save(f'tiles/{name}.png')
    print(f'Generated: {name}.png')

def grass(img):
    GREEN1 = (76, 176, 80)
    GREEN2 = (68, 156, 72)
    GREEN3 = (92, 188, 96)
    DARK = (52, 128, 56)

    draw_rect(img, 0, 0, 32, 32, GREEN2)
    for y in range(0, 32, 4):
        for x in range(0, 32, 4):
            if (x + y) % 8 == 0:
                set_pixel(img, x, y, GREEN1)
                set_pixel(img, x + 1, y, GREEN3)
                set_pixel(img, x, y + 1, GREEN1)
            else:
                set_pixel(img, x, y, DARK)
                set_pixel(img, x + 1, y, GREEN2)
                set_pixel(img, x, y + 1, DARK)

def stone_road(img):
    GRAY1 = (160, 160, 160)
    GRAY2 = (140, 140, 144)
    GRAY3 = (180, 180, 180)
    DARK = (100, 100, 100)

    draw_rect(img, 0, 0, 32, 32, GRAY2)
    for y in range(0, 32, 8):
        for x in range(0, 32, 8):
            draw_rect(img, x + 1, y + 1, 6, 6, GRAY1)
            set_pixel(img, x, y, DARK)
            set_pixel(img, x + 7, y, DARK)
            set_pixel(img, x, y + 7, DARK)
            set_pixel(img, x + 7, y + 7, DARK)
            set_pixel(img, x + 3, y + 3, GRAY3)

def asphalt_road(img):
    BLACK = (80, 80, 80)
    GRAY = (100, 100, 100)
    LINE = (220, 220, 220)

    draw_rect(img, 0, 0, 32, 32, BLACK)
    for y in range(0, 32, 2):
        for x in range(0, 32, 2):
            if (x + y) % 4 == 0:
                set_pixel(img, x, y, GRAY)
    draw_rect(img, 14, 0, 4, 32, LINE)
    for y in range(0, 32, 8):
        draw_rect(img, 14, y + 2, 4, 4, BLACK)

def cave(img):
    DARK = (40, 32, 24)
    BROWN = (80, 60, 48)
    GRAY = (100, 96, 88)

    draw_rect(img, 0, 0, 32, 32, DARK)
    for y in range(0, 32, 4):
        for x in range(0, 32, 4):
            if (x + y) % 8 == 0:
                draw_rect(img, x, y, 3, 3, BROWN)
            else:
                draw_rect(img, x + 1, y + 1, 2, 2, GRAY)
    draw_rect(img, 0, 0, 32, 2, (20, 16, 12))
    draw_rect(img, 0, 0, 2, 32, (20, 16, 12))

def active_volcano(img):
    RED = (220, 40, 40)
    ORANGE = (240, 160, 40)
    YELLOW = (255, 240, 80)
    DARK_RED = (160, 32, 32)
    BROWN = (100, 68, 48)
    GRAY = (120, 116, 108)

    draw_rect(img, 0, 0, 32, 32, GRAY)
    draw_rect(img, 8, 12, 16, 20, BROWN)
    draw_rect(img, 10, 8, 12, 4, DARK_RED)
    draw_rect(img, 12, 4, 8, 4, DARK_RED)
    for y in range(0, 8):
        for x in range(8, 24):
            if abs(x - 16) < (8 - y) / 2:
                if y < 2:
                    set_pixel(img, x, y + 10, RED)
                elif y < 5:
                    set_pixel(img, x, y + 10, ORANGE)
                else:
                    set_pixel(img, x, y + 10, YELLOW)
    set_pixel(img, 14, 12, YELLOW)
    set_pixel(img, 18, 12, YELLOW)
    set_pixel(img, 16, 10, (255, 200, 100))

def barren_mountain(img):
    BROWN = (108, 84, 72)
    DARK = (72, 56, 48)
    GRAY = (140, 136, 128)
    SNOW = (240, 240, 248)

    draw_rect(img, 0, 0, 32, 32, GRAY)
    for y in range(8, 32, 4):
        draw_rect(img, 4, y, 24, 3, BROWN)
        for x in range(4, 28, 4):
            if (x + y) % 8 == 0:
                set_pixel(img, x, y, DARK)
    draw_rect(img, 10, 4, 12, 8, (180, 180, 184))
    for x in range(12, 20):
        for y in range(4, 8):
            if abs(x - 16) < (8 - y):
                set_pixel(img, x, y, SNOW)

def forest(img):
    GREEN1 = (32, 96, 32)
    GREEN2 = (24, 72, 24)
    BROWN = (120, 84, 48)
    DARK = (16, 48, 16)

    draw_rect(img, 0, 0, 32, 32, GREEN2)
    for i in range(4):
        x = 4 + i * 7
        draw_rect(img, x + 2, 20, 3, 12, BROWN)
        draw_rect(img, x, 10, 7, 10, GREEN1)
        draw_rect(img, x + 1, 6, 5, 4, GREEN1)
        set_pixel(img, x + 3, 4, DARK)
    for y in range(26, 32):
        for x in range(0, 32, 2):
            set_pixel(img, x, y, GREEN2)
            set_pixel(img, x + 1, y, DARK)

def village(img):
    WALL = (220, 180, 140)
    ROOF = (180, 80, 60)
    DOOR = (100, 60, 32)
    WIN = (160, 200, 240)
    BROWN = (140, 100, 72)

    draw_rect(img, 0, 0, 32, 32, (140, 180, 120))
    draw_rect(img, 4, 12, 24, 18, WALL)
    draw_rect(img, 4, 8, 24, 6, ROOF)
    draw_rect(img, 2, 6, 28, 4, BROWN)
    draw_rect(img, 13, 20, 6, 10, DOOR)
    draw_rect(img, 6, 16, 5, 5, WIN)
    draw_rect(img, 21, 16, 5, 5, WIN)
    set_pixel(img, 0, 28, (100, 140, 80))
    set_pixel(img, 31, 28, (100, 140, 80))

def fence(img):
    BROWN = (160, 120, 72)
    DARK = (120, 88, 48)

    draw_rect(img, 0, 0, 32, 32, (100, 160, 100))
    for i in range(4):
        x = 2 + i * 8
        draw_rect(img, x, 10, 2, 18, BROWN)
        draw_rect(img, x, 8, 2, 4, DARK)
    draw_rect(img, 0, 12, 32, 3, BROWN)
    draw_rect(img, 0, 20, 32, 3, BROWN)

def well(img):
    STONE = (160, 160, 160)
    DARK = (100, 100, 100)
    WATER = (48, 96, 192)

    draw_rect(img, 0, 0, 32, 32, (100, 160, 100))
    draw_rect(img, 8, 12, 16, 16, STONE)
    draw_rect(img, 8, 12, 16, 3, DARK)
    draw_rect(img, 8, 25, 16, 3, DARK)
    draw_rect(img, 10, 15, 12, 10, WATER)
    draw_rect(img, 12, 4, 8, 8, DARK)
    draw_rect(img, 14, 6, 4, 2, BROWN if False else STONE)

def calm_river(img):
    BLUE1 = (48, 120, 200)
    BLUE2 = (64, 136, 216)
    LIGHT = (80, 160, 232)

    draw_rect(img, 0, 0, 32, 32, BLUE1)
    for y in range(0, 32, 4):
        for x in range(0, 32, 8):
            draw_rect(img, x + (y % 16) // 4, y, 4, 2, LIGHT)
    for y in range(0, 32, 6):
        for x in range(0, 32, 6):
            set_pixel(img, x, y, BLUE2)

def shallow_water(img):
    BLUE1 = (72, 144, 216)
    BLUE2 = (56, 128, 200)
    LIGHT = (104, 176, 240)

    draw_rect(img, 0, 0, 32, 32, BLUE1)
    for y in range(0, 32, 4):
        for x in range(0, 32, 4):
            if (x + y) % 8 == 0:
                set_pixel(img, x, y, LIGHT)
            else:
                set_pixel(img, x, y, BLUE2)
    for y in range(2, 32, 6):
        draw_rect(img, 0, y, 8, 1, LIGHT)
        draw_rect(img, 16, y, 8, 1, LIGHT)

def deep_water(img):
    BLUE1 = (24, 72, 160)
    BLUE2 = (32, 88, 176)
    DARK = (16, 48, 128)

    draw_rect(img, 0, 0, 32, 32, BLUE1)
    for y in range(0, 32, 8):
        for x in range(0, 32, 8):
            draw_rect(img, x + 2, y + 2, 4, 4, BLUE2)
    for y in range(0, 32, 4):
        for x in range(0, 32, 2):
            if (x + y) % 8 == 0:
                set_pixel(img, x, y, DARK)

def wheat_field(img):
    YELLOW1 = (220, 200, 80)
    YELLOW2 = (200, 176, 48)
    GOLD = (240, 216, 100)
    GREEN = (100, 140, 48)

    draw_rect(img, 0, 0, 32, 32, GREEN)
    draw_rect(img, 0, 28, 32, 4, (80, 112, 40))
    for i in range(8):
        x = 2 + i * 4
        draw_rect(img, x, 10, 2, 18, YELLOW2)
        draw_rect(img, x, 6, 2, 6, GOLD)
        set_pixel(img, x, 4, GOLD)
        set_pixel(img, x + 1, 5, GOLD)

def rice_field(img):
    GREEN1 = (80, 140, 64)
    GREEN2 = (96, 160, 80)
    LIGHT = (112, 168, 96)
    WATER = (72, 136, 192)

    draw_rect(img, 0, 0, 32, 32, WATER)
    for y in range(0, 32, 4):
        for x in range(0, 32, 4):
            if (x + y) % 8 == 0:
                draw_rect(img, x, y, 2, 3, GREEN1)
                set_pixel(img, x + 1, y - 1, LIGHT)
            else:
                set_pixel(img, x, y, GREEN2)
    draw_rect(img, 0, 0, 32, 2, WATER)
    draw_rect(img, 0, 30, 32, 2, WATER)

def vegetable_field(img):
    SOIL = (120, 84, 48)
    GREEN1 = (48, 128, 48)
    GREEN2 = (64, 144, 64)
    RED = (220, 48, 48)

    draw_rect(img, 0, 0, 32, 32, SOIL)
    for y in range(0, 32, 8):
        for x in range(0, 32, 8):
            draw_rect(img, x + 1, y + 1, 6, 6, (100, 68, 32))
    for y in range(0, 32, 4):
        for x in range(0, 32, 8):
            draw_rect(img, x + 2, y, 4, 3, GREEN1)
            set_pixel(img, x + 3, y - 1, GREEN2)
    for i in range(4):
        x = 4 + i * 8
        set_pixel(img, x, 20, RED)
        set_pixel(img, x + 2, 12, RED)

def farm_path(img):
    BROWN = (160, 128, 80)
    DARK = (120, 96, 60)
    GREEN = (80, 140, 64)

    draw_rect(img, 0, 0, 32, 32, GREEN)
    draw_rect(img, 12, 0, 8, 32, BROWN)
    for y in range(0, 32, 4):
        for x in range(12, 20, 2):
            set_pixel(img, x, y, DARK)
            set_pixel(img, x + 1, y + 1, DARK)

def flowers(img):
    GREEN = (48, 136, 48)
    PINK = (248, 168, 192)
    RED = (220, 80, 80)
    YELLOW = (248, 224, 80)
    PURPLE = (184, 120, 200)
    WHITE = (248, 248, 248)

    draw_rect(img, 0, 0, 32, 32, GREEN)
    for y in range(0, 32, 8):
        for x in range(0, 32, 8):
            set_pixel(img, x + 2, y + 2, PINK)
            set_pixel(img, x + 4, y + 3, RED)
            set_pixel(img, x + 3, y + 1, YELLOW)
            set_pixel(img, x + 1, y + 4, PURPLE)
            set_pixel(img, x + 5, y + 5, WHITE)
    for y in range(4, 32, 8):
        for x in range(4, 32, 8):
            set_pixel(img, x, y, GREEN)
            set_pixel(img, x + 1, y, GREEN)

def desert(img):
    SAND1 = (224, 192, 120)
    SAND2 = (200, 168, 96)
    DARK = (168, 136, 64)

    draw_rect(img, 0, 0, 32, 32, SAND1)
    for y in range(0, 32, 4):
        for x in range(0, 32, 4):
            if (x + y) % 8 == 0:
                set_pixel(img, x, y, SAND2)
            else:
                set_pixel(img, x, y, DARK)
    for y in range(16, 32, 8):
        for x in range(0, 32, 12):
            draw_rect(img, x, y, 8, 2, SAND2)

def snow_field(img):
    WHITE = (248, 248, 252)
    LIGHT = (232, 240, 248)
    ICE = (200, 216, 232)
    DARK = (184, 200, 224)

    draw_rect(img, 0, 0, 32, 32, WHITE)
    for y in range(0, 32, 4):
        for x in range(0, 32, 4):
            if (x + y) % 8 == 0:
                set_pixel(img, x, y, LIGHT)
            else:
                set_pixel(img, x, y, ICE)
    draw_rect(img, 0, 28, 32, 4, DARK)
    draw_rect(img, 8, 16, 4, 2, ICE)
    draw_rect(img, 20, 8, 4, 2, ICE)

def beach(img):
    SAND = (224, 192, 120)
    WET = (180, 152, 96)
    WATER = (72, 144, 200)
    LIGHT = (240, 216, 160)

    draw_rect(img, 0, 0, 32, 32, SAND)
    draw_rect(img, 0, 24, 32, 8, WET)
    draw_rect(img, 0, 28, 32, 4, WATER)
    for y in range(0, 24, 4):
        for x in range(0, 32, 4):
            if (x + y) % 8 == 0:
                set_pixel(img, x, y, LIGHT)
    for y in range(24, 28, 2):
        for x in range(0, 32, 6):
            set_pixel(img, x, y, (160, 128, 80))

def town(img):
    WALL = (200, 180, 160)
    ROOF = (140, 100, 80)
    DARK = (80, 64, 48)
    WINDOW = (64, 128, 192)
    DOOR = (120, 80, 48)

    draw_rect(img, 0, 0, 32, 32, (140, 160, 180))
    draw_rect(img, 2, 10, 28, 20, WALL)
    draw_rect(img, 0, 6, 32, 6, ROOF)
    draw_rect(img, 0, 4, 32, 3, DARK)
    draw_rect(img, 6, 18, 6, 12, DOOR)
    draw_rect(img, 20, 16, 5, 5, WINDOW)
    draw_rect(img, 8, 4, 4, 3, DARK)
    draw_rect(img, 18, 4, 4, 3, DARK)

def ruins(img):
    GRAY = (140, 136, 128)
    DARK = (100, 96, 88)
    BROWN = (120, 84, 48)
    GREEN = (80, 120, 64)

    draw_rect(img, 0, 0, 32, 32, (160, 160, 152))
    draw_rect(img, 2, 16, 8, 14, GRAY)
    draw_rect(img, 12, 20, 10, 10, GRAY)
    draw_rect(img, 24, 14, 6, 16, GRAY)
    draw_rect(img, 0, 28, 32, 4, DARK)
    draw_rect(img, 4, 20, 4, 4, BROWN)
    for y in range(24, 28, 2):
        for x in range(0, 32, 8):
            set_pixel(img, x, y, GREEN)

def trap(img):
    RED = (200, 48, 48)
    DARK = (120, 32, 32)
    BROWN = (100, 68, 48)
    METAL = (160, 160, 168)

    draw_rect(img, 0, 0, 32, 32, (100, 160, 100))
    draw_rect(img, 4, 12, 24, 16, BROWN)
    draw_rect(img, 6, 14, 20, 12, (80, 48, 32))
    for i in range(3):
        x = 8 + i * 7
        draw_rect(img, x, 16, 4, 8, METAL)
        draw_rect(img, x + 1, 14, 2, 2, DARK)
    draw_rect(img, 2, 28, 28, 2, DARK)
    draw_rect(img, 14, 8, 4, 4, RED)

def mechanism(img):
    GRAY = (140, 140, 144)
    DARK = (80, 80, 84)
    RED = (220, 48, 48)
    YELLOW = (240, 200, 64)
    GREEN = (48, 176, 80)

    draw_rect(img, 0, 0, 32, 32, (120, 120, 128))
    draw_rect(img, 4, 4, 24, 24, GRAY)
    draw_rect(img, 6, 6, 20, 20, DARK)
    draw_rect(img, 8, 8, 6, 6, RED)
    draw_rect(img, 18, 8, 6, 6, YELLOW)
    draw_rect(img, 8, 18, 6, 6, GREEN)
    draw_rect(img, 18, 18, 6, 6, (64, 64, 200))
    draw_rect(img, 12, 12, 8, 8, GRAY)
    set_pixel(img, 15, 15, (200, 200, 200))

tiles = [
    ('grass', grass),
    ('stone_road', stone_road),
    ('asphalt_road', asphalt_road),
    ('cave', cave),
    ('active_volcano', active_volcano),
    ('barren_mountain', barren_mountain),
    ('forest', forest),
    ('village', village),
    ('fence', fence),
    ('well', well),
    ('calm_river', calm_river),
    ('shallow_water', shallow_water),
    ('deep_water', deep_water),
    ('wheat_field', wheat_field),
    ('rice_field', rice_field),
    ('vegetable_field', vegetable_field),
    ('farm_path', farm_path),
    ('flowers', flowers),
    ('desert', desert),
    ('snow_field', snow_field),
    ('beach', beach),
    ('town', town),
    ('ruins', ruins),
    ('trap', trap),
    ('mechanism', mechanism),
]

for name, draw_fn in tiles:
    draw_tile(name, draw_fn)