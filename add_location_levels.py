#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为所有地点添加进入等级限制
"""

import json

with open('maps.json', 'r', encoding='utf-8') as f:
    maps_data = json.load(f)

level_mapping = {
    "zhongli": 1,
    "huangjue_si": 2,
    "huaixi": 3,
    "henan": 4,
    "dingyuan_lvpai_zhai": 5,
    "dingyuan_miaoshan": 6,
    "hezhou": 7,
    "taipingfu": 8,
    "yingtianfu": 9,
    "huizhou": 10,
    "zhedong": 11,
    "jinhua": 12,
    "poyanghu": 13,
    "suzhou": 14,
    "yuandadu": 15,
    "sichuan": 16,
    "yunnan": 17
}

for map_id, map_info in maps_data["maps"].items():
    if "locations" in map_info:
        for loc_id, loc_info in map_info["locations"].items():
            if loc_id in level_mapping:
                loc_info["min_level"] = level_mapping[loc_id]
                print(f"设置 {loc_info['name']} 的进入等级为 {level_mapping[loc_id]}")
            else:
                loc_info["min_level"] = 1
                print(f"设置 {loc_info['name']} 的进入等级为 1 (默认)")

with open('maps.json', 'w', encoding='utf-8') as f:
    json.dump(maps_data, f, ensure_ascii=False, indent=2)

print("\n所有地点的进入等级已设置完成！")
