import json
import random

with open('maps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

original_map = data['maps']['main_map']
original_width = original_map['width']
original_height = original_map['height']
original_data = original_map['data']

# 扩展尺寸 - 每个方向扩展20格
EXPAND_NORTH = 20
EXPAND_SOUTH = 20
EXPAND_WEST = 20
EXPAND_EAST = 20

new_width = original_width + EXPAND_WEST + EXPAND_EAST
new_height = original_height + EXPAND_NORTH + EXPAND_SOUTH

# 26 = 水域（不可通行）
# 25 = 草地
# 3 = 石头路
# 27 = 泥土路

def get_random_grass():
    return random.choice([25, 25, 25, 25, 25, 27])

new_data = []

for y in range(new_height):
    row = []
    for x in range(new_width):
        orig_x = x - EXPAND_WEST
        orig_y = y - EXPAND_NORTH

        if 0 <= orig_x < original_width and 0 <= orig_y < original_height:
            tile = original_data[orig_y][orig_x]
            row.append(tile)
        else:
            # 扩展区域用草地
            row.append(get_random_grass())
    new_data.append(row)

def adjust_location_coords(loc):
    loc['x'] += EXPAND_WEST
    loc['y'] += EXPAND_NORTH
    return loc

locations = original_map.get('locations', {})
for loc_id in locations:
    locations[loc_id] = adjust_location_coords(locations[loc_id])

new_map = {
    "name": original_map['name'],
    "width": new_width,
    "height": new_height,
    "data": new_data,
    "locations": locations
}

data['maps']['main_map'] = new_map

with open('maps.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"地图已扩展:")
print(f"  原尺寸: {original_width} x {original_height}")
print(f"  新尺寸: {new_width} x {new_height}")
print(f"  北扩展: {EXPAND_NORTH}")
print(f"  南扩展: {EXPAND_SOUTH}")
print(f"  西扩展: {EXPAND_WEST}")
print(f"  东扩展: {EXPAND_EAST}")
print(f"\n地点坐标已全部调整")