#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
历史写实风格复杂地图设计：
- 22个地点按真实地理方位布局
- 每个主要城镇有独立的局部区域（农田、市集、城墙）
- 主干道 + 次干道 + 小路形成复杂路网
- 边界有自然地形（山脉、水域、沙漠、雪山）
- 保留足够可探索空间
"""

import json
import random
import math

random.seed(2024)

MAP_WIDTH = 120
MAP_HEIGHT = 120

# 加载现有数据
with open('maps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# ============ 22个地点（按真实地理方位）============
# 中国大致方位：北→北京/元大都，东北→辽东，东→沿海，南→广州，西南→云南/四川，西→长安/襄阳
locations_config = {
    # 中心枢纽：钟离县（凤阳，今安徽凤阳）
    "zhongli": {"name": "钟离县", "x": 60, "y": 60, "min_level": 1, "type": "capital"},
    # 西北方向
    "huangjue_si": {"name": "皇觉寺", "x": 50, "y": 50, "min_level": 2, "type": "temple"},
    "xiangyang": {"name": "襄阳", "x": 35, "y": 55, "min_level": 4, "type": "town"},
    "yuan_dadu": {"name": "元大都", "x": 15, "y": 55, "min_level": 14, "type": "city"},
    "changan": {"name": "长安", "x": 22, "y": 38, "min_level": 18, "type": "city"},
    # 北向
    "beijing": {"name": "北京", "x": 60, "y": 12, "min_level": 17, "type": "city"},
    # 东北
    "haizhou": {"name": "海州", "x": 90, "y": 18, "min_level": 8, "type": "town"},
    # 东向
    "huaixi": {"name": "淮西", "x": 78, "y": 60, "min_level": 3, "type": "village"},
    "henan": {"name": "河南", "x": 90, "y": 55, "min_level": 4, "type": "town"},
    "huizhou": {"name": "徽州", "x": 108, "y": 75, "min_level": 9, "type": "town"},
    "suzhou": {"name": "苏州", "x": 112, "y": 62, "min_level": 13, "type": "city"},
    "zhedong": {"name": "浙东", "x": 110, "y": 48, "min_level": 10, "type": "village"},
    "hangzhou": {"name": "杭州", "x": 115, "y": 38, "min_level": 11, "type": "city"},
    "jinhua": {"name": "金华", "x": 106, "y": 28, "min_level": 12, "type": "town"},
    # 东南
    "yingtian_fu": {"name": "应天府", "x": 102, "y": 108, "min_level": 8, "type": "capital"},
    "nanchang": {"name": "南昌", "x": 82, "y": 102, "min_level": 7, "type": "town"},
    "poyang_hu": {"name": "鄱阳湖", "x": 73, "y": 108, "min_level": 12, "type": "lake"},
    "taiping_fu": {"name": "太平府", "x": 95, "y": 95, "min_level": 7, "type": "town"},
    "hezhou": {"name": "和州", "x": 80, "y": 85, "min_level": 6, "type": "town"},
    "guangzhou": {"name": "广州", "x": 95, "y": 115, "min_level": 9, "type": "city"},
    # 南向
    "dingyuan": {"name": "定远", "x": 60, "y": 82, "min_level": 5, "type": "village"},
    # 西/西南
    "sichuan": {"name": "四川", "x": 18, "y": 92, "min_level": 15, "type": "town"},
    "yunnan": {"name": "云南", "x": 30, "y": 112, "min_level": 16, "type": "town"},
}

# 初始化地图为草地
new_data = [[25 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]


def carve_l_path(x1, y1, x2, y2, tile_id=3):
    """L形路径：水平+垂直"""
    # 水平段
    sx, ex = min(x1, x2), max(x1, x2)
    for x in range(sx, ex + 1):
        if 0 <= x < MAP_WIDTH and 0 <= y1 < MAP_HEIGHT:
            new_data[y1][x] = tile_id
    # 垂直段
    sy, ey = min(y1, y2), max(y1, y2)
    for y in range(sy, ey + 1):
        if 0 <= x2 < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            new_data[y][x2] = tile_id


def carve_zigzag(x1, y1, x2, y2, tile_id=3):
    """之字形复杂路径"""
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return
    # 中间添加曲折
    mid_x = (x1 + x2) // 2
    mid_y = (y1 + y2) // 2
    # 添加2个拐点形成Z形
    offset = min(8, abs(dx) // 3, abs(dy) // 3)
    if offset < 2:
        carve_l_path(x1, y1, x2, y2, tile_id)
        return
    if abs(dx) > abs(dy):
        # 横向为主
        p1y = y1 + (offset if dy > 0 else -offset)
        p2y = y2 - (offset if dy > 0 else -offset)
        carve_l_path(x1, y1, mid_x, p1y, tile_id)
        carve_l_path(mid_x, p1y, x2, p2y, tile_id)
        carve_l_path(x2, p2y, x2, y2, tile_id)
    else:
        # 纵向为主
        p1x = x1 + (offset if dx > 0 else -offset)
        p2x = x2 - (offset if dx > 0 else -offset)
        carve_l_path(x1, y1, p1x, mid_y, tile_id)
        carve_l_path(p1x, mid_y, p2x, y2, tile_id)
        carve_l_path(p2x, y2, x2, y2, tile_id)


# ============ 1. 边界自然地形 ============
# 北部雪山带
for y in range(0, 6):
    for x in range(0, MAP_WIDTH):
        if new_data[y][x] == 25 and random.random() < 0.6:
            new_data[y][x] = 23  # snow_field

# 西部山脉
for x in range(0, 8):
    for y in range(0, MAP_HEIGHT):
        if new_data[y][x] == 25 and random.random() < 0.65:
            new_data[y][x] = 4  # mountain

# 西南沙漠/荒山
for x in range(0, 25):
    for y in range(85, MAP_HEIGHT):
        if new_data[y][x] == 25 and random.random() < 0.4:
            new_data[y][x] = 5  # desert

# 东部海域
for x in range(MAP_WIDTH - 4, MAP_WIDTH):
    for y in range(0, MAP_HEIGHT):
        if new_data[y][x] == 25 and random.random() < 0.7:
            new_data[y][x] = 26  # water

# 东南沿海
for y in range(95, MAP_HEIGHT):
    for x in range(85, MAP_WIDTH):
        if new_data[y][x] == 25 and random.random() < 0.5:
            new_data[y][x] = 26  # water

# 鄱阳湖水域
for dx in range(-3, 4):
    for dy in range(-2, 3):
        nx, ny = 73 + dx, 108 + dy
        if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
            if random.random() < 0.85:
                new_data[ny][nx] = 26

# ============ 2. 主干道（4方向十字）============
# 东西向主干道（y=60） - 2格宽
for x in range(0, MAP_WIDTH):
    new_data[60][x] = 3
    new_data[61][x] = 3

# 南北向主干道（x=60） - 2格宽
for y in range(0, MAP_HEIGHT):
    new_data[y][60] = 3
    new_data[y][61] = 3

# 钟离县中心广场
for dx in range(-3, 4):
    for dy in range(-3, 4):
        nx, ny = 60 + dx, 60 + dy
        if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
            new_data[ny][nx] = 3

# ============ 3. 主干道连接所有大城市 ============
# 西北支线：钟离县 → 皇觉寺 → 襄阳 → 元大都
carve_zigzag(60, 60, 50, 50, 3)
carve_zigzag(50, 50, 35, 55, 3)
carve_zigzag(35, 55, 15, 55, 3)
carve_zigzag(15, 55, 22, 38, 3)  # 元大都→长安

# 北向：钟离县 → 北京
carve_zigzag(60, 60, 60, 12, 3)

# 东北支线：北京 → 海州
carve_zigzag(60, 12, 90, 18, 3)

# 东向：钟离县 → 淮西 → 河南
carve_zigzag(60, 60, 78, 60, 3)
carve_zigzag(78, 60, 90, 55, 3)

# 东向延伸：河南 → 浙东 → 杭州 → 金华
carve_zigzag(90, 55, 110, 48, 3)
carve_zigzag(110, 48, 115, 38, 3)
carve_zigzag(110, 48, 106, 28, 3)

# 东南支线：河南 → 徽州 → 苏州
carve_zigzag(90, 55, 108, 75, 3)
carve_zigzag(108, 75, 112, 62, 3)
carve_zigzag(112, 62, 115, 38, 3)  # 苏州→杭州

# 东南主线：钟离县 → 定远 → 和州 → 太平府 → 应天府
carve_zigzag(60, 60, 60, 82, 3)
carve_zigzag(60, 82, 80, 85, 3)
carve_zigzag(80, 85, 95, 95, 3)
carve_zigzag(95, 95, 102, 108, 3)

# 应天府辐射：应天府 → 南昌 → 鄱阳湖 / 应天府 → 广州
carve_zigzag(102, 108, 82, 102, 3)
carve_zigzag(82, 102, 73, 108, 3)  # 鄱阳湖
carve_zigzag(102, 108, 95, 115, 3)  # 广州

# 南向：定远 → 云南
carve_zigzag(60, 82, 30, 112, 3)

# 西向：钟离县 → 四川
carve_zigzag(60, 60, 18, 92, 3)
carve_zigzag(18, 92, 30, 112, 3)  # 四川→云南

# ============ 4. 次干道（乡镇连接）============
# 钟离县 → 周边
carve_zigzag(60, 60, 73, 108, 3)  # 钟离县→鄱阳湖（穿城而过）

# 河南 ↔ 应天府（横跨）
carve_zigzag(90, 55, 102, 108, 3)

# 襄阳 ↔ 长安
carve_zigzag(35, 55, 22, 38, 3)

# ============ 5. 城镇局部区域（农田+水井+建筑）============
def build_town_area(cx, cy, size=3, has_walls=True):
    """在城镇周围建立局部区域"""
    # 城镇中心放town标记
    if 0 <= cx < MAP_WIDTH and 0 <= cy < MAP_HEIGHT:
        if locations_config.get([k for k, v in locations_config.items() if v['x']==cx and v['y']==cy][0], {}).get('type') == 'city':
            new_data[cy][cx] = 32  # town
        else:
            new_data[cy][cx] = 34  # village

    # 周围农田（东南西北分散）
    farm_tiles = [10, 11, 24]  # wheat, rice, vegetable
    for _ in range(size * 2):
        for _ in range(5):
            dx = random.randint(-size, size)
            dy = random.randint(-size, size)
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                if new_data[ny][nx] == 25:
                    new_data[ny][nx] = random.choice(farm_tiles)
                    break

    # 水井
    for _ in range(2):
        for _ in range(10):
            dx = random.randint(-size, size)
            dy = random.randint(-size, size)
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                if new_data[ny][nx] == 25:
                    new_data[ny][nx] = random.choice([12, 13])
                    break

    # 房屋
    for _ in range(3):
        for _ in range(10):
            dx = random.randint(-size, size)
            dy = random.randint(-size, size)
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                if new_data[ny][nx] in [25, 7]:
                    new_data[ny][nx] = random.choice([28, 29])
                    break


# 为主要城镇建立局部区域
for loc_id, loc in locations_config.items():
    if loc['type'] in ['city', 'capital', 'town']:
        build_town_area(loc['x'], loc['y'], size=3)
    elif loc['type'] == 'village':
        build_town_area(loc['x'], loc['y'], size=2)
    elif loc['type'] == 'temple':
        # 寺庙：周围多一些花
        for _ in range(8):
            dx = random.randint(-3, 3)
            dy = random.randint(-3, 3)
            nx, ny = loc['x'] + dx, loc['y'] + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                if new_data[ny][nx] == 25:
                    new_data[ny][nx] = 22  # flowers

# ============ 6. 自然装饰（保留可探索空间）============
# 树木（5%密度 - 中等）
tree_count = 0
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        if new_data[y][x] == 25 and random.random() < 0.05:
            new_data[y][x] = 7
            tree_count += 1

# 大型树木（10个）
large_tree_count = 0
attempts = 0
while large_tree_count < 10 and attempts < 500:
    x = random.randint(0, MAP_WIDTH - 1)
    y = random.randint(0, MAP_HEIGHT - 1)
    if new_data[y][x] == 25:
        new_data[y][x] = 8
        large_tree_count += 1
    attempts += 1

# 森林群（8个 - 比之前少，留更多空间）
forest_clusters = 0
for _ in range(8):
    cx = random.randint(8, MAP_WIDTH - 8)
    cy = random.randint(8, MAP_HEIGHT - 8)
    # 放在远离主路的位置
    if 50 <= cx <= 70 and 50 <= cy <= 70:
        continue
    size = random.randint(2, 3)
    for dx in range(-size, size + 1):
        for dy in range(-size, size + 1):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                if new_data[ny][nx] == 25 and random.random() < 0.6:
                    new_data[ny][nx] = 2
    forest_clusters += 1

# 洞穴（5个）
cave_count = 0
attempts = 0
while cave_count < 5 and attempts < 500:
    x = random.randint(0, MAP_WIDTH - 1)
    y = random.randint(0, MAP_HEIGHT - 1)
    if new_data[y][x] in [25, 4, 2]:
        new_data[y][x] = 6
        cave_count += 1
    attempts += 1

# 花朵（2%密度）
flower_count = 0
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        if new_data[y][x] == 25 and random.random() < 0.02:
            new_data[y][x] = 22
            flower_count += 1

# 遗迹（3个）
ruins_count = 0
attempts = 0
while ruins_count < 3 and attempts < 500:
    x = random.randint(0, MAP_WIDTH - 1)
    y = random.randint(0, MAP_HEIGHT - 1)
    if new_data[y][x] in [25, 2]:
        new_data[y][x] = 19
        ruins_count += 1
    attempts += 1

# 围栏（道路两旁）
fence_count = 0
for _ in range(20):
    x = random.randint(0, MAP_WIDTH - 1)
    y = random.randint(0, MAP_HEIGHT - 1)
    if new_data[y][x] == 25 and random.random() < 0.5:
        new_data[y][x] = random.choice([17, 18])
        fence_count += 1

# 桥（水域+道路交汇处）
bridge_count = 0
for x in range(1, MAP_WIDTH - 1):
    for y in range(MAP_HEIGHT):
        if new_data[y][x] == 3 and (new_data[y][x-1] == 26 or new_data[y][x+1] == 26):
            new_data[y][x] = 9
            bridge_count += 1

# ============ 7. 怪物分布（20个）============
monster_positions = [
    (100, 45, 50), (100, 50, 55), (100, 55, 65), (100, 65, 55), (100, 70, 60),
    (100, 75, 60), (100, 80, 60), (100, 80, 75), (100, 65, 75),
    (101, 90, 55), (101, 95, 50), (101, 85, 80), (101, 95, 85),
    (101, 35, 55), (101, 25, 60), (101, 30, 70),
    (102, 15, 55), (102, 20, 40), (102, 60, 12), (102, 110, 48),
]

monster_count = 0
for mid, mx, my in monster_positions:
    if 0 <= mx < MAP_WIDTH and 0 <= my < MAP_HEIGHT:
        if new_data[my][mx] in [25, 7, 2]:
            new_data[my][mx] = mid
            monster_count += 1

# 鄱阳湖特殊处理
if 0 <= 73 < MAP_WIDTH and 0 <= 108 < MAP_HEIGHT:
    new_data[108][73] = 26  # 水

# 保存地图
data['maps']['main_map']['data'] = new_data
data['maps']['main_map']['locations'] = locations_config

with open('maps.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 统计
from collections import Counter
cnt = Counter()
for row in new_data:
    for t in row:
        cnt[t] += 1

print(f"=== 历史写实风格复杂地图生成完成 ===")
print(f"地图尺寸: {MAP_WIDTH} x {MAP_HEIGHT}")
print(f"地点数量: {len(locations_config)}")
print(f"路径格数: {cnt.get(3, 0)}")
print(f"草地（可探索）: {cnt.get(25, 0)}")
print(f"树木: {cnt.get(7, 0)} (大型 {cnt.get(8, 0)})")
print(f"森林: {cnt.get(2, 0)}")
print(f"水域: {cnt.get(26, 0)}")
print(f"山脉: {cnt.get(4, 0)}")
print(f"沙漠: {cnt.get(5, 0)}")
print(f"雪山: {cnt.get(23, 0)}")
print(f"洞穴: {cnt.get(6, 0)}")
print(f"花朵: {cnt.get(22, 0)}")
print(f"农田: {cnt.get(10, 0) + cnt.get(11, 0) + cnt.get(24, 0)}")
print(f"遗迹: {cnt.get(19, 0)}")
print(f"围栏: {cnt.get(17, 0) + cnt.get(18, 0)}")
print(f"水井: {cnt.get(12, 0) + cnt.get(13, 0)}")
print(f"桥: {cnt.get(9, 0)}")
print(f"房屋: {cnt.get(28, 0) + cnt.get(29, 0)}")
print(f"城镇/村庄: {cnt.get(32, 0) + cnt.get(34, 0)}")
print(f"怪物: {cnt.get(100, 0) + cnt.get(101, 0) + cnt.get(102, 0)}")
