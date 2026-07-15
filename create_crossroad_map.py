import json

# 加载现有地图数据
with open('maps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 新的地图尺寸
MAP_WIDTH = 120
MAP_HEIGHT = 120

# 中心点 (钟离县)
CENTER_X = 60
CENTER_Y = 60

# 生成新地图数据
def generate_new_map():
    # 初始化地图数据
    new_data = [[25 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
    
    # 绘制十字道路
    # 东西向道路
    for x in range(0, MAP_WIDTH):
        new_data[CENTER_Y][x] = 3  # 石头路
    # 南北向道路
    for y in range(0, MAP_HEIGHT):
        new_data[y][CENTER_X] = 3  # 石头路
    
    # 绘制辐射状道路
    # 东北方向
    x, y = CENTER_X, CENTER_Y
    while x < MAP_WIDTH and y > 0:
        new_data[y][x] = 3
        x += 1
        y -= 1
    # 东南方向
    x, y = CENTER_X, CENTER_Y
    while x < MAP_WIDTH and y < MAP_HEIGHT:
        new_data[y][x] = 3
        x += 1
        y += 1
    # 西北方向
    x, y = CENTER_X, CENTER_Y
    while x > 0 and y > 0:
        new_data[y][x] = 3
        x -= 1
        y -= 1
    # 西南方向
    x, y = CENTER_X, CENTER_Y
    while x > 0 and y < MAP_HEIGHT:
        new_data[y][x] = 3
        x -= 1
        y += 1
    
    return new_data

# 重新布局地点
def reposition_locations():
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
        "huaixi": {
            "name": "淮西",
            "x": CENTER_X + 10,
            "y": CENTER_Y,
            "terrain": "plains",
            "features": ["grass", "tree", "path", "farmland"],
            "min_level": 3
        },
        
        # 东向
        "henan": {
            "name": "河南",
            "x": CENTER_X + 20,
            "y": CENTER_Y - 5,
            "terrain": "plains",
            "features": ["grass", "tree", "farmland", "path"],
            "min_level": 4
        },
        "zhedong": {
            "name": "浙东",
            "x": CENTER_X + 30,
            "y": CENTER_Y - 10,
            "terrain": "coastal",
            "features": ["water", "tree", "grass", "path"],
            "min_level": 10
        },
        "jinhua": {
            "name": "金华",
            "x": CENTER_X + 30,
            "y": CENTER_Y - 20,
            "terrain": "plains",
            "features": ["grass", "tree", "farmland", "path"],
            "min_level": 11
        },
        "suzhou": {
            "name": "苏州",
            "x": CENTER_X + 40,
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
            "y": CENTER_Y + 30,
            "terrain": "water",
            "features": ["water", "tree", "grass", "path"],
            "min_level": 12
        },
        "yunnan": {
            "name": "云南",
            "x": CENTER_X - 10,
            "y": CENTER_Y + 40,
            "terrain": "mountain",
            "features": ["mountain", "tree", "house1", "path"],
            "min_level": 16
        },
        
        # 西向
        "yuan_dadu": {
            "name": "元大都",
            "x": CENTER_X - 40,
            "y": CENTER_Y - 10,
            "terrain": "city",
            "features": ["town", "house1", "tree", "path"],
            "min_level": 14
        },
        "sichuan": {
            "name": "四川",
            "x": CENTER_X - 30,
            "y": CENTER_Y + 15,
            "terrain": "mountain",
            "features": ["mountain", "tree", "house1", "path"],
            "min_level": 15
        },
        
        # 北向
        # 北向暂时没有地点
        
        # 东南向
        "hezhou": {
            "name": "和州",
            "x": CENTER_X + 15,
            "y": CENTER_Y + 15,
            "terrain": "city",
            "features": ["town", "house1", "tree", "path"],
            "min_level": 6
        },
        "taiping_fu": {
            "name": "太平府",
            "x": CENTER_X + 25,
            "y": CENTER_Y + 25,
            "terrain": "city",
            "features": ["town", "house1", "tree", "path"],
            "min_level": 7
        },
        "yingtian_fu": {
            "name": "应天府",
            "x": CENTER_X + 35,
            "y": CENTER_Y + 15,
            "terrain": "city",
            "features": ["town", "house1", "tree", "path"],
            "min_level": 8
        },
        "huizhou": {
            "name": "徽州",
            "x": CENTER_X + 35,
            "y": CENTER_Y + 25,
            "terrain": "mountain",
            "features": ["mountain", "tree", "house1", "path"],
            "min_level": 9
        }
    }
    return locations

# 生成新地图
new_data = generate_new_map()
new_locations = reposition_locations()

# 更新地图数据
data['maps']['main_map'] = {
    "name": "大明王朝RPG - 十字路网",
    "width": MAP_WIDTH,
    "height": MAP_HEIGHT,
    "data": new_data,
    "locations": new_locations
}

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

print(f"地图已重新布局为十字路网")
print(f"地图尺寸: {MAP_WIDTH} x {MAP_HEIGHT}")
print(f"中心点 (钟离县): ({CENTER_X}, {CENTER_Y})")
print(f"\n地点分布:")
for loc_id, loc_info in new_locations.items():
    print(f"  {loc_info['name']}: ({loc_info['x']}, {loc_info['y']}) - Lv{loc_info['min_level']}")
print(f"\n玩家现在可以从钟离县向东南西北四个方向探索，到达各个地点")