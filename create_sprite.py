from PIL import Image, ImageDraw

# 精灵表设置
SPRITE_WIDTH = 32
SPRITE_HEIGHT = 48
GRID_WIDTH = 4  # 4个方向
GRID_HEIGHT = 3  # 3个帧

# 颜色定义
BLACK = (0, 0, 0)
YELLOW = (255, 216, 0)
DARK_YELLOW = (200, 160, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
SKIN = (255, 200, 160)

# 创建精灵表
sprite_sheet = Image.new('RGB', (GRID_WIDTH * SPRITE_WIDTH, GRID_HEIGHT * SPRITE_HEIGHT), BLACK)
draw = ImageDraw.Draw(sprite_sheet)

def draw_character(draw, x, y, direction):
    """绘制角色在指定位置和方向"""
    base_x = x * SPRITE_WIDTH
    base_y = y * SPRITE_HEIGHT
    
    # 头部
    # 帽子
    draw.rectangle([base_x + 10, base_y + 4, base_x + 22, base_y + 10], fill=BLACK)
    draw.rectangle([base_x + 8, base_y + 8, base_x + 24, base_y + 12], fill=BLACK)
    
    # 脸
    draw.rectangle([base_x + 10, base_y + 12, base_x + 22, base_y + 20], fill=SKIN)
    
    # 眼睛
    draw.ellipse([base_x + 12, base_y + 14, base_x + 14, base_y + 16], fill=BLACK)
    draw.ellipse([base_x + 18, base_y + 14, base_x + 20, base_y + 16], fill=BLACK)
    
    # 嘴巴和胡子
    draw.rectangle([base_x + 14, base_y + 18, base_x + 18, base_y + 19], fill=BLACK)
    draw.rectangle([base_x + 12, base_y + 20, base_x + 20, base_y + 21], fill=BLACK)
    
    # 身体
    # 衣服
    draw.rectangle([base_x + 8, base_y + 20, base_x + 24, base_y + 40], fill=YELLOW)
    
    # 腰带
    draw.rectangle([base_x + 10, base_y + 28, base_x + 22, base_y + 32], fill=GREEN)
    
    # 手
    draw.rectangle([base_x + 6, base_y + 24, base_x + 10, base_y + 34], fill=SKIN)
    draw.rectangle([base_x + 22, base_y + 24, base_x + 26, base_y + 34], fill=SKIN)
    
    # 鞋子
    draw.rectangle([base_x + 10, base_y + 40, base_x + 16, base_y + 46], fill=BLACK)
    draw.rectangle([base_x + 16, base_y + 40, base_x + 22, base_y + 46], fill=BLACK)
    
    # 徽章
    draw.ellipse([base_x + 14, base_y + 24, base_x + 18, base_y + 28], fill=WHITE)

# 绘制四个方向的精灵
# 方向顺序：下、左、右、上
directions = ['down', 'left', 'right', 'up']

for dir_idx, direction in enumerate(directions):
    for frame in range(GRID_HEIGHT):
        draw_character(draw, dir_idx, frame, direction)

# 保存精灵表
sprite_sheet.save('player_sprite.png')
print('精灵表已生成: player_sprite.png')

# 查看文件信息
print(f'精灵表尺寸: {sprite_sheet.size}')
print(f'单个精灵尺寸: {SPRITE_WIDTH}x{SPRITE_HEIGHT}')
print('方向顺序: 下、左、右、上')
print('每个方向包含3个行走帧')