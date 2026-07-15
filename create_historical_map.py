#!/usr/bin/env python3
# 生成符合元末明初时期的历史地图

import json

# 地图尺寸
WIDTH = 60
HEIGHT = 60

# 地形类型
tile_types = {
    'water': 26,
    'asphalt_road': 27,
    'grass': 25,
    'mountain': 15,
    'river': 12
}

# 创建符合历史时期的地图
def create_historical_map():
    map_data = []
    
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            # 水域边框
            if x < 2 or x > 57 or y < 2 or y > 57:
                row.append(tile_types['water'])
            # 主要河流（长江、黄河）
            elif (x == 30 and 15 <= y <= 45) or (y == 30 and 15 <= x <= 45):
                row.append(tile_types['river'])
            # 山脉（西部、南部）
            elif (x < 15 and y > 20) or (x > 45 and y > 30):
                row.append(tile_types['mountain'])
            # 道路网络
            elif (x % 10 == 0 or y % 10 == 0):
                row.append(tile_types['asphalt_road'])
            # 其他区域为草地
            else:
                row.append(tile_types['grass'])
        map_data.append(row)
    
    return map_data

# 生成符合历史时期的地点位置
def create_historical_locations():
    locations = {
        'zhongli': {
            'name': '钟离县',
            'x': 20,
            'y': 30,
            'terrain': 'village',
            'features': ['house1', 'house2', 'well', 'wheat_field', 'farm_path'],
            'min_level': 1
        },
        'huangjue_si': {
            'name': '皇觉寺',
            'x': 20,
            'y': 20,
            'terrain': 'temple',
            'features': ['house1', 'tree', 'flowers', 'stone_road'],
            'min_level': 2
        },
        'huaixi': {
            'name': '淮西',
            'x': 30,
            'y': 30,
            'terrain': 'plains',
            'features': ['grass', 'tree', 'farm_path', 'rice_field'],
            'min_level': 3
        },
        'henan': {
            'name': '河南',
            'x': 40,
            'y': 20,
            'terrain': 'plains',
            'features': ['grass', 'tree', 'wheat_field', 'vegetable_field'],
            'min_level': 4
        },
        'dingyuan_lvpai_zhai': {
            'name': '定远驴牌寨',
            'x': 30,
            'y': 20,
            'terrain': 'fortress',
            'features': ['wall', 'house1', 'tree', 'stone_road'],
            'min_level': 5
        },
        'dingyuan_miao_shan': {
            'name': '定远妙山',
            'x': 25,
            'y': 15,
            'terrain': 'mountain',
            'features': ['barren_mountain', 'tree', 'cave', 'stone_road'],
            'min_level': 1
        },
        'hezhou': {
            'name': '和州',
            'x': 30,
            'y': 40,
            'terrain': 'river',
            'features': ['calm_river', 'bridge', 'tree', 'grass'],
            'min_level': 7
        },
        'taiping_fu': {
            'name': '太平府',
            'x': 40,
            'y': 40,
            'terrain': 'city',
            'features': ['town', 'house1', 'tree', 'stone_road'],
            'min_level': 8
        },
        'yingtian_fu': {
            'name': '应天府',
            'x': 40,
            'y': 30,
            'terrain': 'city',
            'features': ['town', 'house1', 'tree', 'stone_road'],
            'min_level': 9
        },
        'huizhou': {
            'name': '徽州',
            'x': 50,
            'y': 40,
            'terrain': 'mountain',
            'features': ['barren_mountain', 'tree', 'house1', 'stone_road'],
            'min_level': 6
        },
        'zhedong': {
            'name': '浙东',
            'x': 50,
            'y': 30,
            'terrain': 'coastal',
            'features': ['calm_river', 'tree', 'grass', 'farm_path'],
            'min_level': 10
        },
        'jinhua': {
            'name': '金华',
            'x': 55,
            'y': 30,
            'terrain': 'plains',
            'features': ['grass', 'tree', 'wheat_field', 'vegetable_field'],
            'min_level': 11
        },
        'poyang_hu': {
            'name': '鄱阳湖',
            'x': 40,
            'y': 45,
            'terrain': 'river',
            'features': ['calm_river', 'tree', 'grass', 'farm_path'],
            'min_level': 12
        },
        'suzhou': {
            'name': '苏州',
            'x': 50,
            'y': 25,
            'terrain': 'city',
            'features': ['town', 'house1', 'tree', 'stone_road'],
            'min_level': 13
        },
        'yuan_dadu': {
            'name': '元大都',
            'x': 30,
            'y': 10,
            'terrain': 'city',
            'features': ['town', 'house1', 'tree', 'stone_road'],
            'min_level': 14
        },
        'sichuan': {
            'name': '四川',
            'x': 10,
            'y': 40,
            'terrain': 'mountain',
            'features': ['barren_mountain', 'tree', 'cave', 'stone_road'],
            'min_level': 15
        },
        'yunnan': {
            'name': '云南',
            'x': 10,
            'y': 50,
            'terrain': 'mountain',
            'features': ['barren_mountain', 'tree', 'cave', 'stone_road'],
            'min_level': 16
        }
    }
    return locations

# 生成地图数据
map_data = create_historical_map()
locations = create_historical_locations()

# 地图配置
map_config = {
    "maps": {
        "main_map": {
            "name": "朱元璋崛起之路",
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
        "0": "water",
        "1": "asphalt_road",
        "2": "grass",
        "3": "mud_path",
        "4": "dirt_path",
        "5": "rice_field",
        "6": "wheat_field",
        "7": "tree",
        "8": "tree2",
        "9": "house1",
        "10": "house2",
        "11": "well",
        "12": "calm_river",
        "13": "waterfall",
        "14": "mud_road",
        "15": "barren_mountain",
        "16": "stone_road",
        "17": "bridge",
        "18": "flowers",
        "19": "farm_path",
        "20": "vegetable_field",
        "21": "town",
        "22": "wall",
        "23": "cave",
        "24": "castle",
        "100": "wolf",
        "101": "tiger",
        "102": "lion"
    }
}

# 保存地图文件
with open('maps.json', 'w', encoding='utf-8') as f:
    json.dump(map_config, f, ensure_ascii=False, indent=2)

print("历史时期地图生成完成！")