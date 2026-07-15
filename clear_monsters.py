#!/usr/bin/env python3
# 清除所有怪物

import json

# 读取地图文件
with open('maps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 获取地图数据
map_data = data['maps']['main_map']['data']

# 清除所有怪物
monster_ids = [100, 101, 102]  # 狼、老虎、狮子
monsters_cleared = 0

for y, row in enumerate(map_data):
    for x, tile_id in enumerate(row):
        if tile_id in monster_ids:
            map_data[y][x] = 27  # 恢复为道路
            monsters_cleared += 1

print(f"清除了 {monsters_cleared} 个怪物")

# 保存修改后的地图文件
with open('maps.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("怪物清除完成！")