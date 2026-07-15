import json
import random

MAP_WIDTH = 120
MAP_HEIGHT = 120

CENTER_X = MAP_WIDTH // 2
CENTER_Y = MAP_HEIGHT // 2

TERRAIN_TILES = {
    'grass': 25,
    'grass_dark': 26,
    'grass_light': 27,
    'path': 3,
    'path_corner': 7,
    'path_t': 8,
    'path_cross': 33,
    'water': 29,
    'water_wave': 40,
    'water_shore': 41,
    'mountain': 35,
    'mountain_peak': 36,
    'tree': 2,
    'tree_large': 4,
    'flower': 13,
    'flower_bed': 14,
    'house1': 1,
    'house2': 6,
    'house3': 16,
    'town': 17,
    'castle': 18,
    'well': 9,
    'farmland': 10,
    'farmland_green': 11,
    'sand': 19,
    'beach': 20,
    'cave': 21,
    'bridge': 22,
    'ruins': 23,
    'fence': 24,
    'wolf': 100,
    'tiger': 101,
    'lion': 102,
}

locations = {
    'zhongli': {'name': '钟离县', 'x': CENTER_X, 'y': CENTER_Y, 'terrain': 'village', 'min_level': 1},
    'huangjue_si': {'name': '皇觉寺', 'x': CENTER_X - 15, 'y': CENTER_Y - 10, 'terrain': 'temple', 'min_level': 2},
    'huaixi': {'name': '淮西', 'x': CENTER_X + 20, 'y': CENTER_Y, 'terrain': 'plains', 'min_level': 3},
    'henan': {'name': '河南', 'x': CENTER_X + 40, 'y': CENTER_Y - 5, 'terrain': 'plains', 'min_level': 4},
    'dingyuan': {'name': '定远', 'x': CENTER_X - 5, 'y': CENTER_Y + 20, 'terrain': 'fortress', 'min_level': 5},
    'hezhou': {'name': '和州', 'x': CENTER_X + 25, 'y': CENTER_Y + 25, 'terrain': 'city', 'min_level': 6},
    'taiping_fu': {'name': '太平府', 'x': CENTER_X + 38, 'y': CENTER_Y + 38, 'terrain': 'city', 'min_level': 7},
    'yingtian_fu': {'name': '应天府', 'x': CENTER_X + 45, 'y': CENTER_Y + 50, 'terrain': 'city', 'min_level': 8},
    'huizhou': {'name': '徽州', 'x': CENTER_X + 55, 'y': CENTER_Y + 25, 'terrain': 'city', 'min_level': 9},
    'zhedong': {'name': '浙东', 'x': CENTER_X + 52, 'y': CENTER_Y - 8, 'terrain': 'coastal', 'min_level': 10},
    'jinhua': {'name': '金华', 'x': CENTER_X + 50, 'y': CENTER_Y - 22, 'terrain': 'plains', 'min_level': 11},
    'poyang_hu': {'name': '鄱阳湖', 'x': CENTER_X + 10, 'y': CENTER_Y + 50, 'terrain': 'water', 'min_level': 12},
    'suzhou': {'name': '苏州', 'x': CENTER_X + 55, 'y': CENTER_Y + 12, 'terrain': 'city', 'min_level': 13},
    'yuan_dadu': {'name': '元大都', 'x': CENTER_X - 50, 'y': CENTER_Y - 5, 'terrain': 'city', 'min_level': 14},
    'sichuan': {'name': '四川', 'x': CENTER_X - 40, 'y': CENTER_Y + 35, 'terrain': 'mountain', 'min_level': 15},
    'yunnan': {'name': '云南', 'x': CENTER_X - 15, 'y': CENTER_Y + 55, 'terrain': 'mountain', 'min_level': 16},
    'beijing': {'name': '北京', 'x': CENTER_X, 'y': CENTER_Y - 50, 'terrain': 'city', 'min_level': 17},
    'changan': {'name': '长安', 'x': CENTER_X - 45, 'y': CENTER_Y - 22, 'terrain': 'city', 'min_level': 18},
    'xiangyang': {'name': '襄阳', 'x': CENTER_X - 25, 'y': CENTER_Y - 5, 'terrain': 'city', 'min_level': 4},
    'nanchang': {'name': '南昌', 'x': CENTER_X + 25, 'y': CENTER_Y + 42, 'terrain': 'city', 'min_level': 7},
    'guangzhou': {'name': '广州', 'x': CENTER_X + 35, 'y': CENTER_Y + 55, 'terrain': 'city', 'min_level': 19},
    'hangzhou': {'name': '杭州', 'x': CENTER_X + 58, 'y': CENTER_Y - 18, 'terrain': 'city', 'min_level': 12},
}

def create_base_map():
    data = []
    for y in range(MAP_HEIGHT):
        row = []
        for x in range(MAP_WIDTH):
            if y < 20:
                row.append(random.choice([TERRAIN_TILES['grass_light'], TERRAIN_TILES['grass']]))
            elif y > MAP_HEIGHT - 25:
                row.append(random.choice([TERRAIN_TILES['grass_dark'], TERRAIN_TILES['grass']]))
            elif x < 25:
                row.append(random.choice([TERRAIN_TILES['grass'], TERRAIN_TILES['grass_dark']]))
            elif x > MAP_WIDTH - 25:
                row.append(random.choice([TERRAIN_TILES['grass'], TERRAIN_TILES['grass_light']]))
            else:
                row.append(random.choice([TERRAIN_TILES['grass'], TERRAIN_TILES['grass_light'], TERRAIN_TILES['grass_dark']]))
        data.append(row)
    return data

def add_main_roads(data):
    for x in range(MAP_WIDTH):
        if x == CENTER_X:
            data[CENTER_Y][x] = TERRAIN_TILES['path_cross']
        else:
            data[CENTER_Y][x] = TERRAIN_TILES['path']
    
    for y in range(MAP_HEIGHT):
        if y == CENTER_Y:
            data[y][CENTER_X] = TERRAIN_TILES['path_cross']
        else:
            data[y][CENTER_X] = TERRAIN_TILES['path']

def add_branch_roads(data):
    branches = [
        (CENTER_X, CENTER_Y, CENTER_X + 25, CENTER_Y),
        (CENTER_X, CENTER_Y, CENTER_X - 25, CENTER_Y),
        (CENTER_X, CENTER_Y, CENTER_X, CENTER_Y + 25),
        (CENTER_X, CENTER_Y, CENTER_X, CENTER_Y - 25),
        (CENTER_X + 25, CENTER_Y, CENTER_X + 25, CENTER_Y + 25),
        (CENTER_X + 25, CENTER_Y, CENTER_X + 50, CENTER_Y),
        (CENTER_X - 25, CENTER_Y, CENTER_X - 25, CENTER_Y + 25),
        (CENTER_X - 25, CENTER_Y, CENTER_X - 50, CENTER_Y),
        (CENTER_X, CENTER_Y + 25, CENTER_X, CENTER_Y + 55),
        (CENTER_X, CENTER_Y - 25, CENTER_X, CENTER_Y - 50),
        (CENTER_X, CENTER_Y + 25, CENTER_X + 25, CENTER_Y + 25),
        (CENTER_X, CENTER_Y + 55, CENTER_X + 45, CENTER_Y + 55),
        (CENTER_X, CENTER_Y + 55, CENTER_X - 15, CENTER_Y + 55),
        (CENTER_X, CENTER_Y - 25, CENTER_X + 50, CENTER_Y - 25),
        (CENTER_X, CENTER_Y - 25, CENTER_X - 45, CENTER_Y - 25),
        (CENTER_X + 25, CENTER_Y + 25, CENTER_X + 38, CENTER_Y + 38),
        (CENTER_X + 50, CENTER_Y, CENTER_X + 50, CENTER_Y - 22),
        (CENTER_X + 50, CENTER_Y, CENTER_X + 50, CENTER_Y + 12),
        (CENTER_X - 25, CENTER_Y + 25, CENTER_X - 40, CENTER_Y + 35),
        (CENTER_X - 50, CENTER_Y, CENTER_X - 50, CENTER_Y - 22),
        (CENTER_X + 25, CENTER_Y + 25, CENTER_X + 25, CENTER_Y + 42),
        (CENTER_X - 15, CENTER_Y + 55, CENTER_X - 40, CENTER_Y + 35),
        (CENTER_X + 50, CENTER_Y - 25, CENTER_X + 58, CENTER_Y - 18),
        (CENTER_X + 58, CENTER_Y - 18, CENTER_X + 52, CENTER_Y - 8),
        (CENTER_X + 52, CENTER_Y - 8, CENTER_X + 55, CENTER_Y + 12),
        (CENTER_X + 55, CENTER_Y + 12, CENTER_X + 55, CENTER_Y + 25),
        (CENTER_X + 38, CENTER_Y + 38, CENTER_X + 45, CENTER_Y + 50),
        (CENTER_X + 45, CENTER_Y + 50, CENTER_X + 35, CENTER_Y + 55),
        (CENTER_X - 25, CENTER_Y, CENTER_X - 25, CENTER_Y - 5),
        (CENTER_X + 50, CENTER_Y + 12, CENTER_X + 55, CENTER_Y + 12),
        (CENTER_X - 45, CENTER_Y - 25, CENTER_X - 45, CENTER_Y - 22),
    ]
    
    for start_x, start_y, end_x, end_y in branches:
        if start_x == end_x:
            min_y = min(start_y, end_y)
            max_y = max(start_y, end_y)
            for y in range(min_y, max_y + 1):
                if 0 <= y < MAP_HEIGHT and 0 <= start_x < MAP_WIDTH:
                    data[y][start_x] = TERRAIN_TILES['path']
        else:
            min_x = min(start_x, end_x)
            max_x = max(start_x, end_x)
            for x in range(min_x, max_x + 1):
                if 0 <= x < MAP_WIDTH and 0 <= start_y < MAP_HEIGHT:
                    data[start_y][x] = TERRAIN_TILES['path']
    
    intersections = [
        (CENTER_X, CENTER_Y),
        (CENTER_X + 25, CENTER_Y),
        (CENTER_X - 25, CENTER_Y),
        (CENTER_X, CENTER_Y + 25),
        (CENTER_X, CENTER_Y - 25),
        (CENTER_X + 50, CENTER_Y),
        (CENTER_X - 50, CENTER_Y),
        (CENTER_X, CENTER_Y + 55),
        (CENTER_X, CENTER_Y - 50),
        (CENTER_X + 25, CENTER_Y + 25),
        (CENTER_X - 25, CENTER_Y + 25),
        (CENTER_X + 38, CENTER_Y + 38),
        (CENTER_X + 50, CENTER_Y - 22),
        (CENTER_X + 50, CENTER_Y + 12),
        (CENTER_X - 40, CENTER_Y + 35),
        (CENTER_X - 50, CENTER_Y - 22),
        (CENTER_X + 25, CENTER_Y + 42),
        (CENTER_X + 58, CENTER_Y - 18),
        (CENTER_X + 52, CENTER_Y - 8),
        (CENTER_X + 55, CENTER_Y + 25),
        (CENTER_X + 45, CENTER_Y + 50),
        (CENTER_X + 35, CENTER_Y + 55),
        (CENTER_X - 25, CENTER_Y - 5),
        (CENTER_X + 55, CENTER_Y + 12),
        (CENTER_X - 45, CENTER_Y - 22),
    ]
    
    for x, y in intersections:
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            data[y][x] = TERRAIN_TILES['path_cross']

def add_locations(data):
    for loc_id, loc in locations.items():
        x, y = loc['x'], loc['y']
        terrain = loc['terrain']
        
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                nx, ny = x + dx, y + dy
                if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                    if abs(dx) <= 1 and abs(dy) <= 1:
                        if terrain == 'village':
                            if dx == 0 and dy == 0:
                                data[ny][nx] = TERRAIN_TILES['house1']
                            elif dx == 1 and dy == 0:
                                data[ny][nx] = TERRAIN_TILES['house2']
                            elif dx == 0 and dy == 1:
                                data[ny][nx] = TERRAIN_TILES['well']
                            elif dx == -1 and dy == 0:
                                data[ny][nx] = TERRAIN_TILES['farmland']
                            else:
                                data[ny][nx] = TERRAIN_TILES['path']
                        elif terrain == 'city':
                            if dx == 0 and dy == 0:
                                data[ny][nx] = TERRAIN_TILES['town']
                            else:
                                data[ny][nx] = TERRAIN_TILES['path']
                        elif terrain == 'temple':
                            if dx == 0 and dy == 0:
                                data[ny][nx] = TERRAIN_TILES['house3']
                            elif dx == 1 and dy == 0:
                                data[ny][nx] = TERRAIN_TILES['flower']
                            else:
                                data[ny][nx] = TERRAIN_TILES['grass']
                        elif terrain == 'fortress':
                            if dx == 0 and dy == 0:
                                data[ny][nx] = TERRAIN_TILES['castle']
                            else:
                                data[ny][nx] = TERRAIN_TILES['path']
                        elif terrain == 'water':
                            if abs(dx) <= 2 and abs(dy) <= 2:
                                data[ny][nx] = TERRAIN_TILES['water']
                            else:
                                data[ny][nx] = TERRAIN_TILES['water_shore']
                        elif terrain == 'mountain':
                            if abs(dx) <= 1 and abs(dy) <= 1:
                                data[ny][nx] = TERRAIN_TILES['mountain']
                            else:
                                data[ny][nx] = TERRAIN_TILES['mountain_peak']
                        elif terrain == 'coastal':
                            if abs(dx) <= 1 and abs(dy) <= 1:
                                data[ny][nx] = TERRAIN_TILES['beach']
                            else:
                                data[ny][nx] = TERRAIN_TILES['water']
                        else:
                            data[ny][nx] = TERRAIN_TILES['grass']

def add_features(data):
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if data[y][x] == TERRAIN_TILES['grass'] or data[y][x] == TERRAIN_TILES['grass_light'] or data[y][x] == TERRAIN_TILES['grass_dark']:
                rand = random.random()
                if rand < 0.08:
                    data[y][x] = TERRAIN_TILES['tree']
                elif rand < 0.12:
                    data[y][x] = TERRAIN_TILES['flower']
                elif rand < 0.15:
                    data[y][x] = TERRAIN_TILES['farmland']
                elif rand < 0.17:
                    data[y][x] = TERRAIN_TILES['farmland_green']
    
    for _ in range(15):
        fx = random.randint(5, MAP_WIDTH - 6)
        fy = random.randint(5, MAP_HEIGHT - 6)
        data[fy][fx] = TERRAIN_TILES['tree_large']
    
    for _ in range(8):
        fx = random.randint(10, MAP_WIDTH - 11)
        fy = random.randint(10, MAP_HEIGHT - 11)
        data[fy][fx] = TERRAIN_TILES['cave']
    
    for _ in range(12):
        fx = random.randint(5, MAP_WIDTH - 6)
        fy = random.randint(5, MAP_HEIGHT - 6)
        data[fy][fx] = TERRAIN_TILES['flower_bed']
    
    for _ in range(8):
        fx = random.randint(5, MAP_WIDTH - 6)
        fy = random.randint(5, MAP_HEIGHT - 6)
        data[fy][fx] = TERRAIN_TILES['fence']
    
    for _ in range(5):
        fx = random.randint(5, MAP_WIDTH - 6)
        fy = random.randint(5, MAP_HEIGHT - 6)
        data[fy][fx] = TERRAIN_TILES['ruins']
    
    for _ in range(5):
        fx = random.randint(5, MAP_WIDTH - 6)
        fy = random.randint(5, MAP_HEIGHT - 6)
        data[fy][fx] = TERRAIN_TILES['sand']
    
    for _ in range(4):
        fx = random.randint(5, MAP_WIDTH - 6)
        fy = random.randint(5, MAP_HEIGHT - 6)
        data[fy][fx] = TERRAIN_TILES['bridge']
    
    for _ in range(6):
        fx = random.randint(5, MAP_WIDTH - 6)
        fy = random.randint(5, MAP_HEIGHT - 6)
        data[fy][fx] = TERRAIN_TILES['well']
    
    water_positions = []
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if data[y][x] == TERRAIN_TILES['water']:
                water_positions.append((x, y))
    
    if water_positions:
        for _ in range(8):
            x, y = random.choice(water_positions)
            data[y][x] = TERRAIN_TILES['water_wave']
        
        for _ in range(10):
            x, y = random.choice(water_positions)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                    if data[ny][nx] not in [TERRAIN_TILES['water'], TERRAIN_TILES['water_wave'], TERRAIN_TILES['water_shore']]:
                        data[ny][nx] = TERRAIN_TILES['water_shore']
                        break
    
    mountain_positions = []
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if data[y][x] == TERRAIN_TILES['mountain']:
                mountain_positions.append((x, y))
    
    if mountain_positions:
        for _ in range(10):
            x, y = random.choice(mountain_positions)
            data[y][x] = TERRAIN_TILES['mountain_peak']
    
    path_positions = []
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if data[y][x] == TERRAIN_TILES['path']:
                path_positions.append((x, y))
    
    if path_positions:
        for _ in range(12):
            x, y = random.choice(path_positions)
            data[y][x] = TERRAIN_TILES['path_corner']
        
        for _ in range(12):
            x, y = random.choice(path_positions)
            data[y][x] = TERRAIN_TILES['path_t']

def add_monsters(data):
    monster_positions = [
        (CENTER_X - 10, CENTER_Y - 15),
        (CENTER_X + 15, CENTER_Y - 5),
        (CENTER_X + 25, CENTER_Y + 15),
        (CENTER_X - 5, CENTER_Y + 25),
        (CENTER_X + 35, CENTER_Y - 10),
        (CENTER_X + 30, CENTER_Y + 30),
        (CENTER_X - 25, CENTER_Y - 15),
        (CENTER_X - 30, CENTER_Y + 20),
        (CENTER_X + 45, CENTER_Y + 8),
        (CENTER_X - 40, CENTER_Y + 30),
        (CENTER_X + 40, CENTER_Y - 18),
        (CENTER_X, CENTER_Y - 42),
        (CENTER_X, CENTER_Y + 48),
        (CENTER_X - 45, CENTER_Y),
        (CENTER_X + 48, CENTER_Y),
        (CENTER_X + 48, CENTER_Y - 25),
        (CENTER_X - 45, CENTER_Y - 20),
        (CENTER_X + 30, CENTER_Y + 45),
        (CENTER_X - 15, CENTER_Y + 45),
        (CENTER_X + 52, CENTER_Y + 20),
    ]
    
    for idx, (x, y) in enumerate(monster_positions):
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            if idx < 8:
                data[y][x] = TERRAIN_TILES['wolf']
            elif idx < 15:
                data[y][x] = TERRAIN_TILES['tiger']
            else:
                data[y][x] = TERRAIN_TILES['lion']

def ensure_all_tiles_used(data):
    used_tiles = set()
    for row in data:
        used_tiles.update(row)
    
    unused_tiles = []
    for name, tile_id in TERRAIN_TILES.items():
        if tile_id not in used_tiles:
            unused_tiles.append((name, tile_id))
    
    if unused_tiles:
        print(f"未使用的tiles: {unused_tiles}")
    
    for name, tile_id in unused_tiles:
        placed = False
        for attempt in range(200):
            x = random.randint(5, MAP_WIDTH - 6)
            y = random.randint(5, MAP_HEIGHT - 6)
            if data[y][x] in [TERRAIN_TILES['grass'], TERRAIN_TILES['grass_light'], TERRAIN_TILES['grass_dark']]:
                data[y][x] = tile_id
                placed = True
                break
        if not placed:
            for attempt in range(100):
                x = random.randint(5, MAP_WIDTH - 6)
                y = random.randint(5, MAP_HEIGHT - 6)
                if data[y][x] == TERRAIN_TILES['path']:
                    data[y][x] = tile_id
                    placed = True
                    break
        if not placed:
            print(f"无法放置 {name} (id: {tile_id})")

def main():
    data = create_base_map()
    add_main_roads(data)
    add_branch_roads(data)
    add_locations(data)
    add_features(data)
    add_monsters(data)
    ensure_all_tiles_used(data)
    
    tile_mapping = {v: k for k, v in TERRAIN_TILES.items()}
    
    map_data = {
        "maps": {
            "main_map": {
                "name": "大明王朝RPG - 十字路网",
                "width": MAP_WIDTH,
                "height": MAP_HEIGHT,
                "data": data,
                "locations": {
                    loc_id: {
                        'name': loc['name'],
                        'x': loc['x'],
                        'y': loc['y'],
                        'terrain': loc['terrain'],
                        'features': [],
                        'min_level': loc['min_level']
                    }
                    for loc_id, loc in locations.items()
                }
            }
        },
        "tile_mapping": tile_mapping
    }
    
    with open('maps.json', 'w', encoding='utf-8') as f:
        json.dump(map_data, f, ensure_ascii=False, indent=2)
    
    print("地图重新设计完成！")
    print(f"地图尺寸: {MAP_WIDTH}x{MAP_HEIGHT}")
    print(f"中心位置: ({CENTER_X}, {CENTER_Y})")
    print(f"地点数量: {len(locations)}")
    
    used_tiles = set()
    for row in data:
        used_tiles.update(row)
    print(f"使用的tiles数量: {len(used_tiles)}")

if __name__ == "__main__":
    main()
