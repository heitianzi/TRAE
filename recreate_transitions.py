#!/usr/bin/env python3
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
    
    # 为每个地点添加连接信息
    for map_id, map_info in maps_data['maps'].items():
        if 'locations' in map_info:
            for loc_id, loc_info in map_info['locations'].items():
                # 这里可以添加更复杂的连接逻辑
                pass
    
    save_maps(maps_data)
    print("连接信息已更新")

if __name__ == "__main__":
    recreate_transitions()
