#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补充怪物到20个，并验证地点名称"""

import json
import random

random.seed(123)

with open('maps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

map_data = data['maps']['main_map']['data']
MAP_WIDTH = data['maps']['main_map']['width']
MAP_HEIGHT = data['maps']['main_map']['height']

# 现有怪物
monster_count = 0
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        if map_data[y][x] in [100, 101, 102]:
            monster_count += 1

print(f"当前怪物数: {monster_count}")

# 补充怪物到20个
# 低级地区（钟离县附近）放狼
wolf_positions = [
    (45, 50), (50, 55), (55, 65), (65, 55), (70, 60),
    (75, 60), (80, 60), (80, 75),
]
# 中级地区（外圈）放老虎
tiger_positions = [
    (90, 55), (95, 50), (85, 80), (95, 85),
    (35, 55), (25, 60), (30, 70), (40, 75),
]
# 高级地区（边界）放狮子
lion_positions = [
    (15, 55), (20, 40), (60, 10), (110, 50),
    (100, 115), (15, 95), (30, 115), (45, 115),
]

all_positions = [(100, x, y) for x, y in wolf_positions] + \
                [(101, x, y) for x, y in tiger_positions] + \
                [(102, x, y) for x, y in lion_positions]

added = 0
for mid, mx, my in all_positions:
    if monster_count >= 20:
        break
    if 0 <= mx < MAP_WIDTH and 0 <= my < MAP_HEIGHT:
        if map_data[my][mx] in [25, 7, 2, 5]:  # 草地/树/森林/沙漠
            map_data[my][mx] = mid
            monster_count += 1
            added += 1

print(f"新增怪物: {added}, 总数: {monster_count}")

data['maps']['main_map']['data'] = map_data

with open('maps.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("怪物补充完成！")
