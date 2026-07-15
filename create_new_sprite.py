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
LIGHT_SKIN = (255, 220, 180)
GRAY = (128, 128, 128)

# 创建精灵表
sprite_sheet = Image.new('RGB', (GRID_WIDTH * SPRITE_WIDTH, GRID_HEIGHT * SPRITE_HEIGHT), BLACK)
draw = ImageDraw.Draw(sprite_sheet)

def draw_character_front(draw, x, y):
    """绘制角色正面（向下）"""
    base_x = x * SPRITE_WIDTH
    base_y = y * SPRITE_HEIGHT
    
    # 帽子（黑色）
    draw.rectangle([base_x + 10, base_y + 4, base_x + 22, base_y + 10], fill=BLACK)
    draw.rectangle([base_x + 8, base_y + 8, base_x + 24, base_y + 12], fill=BLACK)
    
    # 脸部
    draw.rectangle([base_x + 10, base_y + 12, base_x + 22, base_y + 20], fill=SKIN)
    
    # 眼睛（黑色）
    draw.ellipse([base_x + 12, base_y + 14, base_x + 14, base_y + 16], fill=BLACK)
    draw.ellipse([base_x + 18, base_y + 14, base_x + 20, base_y + 16], fill=BLACK)
    
    # 嘴巴和胡子
    draw.rectangle([base_x + 14, base_y + 18, base_x + 18, base_y + 19], fill=BLACK)
    draw.rectangle([base_x + 12, base_y + 20, base_x + 20, base_y + 21], fill=BLACK)
    
    # 衣服（黄色）
    draw.rectangle([base_x + 8, base_y + 20, base_x + 24, base_y + 40], fill=YELLOW)
    
    # 腰带（绿色）
    draw.rectangle([base_x + 10, base_y + 28, base_x + 22, base_y + 32], fill=GREEN)
    
    # 手
    draw.rectangle([base_x + 6, base_y + 24, base_x + 10, base_y + 34], fill=SKIN)
    draw.rectangle([base_x + 22, base_y + 24, base_x + 26, base_y + 34], fill=SKIN)
    
    # 鞋子（黑色）
    draw.rectangle([base_x + 10, base_y + 40, base_x + 16, base_y + 46], fill=BLACK)
    draw.rectangle([base_x + 16, base_y + 40, base_x + 22, base_y + 46], fill=BLACK)
    
    # 徽章（白色）
    draw.ellipse([base_x + 14, base_y + 24, base_x + 18, base_y + 28], fill=WHITE)

def draw_character_left(draw, x, y):
    """绘制角色左侧"""
    base_x = x * SPRITE_WIDTH
    base_y = y * SPRITE_HEIGHT
    
    # 帽子
    draw.rectangle([base_x + 12, base_y + 4, base_x + 22, base_y + 10], fill=BLACK)
    draw.rectangle([base_x + 10, base_y + 8, base_x + 24, base_y + 12], fill=BLACK)
    
    # 脸部
    draw.rectangle([base_x + 12, base_y + 12, base_x + 22, base_y + 20], fill=SKIN)
    
    # 眼睛
    draw.ellipse([base_x + 14, base_y + 14, base_x + 16, base_y + 16], fill=BLACK)
    
    # 嘴巴和胡子
    draw.rectangle([base_x + 16, base_y + 18, base_x + 19, base_y + 19], fill=BLACK)
    draw.rectangle([base_x + 15, base_y + 20, base_x + 19, base_y + 21], fill=BLACK)
    
    # 衣服
    draw.rectangle([base_x + 10, base_y + 20, base_x + 24, base_y + 40], fill=YELLOW)
    
    # 腰带
    draw.rectangle([base_x + 12, base_y + 28, base_x + 22, base_y + 32], fill=GREEN)
    
    # 手
    draw.rectangle([base_x + 8, base_y + 24, base_x + 12, base_y + 34], fill=SKIN)
    
    # 鞋子
    draw.rectangle([base_x + 12, base_y + 40, base_x + 22, base_y + 46], fill=BLACK)
    
    # 徽章
    draw.ellipse([base_x + 16, base_y + 24, base_x + 20, base_y + 28], fill=WHITE)

def draw_character_right(draw, x, y):
    """绘制角色右侧"""
    base_x = x * SPRITE_WIDTH
    base_y = y * SPRITE_HEIGHT
    
    # 帽子
    draw.rectangle([base_x + 10, base_y + 4, base_x + 20, base_y + 10], fill=BLACK)
    draw.rectangle([base_x + 8, base_y + 8, base_x + 22, base_y + 12], fill=BLACK)
    
    # 脸部
    draw.rectangle([base_x + 10, base_y + 12, base_x + 20, base_y + 20], fill=SKIN)
    
    # 眼睛
    draw.ellipse([base_x + 16, base_y + 14, base_x + 18, base_y + 16], fill=BLACK)
    
    # 嘴巴和胡子
    draw.rectangle([base_x + 13, base_y + 18, base_x + 16, base_y + 19], fill=BLACK)
    draw.rectangle([base_x + 13, base_y + 20, base_x + 17, base_y + 21], fill=BLACK)
    
    # 衣服
    draw.rectangle([base_x + 8, base_y + 20, base_x + 22, base_y + 40], fill=YELLOW)
    
    # 腰带
    draw.rectangle([base_x + 10, base_y + 28, base_x + 20, base_y + 32], fill=GREEN)
    
    # 手
    draw.rectangle([base_x + 18, base_y + 24, base_x + 22, base_y + 34], fill=SKIN)
    
    # 鞋子
    draw.rectangle([base_x + 10, base_y + 40, base_x + 20, base_y + 46], fill=BLACK)
    
    # 徽章
    draw.ellipse([base_x + 12, base_y + 24, base_x + 16, base_y + 28], fill=WHITE)

def draw_character_back(draw, x, y):
    """绘制角色背面（向上）"""
    base_x = x * SPRITE_WIDTH
    base_y = y * SPRITE_HEIGHT
    
    # 帽子
    draw.rectangle([base_x + 10, base_y + 4, base_x + 22, base_y + 10], fill=BLACK)
    draw.rectangle([base_x + 8, base_y + 8, base_x + 24, base_y + 12], fill=BLACK)
    
    # 头部
    draw.rectangle([base_x + 10, base_y + 12, base_x + 22, base_y + 20], fill=SKIN)
    
    # 后脑勺
    draw.rectangle([base_x + 14, base_y + 14, base_x + 18, base_y + 18], fill=GRAY)
    
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

# 绘制四个方向的精灵
# 方向顺序：下、左、右、上
for frame in range(GRID_HEIGHT):
    draw_character_front(draw, 0, frame)   # 向下
    draw_character_left(draw, 1, frame)    # 向左
    draw_character_right(draw, 2, frame)   # 向右
    draw_character_back(draw, 3, frame)    # 向上

# 保存精灵表
sprite_sheet.save('player_sprite.png')
print('精灵表已生成: player_sprite.png')
print(f'精灵表尺寸: {sprite_sheet.size}')
print(f'单个精灵尺寸: {SPRITE_WIDTH}x{SPRITE_HEIGHT}')
print('方向顺序: 下、左、右、上')
print('每个方向包含3个行走帧')