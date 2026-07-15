#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据用户参考图重制地图：
- 22个地点，位置精确按参考图布局
- 十字路网 + 四方向分支道路
- 钟离县在地图正中心
- 所有主要路线连通
- 丰富装饰
"""

import json
import random

random.seed(888)

MAP_WIDTH = 120
MAP_HEIGHT = 120
CENTER_X = 60
CENTER_Y = 60

with open('maps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# ========== 22个地点（按参考图精确坐标）==========
# 钟离县位于正中心
locations_config = {
    "zhongli":       {"name": "钟离县",   "x": 60,  "y": 60, "min_level": 1,  "type": "capital"},  # 中心（红点）
    # 北方
    "beijing":       {"name": "北京",     "x": 60,  "y": 10, "min_level": 17, "type": "city"},
    # 东北
    "hangzhou":      {"name": "杭州",     "x": 115, "y": 28, "min_level": 11, "type": "city"},
    "jinhua":        {"name": "金华",     "x": 105, "y": 30, "min_level": 12, "type": "town"},
    "zhedong":       {"name": "浙东",     "x": 115, "y": 47, "min_level": 10, "type": "village"},
    # 东
    "henan":         {"name": "河南",     "x": 100, "y": 55, "min_level": 4,  "type": "town"},
    "suzhou":        {"name": "苏州",     "x": 113, "y": 60, "min_level": 13, "type": "city"},
    "huizhou":       {"name": "徽州",     "x": 113, "y": 75, "min_level": 9,  "type": "town"},
    # 东南
    "yingtian_fu":   {"name": "应天府",   "x": 105, "y": 113, "min_level": 8, "type": "capital"},
    "guangzhou":     {"name": "广州",     "x": 95,  "y": 117, "min_level": 9,  "type": "city"},
    "nanchang":      {"name": "南昌",     "x": 87,  "y": 100, "min_level": 7,  "type": "town"},
    "poyang_hu":     {"name": "鄱阳湖",   "x": 70,  "y": 110, "min_level": 12, "type": "lake"},
    "taiping_fu":    {"name": "太平府",   "x": 100, "y": 95, "min_level": 7,  "type": "town"},
    "hezhou":        {"name": "和州",     "x": 87,  "y": 88, "min_level": 6,  "type": "town"},
    # 南
    "dingyuan":      {"name": "定远",     "x": 50,  "y": 78, "min_level": 5,  "type": "village"},
    "yunnan":        {"name": "云南",     "x": 35,  "y": 113, "min_level": 16, "type": "town"},
    # 西
    "sichuan":       {"name": "四川",     "x": 15,  "y": 100, "min_level": 15, "type": "town"},
    # 西北
    "yuan_dadu":     {"name": "元大都",   "x": 10,  "y": 47, "min_level": 14, "type": "city"},
    "changan":       {"name": "长安",     "x": 13,  "y": 30, "min_level": 18, "type": "city"},
    "xiangyang":     {"name": "襄阳",     "x": 28,  "y": 55, "min_level": 4,  "type": "town"},
    "huangjue_si":   {"name": "皇觉寺",   "x": 42,  "y": 47, "min_level": 2,  "type": "temple"},
    "huaixi":        {"name": "淮西",     "x": 78,  "y": 60, "min_level": 3,  "type": "village"},
}

# 初始化为草地
new_data = [[25 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]


def carve_line(x1, y1, x2, y2, tile_id=3):
    """直线（L形）"""
    sx, ex = min(x1, x2), max(x1, x2)
    for x in range(sx, ex + 1):
        if 0 <= x < MAP_WIDTH and 0 <= y1 < MAP_HEIGHT:
            new_data[y1][x] = tile_id
    sy, ey = min(y1, y2), max(y1, y2)
    for y in range(sy, ey + 1):
        if 0 <= x2 < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            new_data[y][x2] = tile_id


# ========== 1. 十字主干道（2格宽）==========
# 东西向主干道（钟离县水平线）
for x in range(0, MAP_WIDTH):
    new_data[60][x] = 3
    new_data[61][x] = 3
# 南北向主干道（钟离县垂直线）
for y in range(0, MAP_HEIGHT):
    new_data[y][60] = 3
    new_data[y][61] = 3

# 钟离县中心广场
for dx in range(-2, 3):
    for dy in range(-2, 3):
        nx, ny = 60 + dx, 60 + dy
        if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
            new_data[ny][nx] = 3

# ========== 2. 四方向分支道路（按参考图）==========
# --- 北向：北京 ---
# 钟离县 → 北京（沿南北主干道已连通）

# --- 东向分支 ---
# 钟离县 → 淮西（沿主干道）
# 淮西 → 河南
carve_line(78, 60, 100, 55)
# 河南 → 浙东
carve_line(100, 55, 115, 47)
# 浙东 → 杭州
carve_line(115, 47, 115, 28)
# 浙东 → 金华
carve_line(115, 47, 105, 30)
# 河南 → 苏州
carve_line(100, 55, 113, 60)
# 苏州 → 杭州
carve_line(113, 60, 115, 28)
# 苏州 → 徽州
carve_line(113, 60, 113, 75)

# --- 东南分支：钟离县 → 和州 → 太平府 → 应天府 → 广州/南昌/鄱阳湖 ---
# 钟离县 → 和州
carve_line(60, 60, 87, 88)
# 和州 → 太平府
carve_line(87, 88, 100, 95)
# 太平府 → 应天府
carve_line(100, 95, 105, 113)
# 应天府 → 广州
carve_line(105, 113, 95, 117)
# 太平府 → 南昌
carve_line(100, 95, 87, 100)
# 南昌 → 鄱阳湖
carve_line(87, 100, 70, 110)
# 鄱阳湖 → 钟离县（连回主干道）
carve_line(70, 110, 60, 60)

# --- 南向：钟离县 → 定远 → 云南 ---
# 钟离县 → 定远
carve_line(60, 60, 50, 78)
# 定远 → 云南
carve_line(50, 78, 35, 113)

# --- 西向：钟离县 → 四川 ---
# 钟离县 → 四川
carve_line(60, 60, 15, 100)
# 四川 → 云南
carve_line(15, 100, 35, 113)

# --- 西北分支：钟离县 → 皇觉寺 → 襄阳 → 元大都 → 长安 ---
# 钟离县 → 皇觉寺
carve_line(60, 60, 42, 47)
# 皇觉寺 → 襄阳
carve_line(42, 47, 28, 55)
# 襄阳 → 元大都
carve_line(28, 55, 10, 47)
# 元大都 → 长安
carve_line(10, 47, 13, 30)

# ========== 3. 城镇局部区域 ==========
def build_local_area(cx, cy, loc_type):
    """在城镇周围建立局部区域"""
    if loc_type == 'lake':
        # 鄱阳湖：水域标记
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                    if new_data[ny][nx] == 25:
                        new_data[ny][nx] = 26
        return

    # 城镇中心
    if 0 <= cx < MAP_WIDTH and 0 <= cy < MAP_HEIGHT:
        if loc_type == 'city':
            new_data[cy][cx] = 32  # town
        else:
            new_data[cy][cx] = 34  # village

    # 周边农田
    farm_tiles = [10, 11, 24]
    farm_count = 8 if loc_type in ['city', 'capital'] else 4
    for _ in range(farm_count):
        for _ in range(15):
            dx = random.randint(-3, 3)
            dy = random.randint(-3, 3)
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                if new_data[ny][nx] == 25:
                    new_data[ny][nx] = random.choice(farm_tiles)
                    break

    # 水井
    for _ in range(2):
        for _ in range(15):
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                if new_data[ny][nx] == 25:
                    new_data[ny][nx] = random.choice([12, 13])
                    break

    # 房屋
    for _ in range(3):
        for _ in range(15):
            dx = random.randint(-3, 3)
            dy = random.randint(-3, 3)
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                if new_data[ny][nx] in [25, 7]:
                    new_data[ny][nx] = random.choice([28, 29])
                    break


for loc_id, loc in locations_config.items():
    build_local_area(loc['x'], loc['y'], loc['type'])

# ========== 4. 装饰物填充 ==========
# 树木（8%密度）
tree_count = 0
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        if new_data[y][x] == 25 and random.random() < 0.08:
            new_data[y][x] = 7
            tree_count += 1

# 大型树木（15个）
large_tree_count = 0
attempts = 0
while large_tree_count < 15 and attempts < 1000:
    x = random.randint(0, MAP_WIDTH - 1)
    y = random.randint(0, MAP_HEIGHT - 1)
    if new_data[y][x] == 25:
        new_data[y][x] = 8
        large_tree_count += 1
    attempts += 1

# 森林群（10个，分布在远离道路区域）
forest_clusters = 0
for _ in range(10):
    for _ in range(20):
        cx = random.randint(5, MAP_WIDTH - 5)
        cy = random.randint(5, MAP_HEIGHT - 5)
        # 不在主干道上
        if (cy == 60 or cy == 61 or cx == 60 or cx == 61):
            continue
        size = random.randint(2, 3)
        for dx in range(-size, size + 1):
            for dy in range(-size, size + 1):
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                    if new_data[ny][nx] == 25 and random.random() < 0.6:
                        new_data[ny][nx] = 2
        forest_clusters += 1
        break

# 洞穴（8个）
cave_count = 0
attempts = 0
while cave_count < 8 and attempts < 1000:
    x = random.randint(0, MAP_WIDTH - 1)
    y = random.randint(0, MAP_HEIGHT - 1)
    if new_data[y][x] in [25, 4, 2]:
        new_data[y][x] = 6
        cave_count += 1
    attempts += 1

# 花朵（散布）
flower_count = 0
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        if new_data[y][x] == 25 and random.random() < 0.03:
            new_data[y][x] = 22
            flower_count += 1

# 遗迹（5个）
ruins_count = 0
attempts = 0
while ruins_count < 5 and attempts < 1000:
    x = random.randint(0, MAP_WIDTH - 1)
    y = random.randint(0, MAP_HEIGHT - 1)
    if new_data[y][x] in [25, 2]:
        new_data[y][x] = 19
        ruins_count += 1
    attempts += 1

# 围栏
fence_count = 0
for _ in range(30):
    x = random.randint(0, MAP_WIDTH - 1)
    y = random.randint(0, MAP_HEIGHT - 1)
    if new_data[y][x] == 25 and random.random() < 0.5:
        new_data[y][x] = random.choice([17, 18])
        fence_count += 1

# 桥（道路与水域交汇）
bridge_count = 0
for x in range(1, MAP_WIDTH - 1):
    for y in range(1, MAP_HEIGHT - 1):
        if new_data[y][x] == 3:
            neighbors = [new_data[y-1][x], new_data[y+1][x], new_data[y][x-1], new_data[y][x+1]]
            if 26 in neighbors:
                new_data[y][x] = 9
                bridge_count += 1

# 边界自然地形
# 北部雪山
for y in range(0, 5):
    for x in range(MAP_WIDTH):
        if new_data[y][x] == 25 and random.random() < 0.5:
            new_data[y][x] = 23
# 西部山脉
for x in range(0, 6):
    for y in range(MAP_HEIGHT):
        if new_data[y][x] == 25 and random.random() < 0.5:
            new_data[y][x] = 4
# 西南沙漠
for x in range(0, 20):
    for y in range(95, MAP_HEIGHT):
        if new_data[y][x] == 25 and random.random() < 0.3:
            new_data[y][x] = 5
# 东部海域
for x in range(MAP_WIDTH - 3, MAP_WIDTH):
    for y in range(MAP_HEIGHT):
        if new_data[y][x] == 25 and random.random() < 0.6:
            new_data[y][x] = 26

# ========== 5. 怪物分布（20个）==========
monster_positions = [
    # 狼（低级，1-5级区域）- 钟离县周围
    (100, 50, 55), (100, 55, 65), (100, 65, 55), (100, 65, 70),
    (100, 70, 60), (100, 75, 60), (100, 80, 70), (100, 45, 60),
    # 老虎（中级，5-10级区域）- 中等距离
    (101, 90, 55), (101, 100, 50), (101, 85, 80), (101, 95, 85),
    (101, 30, 55), (101, 25, 70), (101, 35, 70), (101, 40, 80),
    # 狮子（高级，10+级区域）- 边界
    (102, 13, 30), (102, 10, 47), (102, 60, 10), (102, 105, 113),
]

monster_count = 0
for mid, mx, my in monster_positions:
    if 0 <= mx < MAP_WIDTH and 0 <= my < MAP_HEIGHT:
        if new_data[my][mx] in [25, 7, 2]:
            new_data[my][mx] = mid
            monster_count += 1

# 保存
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

print(f"=== 参考图地图生成完成 ===")
print(f"地图尺寸: {MAP_WIDTH} x {MAP_HEIGHT}")
print(f"地点数量: {len(locations_config)}")
print(f"路径(路): {cnt.get(3, 0)}")
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
print(f"怪物: {monster_count}")
