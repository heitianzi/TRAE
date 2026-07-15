#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补充怪物到20个"""

import json
import random

random.seed(789)

with open('maps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

map_data = data['maps']['main_map']['data']
MAP_WIDTH = data['maps']['main_map']['width']
MAP_HEIGHT = data['maps']['main_map']['height']

# 统计
monster_count = 0
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        if map_data[y][x] in [100, 101, 102]:
            monster_count += 1

print(f"当前怪物数: {monster_count}")

# 补充8个怪物到20个
additional = [
    (100, 55, 50), (100, 75, 75),  # 狼
    (101, 100, 80), (101, 50, 85),  # 老虎
    (102, 100, 117), (102, 70, 110),  # 狮子
    (101, 115, 47), (100, 60, 70),  # 中级
]

added = 0
for mid, mx, my in additional:
    if 0 <= mx < MAP_WIDTH and 0 <= my < MAP_HEIGHT:
        if map_data[my][mx] in [25, 7, 2]:
            map_data[my][mx] = mid
            monster_count += 1
            added += 1

print(f"新增怪物: {added}, 总数: {monster_count}")

data['maps']['main_map']['data'] = map_data

with open('maps.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("=== 怪物补充完成 ===")
