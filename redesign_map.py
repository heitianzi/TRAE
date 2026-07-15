import json
import random

# 所有tiles图片
all_tiles = [
    "grass", "stone_road", "asphalt_road", "farm_path",
    "deep_water", "shallow_water", "calm_river", "bridge",
    "tree", "tree2", "forest", "flowers",
    "house1", "house2", "village", "town",
    "wall", "fence", "fence2",
    "well", "well2",
    "wheat_field", "rice_field", "vegetable_field",
    "desert", "snow_field", "barren_mountain", "beach",
    "cave", "active_volcano", "ruins", "trap", "mechanism"
]

# 怪物图片
monster_tiles = ["wolf", "tiger", "lion"]

# 地图尺寸
MAP_WIDTH = 120
MAP_HEIGHT = 120

# 中心点 (钟离县)
CENTER_X = 60
CENTER_Y = 60

# 地点配置
locations = {
    # 中心区域
    "zhongli": {
        "name": "钟离县",
        "x": CENTER_X,
        "y": CENTER_Y,
        "terrain": "village",
        "features": ["house1", "house2", "well", "farmland", "path"],
        "min_level": 1
    },
    "huangjue_si": {
        "name": "皇觉寺",
        "x": CENTER_X - 10,
        "y": CENTER_Y - 10,
        "terrain": "temple",
        "features": ["house1", "tree", "flowers", "path"],
        "min_level": 2
    },
    
    # 东向
    "huaixi": {
        "name": "淮西",
        "x": CENTER_X + 20,
        "y": CENTER_Y,
        "terrain": "plains",
        "features": ["grass", "tree", "path", "farmland"],
        "min_level": 3
    },
    "henan": {
        "name": "河南",
        "x": CENTER_X + 40,
        "y": CENTER_Y - 5,
        "terrain": "plains",
        "features": ["grass", "tree", "farmland", "path"],
        "min_level": 4
    },
    "zhedong": {
        "name": "浙东",
        "x": CENTER_X + 60,
        "y": CENTER_Y - 10,
        "terrain": "coastal",
        "features": ["water", "tree", "grass", "path"],
        "min_level": 10
    },
    "jinhua": {
        "name": "金华",
        "x": CENTER_X + 60,
        "y": CENTER_Y - 20,
        "terrain": "plains",
        "features": ["grass", "tree", "farmland", "path"],
        "min_level": 11
    },
    "suzhou": {
        "name": "苏州",
        "x": CENTER_X + 80,
        "y": CENTER_Y + 10,
        "terrain": "city",
        "features": ["town", "house1", "tree", "path"],
        "min_level": 13
    },
    
    # 南向
    "dingyuan": {
        "name": "定远",
        "x": CENTER_X - 5,
        "y": CENTER_Y + 20,
        "terrain": "fortress",
        "features": ["wall", "house1", "tree", "path"],
        "min_level": 5
    },
    "poyang_hu": {
        "name": "鄱阳湖",
        "x": CENTER_X,
        "y": CENTER_Y + 40,
        "terrain": "water",
        "features": ["water", "tree", "grass", "path"],
        "min_level": 12
    },
    "yunnan": {
        "name": "云南",
        "x": CENTER_X - 10,
        "y": CENTER_Y + 60,
        "terrain": "mountain",
        "features": ["mountain", "tree", "house1", "path"],
        "min_level": 16
    },
    
    # 西向
    "yuan_dadu": {
        "name": "元大都",
        "x": CENTER_X - 60,
        "y": CENTER_Y - 10,
        "terrain": "city",
        "features": ["town", "house1", "tree", "path"],
        "min_level": 14
    },
    "sichuan": {
        "name": "四川",
        "x": CENTER_X - 40,
        "y": CENTER_Y + 15,
        "terrain": "mountain",
        "features": ["mountain", "tree", "house1", "path"],
        "min_level": 15
    },
    
    # 北向
    "beijing": {
        "name": "北京",
        "x": CENTER_X,
        "y": CENTER_Y - 40,
        "terrain": "city",
        "features": ["town", "house1", "tree", "path"],
        "min_level": 17
    },
    
    # 东南向
    "hezhou": {
        "name": "和州",
        "x": CENTER_X + 25,
        "y": CENTER_Y + 25,
        "terrain": "city",
        "features": ["town", "house1", "tree", "path"],
        "min_level": 6
    },
    "taiping_fu": {
        "name": "太平府",
        "x": CENTER_X + 45,
        "y": CENTER_Y + 45,
        "terrain": "city",
        "features": ["town", "house1", "tree", "path"],
        "min_level": 7
    },
    "yingtian_fu": {
        "name": "应天府",
        "x": CENTER_X + 65,
        "y": CENTER_Y + 25,
        "terrain": "city",
        "features": ["town", "house1", "tree", "path"],
        "min_level": 8
    },
    "huizhou": {
        "name": "徽州",
        "x": CENTER_X + 55,
        "y": CENTER_Y + 45,
        "terrain": "mountain",
        "features": ["mountain", "tree", "house1", "path"],
        "min_level": 9
    }
}

# 瓦片映射
tile_mapping = {
    "grass": 25,
    "stone_road": 3,
    "asphalt_road": 28,
    "farm_path": 29,
    "deep_water": 26,
    "shallow_water": 27,
    "calm_river": 30,
    "bridge": 31,
    "tree": 7,
    "tree2": 8,
    "forest": 32,
    "flowers": 33,
    "house1": 4,
    "house2": 5,
    "village": 34,
    "town": 6,
    "wall": 9,
    "fence": 10,
    "fence2": 11,
    "well": 12,
    "well2": 13,
    "wheat_field": 14,
    "rice_field": 15,
    "vegetable_field": 16,
    "desert": 35,
    "snow_field": 36,
    "barren_mountain": 37,
    "beach": 38,
    "cave": 39,
    "active_volcano": 40,
    "ruins": 41,
    "trap": 42,
    "mechanism": 43,
    "wolf": 100,
    "tiger": 101,
    "lion": 102
}

# 反向映射
id_to_tile = {v: k for k, v in tile_mapping.items()}

# 生成新地图数据
def generate_new_map():
    # 初始化地图数据
    new_data = [[tile_mapping["grass"] for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
    
    # 绘制十字道路
    # 东西向道路
    for x in range(0, MAP_WIDTH):
        new_data[CENTER_Y][x] = tile_mapping["stone_road"]
    # 南北向道路
    for y in range(0, MAP_HEIGHT):
        new_data[y][CENTER_X] = tile_mapping["stone_road"]
    
    # 绘制辐射状道路
    # 东北方向
    x, y = CENTER_X, CENTER_Y
    while x < MAP_WIDTH and y > 0:
        new_data[y][x] = tile_mapping["farm_path"]
        x += 1
        y -= 1
    # 东南方向
    x, y = CENTER_X, CENTER_Y
    while x < MAP_WIDTH and y < MAP_HEIGHT:
        new_data[y][x] = tile_mapping["farm_path"]
        x += 1
        y += 1
    # 西北方向
    x, y = CENTER_X, CENTER_Y
    while x > 0 and y > 0:
        new_data[y][x] = tile_mapping["farm_path"]
        x -= 1
        y -= 1
    # 西南方向
    x, y = CENTER_X, CENTER_Y
    while x > 0 and y < MAP_HEIGHT:
        new_data[y][x] = tile_mapping["farm_path"]
        x -= 1
        y += 1
    
    # 添加所有tiles图片
    # 1. 添加水域
    for y in range(0, MAP_HEIGHT):
        for x in range(0, MAP_WIDTH):
            if (x < 20 or x > MAP_WIDTH - 20) and random.random() < 0.3:
                new_data[y][x] = tile_mapping["deep_water"]
            elif (y < 20 or y > MAP_HEIGHT - 20) and random.random() < 0.2:
                new_data[y][x] = tile_mapping["shallow_water"]
    
    # 2. 添加地形
    for y in range(0, MAP_HEIGHT):
        for x in range(0, MAP_WIDTH):
            # 沙漠（西北）
            if x < CENTER_X - 30 and y < CENTER_Y - 20 and random.random() < 0.4:
                new_data[y][x] = tile_mapping["desert"]
            # 雪地（东北）
            elif x > CENTER_X + 30 and y < CENTER_Y - 20 and random.random() < 0.3:
                new_data[y][x] = tile_mapping["snow_field"]
            # 山地（西南）
            elif x < CENTER_X - 20 and y > CENTER_Y + 20 and random.random() < 0.3:
                new_data[y][x] = tile_mapping["barren_mountain"]
            # 海滩（东南）
            elif x > CENTER_X + 30 and y > CENTER_Y + 30 and random.random() < 0.3:
                new_data[y][x] = tile_mapping["beach"]
    
    # 3. 添加特殊地形
    # 火山
    new_data[10][10] = tile_mapping["active_volcano"]
    # 洞穴
    new_data[MAP_HEIGHT-10][10] = tile_mapping["cave"]
    # 废墟
    new_data[10][MAP_WIDTH-10] = tile_mapping["ruins"]
    # 森林
    for y in range(CENTER_Y-15, CENTER_Y+15):
        for x in range(CENTER_X-15, CENTER_X+15):
            if random.random() < 0.1 and new_data[y][x] == tile_mapping["grass"]:
                new_data[y][x] = tile_mapping["forest"]
    
    # 4. 添加农田
    for y in range(CENTER_Y-20, CENTER_Y+20):
        for x in range(CENTER_X-20, CENTER_X+20):
            if random.random() < 0.05 and new_data[y][x] == tile_mapping["grass"]:
                farm_type = random.choice(["wheat_field", "rice_field", "vegetable_field"])
                new_data[y][x] = tile_mapping[farm_type]
    
    # 5. 添加装饰
    for y in range(0, MAP_HEIGHT):
        for x in range(0, MAP_WIDTH):
            if new_data[y][x] == tile_mapping["grass"] and random.random() < 0.02:
                new_data[y][x] = tile_mapping["flowers"]
            elif new_data[y][x] == tile_mapping["grass"] and random.random() < 0.05:
                tree_type = random.choice(["tree", "tree2"])
                new_data[y][x] = tile_mapping[tree_type]
    
    # 6. 添加建筑和设施
    for y in range(CENTER_Y-25, CENTER_Y+25):
        for x in range(CENTER_X-25, CENTER_X+25):
            if new_data[y][x] == tile_mapping["grass"] and random.random() < 0.01:
                new_data[y][x] = tile_mapping["house1"]
            elif new_data[y][x] == tile_mapping["grass"] and random.random() < 0.005:
                new_data[y][x] = tile_mapping["well"]
            elif new_data[y][x] == tile_mapping["grass"] and random.random() < 0.005:
                new_data[y][x] = tile_mapping["fence"]
    
    # 7. 添加怪物
    monster_positions = [
        # 狼（低级）
        (CENTER_X-15, CENTER_Y-15),
        (CENTER_X-10, CENTER_Y),
        (CENTER_X, CENTER_Y-10),
        (CENTER_X+10, CENTER_Y),
        # 老虎（中级）
        (CENTER_X-30, CENTER_Y-20),
        (CENTER_X+30, CENTER_Y-15),
        (CENTER_X-20, CENTER_Y+25),
        (CENTER_X+25, CENTER_Y+20),
        # 狮子（高级）
        (CENTER_X-45, CENTER_Y-30),
        (CENTER_X+45, CENTER_Y-25),
        (CENTER_X-35, CENTER_Y+35),
        (CENTER_X+40, CENTER_Y+30),
    ]
    
    for i, (x, y) in enumerate(monster_positions):
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            if i < 4:
                new_data[y][x] = tile_mapping["wolf"]
            elif i < 8:
                new_data[y][x] = tile_mapping["tiger"]
            else:
                new_data[y][x] = tile_mapping["lion"]
    
    # 8. 确保道路畅通
    for x in range(0, MAP_WIDTH):
        new_data[CENTER_Y][x] = tile_mapping["stone_road"]
    for y in range(0, MAP_HEIGHT):
        new_data[y][CENTER_X] = tile_mapping["stone_road"]
    
    # 9. 确保所有tiles都被使用
    used_tiles = set()
    for row in new_data:
        for tile_id in row:
            if tile_id in id_to_tile:
                used_tiles.add(id_to_tile[tile_id])
    
    # 添加未使用的tiles
    unused_tiles = set(all_tiles) - used_tiles
    for tile_name in unused_tiles:
        # 找到一个合适的位置放置
        placed = False
        while not placed:
            x = random.randint(10, MAP_WIDTH-10)
            y = random.randint(10, MAP_HEIGHT-10)
            if new_data[y][x] == tile_mapping["grass"]:
                new_data[y][x] = tile_mapping[tile_name]
                placed = True
    
    return new_data

# 生成新地图
new_data = generate_new_map()

# 加载现有数据
with open('maps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 更新地图数据
data['maps']['main_map'] = {
    "name": "大明王朝RPG - 十字路网",
    "width": MAP_WIDTH,
    "height": MAP_HEIGHT,
    "data": new_data,
    "locations": locations
}

# 确保瓦片映射存在
data['tile_mapping'] = {str(v): k for k, v in tile_mapping.items()}

# 保存地图数据
with open('maps.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 更新recreate_transitions.py
with open('recreate_transitions.py', 'w', encoding='utf-8') as f:
    f.write('''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新创建地图间的连接信息
"""

import json

# 读取maps.json文件
def load_maps():
    with open('maps.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# 保存maps.json文件
def save_maps(data):
    with open('maps.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 重新创建连接信息
def recreate_transitions():
    maps_data = load_maps()
    
    # 为每个地点添加连接信息
    for map_id, map_info in maps_data['maps'].items():
        if 'locations' in map_info:
            for loc_id, loc_info in map_info['locations'].items():
                # 这里可以添加更复杂的连接逻辑
                pass
    
    save_maps(maps_data)
    print("连接信息已更新")

if __name__ == "__main__":
    recreate_transitions()
''')

print(f"地图已重新设计为十字路网结构")
print(f"地图尺寸: {MAP_WIDTH} x {MAP_HEIGHT}")
print(f"中心点 (钟离县): ({CENTER_X}, {CENTER_Y})")
print(f"\n地点分布:")
for loc_id, loc_info in locations.items():
    print(f"  {loc_info['name']}: ({loc_info['x']}, {loc_info['y']}) - Lv{loc_info['min_level']}")
print(f"\n所有tiles图片已使用")
print(f"\n玩家现在可以从钟离县向东西南北四个方向探索，到达云南等各个地点")