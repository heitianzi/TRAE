#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重塑大明王朝RPG地图：
1. 完整的十字路网结构
2. 22个地点之间通过道路连通
3. 丰富的地图装饰（树木、花朵、农田、遗迹、洞穴）
4. 20个怪物分布
5. 主要路线全部连通
"""

import json
import random

random.seed(42)  # 固定随机种子保证结果一致

# 加载现有数据
with open('maps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

MAP_WIDTH = 120
MAP_HEIGHT = 120
CENTER_X = 60
CENTER_Y = 60

# 22个地点（全部更新坐标以便形成合理路网）
locations_config = {
    # 中心枢纽
    "zhongli": {"name": "钟离县", "x": 60, "y": 60, "min_level": 1, "type": "town"},
    # 皇觉寺（西北方向）
    "huangjue_si": {"name": "皇觉寺", "x": 50, "y": 50, "min_level": 2, "type": "temple"},
    # 东向
    "huaixi": {"name": "淮西", "x": 75, "y": 60, "min_level": 3, "type": "village"},
    "henan": {"name": "河南", "x": 90, "y": 55, "min_level": 4, "type": "village"},
    "xiangyang": {"name": "襄阳", "x": 35, "y": 55, "min_level": 4, "type": "town"},
    "dingyuan": {"name": "定远", "x": 60, "y": 80, "min_level": 5, "type": "village"},
    "hezhou": {"name": "和州", "x": 80, "y": 85, "min_level": 6, "type": "town"},
    "taiping_fu": {"name": "太平府", "x": 95, "y": 95, "min_level": 7, "type": "town"},
    "nanchang": {"name": "南昌", "x": 85, "y": 105, "min_level": 7, "type": "town"},
    "yingtian_fu": {"name": "应天府", "x": 105, "y": 108, "min_level": 8, "type": "city"},
    "guangzhou": {"name": "广州", "x": 100, "y": 115, "min_level": 9, "type": "city"},
    "huizhou": {"name": "徽州", "x": 110, "y": 80, "min_level": 9, "type": "town"},
    "zhedong": {"name": "浙东", "x": 110, "y": 50, "min_level": 10, "type": "village"},
    "hangzhou": {"name": "杭州", "x": 115, "y": 40, "min_level": 11, "type": "city"},
    "jinhua": {"name": "金华", "x": 108, "y": 30, "min_level": 12, "type": "town"},
    "poyang_hu": {"name": "鄱阳湖", "x": 75, "y": 110, "min_level": 12, "type": "lake"},
    "suzhou": {"name": "苏州", "x": 113, "y": 65, "min_level": 13, "type": "city"},
    # 北向
    "yuan_dadu": {"name": "元大都", "x": 15, "y": 55, "min_level": 14, "type": "city"},
    "changan": {"name": "长安", "x": 20, "y": 40, "min_level": 18, "type": "city"},
    "beijing": {"name": "北京", "x": 60, "y": 10, "min_level": 17, "type": "city"},
    # 西向
    "sichuan": {"name": "四川", "x": 15, "y": 95, "min_level": 15, "type": "town"},
    "yunnan": {"name": "云南", "x": 30, "y": 115, "min_level": 16, "type": "town"},
}

# 初始化地图（全部为草地）
new_data = [[25 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]


def carve_path(x1, y1, x2, y2, tile_id=3, width=1):
    """在两点之间雕刻路径（先水平后垂直）"""
    # 水平段
    sx, ex = min(x1, x2), max(x1, x2)
    for x in range(sx, ex + 1):
        for w in range(-width // 2, width // 2 + 1):
            nx = x
            ny = y1 + w
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                new_data[ny][nx] = tile_id
    # 垂直段
    sy, ey = min(y1, y2), max(y1, y2)
    for y in range(sy, ey + 1):
        for w in range(-width // 2, width // 2 + 1):
            nx = x2 + w
            ny = y
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                new_data[ny][nx] = tile_id


# ========== 1. 十字主干道 ==========
# 东西向主干道（y=60）
for x in range(0, MAP_WIDTH):
    new_data[CENTER_Y][x] = 3  # 石头路
    new_data[CENTER_Y - 1][x] = 3  # 加宽成2格
# 南北向主干道（x=60）
for y in range(0, MAP_HEIGHT):
    new_data[y][CENTER_X] = 3
    new_data[y][CENTER_X - 1] = 3  # 加宽

# 钟离县中心广场（特殊标记）
for dx in range(-2, 3):
    for dy in range(-2, 3):
        nx, ny = CENTER_X + dx, CENTER_Y + dy
        if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
            new_data[ny][nx] = 3

# ========== 2. 各方向分支路网 ==========
# 东向分支（钟离县 → 淮西 → 河南 → 浙东/徽州/应天府）
carve_path(60, 60, 75, 60)  # 钟离→淮西
carve_path(75, 60, 90, 55)  # 淮西→河南
carve_path(90, 55, 110, 50)  # 河南→浙东
carve_path(90, 55, 110, 80)  # 河南→徽州
carve_path(90, 55, 105, 108)  # 河南→应天府
carve_path(110, 50, 115, 40)  # 浙东→杭州
carve_path(110, 50, 108, 30)  # 浙东→金华
carve_path(110, 80, 113, 65)  # 徽州→苏州
carve_path(113, 65, 115, 40)  # 苏州→杭州

# 东南分支（应天府 → 广州、南昌、鄱阳湖）
carve_path(105, 108, 100, 115)  # 应天府→广州
carve_path(105, 108, 85, 105)  # 应天府→南昌
carve_path(85, 105, 75, 110)  # 南昌→鄱阳湖
carve_path(75, 110, 60, 80)  # 鄱阳湖→定远

# 东南分支（钟离县 → 定远 → 和州 → 太平府）
carve_path(60, 60, 60, 80)  # 钟离→定远（部分主干道）
carve_path(60, 80, 80, 85)  # 定远→和州
carve_path(80, 85, 95, 95)  # 和州→太平府
carve_path(95, 95, 105, 108)  # 太平府→应天府

# 南向分支（钟离县 → 定远 → 云南）
carve_path(60, 80, 30, 115)  # 定远→云南

# 西南分支（钟离县 → 四川）
carve_path(60, 60, 15, 95)  # 钟离→四川
carve_path(15, 95, 30, 115)  # 四川→云南

# 西向分支（钟离县 → 襄阳 → 元大都）
carve_path(60, 60, 35, 55)  # 钟离→襄阳
carve_path(35, 55, 15, 55)  # 襄阳→元大都
carve_path(15, 55, 20, 40)  # 元大都→长安

# 西北分支（钟离县 → 皇觉寺）
carve_path(60, 60, 50, 50)  # 钟离→皇觉寺
carve_path(50, 50, 35, 55)  # 皇觉寺→襄阳

# 北向分支（钟离县 → 北京）
carve_path(60, 60, 60, 10)  # 钟离→北京（部分主干道）

# ========== 3. 地图边界 ==========
# 北部雪山
for y in range(0, 8):
    for x in range(0, MAP_WIDTH):
        if new_data[y][x] == 25 and random.random() < 0.4:
            new_data[y][x] = 23  # snow_field

# 西部山脉
for x in range(0, 10):
    for y in range(0, MAP_HEIGHT):
        if new_data[y][x] == 25 and random.random() < 0.5:
            new_data[y][x] = 4  # mountain

# 南部沙漠/荒山
for y in range(MAP_HEIGHT - 8, MAP_HEIGHT):
    for x in range(0, MAP_WIDTH):
        if new_data[y][x] == 25 and random.random() < 0.3:
            new_data[y][x] = 5  # desert

# 东部水域
for x in range(MAP_WIDTH - 5, MAP_WIDTH):
    for y in range(0, MAP_HEIGHT):
        if new_data[y][x] == 25 and random.random() < 0.5:
            new_data[y][x] = 26  # water

# ========== 4. 装饰物填充（提高密度） ==========
# 树木（8%密度，常规）
tree_count = 0
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        if new_data[y][x] == 25 and random.random() < 0.08:
            new_data[y][x] = 7  # tree
            tree_count += 1

# 大型树木（15个）
large_tree_count = 0
attempts = 0
while large_tree_count < 15 and attempts < 1000:
    x = random.randint(0, MAP_WIDTH - 1)
    y = random.randint(0, MAP_HEIGHT - 1)
    if new_data[y][x] == 25:
        new_data[y][x] = 8  # tree2 (large)
        large_tree_count += 1
    attempts += 1

# 森林地块（2x2或3x3的密集树林）
forest_clusters = 0
for _ in range(12):
    cx = random.randint(5, MAP_WIDTH - 6)
    cy = random.randint(5, MAP_HEIGHT - 6)
    size = random.randint(2, 3)
    for dx in range(-size, size + 1):
        for dy in range(-size, size + 1):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                if new_data[ny][nx] == 25 and random.random() < 0.7:
                    new_data[ny][nx] = 2  # forest
    forest_clusters += 1

# 洞穴（8个）
cave_count = 0
attempts = 0
while cave_count < 8 and attempts < 500:
    x = random.randint(0, MAP_WIDTH - 1)
    y = random.randint(0, MAP_HEIGHT - 1)
    if new_data[y][x] == 25 or new_data[y][x] == 4:
        new_data[y][x] = 6  # cave
        cave_count += 1
    attempts += 1

# 花朵（散布装饰）
flower_count = 0
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        if new_data[y][x] == 25 and random.random() < 0.04:
            new_data[y][x] = 22  # flowers
            flower_count += 1

# 农田（麦田/稻田/菜地）- 主要分布在村庄附近
farm_count = 0
attempts = 0
farm_types = [10, 11, 24]  # wheat_field, rice_field, vegetable_field
while farm_count < 60 and attempts < 2000:
    x = random.randint(0, MAP_WIDTH - 1)
    y = random.randint(0, MAP_HEIGHT - 1)
    if new_data[y][x] == 25:
        # 检查附近是否有村庄/地点
        near_loc = False
        for loc_id, loc_info in locations_config.items():
            if abs(loc_info["x"] - x) < 8 and abs(loc_info["y"] - y) < 8:
                near_loc = True
                break
        if near_loc or random.random() < 0.5:
            new_data[y][x] = random.choice(farm_types)
            farm_count += 1
    attempts += 1

# 遗迹（5个）
ruins_count = 0
attempts = 0
while ruins_count < 5 and attempts < 500:
    x = random.randint(0, MAP_WIDTH - 1)
    y = random.randint(0, MAP_HEIGHT - 1)
    if new_data[y][x] == 25 or new_data[y][x] == 2:
        new_data[y][x] = 19  # ruins
        ruins_count += 1
    attempts += 1

# 围栏（道路两旁装饰）
fence_count = 0
for _ in range(30):
    x = random.randint(0, MAP_WIDTH - 1)
    y = random.randint(0, MAP_HEIGHT - 1)
    if new_data[y][x] == 25 and random.random() < 0.5:
        new_data[y][x] = 17  # fence
        fence_count += 1
    elif new_data[y][x] == 25 and random.random() < 0.3:
        new_data[y][x] = 18  # fence2
        fence_count += 1

# 房子（20个 - 散落在城镇附近）
for _ in range(20):
    # 随机选一个城镇
    loc_id = random.choice(list(locations_config.keys()))
    loc = locations_config[loc_id]
    for _ in range(5):
        dx = random.randint(-4, 4)
        dy = random.randint(-4, 4)
        nx, ny = loc["x"] + dx, loc["y"] + dy
        if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
            if new_data[ny][nx] == 25 or new_data[ny][nx] == 7:
                new_data[ny][nx] = random.choice([28, 29])  # house1, house2
                break

# 水井（每个主要城镇都加一个）
well_count = 0
for loc_id, loc in locations_config.items():
    if loc["type"] in ["town", "city", "village"]:
        for dx in [-2, 2]:
            for dy in [-2, 2]:
                nx, ny = loc["x"] + dx, loc["y"] + dy
                if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                    if new_data[ny][nx] in [25, 7]:
                        new_data[ny][nx] = random.choice([12, 13])  # well, well2
                        well_count += 1
                        break

# 桥（道路过河时）
bridge_count = 0
for x in range(0, MAP_WIDTH):
    for y in range(0, MAP_HEIGHT):
        if new_data[y][x] == 3 and x + 1 < MAP_WIDTH and new_data[y][x + 1] == 26:
            new_data[y][x] = 9  # bridge
            bridge_count += 1

# ========== 5. 怪物分布（20个） ==========
monster_count = 0
monster_types = {100: "狼", 101: "老虎", 102: "狮子"}
monster_distribution = [
    # 低级地区：狼
    (100, 45, 50), (100, 50, 55), (100, 55, 65), (100, 65, 55), (100, 70, 60),
    (100, 75, 60), (100, 80, 60), (100, 80, 75),
    # 中级地区：老虎
    (101, 90, 55), (101, 95, 50), (101, 85, 80), (101, 95, 85),
    (101, 35, 55), (101, 25, 60), (101, 30, 70),
    # 高级地区：狮子
    (102, 15, 55), (102, 20, 40), (102, 60, 10), (102, 110, 50),
    (102, 100, 115),
]

for monster_id, mx, my in monster_distribution:
    if 0 <= mx < MAP_WIDTH and 0 <= my < MAP_HEIGHT:
        if new_data[my][mx] in [25, 7, 2]:  # 在草地/树/森林
            new_data[my][mx] = monster_id
            monster_count += 1

# 城镇/特殊地点的特殊标记（房屋、城镇）
for loc_id, loc in locations_config.items():
    x, y = loc["x"], loc["y"]
    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
        # 在地点中心放置城镇标记
        if loc["type"] == "city":
            new_data[y][x] = 32  # town
        elif loc["type"] == "town":
            new_data[y][x] = 34  # village
        elif loc["type"] == "temple":
            new_data[y][x] = 28  # house1
        elif loc["type"] == "lake":
            new_data[y][x] = 26  # water

# 保存地图数据
data['maps']['main_map']['data'] = new_data
data['maps']['main_map']['locations'] = locations_config

# 保存
with open('maps.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"=== 地图重塑完成 ===")
print(f"地图尺寸: {MAP_WIDTH} x {MAP_HEIGHT}")
print(f"地点数量: {len(locations_config)}")
print(f"树木: {tree_count} (含大型树 {large_tree_count} 个)")
print(f"森林群: {forest_clusters}")
print(f"洞穴: {cave_count}")
print(f"花朵: {flower_count}")
print(f"农田: {farm_count}")
print(f"遗迹: {ruins_count}")
print(f"围栏: {fence_count}")
print(f"水井: {well_count}")
print(f"桥: {bridge_count}")
print(f"怪物: {monster_count}")
