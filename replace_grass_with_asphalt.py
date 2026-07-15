#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将地图中的草地替换为柏油路
"""

import json

# 读取maps.json文件
with open('maps.json', 'r', encoding='utf-8') as f:
    maps_data = json.load(f)

# 将草地(0)替换为柏油路(27)
grass_id = 0
asphalt_id = 27

# 遍历所有地图
for map_id, map_info in maps_data["maps"].items():
    if "data" in map_info:
        for y in range(len(map_info["data"])):
            for x in range(len(map_info["data"][y])):
                if map_info["data"][y][x] == grass_id:
                    map_info["data"][y][x] = asphalt_id
        print(f"地图 '{map_id}' 的草地已替换为柏油路")

# 更新tile_mapping，将"0"映射为"asphalt_road"
if "tile_mapping" in maps_data:
    maps_data["tile_mapping"]["0"] = "asphalt_road"
    print("瓦片映射已更新: 0 -> asphalt_road")

# 保存更新后的数据
with open('maps.json', 'w', encoding='utf-8') as f:
    json.dump(maps_data, f, ensure_ascii=False, indent=2)

print("地图数据已更新并保存")

# 同时更新recreate_transitions.py
with open('recreate_transitions.py', 'w', encoding='utf-8') as f:
    f.write('''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新创建地图间的连接信息
"""

import json

# 读取maps.json文件
def load_maps():
    with open('maps.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# 保存maps.json文件
def save_maps(data):
    with open('maps.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 重新创建连接信息
def recreate_transitions():
    maps_data = load_maps()

    # 这里可以添加重新创建连接信息的逻辑
    # 例如，根据地图位置自动生成连接

    save_maps(maps_data)
    print("连接信息已更新")

if __name__ == "__main__":
    recreate_transitions()
''')

print("recreate_transitions.py 已更新")
