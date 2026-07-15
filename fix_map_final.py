#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修正：保持22个地点（移除海州），补充怪物到20个"""

import json
import random

random.seed(456)

with open('maps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

map_data = data['maps']['main_map']['data']
locations = data['maps']['main_map']['locations']
MAP_WIDTH = data['maps']['main_map']['width']
MAP_HEIGHT = data['maps']['main_map']['height']

# 移除海州（保持22个地点）
if 'haizhou' in locations:
    del locations['haizhou']
    print(f"已移除海州，当前地点数: {len(locations)}")

# 统计当前怪物
monster_count = 0
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        if map_data[y][x] in [100, 101, 102]:
            monster_count += 1

print(f"当前怪物数: {monster_count}")

# 补充怪物到20个
# 低级地区：狼（钟离县周围及主要路线）
wolf_positions = [
    (45, 50), (50, 55), (55, 65), (65, 55), (65, 70),
    (70, 65), (75, 60), (80, 65), (80, 75),
]
# 中级地区：老虎（外部区域）
tiger_positions = [
    (88, 55), (95, 65), (85, 80), (95, 85),
    (35, 55), (28, 65), (30, 75), (40, 80),
    (100, 50), (108, 60),
]
# 高级地区：狮子（边界危险区域）
lion_positions = [
    (15, 55), (20, 40), (60, 12), (110, 50),
    (60, 110), (95, 115),
]

all_positions = [(100, x, y) for x, y in wolf_positions] + \
                [(101, x, y) for x, y in tiger_positions] + \
                [(102, x, y) for x, y in lion_positions]

added = 0
for mid, mx, my in all_positions:
    if 0 <= mx < MAP_WIDTH and 0 <= my < MAP_HEIGHT:
        if map_data[my][mx] in [25, 7, 2, 5]:  # 草地/树/森林/沙漠
            map_data[my][mx] = mid
            monster_count += 1
            added += 1
            if monster_count >= 20:
                break

print(f"新增怪物: {added}，总数: {monster_count}")

data['maps']['main_map']['data'] = map_data
data['maps']['main_map']['locations'] = locations

with open('maps.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"地点数: {len(locations)}")
print("=== 修正完成 ===")
