#!/usr/bin/env python3
# 为各个地点添加怪物

import json

# 读取地图文件
with open('maps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 获取地图数据
map_data = data['maps']['main_map']['data']
locations = data['maps']['main_map']['locations']

# 怪物配置
monsters = {
    'wolf': 100,      # 狼 - 低级
    'tiger': 101,     # 老虎 - 中级
    'lion': 102       # 狮子 - 高级
}

# 为每个地点添加怪物
def add_monsters_to_location(location_name, x, y, monster_type):
    """为地点添加怪物"""
    monster_id = monsters[monster_type]
    
    # 在地点周围添加怪物（减少数量）
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # 只在对角线添加
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 60 and 0 <= ny < 60:
            # 检查是否是空地
            if map_data[ny][nx] == 27:  # asphalt_road
                map_data[ny][nx] = monster_id
                print(f"在 {location_name} 附近添加 {monster_type}")

# 为各个地点添加相应等级的怪物
locations_monsters = {
    'zhongli': ('wolf', 30, 30),           # 钟离县 - 狼
    'huangjue_si': ('wolf', 30, 20),       # 皇觉寺 - 狼
    'huaixi': ('wolf', 20, 30),            # 淮西 - 狼
    'henan': ('tiger', 40, 30),            # 河南 - 老虎
    'dingyuan_lvpai_zhai': ('tiger', 30, 40),  # 定远驴牌寨 - 老虎
    'dingyuan_miao_shan': ('tiger', 30, 50),    # 定远妙山 - 老虎
    'hezhou': ('tiger', 20, 40),            # 和州 - 老虎
    'taiping_fu': ('lion', 40, 40),         # 太平府 - 狮子
    'yingtian_fu': ('lion', 30, 40),        # 应天府 - 狮子
    'huizhou': ('lion', 20, 30),            # 徽州 - 狮子
    'zhedong': ('lion', 40, 20),            # 浙东 - 狮子
    'jinhua': ('lion', 50, 30),             # 金华 - 狮子
    'poyang_hu': ('tiger', 30, 20),         # 鄱阳湖 - 老虎
    'suzhou': ('lion', 20, 20),             # 苏州 - 狮子
    'yuan_dadu': ('lion', 40, 10),          # 元大都 - 狮子
    'sichuan': ('lion', 10, 30),            # 四川 - 狮子
    'yunnan': ('lion', 50, 50)              # 云南 - 狮子
}

# 执行添加怪物
for location_name, (monster_type, x, y) in locations_monsters.items():
    add_monsters_to_location(location_name, x, y, monster_type)

# 保存修改后的地图文件
with open('maps.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n怪物添加完成！")