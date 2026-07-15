import json

# 创建二维延展式大地图数据
# 17个地点分布在二维平面上
# 地图尺寸：60x60
# 使用所有32个tiles图片

def create_extended_map():
    # 定义17个地点，每个地点有坐标和地形特征
    locations = {
        "zhongli": {"name": "钟离县", "x": 30, "y": 30, "terrain": "village", "features": ["house1", "house2", "well", "wheat_field", "farm_path"]},
        "huangjue_si": {"name": "皇觉寺", "x": 30, "y": 20, "terrain": "temple", "features": ["house1", "tree", "flowers", "stone_road"]},
        "huaixi": {"name": "淮西", "x": 20, "y": 30, "terrain": "plains", "features": ["grass", "tree", "farm_path", "rice_field"]},
        "henan": {"name": "河南", "x": 40, "y": 30, "terrain": "plains", "features": ["grass", "tree", "wheat_field", "vegetable_field"]},
        "dingyuan_lvpai_zhai": {"name": "定远驴牌寨", "x": 30, "y": 40, "terrain": "fortress", "features": ["wall", "house1", "tree", "stone_road"]},
        "dingyuan_miao_shan": {"name": "定远妙山", "x": 30, "y": 50, "terrain": "mountain", "features": ["barren_mountain", "tree", "cave", "stone_road"]},
        "hezhou": {"name": "和州", "x": 20, "y": 40, "terrain": "river", "features": ["calm_river", "bridge", "tree", "grass"]},
        "taiping_fu": {"name": "太平府", "x": 40, "y": 40, "terrain": "city", "features": ["town", "house2", "asphalt_road", "well2"]},
        "yingtian_fu": {"name": "应天府", "x": 30, "y": 40, "terrain": "capital", "features": ["town", "house1", "house2", "asphalt_road", "wall"]},
        "huizhou": {"name": "徽州", "x": 20, "y": 30, "terrain": "mountain", "features": ["tree", "forest", "farm_path", "house1"]},
        "zhedong": {"name": "浙东", "x": 40, "y": 20, "terrain": "coastal", "features": ["beach", "shallow_water", "tree", "house2"]},
        "jinhua": {"name": "金华", "x": 50, "y": 30, "terrain": "plains", "features": ["grass", "rice_field", "vegetable_field", "farm_path"]},
        "poyang_hu": {"name": "鄱阳湖", "x": 30, "y": 20, "terrain": "lake", "features": ["calm_river", "deep_water", "bridge", "tree"]},
        "suzhou": {"name": "苏州", "x": 20, "y": 20, "terrain": "garden", "features": ["flowers", "tree", "house1", "stone_road", "well"]},
        "yuan_dadu": {"name": "元大都", "x": 40, "y": 10, "terrain": "imperial", "features": ["town", "wall", "house2", "asphalt_road", "mechanism"]},
        "sichuan": {"name": "四川", "x": 10, "y": 30, "terrain": "basin", "features": ["grass", "tree", "rice_field", "farm_path"]},
        "yunnan": {"name": "云南", "x": 10, "y": 50, "terrain": "south", "features": ["tree", "forest", "flowers", "grass"]}
    }

    # 创建60x60的空白地图 (全部是草地)
    width = 60
    height = 60
    map_data = [[0 for _ in range(width)] for _ in range(height)]

    # 定义所有地形类型对应的瓦片ID
    terrain_tiles = {
        "grass": 0,
        "stone_road": 1,
        "calm_river": 2,
        "shallow_water": 3,
        "deep_water": 4,
        "house1": 5,
        "house2": 6,
        "tree": 7,
        "tree2": 8,
        "well": 9,
        "well2": 10,
        "fence": 11,
        "fence2": 12,
        "bridge": 13,
        "wall": 14,
        "wheat_field": 15,
        "rice_field": 16,
        "vegetable_field": 17,
        "flowers": 18,
        "forest": 19,
        "village": 20,
        "town": 21,
        "barren_mountain": 22,
        "cave": 23,
        "beach": 24,
        "desert": 25,
        "snow_field": 26,
        "asphalt_road": 27,
        "farm_path": 28,
        "ruins": 29,
        "trap": 30,
        "mechanism": 31,
        "active_volcano": 32
    }

    # 创建地点函数
    def create_location(loc_x, loc_y, terrain, features):
        # 每个地点占据7x7的区域
        for y in range(max(0, loc_y-3), min(height, loc_y+4)):
            for x in range(max(0, loc_x-3), min(width, loc_x+3)):
                # 四周围墙或边界
                if y == loc_y-3 or y == loc_y+3:
                    if x != loc_x:
                        if terrain in ["lake", "river", "coastal"]:
                            map_data[y][x] = terrain_tiles["shallow_water"]
                        else:
                            map_data[y][x] = terrain_tiles["tree"]
                elif x == loc_x-3 or x == loc_x+3:
                    if terrain in ["lake", "river", "coastal"]:
                        map_data[y][x] = terrain_tiles["shallow_water"]
                    else:
                        map_data[y][x] = terrain_tiles["tree"]

                # 中央区域根据地形类型填充
                if loc_x-2 < x < loc_x+2 and loc_y-2 < y < loc_y+2:
                    if terrain == "village":
                        if x == loc_x and y == loc_y:
                            map_data[y][x] = terrain_tiles["village"]
                        elif (x == loc_x-1 and y == loc_y-1) or (x == loc_x+1 and y == loc_y+1):
                            map_data[y][x] = terrain_tiles["house1"]
                        elif (x == loc_x-1 and y == loc_y+1) or (x == loc_x+1 and y == loc_y-1):
                            map_data[y][x] = terrain_tiles["house2"]
                        elif x == loc_x and y == loc_y-1:
                            map_data[y][x] = terrain_tiles["well"]
                        elif x == loc_x and y == loc_y+1:
                            map_data[y][x] = terrain_tiles["wheat_field"]
                        else:
                            map_data[y][x] = terrain_tiles["grass"]
                    
                    elif terrain == "temple":
                        if x == loc_x and y == loc_y:
                            map_data[y][x] = terrain_tiles["house1"]
                        elif abs(x - loc_x) + abs(y - loc_y) == 1:
                            map_data[y][x] = terrain_tiles["tree"]
                        elif abs(x - loc_x) + abs(y - loc_y) == 2:
                            map_data[y][x] = terrain_tiles["flowers"]
                        else:
                            map_data[y][x] = terrain_tiles["grass"]
                    
                    elif terrain == "plains":
                        if (x + y) % 3 == 0:
                            map_data[y][x] = terrain_tiles["tree"]
                        elif (x + y) % 3 == 1:
                            if "rice_field" in features:
                                map_data[y][x] = terrain_tiles["rice_field"]
                            else:
                                map_data[y][x] = terrain_tiles["wheat_field"]
                        else:
                            map_data[y][x] = terrain_tiles["grass"]
                    
                    elif terrain == "fortress":
                        if x == loc_x and y == loc_y:
                            map_data[y][x] = terrain_tiles["house1"]
                        elif abs(x - loc_x) == 2 or abs(y - loc_y) == 2:
                            map_data[y][x] = terrain_tiles["wall"]
                        else:
                            map_data[y][x] = terrain_tiles["stone_road"]
                    
                    elif terrain == "mountain":
                        if x == loc_x and y == loc_y:
                            map_data[y][x] = terrain_tiles["barren_mountain"]
                        elif abs(x - loc_x) + abs(y - loc_y) == 1:
                            map_data[y][x] = terrain_tiles["tree"]
                        elif abs(x - loc_x) + abs(y - loc_y) == 2 and "cave" in features:
                            map_data[y][x] = terrain_tiles["cave"]
                        else:
                            map_data[y][x] = terrain_tiles["grass"]
                    
                    elif terrain == "river":
                        if y == loc_y:
                            map_data[y][x] = terrain_tiles["calm_river"]
                        elif x == loc_x and "bridge" in features:
                            map_data[y][x] = terrain_tiles["bridge"]
                        else:
                            map_data[y][x] = terrain_tiles["grass"]
                    
                    elif terrain == "city":
                        if x == loc_x and y == loc_y:
                            map_data[y][x] = terrain_tiles["town"]
                        elif abs(x - loc_x) + abs(y - loc_y) == 1:
                            map_data[y][x] = terrain_tiles["house2"]
                        elif abs(x - loc_x) + abs(y - loc_y) == 2:
                            map_data[y][x] = terrain_tiles["asphalt_road"]
                        else:
                            map_data[y][x] = terrain_tiles["well2"]
                    
                    elif terrain == "capital":
                        if x == loc_x and y == loc_y:
                            map_data[y][x] = terrain_tiles["town"]
                        elif abs(x - loc_x) == 2 or abs(y - loc_y) == 2:
                            map_data[y][x] = terrain_tiles["wall"]
                        elif abs(x - loc_x) + abs(y - loc_y) == 1:
                            map_data[y][x] = terrain_tiles["house1"]
                        else:
                            map_data[y][x] = terrain_tiles["asphalt_road"]
                    
                    elif terrain == "coastal":
                        if y == loc_y-2:
                            map_data[y][x] = terrain_tiles["shallow_water"]
                        elif y == loc_y+2:
                            map_data[y][x] = terrain_tiles["beach"]
                        elif x == loc_x and y == loc_y:
                            map_data[y][x] = terrain_tiles["house2"]
                        else:
                            map_data[y][x] = terrain_tiles["grass"]
                    
                    elif terrain == "lake":
                        if abs(x - loc_x) + abs(y - loc_y) <= 2:
                            map_data[y][x] = terrain_tiles["calm_river"]
                        elif abs(x - loc_x) + abs(y - loc_y) == 3:
                            map_data[y][x] = terrain_tiles["deep_water"]
                        elif x == loc_x and y == loc_y and "bridge" in features:
                            map_data[y][x] = terrain_tiles["bridge"]
                        else:
                            map_data[y][x] = terrain_tiles["tree"]
                    
                    elif terrain == "garden":
                        if x == loc_x and y == loc_y:
                            map_data[y][x] = terrain_tiles["house1"]
                        elif abs(x - loc_x) + abs(y - loc_y) == 1:
                            map_data[y][x] = terrain_tiles["flowers"]
                        elif abs(x - loc_x) + abs(y - loc_y) == 2:
                            map_data[y][x] = terrain_tiles["tree"]
                        else:
                            map_data[y][x] = terrain_tiles["stone_road"]
                    
                    elif terrain == "imperial":
                        if x == loc_x and y == loc_y:
                            map_data[y][x] = terrain_tiles["town"]
                        elif abs(x - loc_x) == 2 or abs(y - loc_y) == 2:
                            map_data[y][x] = terrain_tiles["wall"]
                        elif abs(x - loc_x) + abs(y - loc_y) == 1:
                            map_data[y][x] = terrain_tiles["house2"]
                        elif x == loc_x and y == loc_y-1:
                            map_data[y][x] = terrain_tiles["mechanism"]
                        else:
                            map_data[y][x] = terrain_tiles["asphalt_road"]
                    
                    elif terrain == "basin":
                        if (x + y) % 2 == 0:
                            map_data[y][x] = terrain_tiles["rice_field"]
                        else:
                            map_data[y][x] = terrain_tiles["grass"]
                    
                    elif terrain == "south":
                        if (x + y) % 3 == 0:
                            map_data[y][x] = terrain_tiles["forest"]
                        elif (x + y) % 3 == 1:
                            map_data[y][x] = terrain_tiles["flowers"]
                        else:
                            map_data[y][x] = terrain_tiles["grass"]

    # 创建连接道路函数
    def create_road(from_x, from_y, to_x, to_y, road_type="stone_road"):
        road_tile = terrain_tiles[road_type]
        # 水平道路
        if from_y == to_y:
            start_x = min(from_x, to_x)
            end_x = max(from_x, to_x)
            for x in range(start_x, end_x + 1):
                if 0 <= x < width and 0 <= from_y < height:
                    if map_data[from_y][x] == terrain_tiles["grass"]:
                        map_data[from_y][x] = road_tile
        # 垂直道路
        elif from_x == to_x:
            start_y = min(from_y, to_y)
            end_y = max(from_y, to_y)
            for y in range(start_y, end_y + 1):
                if 0 <= from_x < width and 0 <= y < height:
                    if map_data[y][from_x] == terrain_tiles["grass"]:
                        map_data[y][from_x] = road_tile

    # 创建所有地点
    for loc_id, loc_info in locations.items():
        create_location(loc_info["x"], loc_info["y"], loc_info["terrain"], loc_info["features"])

    # 创建地点之间的连接道路
    # 钟离县 -> 皇觉寺 (北)
    create_road(30, 30, 30, 20, "stone_road")
    
    # 钟离县 -> 淮西 (西)
    create_road(30, 30, 20, 30, "farm_path")
    
    # 钟离县 -> 河南 (东)
    create_road(30, 30, 40, 30, "farm_path")
    
    # 钟离县 -> 定远驴牌寨 (南)
    create_road(30, 30, 30, 40, "stone_road")
    
    # 定远驴牌寨 -> 定远妙山 (南)
    create_road(30, 40, 30, 50, "stone_road")
    
    # 定远驴牌寨 -> 和州 (西)
    create_road(30, 40, 20, 40, "stone_road")
    
    # 定远驴牌寨 -> 太平府 (东)
    create_road(30, 40, 40, 40, "asphalt_road")
    
    # 和州 -> 徽州 (北)
    create_road(20, 40, 20, 30, "stone_road")
    
    # 太平府 -> 浙东 (北)
    create_road(40, 40, 40, 20, "asphalt_road")
    
    # 浙东 -> 金华 (东)
    create_road(40, 20, 50, 20, "farm_path")
    
    # 金华 -> 鄱阳湖 (南)
    create_road(50, 20, 50, 30, "farm_path")
    
    # 鄱阳湖 -> 苏州 (西)
    create_road(50, 30, 20, 30, "stone_road")
    
    # 苏州 -> 元大都 (北)
    create_road(20, 30, 20, 10, "asphalt_road")
    
    # 元大都 -> 皇觉寺 (东)
    create_road(20, 10, 30, 10, "asphalt_road")
    
    # 淮西 -> 四川 (西)
    create_road(20, 30, 10, 30, "farm_path")
    
    # 四川 -> 云南 (南)
    create_road(10, 30, 10, 50, "stone_road")

    # 添加一些额外的地形特征
    # 在地图边缘添加一些特殊地形
    for i in range(0, 60, 10):
        map_data[0][i] = terrain_tiles["snow_field"]
        map_data[59][i] = terrain_tiles["desert"]
        map_data[i][0] = terrain_tiles["snow_field"]
        map_data[i][59] = terrain_tiles["desert"]

    # 添加一些废墟和陷阱
    map_data[15][15] = terrain_tiles["ruins"]
    map_data[45][45] = terrain_tiles["ruins"]
    map_data[25][35] = terrain_tiles["trap"]
    map_data[35][25] = terrain_tiles["trap"]

    # 添加活火山
    map_data[50][50] = terrain_tiles["active_volcano"]

    return map_data, locations, terrain_tiles

def save_map():
    map_data, locations, terrain_tiles = create_extended_map()

    # 创建瓦片映射
    tile_mapping = {}
    for tile_name, tile_id in terrain_tiles.items():
        tile_mapping[str(tile_id)] = tile_name

    # 创建地图JSON结构
    map_json = {
        "maps": {
            "main_map": {
                "name": "朱元璋崛起之路",
                "width": 60,
                "height": 60,
                "data": map_data,
                "locations": locations
            }
        },
        "tile_mapping": tile_mapping
    }

    with open('maps.json', 'w', encoding='utf-8') as f:
        json.dump(map_json, f, ensure_ascii=False, indent=2)

    print("地图数据已生成并保存到 maps.json")
    print(f"地图尺寸: {len(map_data[0])}x{len(map_data)}")
    print(f"包含 {len(locations)} 个地点")
    print(f"使用了 {len(terrain_tiles)} 种瓦片类型")

if __name__ == "__main__":
    save_map()