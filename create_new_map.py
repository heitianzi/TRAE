#!/usr/bin/env python3
# 生成符合用户要求的地图格局

import json

# 地图尺寸
WIDTH = 60
HEIGHT = 60

# 地形类型
tile_types = {
    'water': 26,      # 水域
    'asphalt_road': 27, # 道路
    'grass': 25,      # 草地
    'farmland': 6,    # 农田
    'path': 3,        # 小路
    'mountain': 15    # 山脉
}

# 创建新的地图格局
def create_new_map():
    map_data = []
    
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            # 边界水域
            if x < 5 or x > 54 or y < 5 or y > 54:
                row.append(tile_types['water'])
            # 主要道路网络
            elif (x % 10 == 0 and 5 <= y <= 54) or (y % 10 == 0 and 5 <= x <= 54):
                row.append(tile_types['asphalt_road'])
            # 农田区域（模拟图片中的庄稼）
            elif (15 <= x <= 25 and 15 <= y <= 25) or (15 <= x <= 25 and 35 <= y <= 45):
                row.append(tile_types['farmland'])
            # 小路
            elif (x % 5 == 0 and 5 <= y <= 54) or (y % 5 == 0 and 5 <= x <= 54):
                row.append(tile_types['path'])
            # 其他区域为草地
            else:
                row.append(tile_types['grass'])
        map_data.append(row)
    
    return map_data

# 生成地点位置
def create_locations():
    locations = {
        'zhongli_north': {
            'name': '钟离县-北',
            'x': 30,
            'y': 15,
            'terrain': 'village',
            'features': ['house1', 'house2', 'well', 'farmland', 'path'],
            'min_level': 1
        },
        'zhongli_south': {
            'name': '钟离县-南',
            'x': 30,
            'y': 45,
            'terrain': 'village',
            'features': ['house1', 'house2', 'well', 'farmland', 'path'],
            'min_level': 1
        },
        'huangjue_si': {
            'name': '皇觉寺',
            'x': 20,
            'y': 20,
            'terrain': 'temple',
            'features': ['house1', 'tree', 'flowers', 'path'],
            'min_level': 2
        },
        'huaixi': {
            'name': '淮西',
            'x': 40,
            'y': 30,
            'terrain': 'plains',
            'features': ['grass', 'tree', 'path', 'farmland'],
            'min_level': 3
        },
        'henan': {
            'name': '河南',
            'x': 50,
            'y': 20,
            'terrain': 'plains',
            'features': ['grass', 'tree', 'farmland', 'path'],
            'min_level': 4
        },
        'dingyuan': {
            'name': '定远',
            'x': 20,
            'y': 40,
            'terrain': 'fortress',
            'features': ['wall', 'house1', 'tree', 'path'],
            'min_level': 5
        },
        'hezhou': {
            'name': '和州',
            'x': 30,
            'y': 30,
            'terrain': 'city',
            'features': ['town', 'house1', 'tree', 'path'],
            'min_level': 6
        },
        'taiping_fu': {
            'name': '太平府',
            'x': 40,
            'y': 40,
            'terrain': 'city',
            'features': ['town', 'house1', 'tree', 'path'],
            'min_level': 7
        },
        'yingtian_fu': {
            'name': '应天府',
            'x': 45,
            'y': 35,
            'terrain': 'city',
            'features': ['town', 'house1', 'tree', 'path'],
            'min_level': 8
        },
        'huizhou': {
            'name': '徽州',
            'x': 55,
            'y': 45,
            'terrain': 'mountain',
            'features': ['mountain', 'tree', 'house1', 'path'],
            'min_level': 9
        },
        'zhedong': {
            'name': '浙东',
            'x': 55,
            'y': 25,
            'terrain': 'coastal',
            'features': ['water', 'tree', 'grass', 'path'],
            'min_level': 10
        },
        'jinhua': {
            'name': '金华',
            'x': 50,
            'y': 15,
            'terrain': 'plains',
            'features': ['grass', 'tree', 'farmland', 'path'],
            'min_level': 11
        },
        'poyang_hu': {
            'name': '鄱阳湖',
            'x': 40,
            'y': 50,
            'terrain': 'water',
            'features': ['water', 'tree', 'grass', 'path'],
            'min_level': 12
        },
        'suzhou': {
            'name': '苏州',
            'x': 50,
            'y': 50,
            'terrain': 'city',
            'features': ['town', 'house1', 'tree', 'path'],
            'min_level': 13
        },
        'yuan_dadu': {
            'name': '元大都',
            'x': 10,
            'y': 10,
            'terrain': 'city',
            'features': ['town', 'house1', 'tree', 'path'],
            'min_level': 14
        },
        'sichuan': {
            'name': '四川',
            'x': 10,
            'y': 40,
            'terrain': 'mountain',
            'features': ['mountain', 'tree', 'house1', 'path'],
            'min_level': 15
        },
        'yunnan': {
            'name': '云南',
            'x': 15,
            'y': 50,
            'terrain': 'mountain',
            'features': ['mountain', 'tree', 'house1', 'path'],
            'min_level': 16
        }
    }
    return locations

# 生成地图数据
map_data = create_new_map()
locations = create_locations()

# 地图配置
map_config = {
    "maps": {
        "main_map": {
            "name": "大明王朝RPG",
            "width": WIDTH,
            "height": HEIGHT,
            "data": map_data,
            "locations": locations
        }
    },
    "tile_mapping": {
        "25": "grass",
        "26": "water",
        "27": "asphalt_road",
        "3": "mud_path",
        "6": "wheat_field",
        "7": "tree",
        "9": "house1",
        "10": "house2",
        "11": "well",
        "12": "calm_river",
        "15": "barren_mountain",
        "16": "stone_road",
        "19": "farm_path",
        "21": "town",
        "22": "wall",
        "100": "wolf",
        "101": "tiger",
        "102": "lion"
    }
}

# 保存地图文件
with open('maps.json', 'w', encoding='utf-8') as f:
    json.dump(map_config, f, ensure_ascii=False, indent=2)

print("新地图格局生成完成！")