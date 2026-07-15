#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import json
import os

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
TILE_SIZE = 32

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("高级地图编辑器")
clock = pygame.time.Clock()

try:
    font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 18)
    big_font = pygame.font.Font(None, 32)
except:
    font = pygame.font.SysFont("SimHei", 24)
    small_font = pygame.font.SysFont("SimHei", 18)
    big_font = pygame.font.SysFont("SimHei", 32)

tiles = {}
tiles_dir = "tiles"
tile_names = []

for filename in os.listdir(tiles_dir):
    if filename.endswith(".png"):
        tile_name = os.path.splitext(filename)[0]
        tile_path = os.path.join(tiles_dir, filename)
        try:
            tiles[tile_name] = pygame.image.load(tile_path).convert()
            tile_names.append(tile_name)
        except:
            print(f"加载瓦片失败: {tile_path}")

def load_maps():
    try:
        with open('maps.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"maps": {}, "tile_mapping": {}}

def save_maps(data):
    with open('maps.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    update_recreate_transitions(data)
    print("地图数据已保存")

def update_recreate_transitions(maps_data):
    all_locations = []
    for map_id, map_info in maps_data.get("maps", {}).items():
        for loc_id, loc_info in map_info.get("locations", {}).items():
            all_locations.append({
                "id": loc_id,
                "name": loc_info["name"],
                "x": loc_info["x"],
                "y": loc_info["y"],
                "map": map_id
            })
    
    transitions_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def load_maps():
    with open('maps.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_maps(data):
    with open('maps.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def recreate_transitions():
    maps_data = load_maps()
    
    locations = []
    for map_id, map_info in maps_data.get("maps", {}).items():
        for loc_id, loc_info in map_info.get("locations", {}).items():
            locations.append({
                "id": loc_id,
                "name": loc_info["name"],
                "x": loc_info["x"],
                "y": loc_info["y"],
                "map": map_id
            })
    
    for map_id, map_info in maps_data.get("maps", {}).items():
        if 'locations' not in map_info:
            map_info['locations'] = {}
        
        if 'exits' not in map_info:
            map_info['exits'] = []
        
        exits = []
        for loc_id, loc_info in map_info['locations'].items():
            for other_loc in locations:
                if other_loc['map'] != map_id or other_loc['id'] != loc_id:
                    dx = other_loc['x'] - loc_info['x']
                    dy = other_loc['y'] - loc_info['y']
                    distance = (dx*dx + dy*dy) ** 0.5
                    if distance < 30:
                        if dx > 0:
                            direction = "东"
                        elif dx < 0:
                            direction = "西"
                        elif dy > 0:
                            direction = "南"
                        else:
                            direction = "北"
                        
                        exits.append({
                            "direction": direction,
                            "from_x": loc_info["x"],
                            "from_y": loc_info["y"],
                            "to_x": other_loc["x"],
                            "to_y": other_loc["y"],
                            "target_map": other_loc["map"],
                            "target_location": other_loc["id"]
                        })
        
        map_info['exits'] = exits
    
    save_maps(maps_data)
    print("连接信息已更新")

if __name__ == "__main__":
    recreate_transitions()
'''
    
    with open('recreate_transitions.py', 'w', encoding='utf-8') as f:
        f.write(transitions_code)
    print("recreate_transitions.py 已更新")

class MapEditor:
    def __init__(self):
        self.maps_data = load_maps()
        self.map_ids = list(self.maps_data.get("maps", {}).keys())
        self.current_map_index = 0
        self.current_map = self.map_ids[0] if self.map_ids else "main_map"
        
        self.selected_tile = 0
        self.scroll_x = 0
        self.scroll_y = 0
        self.edit_mode = "tiles"
        self.dragging = False
        self.last_mouse_pos = (0, 0)
        self.selected_location = None
        self.connection_start = None
        self.connection_end = None
        
        self.target_map_for_connection = None
        self.editing_location_name = False
        self.location_name_input = ""
        
        self._initialize_map_data()
    
    def _initialize_map_data(self):
        if not self.maps_data.get("maps"):
            self.maps_data["maps"] = {}
        
        if self.current_map not in self.maps_data["maps"]:
            self.maps_data["maps"][self.current_map] = {
                "name": "新地图",
                "width": 60,
                "height": 60,
                "data": [[0 for _ in range(60)] for _ in range(60)],
                "locations": {},
                "exits": []
            }
        
        for map_id, map_info in self.maps_data["maps"].items():
            if "exits" not in map_info:
                map_info["exits"] = []
            if "locations" not in map_info:
                map_info["locations"] = {}
            if "width" not in map_info:
                map_info["width"] = 60
            if "height" not in map_info:
                map_info["height"] = 60
        
        if "tile_mapping" not in self.maps_data:
            self.maps_data["tile_mapping"] = {}
            for i, tile_name in enumerate(tile_names):
                self.maps_data["tile_mapping"][str(i)] = tile_name
        
        self.map_info = self.maps_data["maps"][self.current_map]
        self.map_data = self.map_info["data"]
        self.locations = self.map_info.get("locations", {})
        self.exits = self.map_info.get("exits", [])
        self.map_width = self.map_info["width"]
        self.map_height = self.map_info["height"]
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.edit_mode == "tiles":
                            self.handle_tile_click(event.pos)
                        elif self.edit_mode == "connections":
                            self.handle_connection_click(event.pos)
                        elif self.edit_mode == "locations":
                            self.handle_location_click(event.pos)
                        elif self.edit_mode == "map_select":
                            self.handle_map_select_click(event.pos)
                    elif event.button == 3:
                        self.dragging = True
                        self.last_mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        self.dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging:
                        dx, dy = event.pos[0] - self.last_mouse_pos[0], event.pos[1] - self.last_mouse_pos[1]
                        self.scroll_x += dx
                        self.scroll_y += dy
                        self.last_mouse_pos = event.pos
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.edit_mode = "tiles"
                    elif event.key == pygame.K_2:
                        self.edit_mode = "connections"
                    elif event.key == pygame.K_3:
                        self.edit_mode = "locations"
                    elif event.key == pygame.K_4:
                        self.edit_mode = "map_select"
                    elif event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                        save_maps(self.maps_data)
                    elif event.key == pygame.K_UP:
                        self.selected_tile = (self.selected_tile - 1) % len(tile_names)
                    elif event.key == pygame.K_DOWN:
                        self.selected_tile = (self.selected_tile + 1) % len(tile_names)
                    elif event.key == pygame.K_LEFT and self.edit_mode == "map_select":
                        self.current_map_index = (self.current_map_index - 1) % len(self.map_ids)
                        self.current_map = self.map_ids[self.current_map_index]
                        self._initialize_map_data()
                    elif event.key == pygame.K_RIGHT and self.edit_mode == "map_select":
                        self.current_map_index = (self.current_map_index + 1) % len(self.map_ids)
                        self.current_map = self.map_ids[self.current_map_index]
                        self._initialize_map_data()
                    elif event.key == pygame.K_DELETE:
                        if self.edit_mode == "locations" and self.selected_location:
                            del self.locations[self.selected_location]
                            self.selected_location = None
                        elif self.edit_mode == "connections":
                            self.connection_start = None
                            self.connection_end = None
                    elif event.key == pygame.K_n and event.mod & pygame.KMOD_CTRL:
                        self.create_new_map()
                    elif self.editing_location_name:
                        if event.key == pygame.K_RETURN:
                            if self.location_name_input.strip():
                                self.locations[self.selected_location]["name"] = self.location_name_input.strip()
                            self.editing_location_name = False
                            self.location_name_input = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.location_name_input = self.location_name_input[:-1]
                        elif event.unicode:
                            self.location_name_input += event.unicode
            
            screen.fill(GRAY)
            
            self.draw_map()
            self.draw_sidebar()
            self.draw_edit_mode()
            self.draw_info()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
    
    def create_new_map(self):
        new_map_id = f"map_{len(self.map_ids) + 1}"
        self.maps_data["maps"][new_map_id] = {
            "name": f"新地图{len(self.map_ids) + 1}",
            "width": 60,
            "height": 60,
            "data": [[0 for _ in range(60)] for _ in range(60)],
            "locations": {},
            "exits": []
        }
        self.map_ids.append(new_map_id)
        self.current_map_index = len(self.map_ids) - 1
        self.current_map = new_map_id
        self._initialize_map_data()
        print(f"创建新地图: {new_map_id}")
    
    def draw_map(self):
        map_width = self.map_width * TILE_SIZE
        map_height = self.map_height * TILE_SIZE
        
        start_x = max(0, -self.scroll_x // TILE_SIZE)
        start_y = max(0, -self.scroll_y // TILE_SIZE)
        end_x = min(self.map_width, (SCREEN_WIDTH - 320 - self.scroll_x) // TILE_SIZE + 1)
        end_y = min(self.map_height, (SCREEN_HEIGHT - self.scroll_y) // TILE_SIZE + 1)
        
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile_id = self.map_data[y][x]
                tile_name = self.maps_data["tile_mapping"].get(str(tile_id), "grass")
                tile_image = tiles.get(tile_name, None)
                if tile_image:
                    screen.blit(tile_image, (
                        x * TILE_SIZE + self.scroll_x,
                        y * TILE_SIZE + self.scroll_y
                    ))
        
        for y in range(start_y, end_y + 1):
            pygame.draw.line(
                screen, LIGHT_GRAY,
                (self.scroll_x, y * TILE_SIZE + self.scroll_y),
                (self.scroll_x + (end_x - start_x) * TILE_SIZE, y * TILE_SIZE + self.scroll_y)
            )
        for x in range(start_x, end_x + 1):
            pygame.draw.line(
                screen, LIGHT_GRAY,
                (x * TILE_SIZE + self.scroll_x, self.scroll_y),
                (x * TILE_SIZE + self.scroll_x, self.scroll_y + (end_y - start_y) * TILE_SIZE)
            )
        
        for loc_id, loc_info in self.locations.items():
            x = loc_info["x"] * TILE_SIZE + self.scroll_x
            y = loc_info["y"] * TILE_SIZE + self.scroll_y
            color = YELLOW if loc_id == self.selected_location else RED
            pygame.draw.circle(screen, color, (x + TILE_SIZE//2, y + TILE_SIZE//2), 8)
            pygame.draw.circle(screen, BLACK, (x + TILE_SIZE//2, y + TILE_SIZE//2), 8, 1)
            
            text = small_font.render(loc_info["name"], True, BLACK)
            bg_rect = text.get_rect(topleft=(x - 30, y - 35))
            bg_rect.width += 10
            pygame.draw.rect(screen, WHITE, bg_rect)
            screen.blit(text, (x - 30, y - 35))
        
        for exit_info in self.exits:
            if "from_x" in exit_info and "from_y" in exit_info:
                x1 = exit_info["from_x"] * TILE_SIZE + self.scroll_x + TILE_SIZE//2
                y1 = exit_info["from_y"] * TILE_SIZE + self.scroll_y + TILE_SIZE//2
                
                if "to_x" in exit_info and "to_y" in exit_info:
                    x2 = exit_info["to_x"] * TILE_SIZE + self.scroll_x + TILE_SIZE//2
                    y2 = exit_info["to_y"] * TILE_SIZE + self.scroll_y + TILE_SIZE//2
                    pygame.draw.line(screen, CYAN, (x1, y1), (x2, y2), 2)
                
                pygame.draw.circle(screen, BLUE, (x1, y1), 5)
                direction = exit_info.get("direction", "")
                text = small_font.render(direction, True, BLUE)
                screen.blit(text, (x1 + 10, y1 - 10))
        
        if self.connection_start:
            start_x = self.connection_start[0] * TILE_SIZE + self.scroll_x + TILE_SIZE//2
            start_y = self.connection_start[1] * TILE_SIZE + self.scroll_y + TILE_SIZE//2
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x < SCREEN_WIDTH - 320:
                pygame.draw.line(screen, PURPLE, (start_x, start_y), (mouse_x, mouse_y), 2)
                pygame.draw.circle(screen, PURPLE, (mouse_x, mouse_y), 4)
    
    def draw_sidebar(self):
        sidebar_x = SCREEN_WIDTH - 300
        sidebar_y = 20
        sidebar_width = 280
        sidebar_height = SCREEN_HEIGHT - 40
        
        pygame.draw.rect(screen, LIGHT_GRAY, (sidebar_x, sidebar_y, sidebar_width, sidebar_height))
        
        if self.edit_mode == "tiles":
            self.draw_tile_selector(sidebar_x, sidebar_y, sidebar_width, sidebar_height)
        elif self.edit_mode == "connections":
            self.draw_connection_editor(sidebar_x, sidebar_y, sidebar_width, sidebar_height)
        elif self.edit_mode == "locations":
            self.draw_location_editor(sidebar_x, sidebar_y, sidebar_width, sidebar_height)
        elif self.edit_mode == "map_select":
            self.draw_map_selector(sidebar_x, sidebar_y, sidebar_width, sidebar_height)
    
    def draw_tile_selector(self, x, y, width, height):
        title = font.render("瓦片选择", True, BLACK)
        screen.blit(title, (x + 10, y + 10))
        
        tiles_per_row = 5
        tile_size = 32
        spacing = 2
        start_y = y + 40
        
        for i, tile_name in enumerate(tile_names):
            row = i // tiles_per_row
            col = i % tiles_per_row
            tile_x = x + col * (tile_size + spacing) + 10
            tile_y = start_y + row * (tile_size + spacing) + 10
            
            if i == self.selected_tile:
                pygame.draw.rect(screen, GREEN, (tile_x-2, tile_y-2, tile_size+4, tile_size+4))
            
            tile_image = tiles.get(tile_name, None)
            if tile_image:
                screen.blit(tile_image, (tile_x, tile_y))
            
            text = small_font.render(tile_name, True, BLACK)
            screen.blit(text, (tile_x, tile_y + tile_size + 2))
        
        selected_name = tile_names[self.selected_tile] if tile_names else "无"
        text = font.render(f"选中: {selected_name}", True, BLACK)
        screen.blit(text, (x + 10, y + height - 30))
    
    def draw_connection_editor(self, x, y, width, height):
        title = font.render("连接编辑", True, BLACK)
        screen.blit(title, (x + 10, y + 10))
        
        info_texts = [
            "1. 点击地图上的格子作为起点",
            "2. 再次点击作为终点",
            "3. 自动计算方向和目标",
            "Delete: 取消当前连接"
        ]
        
        for i, text in enumerate(info_texts):
            surface = small_font.render(text, True, BLACK)
            screen.blit(surface, (x + 10, y + 40 + i * 20))
        
        if self.connection_start:
            text = small_font.render(f"起点: ({self.connection_start[0]}, {self.connection_start[1]})", True, BLACK)
            screen.blit(text, (x + 10, y + 120))
        
        text = small_font.render("现有连接:", True, BLACK)
        screen.blit(text, (x + 10, y + 150))
        
        for i, exit_info in enumerate(self.exits[:8]):
            direction = exit_info.get("direction", "未知")
            target_map = exit_info.get("target_map", "主地图")
            target_loc = exit_info.get("target_location", "")
            if target_loc:
                text = small_font.render(f"{direction} -> {target_map} ({target_loc})", True, BLACK)
            else:
                text = small_font.render(f"{direction} -> {target_map}", True, BLACK)
            screen.blit(text, (x + 10, y + 170 + i * 20))
    
    def draw_location_editor(self, x, y, width, height):
        title = font.render("地点编辑", True, BLACK)
        screen.blit(title, (x + 10, y + 10))
        
        info_texts = [
            "点击地图创建新地点",
            "选择地点进行编辑",
            "按Delete删除选中地点",
            "按Enter编辑地点名称"
        ]
        
        for i, text in enumerate(info_texts):
            surface = small_font.render(text, True, BLACK)
            screen.blit(surface, (x + 10, y + 40 + i * 20))
        
        if self.selected_location:
            loc_info = self.locations[self.selected_location]
            text = small_font.render(f"选中: {loc_info['name']}", True, BLACK)
            screen.blit(text, (x + 10, y + 120))
            text = small_font.render(f"位置: ({loc_info['x']}, {loc_info['y']})", True, BLACK)
            screen.blit(text, (x + 10, y + 140))
            text = small_font.render(f"ID: {self.selected_location}", True, BLACK)
            screen.blit(text, (x + 10, y + 160))
            
            if self.editing_location_name:
                pygame.draw.rect(screen, GREEN, (x + 10, y + 180, 200, 25))
                text = small_font.render(f"名称: {self.location_name_input}_", True, BLACK)
            else:
                text = small_font.render(f"名称: {loc_info['name']}", True, BLACK)
            screen.blit(text, (x + 10, y + 180))
        
        text = small_font.render("现有地点:", True, BLACK)
        screen.blit(text, (x + 10, y + 210))
        
        for i, (loc_id, loc_info) in enumerate(list(self.locations.items())[:8]):
            text = small_font.render(f"{loc_info['name']}", True, BLACK)
            screen.blit(text, (x + 10, y + 230 + i * 20))
    
    def draw_map_selector(self, x, y, width, height):
        title = font.render("地图选择", True, BLACK)
        screen.blit(title, (x + 10, y + 10))
        
        info_texts = [
            "左右箭头: 切换地图",
            "Ctrl+N: 创建新地图",
            "当前地图:"
        ]
        
        for i, text in enumerate(info_texts):
            surface = small_font.render(text, True, BLACK)
            screen.blit(surface, (x + 10, y + 40 + i * 20))
        
        current_map_name = self.map_info.get("name", "未知")
        text = big_font.render(f"{self.current_map}: {current_map_name}", True, BLUE)
        screen.blit(text, (x + 10, y + 100))
        
        text = small_font.render(f"尺寸: {self.map_width} x {self.map_height}", True, BLACK)
        screen.blit(text, (x + 10, y + 140))
        
        text = small_font.render(f"地点数: {len(self.locations)}", True, BLACK)
        screen.blit(text, (x + 10, y + 160))
        
        text = small_font.render(f"连接数: {len(self.exits)}", True, BLACK)
        screen.blit(text, (x + 10, y + 180))
        
        text = small_font.render("所有地图:", True, BLACK)
        screen.blit(text, (x + 10, y + 210))
        
        for i, map_id in enumerate(self.map_ids):
            map_name = self.maps_data["maps"][map_id].get("name", "未知")
            color = BLUE if map_id == self.current_map else BLACK
            prefix = ">" if map_id == self.current_map else " "
            text = small_font.render(f"{prefix} {map_id}: {map_name}", True, color)
            screen.blit(text, (x + 10, y + 230 + i * 20))
    
    def draw_edit_mode(self):
        mode_text = {
            "tiles": "图块编辑",
            "connections": "连接编辑",
            "locations": "地点编辑",
            "map_select": "地图选择"
        }
        text = font.render(f"编辑模式: {mode_text.get(self.edit_mode, '未知')}", True, BLACK)
        screen.blit(text, (20, 20))
        
        map_name = self.map_info.get("name", "未知")
        map_text = f"当前地图: {self.current_map} ({map_name})"
        text = font.render(map_text, True, BLACK)
        screen.blit(text, (20, 50))
        
        text = font.render(f"地图尺寸: {self.map_width} x {self.map_height}", True, BLACK)
        screen.blit(text, (20, 80))
    
    def draw_info(self):
        info_texts = [
            "快捷键:",
            "1: 图块编辑",
            "2: 连接编辑",
            "3: 地点编辑",
            "4: 地图选择",
            "上/下箭头: 选择瓦片",
            "Ctrl+S: 保存",
            "Delete: 删除选中项",
            "右键拖动: 移动地图",
            "Ctrl+N: 创建新地图"
        ]
        
        for i, text in enumerate(info_texts):
            surface = font.render(text, True, BLACK)
            screen.blit(surface, (20, SCREEN_HEIGHT - 250 + i * 25))
    
    def handle_tile_click(self, pos):
        if pos[0] < SCREEN_WIDTH - 320:
            grid_x = (pos[0] - self.scroll_x) // TILE_SIZE
            grid_y = (pos[1] - self.scroll_y) // TILE_SIZE
            
            if 0 <= grid_x < self.map_width and 0 <= grid_y < self.map_height:
                self.map_data[grid_y][grid_x] = self.selected_tile
    
    def handle_connection_click(self, pos):
        if pos[0] < SCREEN_WIDTH - 320:
            grid_x = (pos[0] - self.scroll_x) // TILE_SIZE
            grid_y = (pos[1] - self.scroll_y) // TILE_SIZE
            
            if 0 <= grid_x < self.map_width and 0 <= grid_y < self.map_height:
                if not self.connection_start:
                    self.connection_start = (grid_x, grid_y)
                else:
                    self.connection_end = (grid_x, grid_y)
                    
                    dx = grid_x - self.connection_start[0]
                    dy = grid_y - self.connection_start[1]
                    direction = ""
                    
                    if abs(dx) > abs(dy):
                        direction = "东" if dx > 0 else "西"
                    else:
                        direction = "南" if dy > 0 else "北"
                    
                    target_location = None
                    for loc_id, loc_info in self.locations.items():
                        if loc_info["x"] == grid_x and loc_info["y"] == grid_y:
                            target_location = loc_id
                            break
                    
                    new_exit = {
                        "direction": direction,
                        "from_x": self.connection_start[0],
                        "from_y": self.connection_start[1],
                        "to_x": grid_x,
                        "to_y": grid_y,
                        "target_map": self.current_map
                    }
                    
                    if target_location:
                        new_exit["target_location"] = target_location
                    
                    self.exits.append(new_exit)
                    
                    self.connection_start = None
                    self.connection_end = None
    
    def handle_location_click(self, pos):
        if pos[0] < SCREEN_WIDTH - 320:
            grid_x = (pos[0] - self.scroll_x) // TILE_SIZE
            grid_y = (pos[1] - self.scroll_y) // TILE_SIZE
            
            if 0 <= grid_x < self.map_width and 0 <= grid_y < self.map_height:
                clicked_location = None
                for loc_id, loc_info in self.locations.items():
                    if loc_info["x"] == grid_x and loc_info["y"] == grid_y:
                        clicked_location = loc_id
                        break
                
                if clicked_location:
                    self.selected_location = clicked_location
                    self.editing_location_name = True
                    self.location_name_input = self.locations[clicked_location]["name"]
                else:
                    new_loc_id = f"loc_{len(self.locations) + 1}"
                    new_loc_name = f"地点{len(self.locations) + 1}"
                    self.locations[new_loc_id] = {
                        "name": new_loc_name,
                        "x": grid_x,
                        "y": grid_y,
                        "terrain": "grass",
                        "features": [],
                        "min_level": 1
                    }
                    self.selected_location = new_loc_id
                    self.editing_location_name = True
                    self.location_name_input = new_loc_name
    
    def handle_map_select_click(self, pos):
        pass

if __name__ == "__main__":
    editor = MapEditor()
    editor.run()
