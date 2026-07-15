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

def house1(img):
    WALL = (220, 180, 140)
    ROOF = (180, 80, 60)
    DOOR = (100, 60, 32)
    WINDOW = (160, 200, 240)
    BROWN = (140, 100, 72)

    draw_rect(img, 0, 0, 32, 32, (140, 180, 120))
    draw_rect(img, 6, 12, 20, 18, WALL)
    draw_rect(img, 6, 8, 20, 6, ROOF)
    draw_rect(img, 4, 6, 24, 4, BROWN)
    draw_rect(img, 14, 20, 4, 10, DOOR)
    draw_rect(img, 8, 16, 4, 4, WINDOW)
    draw_rect(img, 20, 16, 4, 4, WINDOW)

def house2(img):
    WALL = (200, 160, 120)
    ROOF = (160, 160, 160)
    DOOR = (120, 80, 48)
    WINDOW = (180, 220, 255)
    BROWN = (120, 80, 48)

    draw_rect(img, 0, 0, 32, 32, (140, 180, 120))
    draw_rect(img, 8, 10, 16, 20, WALL)
    draw_rect(img, 4, 4, 24, 8, ROOF)
    draw_rect(img, 12, 18, 8, 12, DOOR)
    draw_rect(img, 10, 12, 5, 5, WINDOW)
    draw_rect(img, 17, 12, 5, 5, WINDOW)

def wall(img):
    STONE = (160, 160, 160)
    DARK = (100, 100, 100)
    BROWN = (120, 84, 48)

    draw_rect(img, 0, 0, 32, 32, (140, 180, 120))
    draw_rect(img, 0, 12, 32, 16, STONE)
    draw_rect(img, 0, 8, 32, 4, DARK)
    draw_rect(img, 0, 26, 32, 2, DARK)
    for x in range(0, 32, 8):
        draw_rect(img, x, 14, 4, 12, (140, 140, 140))

def bridge(img):
    WOOD = (160, 120, 72)
    DARK = (120, 88, 48)
    WATER = (48, 120, 200)

    draw_rect(img, 0, 0, 32, 32, WATER)
    draw_rect(img, 0, 12, 32, 8, WOOD)
    for y in range(12, 20):
        for x in range(0, 32, 4):
            set_pixel(img, x, y, DARK)
    draw_rect(img, 0, 10, 32, 2, DARK)
    draw_rect(img, 0, 20, 32, 2, DARK)

def tree(img):
    GREEN = (32, 96, 32)
    DARK = (24, 72, 24)
    BROWN = (120, 84, 48)

    draw_rect(img, 0, 0, 32, 32, (140, 180, 120))
    draw_rect(img, 14, 16, 4, 10, BROWN)
    draw_rect(img, 10, 8, 12, 10, GREEN)
    draw_rect(img, 12, 4, 8, 6, GREEN)
    set_pixel(img, 15, 2, DARK)
    set_pixel(img, 17, 3, DARK)

def tree2(img):
    GREEN = (48, 128, 48)
    DARK = (32, 96, 32)
    BROWN = (140, 100, 64)

    draw_rect(img, 0, 0, 32, 32, (140, 180, 120))
    draw_rect(img, 13, 18, 6, 8, BROWN)
    draw_rect(img, 8, 10, 16, 10, GREEN)
    draw_rect(img, 12, 6, 8, 6, GREEN)
    set_pixel(img, 14, 4, DARK)
    set_pixel(img, 18, 4, DARK)

def well2(img):
    STONE = (160, 160, 160)
    DARK = (100, 100, 100)
    WATER = (48, 96, 192)
    WOOD = (160, 120, 72)

    draw_rect(img, 0, 0, 32, 32, (140, 180, 120))
    draw_rect(img, 10, 14, 12, 14, STONE)
    draw_rect(img, 10, 14, 12, 2, DARK)
    draw_rect(img, 10, 26, 12, 2, DARK)
    draw_rect(img, 12, 16, 8, 8, WATER)
    draw_rect(img, 8, 8, 16, 8, WOOD)
    draw_rect(img, 14, 10, 4, 4, (180, 140, 96))

def fence2(img):
    WOOD = (160, 120, 72)
    DARK = (120, 88, 48)

    draw_rect(img, 0, 0, 32, 32, (140, 180, 120))
    for i in range(5):
        x = i * 6
        draw_rect(img, x, 12, 2, 12, WOOD)
        draw_rect(img, x, 10, 2, 4, DARK)
    draw_rect(img, 0, 14, 32, 2, WOOD)
    draw_rect(img, 0, 20, 32, 2, WOOD)

tiles = [
    ('house1', house1),
    ('house2', house2),
    ('wall', wall),
    ('bridge', bridge),
    ('tree', tree),
    ('tree2', tree2),
    ('well2', well2),
    ('fence2', fence2),
]

for name, draw_fn in tiles:
    draw_tile(name, draw_fn)