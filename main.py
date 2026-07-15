import pygame
import sys
import os
import json
import asyncio

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("大明王朝 - 朱元璋的崛起")

clock = pygame.time.Clock()

CHINESE_FONT = None
font_paths = [
    "fonts/STHeiti Light.ttc",
    "fonts/PingFang.ttc",
    "fonts/Arial Unicode.ttf",
    "fonts/Hiragino Sans GB.ttc"
]
for font_path in font_paths:
    if os.path.exists(font_path):
        try:
            CHINESE_FONT = pygame.font.Font(font_path, 24)
            break
        except:
            continue

if CHINESE_FONT is None:
    try:
        CHINESE_FONT = pygame.font.SysFont("simhei", 24)
    except:
        try:
            CHINESE_FONT = pygame.font.SysFont("arial", 24)
        except:
            CHINESE_FONT = pygame.font.Font(None, 24)

tile_images = {}
tiles_dir = "tiles"

def load_tiles():
    import glob
    tile_pattern = os.path.join(tiles_dir, "*.png")
    tile_files = glob.glob(tile_pattern)
    
    for filepath in tile_files:
        filename = os.path.basename(filepath)
        tile_name = os.path.splitext(filename)[0]
        try:
            image = pygame.image.load(filepath).convert()
            tile_images[tile_name] = image
        except Exception as e:
            print(f"加载瓦片失败: {filepath}, 错误: {e}")
    
    print(f"已加载 {len(tile_images)} 个瓦片")

map_data = None
tile_map = None
locations = None

def load_map(map_name):
    global map_data, tile_map, locations

    map_file = "maps.json"
    if not os.path.exists(map_file):
        print(f"地图文件 {map_file} 不存在")
        return False

    try:
        with open(map_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if map_name not in data.get('maps', {}):
            print(f"地图 {map_name} 不存在")
            return False

        map_info = data['maps'][map_name]
        map_data = map_info['data']
        locations = map_info.get('locations', {})

        string_mapping = data.get('tile_mapping', {})
        tile_map = {int(k): v for k, v in string_mapping.items()}

        return True
    except Exception as e:
        print(f"加载地图失败: {e}")
        return False

def get_current_location_name(player_x, player_y):
    if not locations:
        return "未知地点"
    
    for loc_id, loc_info in locations.items():
        loc_x = loc_info["x"]
        loc_y = loc_info["y"]
        if abs(loc_x - player_x) <= 2 and abs(loc_y - player_y) <= 2:
            return loc_info["name"]
    
    return "朱元璋崛起之路"

def get_current_location_id(player_x, player_y):
    """获取当前地点的ID"""
    if not locations:
        return None
    
    for loc_id, loc_info in locations.items():
        loc_x = loc_info["x"]
        loc_y = loc_info["y"]
        if abs(loc_x - player_x) <= 2 and abs(loc_y - player_y) <= 2:
            return loc_id
    
    return None

def get_location_min_level(player_x, player_y):
    """获取地点的最低进入等级"""
    if not locations:
        return 1
    
    for loc_id, loc_info in locations.items():
        loc_x = loc_info["x"]
        loc_y = loc_info["y"]
        if abs(loc_x - player_x) <= 2 and abs(loc_y - player_y) <= 2:
            return loc_info.get("min_level", 1)
    
    return 1

load_map('main_map')

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = 48
        self.direction = 'down'
        self.frame = 0
        self.frame_count = 0

        self.speed = 150
        self.target_x = x
        self.target_y = y
        self.is_moving = False
        self.moving_timer = 3

        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 100
        
        self.name = "朱元璋"
        self.base_attack = 10
        self.base_defense = 5
        self.attack = self.base_attack
        self.defense = self.base_defense
        
        # 血量系统
        self.base_hp = 100
        self.max_hp = self.base_hp
        self.hp = self.max_hp
        
        # 体力值系统
        self.base_stamina = 100
        self.max_stamina = self.base_stamina
        self.stamina = self.max_stamina
        self.stamina_regen = 5  # 每秒恢复5点体力
        
        # 食物系统
        self.food = 0
        self.max_food = 20
        
        # 装备系统
        self.equipment = {
            "weapon": "碗",
            "wrist_guard": "",
            "necklace": "",
            "amulet": "",
            "ring": "",
            "helmet": "",
            "gauntlet": "",
            "shoulder": "",
            "belt": "",
            "boots": ""
        }
        
        # 装备数据
        self.equipment_data = self.load_equipment_data()
        
        # 挂机状态
        self.auto_farming = True

        self.load_sprite()
        
    def load_equipment_data(self):
        """加载装备数据"""
        try:
            with open('equipment.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('equipment', [])
        except:
            return []
    
    def calculate_stats(self):
        """计算当前属性"""
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.max_hp = self.base_hp
        self.max_stamina = self.base_stamina
        
        for eq_type, eq_name in self.equipment.items():
            if eq_name:
                for eq in self.equipment_data:
                    if eq['name'] == eq_name:
                        self.attack += eq['attack']
                        self.defense += eq['defense']
                        break
        
        # 如果当前血量超过最大血量，调整血量
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        
        # 如果当前体力超过最大体力，调整体力
        if self.stamina > self.max_stamina:
            self.stamina = self.max_stamina
    
    def consume_stamina(self, amount):
        """消耗体力值"""
        self.stamina = max(0, self.stamina - amount)
        return self.stamina
    
    def add_food(self, amount):
        """添加食物"""
        self.food = min(self.max_food, self.food + amount)
        return self.food
    
    def eat_food(self):
        """吃饭恢复体力"""
        if self.food > 0:
            self.food -= 1
            self.stamina = min(self.max_stamina, self.stamina + 30)
            return True
        return False
    
    def get_equipment_by_type(self, eq_type):
        """根据类型获取装备"""
        return [eq for eq in self.equipment_data if eq['type'] == eq_type]
    
    def toggle_auto_farming(self):
        """切换挂机状态"""
        self.auto_farming = not self.auto_farming
        return self.auto_farming

    def load_sprite(self):
        sprite_path = "player_sprite.png"
        if os.path.exists(sprite_path):
            self.sprite_sheet = pygame.image.load(sprite_path).convert()
        else:
            self.sprite_sheet = None
            self.color = (255, 0, 0)

    def gain_exp(self, amount):
        self.exp += amount
        while self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        if self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level += 1
            self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
            return True
        return False

    def get_level(self):
        return self.level

    def try_move(self, dx, dy):
        if self.is_moving:
            return

        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < len(map_data[0]) and 0 <= new_y < len(map_data):
            tile_type = map_data[new_y][new_x]
            # 允许在道路、草地、农田等可通行地形上移动
            if tile_type not in [26]:  # 只有水域 (26) 不能移动
                self.target_x = new_x
                self.target_y = new_y
                self.is_moving = True
                self.moving_timer = 0

                if dx < 0:
                    self.direction = 'left'
                elif dx > 0:
                    self.direction = 'right'
                elif dy < 0:
                    self.direction = 'up'
                elif dy > 0:
                    self.direction = 'down'
                
                # 移动完成后检查是否进入新地点
                return True
        return False

    def update(self, dt):
        # 挂机获得经验
        if self.auto_farming:
            self.gain_exp(2 * dt)  # 每秒获得2点经验
        
        # 体力值恢复
        if self.stamina < self.max_stamina:
            self.stamina = min(self.max_stamina, self.stamina + self.stamina_regen * dt)
        
        if self.is_moving:
            self.moving_timer += dt
            pixels_to_move = TILE_SIZE
            move_duration = pixels_to_move / self.speed
            progress = min(self.moving_timer / move_duration, 1.0)
            self.x = self.target_x - (self.target_x - self.x) * (1.0 - progress)
            self.y = self.target_y - (self.target_y - self.y) * (1.0 - progress)

            if progress >= 1.0:
                self.x = self.target_x
                self.y = self.target_y
                self.is_moving = False
                return True  # 返回True表示移动完成

            self.frame_count += 1
            if self.frame_count >= 6:
                self.frame = (self.frame + 1) % 3
                self.frame_count = 0
        
        return False

    def draw(self, surface, camera_x, camera_y):
        screen_x = self.x * TILE_SIZE - camera_x
        screen_y = self.y * TILE_SIZE - camera_y - 16

        if self.sprite_sheet:
            direction_idx = {'down': 0, 'left': 1, 'right': 2, 'up': 3}[self.direction]
            sprite_x = direction_idx * TILE_SIZE
            sprite_y = self.frame * 48
            sprite_rect = pygame.Rect(sprite_x, sprite_y, TILE_SIZE, 48)
            sprite = self.sprite_sheet.subsurface(sprite_rect)
            surface.blit(sprite, (screen_x, screen_y))
        else:
            pygame.draw.rect(surface, self.color, (screen_x, screen_y, self.width, self.height))

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, rect):
        return rect.move(-self.camera.x, -self.camera.y)

    def update(self, target):
        x = target.x * TILE_SIZE - self.width // 2 + TILE_SIZE // 2
        y = target.y * TILE_SIZE - self.height // 2 + TILE_SIZE // 2

        x = max(0, min(x, len(map_data[0]) * TILE_SIZE - self.width))
        y = max(0, min(y, len(map_data) * TILE_SIZE - self.height))

        self.camera = pygame.Rect(int(x), int(y), self.width, self.height)

class Game:
    def __init__(self):
        self.player = Player(60, 60)
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.font = CHINESE_FONT
        # 创建小字体
        if CHINESE_FONT:
            try:
                # 尝试使用相同的字体但更小的大小
                self.small_font = pygame.font.Font(None, 14)
            except:
                self.small_font = pygame.font.Font(None, 14)
        else:
            self.small_font = pygame.font.Font(None, 14)
        self.scene_name = get_current_location_name(self.player.x, self.player.y)
        
        # 装备掉落相关
        self.show_equipment_drop = False
        self.dropped_equipment = None
        
        # 装备栏展开/收起状态
        self.equipment_panel_visible = True
        
        # 砍树系统
        self.chopping_tree = False
        self.chopping_progress = 0
        self.chopping_max = 5.0  # 5秒砍树时间
        self.chopping_timer = 0
        self.auto_equip_timer = 0
        self.auto_equip_max = 3.0  # 3秒自动操作时间
        
        # 战斗系统
        self.in_battle = False
        self.battle_progress = 0
        self.battle_max = 5.0  # 5秒战斗时间
        self.battle_timer = 0
        self.current_monster = None
        self.battle_result = None  # "win" or "lose"
        self.battle_result_timer = 0
        self.battle_result_max = 3.0  # 显示结果3秒
        
        # 加载怪物数据
        self.monsters_data = self.load_monsters_data()
        
        # 怪物位置
        self.monsters = self.load_monsters()
        
        # 剧情系统
        self.stories_data = self.load_stories_data()
        self.visited_locations = set()  # 记录已访问的地点
        
        # 加载地图数据
        self.maps_data = self.load_maps_data()
        self.showing_story = False
        self.current_story = None
        self.story_text = ""
        self.story_display_text = ""
        self.story_timer = 0
        self.story_char_delay = 0.05  # 每个字符显示的间隔（秒）
        self.story_char_index = 0
        
        self.load_resources()
        
        # 品质颜色映射
        self.quality_colors = {
            "white": (255, 255, 255),
            "green": (0, 255, 0),
            "blue": (0, 191, 255),
            "purple": (148, 0, 211),
            "orange": (255, 165, 0)
        }
        
        # 品质中文映射
        self.quality_names = {
            "white": "白色",
            "green": "绿色",
            "blue": "蓝色",
            "purple": "紫色",
            "orange": "橙色"
        }
        
        # 村庄和水井恢复冷却计时器
        self.village_timer = 0
        self.well_timer = 0
        self.village_cooldown = 1.0  # 1秒冷却
        self.well_cooldown = 1.0  # 1秒冷却
        
        # 当前状态显示
        self.current_status = ""
        self.status_timer = 0
        
        # 小地图系统
        self.minimap_visible = False
        self.minimap_scale = 2
        self.minimap_width = 400
        self.minimap_height = 400
    
    def toggle_minimap(self):
        """切换小地图显示"""
        self.minimap_visible = not self.minimap_visible
    
    def draw_minimap(self, surface):
        """绘制小地图"""
        if not self.minimap_visible:
            return
        
        minimap_x = (SCREEN_WIDTH - self.minimap_width) // 2
        minimap_y = (SCREEN_HEIGHT - self.minimap_height) // 2
        
        pygame.draw.rect(surface, (0, 0, 0), (minimap_x, minimap_y, self.minimap_width, self.minimap_height))
        pygame.draw.rect(surface, (100, 100, 100), (minimap_x + 2, minimap_y + 2, self.minimap_width - 4, self.minimap_height - 4))
        
        if map_data is None:
            return
        
        map_width = len(map_data[0]) if map_data else 0
        map_height = len(map_data) if map_data else 0
        
        if map_width == 0 or map_height == 0:
            return
        
        scale_x = (self.minimap_width - 4) / map_width
        scale_y = (self.minimap_height - 4) / map_height
        
        for y, row in enumerate(map_data):
            for x, tile_id in enumerate(row):
                tile_name = tile_map.get(tile_id, "grass")
                
                if tile_name in ["path", "path_corner", "path_t", "path_cross", "stone_road", "asphalt_road", "farm_path"]:
                    color = (150, 150, 100)
                elif tile_name in ["water", "water_wave", "water_shore", "calm_river", "shallow_water", "deep_water"]:
                    color = (50, 100, 200)
                elif tile_name in ["mountain", "mountain_peak", "barren_mountain", "active_volcano"]:
                    color = (100, 100, 100)
                elif tile_name in ["tree", "tree2", "tree_large", "forest"]:
                    color = (30, 100, 30)
                elif tile_name in ["house1", "house2", "house3", "town", "castle", "village"]:
                    color = (150, 100, 50)
                elif tile_name in ["farmland", "farmland_green", "wheat_field", "rice_field", "vegetable_field"]:
                    color = (100, 150, 50)
                elif tile_name in ["wolf", "tiger", "lion"]:
                    color = (200, 50, 50)
                else:
                    color = (80, 120, 80)
                
                mx = minimap_x + 2 + x * scale_x
                my = minimap_y + 2 + y * scale_y
                mw = max(1, scale_x)
                mh = max(1, scale_y)
                
                pygame.draw.rect(surface, color, (mx, my, mw, mh))
        
        for loc_id, loc_info in locations.items():
            if "x" in loc_info and "y" in loc_info:
                mx = minimap_x + 2 + loc_info["x"] * scale_x
                my = minimap_y + 2 + loc_info["y"] * scale_y
                pygame.draw.circle(surface, (255, 200, 0), (mx + scale_x/2, my + scale_y/2), 4)
                
                name_text = self.small_font.render(loc_info["name"], True, (255, 255, 255))
                surface.blit(name_text, (mx - 20, my - 25))
        
        player_mx = minimap_x + 2 + self.player.x * scale_x
        player_my = minimap_y + 2 + self.player.y * scale_y
        pygame.draw.circle(surface, (255, 0, 0), (player_mx + scale_x/2, player_my + scale_y/2), 5)
        pygame.draw.circle(surface, (255, 255, 0), (player_mx + scale_x/2, player_my + scale_y/2), 5, 2)
        
        title = self.font.render("世界地图", True, (255, 255, 255))
        title_rect = title.get_rect(center=(minimap_x + self.minimap_width//2, minimap_y - 15))
        surface.blit(title, title_rect)
        
        hint = self.small_font.render("按M键关闭地图", True, (200, 200, 200))
        hint_rect = hint.get_rect(center=(minimap_x + self.minimap_width//2, minimap_y + self.minimap_height + 20))
        surface.blit(hint, hint_rect)
    
    def drop_equipment(self):
        """随机掉落装备"""
        import random
        equipment_list = self.player.equipment_data
        if equipment_list:
            # 获取当前地图等级
            current_location_level = get_location_min_level(int(self.player.x), int(self.player.y))
            
            # 根据地图等级确定可掉落的品质
            if current_location_level <= 1:
                # 钟离县等低级地图，只能掉落绿色及以下品质
                available_equipment = [eq for eq in equipment_list if eq['quality'] in ['white', 'green']]
            elif current_location_level <= 5:
                # 中级地图，可掉落蓝色及以下品质
                available_equipment = [eq for eq in equipment_list if eq['quality'] in ['white', 'green', 'blue']]
            elif current_location_level <= 10:
                # 高级地图，可掉落紫色及以下品质
                available_equipment = [eq for eq in equipment_list if eq['quality'] in ['white', 'green', 'blue', 'purple']]
            else:
                # 最高级地图，可掉落所有品质
                available_equipment = equipment_list
            
            if available_equipment:
                # 随机选择一件装备
                self.dropped_equipment = random.choice(available_equipment)
                self.show_equipment_drop = True
                print(f"掉落装备: {self.dropped_equipment['name']} (品质: {self.dropped_equipment['quality']})")
            else:
                print("当前地图等级无法掉落装备")
    
    def replace_equipment(self):
        """替换装备"""
        if self.dropped_equipment:
            eq_type = self.dropped_equipment['type']
            self.player.equipment[eq_type] = self.dropped_equipment['name']
            # 重新计算属性
            self.player.calculate_stats()
            print(f"已装备: {self.dropped_equipment['name']}")
            self.show_equipment_drop = False
            self.dropped_equipment = None
    
    def draw_equipment_drop(self, surface):
        """绘制装备掉落界面"""
        if not self.dropped_equipment:
            return
        
        # 计算界面位置
        width = 300
        height = 150
        x = (SCREEN_WIDTH - width) // 2
        y = (SCREEN_HEIGHT - height) // 2
        
        # 绘制背景
        pygame.draw.rect(surface, (50, 50, 50, 200), (x, y, width, height), border_radius=10)
        
        # 绘制标题
        title = self.font.render("获得装备", True, WHITE)
        title_rect = title.get_rect(center=(x + width//2, y + 20))
        surface.blit(title, title_rect)
        
        # 绘制装备信息
        eq = self.dropped_equipment
        name_color = self.quality_colors.get(eq['quality'], WHITE)
        name_text = self.font.render(eq['name'], True, name_color)
        name_rect = name_text.get_rect(center=(x + width//2, y + 50))
        surface.blit(name_text, name_rect)
        
        # 绘制部位信息
        slot_text = self.small_font.render(f"部位: {eq.get('slot', '未知')}", True, (200, 200, 200))
        slot_rect = slot_text.get_rect(center=(x + width//2, y + 70))
        surface.blit(slot_text, slot_rect)
        
        # 绘制属性
        attack_text = self.small_font.render(f"攻击: +{eq['attack']}", True, WHITE)
        defense_text = self.small_font.render(f"防御: +{eq['defense']}", True, WHITE)
        quality_name = self.quality_names.get(eq['quality'], eq['quality'])
        quality_text = self.small_font.render(f"品质: {quality_name}", True, name_color)
        
        surface.blit(attack_text, (x + 50, y + 80))
        surface.blit(defense_text, (x + 180, y + 80))
        surface.blit(quality_text, (x + 50, y + 100))
        
        # 绘制操作提示
        hint_text = self.small_font.render("按R替换，按Q丢弃", True, (200, 200, 200))
        hint_rect = hint_text.get_rect(center=(x + width//2, y + 130))
        surface.blit(hint_text, hint_rect)
    
    def update_chopping(self, dt):
        """更新砍树系统"""
        # 检查体力值
        if self.player.stamina <= 0:
            return
        
        # 检查是否在树附近
        player_x, player_y = int(self.player.x), int(self.player.y)
        near_tree = self.is_near_tree(player_x, player_y)
        
        if near_tree:
            if not self.chopping_tree:
                # 开始砍树
                self.chopping_tree = True
                self.chopping_progress = 0
                self.chopping_timer = 0
            else:
                # 砍树进度
                self.chopping_timer += dt
                self.chopping_progress = min(self.chopping_timer / self.chopping_max, 1.0)
                
                if self.chopping_progress >= 1.0:
                    # 砍树完成，掉落装备
                    self.drop_equipment()
                    # 砍树消耗体力
                    self.player.consume_stamina(10)
                    self.chopping_tree = False
                    self.chopping_progress = 0
                    self.chopping_timer = 0
                    self.auto_equip_timer = 0
        else:
            # 不在树附近，停止砍树
            self.chopping_tree = False
            self.chopping_progress = 0
            self.chopping_timer = 0
        
        # 自动装备逻辑
        if self.show_equipment_drop:
            self.auto_equip_timer += dt
            if self.auto_equip_timer >= self.auto_equip_max:
                # 自动判断是否装备
                self.auto_equip()
    
    def update_battle(self, dt):
        """更新战斗系统"""
        # 检查体力值
        if self.player.stamina <= 0:
            return
        
        # 如果正在显示战斗结果
        if self.battle_result is not None:
            self.battle_result_timer += dt
            if self.battle_result_timer >= self.battle_result_max:
                self.battle_result = None
                self.battle_result_timer = 0
            return
        
        # 检查是否在怪物附近
        player_x, player_y = int(self.player.x), int(self.player.y)
        near_monster = self.is_near_monster(player_x, player_y)
        
        if near_monster:
            if not self.in_battle:
                # 开始战斗
                self.in_battle = True
                self.battle_progress = 0
                self.battle_timer = 0
                self.current_monster = near_monster
            else:
                # 战斗进度
                self.battle_timer += dt
                self.battle_progress = min(self.battle_timer / self.battle_max, 1.0)
                
                if self.battle_progress >= 1.0:
                    # 战斗结束，判断胜负
                    self.check_battle_result()
                    # 战斗消耗体力
                    self.player.consume_stamina(15)
        else:
            # 不在怪物附近，停止战斗
            self.in_battle = False
            self.battle_progress = 0
            self.battle_timer = 0
            self.current_monster = None
    
    def is_near_monster(self, x, y):
        """检查是否在怪物附近"""
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if (nx, ny) in self.monsters:
                    return self.monsters[(nx, ny)]
        return None
    
    def check_battle_result(self):
        """判断战斗胜负"""
        if not self.current_monster:
            return
        
        player_atk = self.player.attack
        player_def = self.player.defense
        monster_atk = self.current_monster['attack']
        monster_def = self.current_monster['defense']
        
        # 玩家战力 = 攻击力 + 防御力
        player_power = player_atk + player_def
        monster_power = monster_atk + monster_def
        
        if player_power >= monster_power:
            # 胜利
            self.battle_result = "win"
            exp_reward = self.current_monster['exp_reward']
            self.player.gain_exp(exp_reward)
            print(f"战斗胜利！获得 {exp_reward} 经验")
        else:
            # 失败
            self.battle_result = "lose"
            print(f"战斗失败！攻击力 {player_atk}，防御力 {player_def} 还不够，继续努力！")
        
        self.in_battle = False
        self.battle_progress = 0
        self.battle_timer = 0
        self.battle_result_timer = 0
    
    def update_story(self, dt):
        """更新剧情系统"""
        # 更新剧情文字显示
        if self.showing_story:
            self.story_timer += dt
            if self.story_timer >= self.story_char_delay:
                self.story_timer = 0
                if self.story_char_index < len(self.story_text):
                    self.story_display_text += self.story_text[self.story_char_index]
                    self.story_char_index += 1
    
    def trigger_story(self, location_name):
        """触发剧情"""
        if location_name in self.stories_data:
            story_data = self.stories_data[location_name]
            self.current_story = story_data
            self.story_text = story_data['story']
            self.story_display_text = ""
            self.story_char_index = 0
            self.showing_story = True
            print(f"触发剧情: {story_data['name']} - {story_data['year']}")
    
    def check_new_location(self):
        """检查是否进入新地点"""
        current_location_id = self.get_current_location_id()
        if current_location_id and current_location_id not in self.visited_locations:
            self.visited_locations.add(current_location_id)
            self.trigger_story(current_location_id)
    
    def is_near_tree(self, x, y):
        """检查是否在树附近"""
        # 检查周围8个格子
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(map_data[0]) and 0 <= ny < len(map_data):
                    tile_id = map_data[ny][nx]
                    # 检查是否是树
                    if tile_id == 7 or tile_id == 8:  # tree 和 tree2
                        return True
        return False
    
    def is_near_farm(self, x, y):
        """检查是否在农田附近"""
        # 检查周围8个格子
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(map_data[0]) and 0 <= ny < len(map_data):
                    tile_id = map_data[ny][nx]
                    # 检查是否是农田
                    if tile_id in [14, 15, 16]:  # wheat_field, rice_field, vegetable_field
                        return True
        return False
    
    def plant_crop(self):
        """种菜"""
        if self.player.stamina >= 20:
            self.player.consume_stamina(20)
            # 增加食物
            self.player.add_food(3)
            return True
        return False
    
    def is_near_village(self, x, y):
        """检查是否在村庄附近"""
        # 检查周围8个格子
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(map_data[0]) and 0 <= ny < len(map_data):
                    tile_id = map_data[ny][nx]
                    # 检查是否是村庄
                    if tile_id == 34:  # village
                        return True
        return False
    
    def is_near_well(self, x, y):
        """检查是否在水井附近"""
        # 检查周围8个格子
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(map_data[0]) and 0 <= ny < len(map_data):
                    tile_id = map_data[ny][nx]
                    # 检查是否是水井
                    if tile_id == 12 or tile_id == 13:  # well 和 well2
                        return True
        return False
    
    def draw_chopping_progress(self, surface):
        """绘制砍树进度条"""
        width = 200
        height = 20
        x = (SCREEN_WIDTH - width) // 2
        y = SCREEN_HEIGHT - 100
        
        # 绘制背景
        pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height), border_radius=5)
        
        # 绘制进度
        progress_width = int(width * self.chopping_progress)
        pygame.draw.rect(surface, (0, 255, 0), (x, y, progress_width, height), border_radius=5)
        
        # 绘制文字
        text = self.font.render("砍树中...", True, WHITE)
        text_rect = text.get_rect(center=(x + width//2, y - 20))
        surface.blit(text, text_rect)
    
    def draw_battle_progress(self, surface):
        """绘制战斗进度条"""
        width = 200
        height = 20
        x = (SCREEN_WIDTH - width) // 2
        y = SCREEN_HEIGHT - 150
        
        # 绘制背景
        pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height), border_radius=5)
        
        # 绘制进度
        progress_width = int(width * self.battle_progress)
        pygame.draw.rect(surface, (255, 0, 0), (x, y, progress_width, height), border_radius=5)
        
        # 绘制文字
        if self.current_monster:
            monster_name = self.current_monster['name']
            text = self.font.render(f"战斗: {monster_name}", True, WHITE)
        else:
            text = self.font.render("战斗中...", True, WHITE)
        text_rect = text.get_rect(center=(x + width//2, y - 20))
        surface.blit(text, text_rect)
    
    def draw_battle_result(self, surface):
        """绘制战斗结果"""
        width = 300
        height = 150
        x = (SCREEN_WIDTH - width) // 2
        y = (SCREEN_HEIGHT - height) // 2
        
        # 绘制背景
        pygame.draw.rect(surface, (50, 50, 50, 220), (x, y, width, height), border_radius=10)
        
        if self.battle_result == "win":
            # 胜利
            title = self.font.render("战斗胜利!", True, (0, 255, 0))
            title_rect = title.get_rect(center=(x + width//2, y + 30))
            surface.blit(title, title_rect)
            
            if self.current_monster:
                exp_text = self.small_font.render(f"获得 {self.current_monster['exp_reward']} 经验", True, (255, 255, 0))
                exp_rect = exp_text.get_rect(center=(x + width//2, y + 70))
                surface.blit(exp_text, exp_rect)
        else:
            # 失败
            title = self.font.render("战斗失败!", True, (255, 0, 0))
            title_rect = title.get_rect(center=(x + width//2, y + 30))
            surface.blit(title, title_rect)
            
            hint_text = self.small_font.render("攻击力和防御力还不够", True, (200, 200, 200))
            hint_rect = hint_text.get_rect(center=(x + width//2, y + 60))
            surface.blit(hint_text, hint_rect)
            
            atk_text = self.small_font.render(f"当前攻击力: {self.player.attack}", True, WHITE)
            def_text = self.small_font.render(f"当前防御力: {self.player.defense}", True, WHITE)
            surface.blit(atk_text, (x + 50, y + 85))
            surface.blit(def_text, (x + 50, y + 105))
    
    def draw_monsters(self, surface):
        """绘制怪物"""
        for (mx, my), monster in self.monsters.items():
            screen_x = mx * TILE_SIZE - self.camera.camera.x
            screen_y = my * TILE_SIZE - self.camera.camera.y
            
            sprite_name = monster['sprite']
            if sprite_name in self.monster_sprites:
                surface.blit(self.monster_sprites[sprite_name], (screen_x, screen_y))
    
    def draw_story(self, surface):
        """绘制剧情界面"""
        if not self.current_story:
            return
        
        # 绘制半透明背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        
        # 绘制剧情框
        story_width = 600
        story_height = 300
        story_x = (SCREEN_WIDTH - story_width) // 2
        story_y = (SCREEN_HEIGHT - story_height) // 2
        
        pygame.draw.rect(surface, (50, 50, 50, 220), (story_x, story_y, story_width, story_height), border_radius=10)
        pygame.draw.rect(surface, (200, 200, 200), (story_x, story_y, story_width, story_height), 2, border_radius=10)
        
        # 绘制标题（地点名和年份）
        if self.current_story:
            title_text = self.font.render(f"{self.current_story['name']} - {self.current_story['year']}", True, (255, 215, 0))
            title_rect = title_text.get_rect(center=(story_x + story_width//2, story_y + 30))
            surface.blit(title_text, title_rect)
        
        # 绘制剧情文字（逐字显示）
        # 将文字分成多行显示
        lines = []
        current_line = ""
        max_line_width = story_width - 40
        
        for char in self.story_display_text:
            test_line = current_line + char
            test_width = self.font.size(test_line)[0]
            if test_width <= max_line_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = char
        
        if current_line:
            lines.append(current_line)
        
        # 绘制每一行
        line_height = 30
        start_y = story_y + 60
        for i, line in enumerate(lines):
            if i >= 8:  # 最多显示8行
                break
            text = self.font.render(line, True, WHITE)
            text_rect = text.get_rect(topleft=(story_x + 20, start_y + i * line_height))
            surface.blit(text, text_rect)
        
        # 绘制提示文字
        hint_text = self.small_font.render("按回车键继续", True, (200, 200, 200))
        hint_rect = hint_text.get_rect(center=(story_x + story_width//2, story_y + story_height - 30))
        surface.blit(hint_text, hint_rect)
    
    def auto_equip(self):
        """自动装备逻辑"""
        if not self.dropped_equipment:
            return
        
        eq = self.dropped_equipment
        eq_type = eq['type']
        current_eq_name = self.player.equipment.get(eq_type, "")
        
        # 品质优先级
        quality_order = {"white": 1, "green": 2, "blue": 3, "purple": 4, "orange": 5}
        
        if current_eq_name:
            # 找到当前装备
            current_eq = None
            for item in self.player.equipment_data:
                if item['name'] == current_eq_name:
                    current_eq = item
                    break
            
            if current_eq:
                current_quality = quality_order.get(current_eq['quality'], 0)
                new_quality = quality_order.get(eq['quality'], 0)
                
                if new_quality > current_quality:
                    # 新装备品质更好，自动装备
                    self.player.equipment[eq_type] = eq['name']
                    self.player.calculate_stats()
                    print(f"自动装备: {eq['name']}")
                else:
                    # 新装备品质更差，自动丢弃
                    print(f"自动丢弃: {eq['name']}")
        else:
            # 没有当前装备，自动装备
            self.player.equipment[eq_type] = eq['name']
            self.player.calculate_stats()
            print(f"自动装备: {eq['name']}")
        
        # 关闭装备掉落界面
        self.show_equipment_drop = False
        self.dropped_equipment = None

    def load_resources(self):
        load_tiles()
        self.load_monster_sprites()
    
    def load_monsters_data(self):
        """加载怪物数据"""
        try:
            with open('monsters.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('monsters', [])
        except:
            return []
    
    def load_monsters(self):
        """加载怪物位置"""
        monsters = {}
        for y, row in enumerate(map_data):
            for x, tile_id in enumerate(row):
                if tile_id == 100:  # wolf
                    monsters[(x, y)] = self.get_monster_by_id(1)
                elif tile_id == 101:  # tiger
                    monsters[(x, y)] = self.get_monster_by_id(2)
                elif tile_id == 102:  # lion
                    monsters[(x, y)] = self.get_monster_by_id(3)
        return monsters
    
    def load_stories_data(self):
        """加载剧情数据"""
        try:
            with open('stories.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('stories', {})
        except:
            return {}
    
    def load_maps_data(self):
        """加载地图数据"""
        try:
            with open('maps.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"maps": {}}
    
    def get_current_location_id(self):
        """获取当前地点的ID"""
        x, y = int(self.player.x), int(self.player.y)
        locations = self.maps_data['maps']['main_map']['locations']
        
        # 检查是否在某个地点的范围内
        for loc_id, loc_data in locations.items():
            loc_x, loc_y = loc_data['x'], loc_data['y']
            if abs(x - loc_x) <= 2 and abs(y - loc_y) <= 2:
                return loc_id
        
        return None
    
    def get_monster_by_id(self, monster_id):
        """根据ID获取怪物数据"""
        for monster in self.monsters_data:
            if monster['id'] == monster_id:
                return monster.copy()
        return None
    
    def load_monster_sprites(self):
        """加载怪物精灵"""
        self.monster_sprites = {}
        for monster in self.monsters_data:
            sprite_name = monster['sprite']
            sprite_path = f"tiles/{sprite_name}.png"
            if os.path.exists(sprite_path):
                img = pygame.image.load(sprite_path).convert_alpha()
                self.monster_sprites[sprite_name] = img
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_RETURN and self.showing_story:
                    # 按回车键结束剧情
                    self.showing_story = False
                    self.current_story = None
                    self.story_text = ""
                    self.story_display_text = ""
                    self.story_char_index = 0
                elif event.key == pygame.K_a:
                    # 按A键切换挂机状态
                    is_farming = self.player.toggle_auto_farming()
                    print(f"挂机状态: {'开启' if is_farming else '关闭'}")
                elif event.key == pygame.K_r and self.show_equipment_drop:
                    # 按R键替换装备
                    self.replace_equipment()
                elif event.key == pygame.K_q and self.show_equipment_drop:
                    # 按Q键丢弃装备
                    self.show_equipment_drop = False
                    self.dropped_equipment = None
                elif event.key == pygame.K_e:
                    # 按E键切换装备栏展开/收起
                    self.equipment_panel_visible = not self.equipment_panel_visible
                elif event.key == pygame.K_s:
                    # 按S键保存游戏
                    self.save_game()
                    print("游戏已保存！")
                elif event.key == pygame.K_l:
                    # 按L键加载游戏
                    success = self.load_game()
                    if success:
                        print("游戏已加载！")
                    else:
                        print("没有找到存档文件！")
                elif event.key == pygame.K_m:
                    # 按M键打开/关闭小地图
                    self.toggle_minimap()
                    print(f"小地图: {'打开' if self.minimap_visible else '关闭'}")
                elif event.key == pygame.K_p:
                    # 按P键种菜
                    if self.is_near_farm(int(self.player.x), int(self.player.y)):
                        success = self.plant_crop()
                        if success:
                            print("种菜成功，获得了3个食物！")
                        else:
                            print("体力不足，无法种菜！")
                    else:
                        print("附近没有农田，无法种菜！")
                elif event.key == pygame.K_f:
                    # 按F键吃饭
                    success = self.player.eat_food()
                    if success:
                        print("吃饭成功，恢复了30点体力！")
                    else:
                        print("没有食物了！")

        # 如果正在显示剧情，不允许移动
        if self.showing_story:
            return True

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1
        elif keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1

        if dx != 0 or dy != 0:
            if not self.player.auto_farming:
                # 计算目标位置
                target_x = int(self.player.x) + dx
                target_y = int(self.player.y) + dy
                
                # 检查当前位置的等级
                current_min_level = get_location_min_level(int(self.player.x), int(self.player.y))
                
                # 检查目标位置的等级要求
                target_min_level = get_location_min_level(target_x, target_y)
                
                # 如果玩家当前在高等级区域，允许移动（即使目标位置也是高等级）
                if current_min_level > self.player.level:
                    self.player.try_move(dx, dy)
                    self.scene_name = get_current_location_name(int(self.player.x), int(self.player.y))
                elif target_min_level > self.player.level:
                    print(f"等级不足！需要等级 {target_min_level} 才能进入该区域")
                else:
                    self.player.try_move(dx, dy)
                    self.scene_name = get_current_location_name(int(self.player.x), int(self.player.y))

        return True

    def draw_map(self, surface):
        if map_data is None:
            return
        
        map_height = len(map_data)
        if map_height == 0:
            return
        
        map_width = len(map_data[0]) if map_data[0] else 0
        
        visible_tiles_x = SCREEN_WIDTH // TILE_SIZE + 2
        visible_tiles_y = SCREEN_HEIGHT // TILE_SIZE + 2
        
        start_x = max(0, int(self.camera.camera.x // TILE_SIZE) - 1)
        start_y = max(0, int(self.camera.camera.y // TILE_SIZE) - 1)
        end_x = min(map_width, start_x + visible_tiles_x)
        end_y = min(map_height, start_y + visible_tiles_y)
        
        for y in range(start_y, end_y):
            if y >= len(map_data):
                continue
            row = map_data[y]
            for x in range(start_x, end_x):
                if x >= len(row):
                    continue
                tile_id = row[x]
                tile_name = tile_map.get(tile_id, "grass")
                
                if tile_name in tile_images:
                    tile_image = tile_images[tile_name]
                else:
                    if "grass" in tile_images:
                        tile_image = tile_images["grass"]
                    else:
                        tile_image = None
                
                if tile_image:
                    screen_x = x * TILE_SIZE - self.camera.camera.x
                    screen_y = y * TILE_SIZE - self.camera.camera.y
                    surface.blit(tile_image, (screen_x, screen_y))

    def draw_ui(self, surface):
        self.scene_name = get_current_location_name(int(self.player.x), int(self.player.y))
        current_min_level = get_location_min_level(int(self.player.x), int(self.player.y))
        
        # 绘制场景名称
        text = self.font.render(self.scene_name, True, WHITE)
        text_rect = text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        pygame.draw.rect(surface, BLACK, (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10))
        surface.blit(text, text_rect)

        if current_min_level > 1:
            level_text = self.font.render(f"进入等级: {current_min_level}", True, WHITE)
            level_rect = level_text.get_rect(topright=(SCREEN_WIDTH - 20, 50))
            pygame.draw.rect(surface, BLACK, (level_rect.x - 10, level_rect.y - 5, level_rect.width + 20, level_rect.height + 10))
            surface.blit(level_text, level_rect)

        # 绘制精致的角色属性界面
        player = self.player
        gui_width = 220
        gui_height = 240
        gui_x = 20
        gui_y = 20
        
        # 绘制半透明圆角矩形背景
        pygame.draw.rect(surface, (50, 50, 50, 180), (gui_x, gui_y, gui_width, gui_height), border_radius=10)
        
        # 绘制角色信息
        name_text = self.font.render(player.name, True, (255, 215, 0))  # 金色
        level_text = self.font.render(f"等级: {player.level}", True, WHITE)
        exp_text = self.font.render(f"经验: {int(player.exp)}/{player.exp_to_next_level}", True, WHITE)

        attack_text = self.font.render(f"攻击: {player.attack}", True, WHITE)
        defense_text = self.font.render(f"防御: {player.defense}", True, WHITE)
        
        # 绘制血量条
        hp_ratio = min(player.hp / player.max_hp, 1.0)
        hp_bar_width = gui_width - 40
        hp_bar_height = 12
        hp_bar_x = gui_x + 20
        hp_bar_y = gui_y + 95
        
        # 血量条背景
        pygame.draw.rect(surface, (80, 80, 80), (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), border_radius=3)
        # 血量条
        if hp_ratio > 0.5:
            hp_color = (0, 255, 0)
        elif hp_ratio > 0.25:
            hp_color = (255, 255, 0)
        else:
            hp_color = (255, 0, 0)
        pygame.draw.rect(surface, hp_color, (hp_bar_x, hp_bar_y, hp_bar_width * hp_ratio, hp_bar_height), border_radius=3)
        
        # 绘制血量文字
        hp_text = self.font.render(f"HP: {int(player.hp)}/{player.max_hp}", True, WHITE)
        surface.blit(hp_text, (hp_bar_x, hp_bar_y - 18))
        
        # 绘制体力值条
        stamina_ratio = min(player.stamina / player.max_stamina, 1.0)
        stamina_bar_width = gui_width - 40
        stamina_bar_height = 12
        stamina_bar_x = gui_x + 20
        stamina_bar_y = hp_bar_y + 30
        
        # 体力值条背景
        pygame.draw.rect(surface, (80, 80, 80), (stamina_bar_x, stamina_bar_y, stamina_bar_width, stamina_bar_height), border_radius=3)
        # 体力值条
        if stamina_ratio > 0.5:
            stamina_color = (0, 128, 255)  # 蓝色
        elif stamina_ratio > 0.25:
            stamina_color = (0, 255, 255)  # 青色
        else:
            stamina_color = (255, 165, 0)  # 橙色
        pygame.draw.rect(surface, stamina_color, (stamina_bar_x, stamina_bar_y, stamina_bar_width * stamina_ratio, stamina_bar_height), border_radius=3)
        
        # 绘制体力值文字
        stamina_text = self.font.render(f"体力: {int(player.stamina)}/{player.max_stamina}", True, WHITE)
        surface.blit(stamina_text, (stamina_bar_x, stamina_bar_y - 18))
        
        # 绘制食物数量
        food_text = self.font.render(f"食物: {player.food}/{player.max_food}", True, WHITE)
        surface.blit(food_text, (gui_x + 20, stamina_bar_y + 30))
        
        # 绘制当前状态（正在吃饭/正在喝水）
        if self.current_status:
            status_text = self.font.render(self.current_status, True, (0, 255, 0))
            surface.blit(status_text, (gui_x + 20, stamina_bar_y + 55))
        
        # 绘制经验条
        exp_ratio = min(player.exp / player.exp_to_next_level, 1.0)
        exp_bar_width = gui_width - 40
        exp_bar_height = 10
        exp_bar_x = gui_x + 20
        exp_bar_y = gui_y + 125
        
        pygame.draw.rect(surface, (80, 80, 80), (exp_bar_x, exp_bar_y, exp_bar_width, exp_bar_height), border_radius=3)
        pygame.draw.rect(surface, (0, 191, 255), (exp_bar_x, exp_bar_y, exp_bar_width * exp_ratio, exp_bar_height), border_radius=3)
        
        # 绘制文本
        surface.blit(name_text, (gui_x + 20, gui_y + 20))
        surface.blit(level_text, (gui_x + 20, gui_y + 45))
        surface.blit(exp_text, (gui_x + 20, gui_y + 65))
        surface.blit(attack_text, (gui_x + 20, gui_y + 145))
        surface.blit(defense_text, (gui_x + 20, gui_y + 170))
        
        # 绘制装备面板
        if self.equipment_panel_visible:
            equipment_gui_y = gui_y + gui_height + 10
            equipment_gui_width = 250
            equipment_gui_height = 220
            
            # 绘制装备面板背景
            pygame.draw.rect(surface, (100, 150, 100, 180), (gui_x, equipment_gui_y, equipment_gui_width, equipment_gui_height), border_radius=10)
            
            # 绘制标题
            title_text = self.font.render("装备", True, WHITE)
            title_rect = title_text.get_rect(center=(gui_x + equipment_gui_width//2, equipment_gui_y + 20))
            surface.blit(title_text, title_rect)
            
            # 装备分类 - 采用参考图片的布局
            equipment_layout = [
                # 左侧攻具
                [("weapon", "武器"), ("wrist_guard", "护腕"), ("necklace", "项链"), ("amulet", "护符"), ("ring", "戒指")],
                # 右侧防具
                [("helmet", "帽子"), ("gauntlet", "护手"), ("shoulder", "护肩"), ("belt", "腰带"), ("boots", "靴子")]
            ]
            
            # 装备属性加成
            equipment_stats = {
                "碗": "攻击+1"
            }
            
            # 从装备数据中获取属性
            for eq in self.player.equipment_data:
                stats = []
                if eq['attack'] > 0:
                    stats.append(f"攻击+{eq['attack']}")
                if eq['defense'] > 0:
                    stats.append(f"防御+{eq['defense']}")
                if stats:
                    equipment_stats[eq['name']] = " ".join(stats)
            
            # 绘制装备格子
            for col, category in enumerate(equipment_layout):
                for row, (eq_key, eq_name) in enumerate(category):
                    slot_x = gui_x + 30 + col * 100
                    slot_y = equipment_gui_y + 50 + row * 30
                    slot_width = 80
                    slot_height = 25
                    
                    # 绘制格子
                    pygame.draw.rect(surface, (50, 80, 50), (slot_x, slot_y, slot_width, slot_height), border_radius=3)
                    
                    # 绘制装备名称和属性
                    eq_value = self.player.equipment[eq_key]
                    if eq_value:
                        # 显示装备名称
                        eq_text = self.small_font.render(eq_value, True, WHITE)
                        text_rect = eq_text.get_rect(topleft=(slot_x + 5, slot_y + 2))
                        surface.blit(eq_text, text_rect)
                        
                        # 显示装备属性
                        if eq_value in equipment_stats:
                            stat_text = self.small_font.render(equipment_stats[eq_value], True, (255, 255, 0))  # 黄色
                            stat_rect = stat_text.get_rect(topleft=(slot_x + 5, slot_y + 12))
                            surface.blit(stat_text, stat_rect)
                    else:
                        # 显示装备部位名称
                        eq_text = self.small_font.render(eq_name, True, (150, 150, 150))
                        text_rect = eq_text.get_rect(center=(slot_x + slot_width//2, slot_y + slot_height//2))
                        surface.blit(eq_text, text_rect)

    async def run(self):
        running = True
        last_time = pygame.time.get_ticks()
        while running:
            current_time = pygame.time.get_ticks()
            dt = (current_time - last_time) / 1000.0
            last_time = current_time

            running = self.handle_events()
            move_completed = self.player.update(dt)
            
            # 检查体力值是否为0
            if self.player.stamina <= 0:
                # 体力值为0，传送回钟离县
                self.player.x = 60
                self.player.y = 60
                self.player.target_x = 60
                self.player.target_y = 60
                self.player.stamina = 50  # 恢复一些体力
                print("体力耗尽，已传送回钟离县！")
            
            # 检查是否在村庄附近（吃饭）
            if self.is_near_village(int(self.player.x), int(self.player.y)):
                self.village_timer += dt
                if self.village_timer >= self.village_cooldown:
                    self.village_timer = 0
                    if self.player.stamina < self.player.max_stamina:
                        old_stamina = self.player.stamina
                        self.player.stamina = min(self.player.max_stamina, self.player.stamina + 5)
                        if self.player.stamina > old_stamina:
                            self.current_status = "正在吃饭"
                            self.status_timer = 0
            
            # 检查是否在水井附近（喝水）
            if self.is_near_well(int(self.player.x), int(self.player.y)):
                self.well_timer += dt
                if self.well_timer >= self.well_cooldown:
                    self.well_timer = 0
                    if self.player.stamina < self.player.max_stamina:
                        old_stamina = self.player.stamina
                        self.player.stamina = min(self.player.max_stamina, self.player.stamina + 1)
                        if self.player.stamina > old_stamina:
                            self.current_status = "正在喝水"
                            self.status_timer = 0
            
            # 更新状态显示计时器
            self.status_timer += dt
            if self.status_timer >= 1.0:
                self.current_status = ""
            
            # 砍树系统更新
            self.update_chopping(dt)
            
            # 战斗系统更新
            self.update_battle(dt)
            
            # 剧情系统更新
            if move_completed:
                self.check_new_location()
            self.update_story(dt)
            
            self.camera.update(self.player)

            screen.fill(BLACK)
            self.draw_map(screen)
            self.draw_monsters(screen)
            self.player.draw(screen, self.camera.camera.x, self.camera.camera.y)
            self.draw_ui(screen)
            
            # 绘制剧情界面
            if self.showing_story:
                self.draw_story(screen)
            
            # 绘制砍树进度条
            if self.chopping_tree:
                self.draw_chopping_progress(screen)
            
            # 绘制战斗进度条
            if self.in_battle:
                self.draw_battle_progress(screen)
            
            # 绘制战斗结果
            if self.battle_result is not None:
                self.draw_battle_result(screen)
            
            # 绘制装备掉落界面
            if self.show_equipment_drop:
                self.draw_equipment_drop(screen)
            
            # 绘制小地图
            self.draw_minimap(screen)

            pygame.display.flip()
            clock.tick(FPS)
            
            await asyncio.sleep(0)

if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run())