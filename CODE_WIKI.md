# 社稷归墟传 - 大明王朝RPG 代码Wiki

## 1. 项目概述

本项目是一款基于 **Pygame** 开发的2D角色扮演游戏，以明朝开国皇帝朱元璋的崛起之路为背景。玩家扮演朱元璋，从钟离县出发，历经皇觉寺出家、红巾军起义、南征北战，最终建立大明王朝。

### 核心特色

- **开放世界地图**：120x120 的瓦片地图，包含20+个历史地点
- **十字路网结构**：以钟离县为中心，四通八达的道路网络
- **多系统玩法**：砍树、战斗、种菜、装备、剧情等
- **挂机系统**：支持自动打怪升级
- **存档系统**：完整的进度保存与加载功能

---

## 2. 项目架构

### 2.1 目录结构

```
game/
├── tiles/                  # 瓦片资源目录 (36个瓦片)
├── main.py                 # 游戏主程序
├── map_editor.py           # 地图编辑器
├── maps.json               # 地图数据
├── equipment.json          # 装备数据
├── monsters.json           # 怪物数据
├── stories.json            # 剧情数据
├── player_sprite.png       # 玩家精灵图
└── 辅助工具脚本/            # 地图生成、怪物添加等脚本
```

### 2.2 架构分层

```
┌─────────────────────────────────────┐
│           UI 层 (Game.draw_ui)       │
│   角色属性面板、装备栏、小地图、剧情   │
├─────────────────────────────────────┤
│         游戏逻辑层 (Game类)          │
│   战斗、砍树、种菜、存档、事件处理    │
├─────────────────────────────────────┤
│         实体层 (Player/Camera)       │
│   玩家状态、移动、属性计算            │
├─────────────────────────────────────┤
│         数据层 (JSON文件)            │
│   地图、装备、怪物、剧情数据          │
└─────────────────────────────────────┘
```

---

## 3. 核心模块

### 3.1 游戏主程序 [main.py](file:///Users/qiuyelong/Documents/trae_projects/game/main.py)

#### 全局常量

| 常量 | 值 | 说明 |
|------|-----|------|
| SCREEN_WIDTH | 800 | 屏幕宽度 |
| SCREEN_HEIGHT | 600 | 屏幕高度 |
| TILE_SIZE | 32 | 瓦片大小(像素) |
| FPS | 60 | 帧率 |

#### 全局变量

- `tile_images` - 瓦片图片缓存字典
- `map_data` - 当前地图数据(二维数组)
- `tile_map` - 瓦片ID到名称的映射
- `locations` - 地点信息字典
- `CHINESE_FONT` - 中文字体对象

---

### 3.2 玩家模块 (Player类)

#### 类定义

```python
class Player:
    def __init__(self, x, y):
        # 位置属性
        self.x, self.y = x, y
        self.target_x, self.target_y = x, y
        self.is_moving = False
        
        # 角色属性
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 100
        self.base_attack = 10
        self.base_defense = 5
        
        # 生命系统
        self.base_hp = 100
        self.max_hp = 100
        self.hp = 100
        
        # 体力系统
        self.base_stamina = 100
        self.max_stamina = 100
        self.stamina = 100
        self.stamina_regen = 5
        
        # 食物系统
        self.food = 0
        self.max_food = 20
        
        # 装备系统
        self.equipment = {
            "weapon": "碗", "wrist_guard": "", ...
        }
        
        # 挂机状态
        self.auto_farming = True
```

#### 核心方法

| 方法 | 功能说明 |
|------|----------|
| `try_move(dx, dy)` | 尝试移动，检测地形是否可通行 |
| `update(dt)` | 更新玩家状态，处理移动动画和挂机经验 |
| `draw(surface, cx, cy)` | 绘制玩家精灵 |
| `gain_exp(amount)` | 获取经验，触发升级 |
| `level_up()` | 升级，提升属性 |
| `calculate_stats()` | 根据装备计算实际属性 |
| `consume_stamina(amount)` | 消耗体力 |
| `eat_food()` | 吃食物恢复体力 |
| `toggle_auto_farming()` | 切换挂机状态 |

---

### 3.3 相机模块 (Camera类)

```python
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
    
    def update(self, target):
        # 跟随目标移动，限制边界
        x = target.x * TILE_SIZE - self.width // 2 + TILE_SIZE // 2
        y = target.y * TILE_SIZE - self.height // 2 + TILE_SIZE // 2
        x = max(0, min(x, map_width - self.width))
        y = max(0, min(y, map_height - self.height))
```

---

### 3.4 游戏核心模块 (Game类)

#### 初始化与资源加载

```python
class Game:
    def __init__(self):
        self.player = Player(60, 60)           # 创建玩家
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.monsters_data = self.load_monsters_data()  # 加载怪物
        self.monsters = self.load_monsters()            # 加载怪物位置
        self.stories_data = self.load_stories_data()    # 加载剧情
        self.maps_data = self.load_maps_data()          # 加载地图
        self.load_resources()                           # 加载资源
```

#### 游戏系统

| 系统 | 核心方法 | 功能说明 |
|------|----------|----------|
| **战斗系统** | `update_battle(dt)` | 检测怪物、战斗进度、胜负判定 |
| **砍树系统** | `update_chopping(dt)` | 检测树木、砍树进度、装备掉落 |
| **种菜系统** | `plant_crop()` | 在农田附近种菜获得食物 |
| **剧情系统** | `trigger_story(location)` | 首次进入地点触发剧情 |
| **装备系统** | `drop_equipment()` / `auto_equip()` | 装备掉落与自动装备 |
| **存档系统** | `save_game()` / `load_game()` | 保存/加载游戏进度 |
| **小地图** | `draw_minimap(surface)` | 绘制全局地图 |

#### 事件处理

| 按键 | 功能 |
|------|------|
| WASD / 方向键 | 移动角色 |
| M | 打开/关闭小地图 |
| S | 保存游戏 |
| L | 加载游戏 |
| A | 切换挂机状态 |
| E | 切换装备栏显示 |
| P | 种菜 |
| F | 吃饭 |
| R | 替换装备 |
| Q | 丢弃装备 |
| Enter | 跳过剧情 |
| Esc | 退出游戏 |

#### 主循环

```python
async def run(self):
    running = True
    while running:
        dt = (current_time - last_time) / 1000.0
        
        # 1. 事件处理
        running = self.handle_events()
        
        # 2. 更新状态
        move_completed = self.player.update(dt)
        self.update_chopping(dt)
        self.update_battle(dt)
        self.update_story(dt)
        self.camera.update(self.player)
        
        # 3. 绘制画面
        self.draw_map(screen)
        self.draw_monsters(screen)
        self.player.draw(screen, cx, cy)
        self.draw_ui(screen)
        
        pygame.display.flip()
        clock.tick(FPS)
```

---

## 4. 数据存储结构

### 4.1 地图数据 [maps.json](file:///Users/qiuyelong/Documents/trae_projects/game/maps.json)

```json
{
  "maps": {
    "main_map": {
      "name": "大明王朝RPG - 十字路网",
      "width": 120,
      "height": 120,
      "data": [[25, 27, 3, ...], ...],
      "locations": {
        "zhongli": {
          "name": "钟离县",
          "x": 60,
          "y": 60,
          "min_level": 1
        }
      }
    }
  },
  "tile_mapping": {
    "0": "grass",
    "3": "stone_road",
    "7": "tree",
    ...
  }
}
```

#### 瓦片ID映射

| ID | 名称 | 说明 |
|----|------|------|
| 2 | forest | 森林 |
| 3 | stone_road | 石头路 |
| 7 | tree | 树 |
| 8 | tree2 | 大树 |
| 10 | wheat_field | 麦田 |
| 11 | rice_field | 稻田 |
| 12 | well | 水井 |
| 25 | grass | 草地 |
| 26 | water | 水域(不可通行) |
| 27 | asphalt_road | 柏油路 |
| 34 | village | 村庄 |
| 100 | wolf | 狼 |
| 101 | tiger | 老虎 |
| 102 | lion | 狮子 |

### 4.2 装备数据 [equipment.json](file:///Users/qiuyelong/Documents/trae_projects/game/equipment.json)

```json
{
  "equipment": [
    {
      "id": "iron_sword",
      "name": "长剑",
      "type": "weapon",
      "slot": "武器",
      "attack": 5,
      "defense": 0,
      "quality": "green"
    }
  ]
}
```

#### 品质等级

| 品质 | 颜色 | 优先级 |
|------|------|--------|
| white | 白色 | 1 |
| green | 绿色 | 2 |
| blue | 蓝色 | 3 |
| purple | 紫色 | 4 |
| orange | 橙色 | 5 |

#### 装备部位

```python
equipment_slots = {
    "weapon": "武器",
    "wrist_guard": "护腕",
    "necklace": "项链",
    "amulet": "护符",
    "ring": "戒指",
    "helmet": "帽子",
    "gauntlet": "护手",
    "shoulder": "护肩",
    "belt": "腰带",
    "boots": "靴子"
}
```

### 4.3 怪物数据 [monsters.json](file:///Users/qiuyelong/Documents/trae_projects/game/monsters.json)

```json
{
  "monsters": [
    {
      "id": 1,
      "name": "狼",
      "attack": 5,
      "defense": 2,
      "hp": 20,
      "sprite": "wolf",
      "exp_reward": 50,
      "min_level": 1
    }
  ],
  "tile_mapping": {
    "wolf": 100,
    "tiger": 101,
    "lion": 102
  }
}
```

### 4.4 剧情数据 [stories.json](file:///Users/qiuyelong/Documents/trae_projects/game/stories.json)

```json
{
  "stories": {
    "zhongli_north": {
      "name": "钟离县-北",
      "year": "1344年",
      "story": "1344年，朱元璋十七岁..."
    }
  }
}
```

### 4.5 存档数据 (savegame.json)

```json
{
  "player": {
    "x": 60, "y": 60,
    "level": 5, "exp": 250,
    "hp": 100, "stamina": 80,
    "food": 5,
    "equipment": {"weapon": "长剑", ...}
  },
  "visited_locations": ["zhongli", "huangjue_si"],
  "save_time": 1620000000
}
```

---

## 5. 依赖关系

### 5.1 Python依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| pygame | >=2.0 | 游戏引擎 |
| json | 内置 | 数据存储 |
| asyncio | 内置 | 异步主循环 |
| os | 内置 | 文件操作 |
| glob | 内置 | 文件匹配 |

### 5.2 模块依赖图

```
main.py
├── pygame (游戏引擎)
├── maps.json (地图数据)
│   ├── tile_mapping (瓦片映射)
│   └── locations (地点信息)
├── equipment.json (装备数据)
├── monsters.json (怪物数据)
├── stories.json (剧情数据)
└── tiles/ (瓦片资源)
    ├── grass.png
    ├── tree.png
    ├── wolf.png
    └── ...
```

---

## 6. 项目运行方式

### 6.1 开发环境运行

```bash
cd /path/to/game
python3 main.py
```

### 6.2 浏览器运行 (Pygbag)

```bash
pip install pygbag
pygbag --build .
# 输出目录: build/web
```

### 6.3 注意事项

- **中文字体**：游戏会自动查找系统中文字体（STHeiti、PingFang、Arial Unicode等）
- **Pygbag限制**：WebAssembly环境下中文字体支持有限，建议使用本地Python运行
- **存档路径**：存档文件保存在当前目录 `savegame.json`

---

## 7. 辅助工具脚本

### 7.1 地图生成工具

| 脚本 | 功能说明 |
|------|----------|
| [create_crossroad_map.py](file:///Users/qiuyelong/Documents/trae_projects/game/create_crossroad_map.py) | 生成十字路网地图 |
| [create_historical_map.py](file:///Users/qiuyelong/Documents/trae_projects/game/create_historical_map.py) | 生成历史地图 |
| [create_new_map.py](file:///Users/qiuyelong/Documents/trae_projects/game/create_new_map.py) | 创建新地图 |
| [create_zigzag_map.py](file:///Users/qiuyelong/Documents/trae_projects/game/create_zigzag_map.py) | 生成之字形道路地图 |
| [expand_map.py](file:///Users/qiuyelong/Documents/trae_projects/game/expand_map.py) | 扩展地图尺寸 |
| [generate_extended_map.py](file:///Users/qiuyelong/Documents/trae_projects/game/generate_extended_map.py) | 生成扩展地图 |

### 7.2 地图编辑工具

| 脚本 | 功能说明 |
|------|----------|
| [map_editor.py](file:///Users/qiuyelong/Documents/trae_projects/game/map_editor.py) | 可视化地图编辑器 |
| [redesign_crossroad_map.py](file:///Users/qiuyelong/Documents/trae_projects/game/redesign_crossroad_map.py) | 重新设计十字路网 |
| [redesign_map.py](file:///Users/qiuyelong/Documents/trae_projects/game/redesign_map.py) | 重新设计地图 |
| [redesign_map_fixed.py](file:///Users/qiuyelong/Documents/trae_projects/game/redesign_map_fixed.py) | 修复地图设计 |
| [replace_grass_with_asphalt.py](file:///Users/qiuyelong/Documents/trae_projects/game/replace_grass_with_asphalt.py) | 替换草地为柏油路 |
| [restore_original_map.py](file:///Users/qiuyelong/Documents/trae_projects/game/restore_original_map.py) | 恢复原始地图 |

### 7.3 数据管理工具

| 脚本 | 功能说明 |
|------|----------|
| [add_monsters.py](file:///Users/qiuyelong/Documents/trae_projects/game/add_monsters.py) | 为地点添加怪物 |
| [add_location_levels.py](file:///Users/qiuyelong/Documents/trae_projects/game/add_location_levels.py) | 为地点添加等级限制 |
| [clear_monsters.py](file:///Users/qiuyelong/Documents/trae_projects/game/clear_monsters.py) | 清除所有怪物 |
| [recreate_transitions.py](file:///Users/qiuyelong/Documents/trae_projects/game/recreate_transitions.py) | 重新创建地点连接 |
| [create_monster.py](file:///Users/qiuyelong/Documents/trae_projects/game/create_monster.py) | 创建怪物 |
| [generate_tiles.py](file:///Users/qiuyelong/Documents/trae_projects/game/generate_tiles.py) | 生成瓦片 |
| [generate_extra_tiles.py](file:///Users/qiuyelong/Documents/trae_projects/game/generate_extra_tiles.py) | 生成额外瓦片 |

---

## 8. 关键设计模式

### 8.1 数据驱动设计

游戏的地图、装备、怪物、剧情等全部通过JSON文件配置，无需修改代码即可扩展内容。

### 8.2 状态机模式

玩家和游戏对象通过状态标志管理行为：
- `is_moving` - 移动状态
- `in_battle` - 战斗状态
- `showing_story` - 剧情状态
- `auto_farming` - 挂机状态

### 8.3 观察者模式

事件处理采用Pygame的事件队列机制，通过 `handle_events()` 统一处理用户输入。

---

## 9. 扩展指南

### 9.1 添加新地点

1. 在 `maps.json` 的 `locations` 中添加新地点配置
2. 在 `stories.json` 中添加对应剧情（可选）
3. 在 `add_location_levels.py` 中设置进入等级
4. 在 `add_monsters.py` 中添加怪物（可选）

### 9.2 添加新装备

在 `equipment.json` 中添加装备项：

```json
{
  "id": "new_equipment_id",
  "name": "装备名称",
  "type": "weapon",  // 装备类型
  "slot": "武器",    // 显示名称
  "attack": 10,
  "defense": 5,
  "quality": "blue"
}
```

### 9.3 添加新怪物

在 `monsters.json` 中添加怪物：

```json
{
  "id": 4,
  "name": "新怪物",
  "attack": 20,
  "defense": 10,
  "hp": 80,
  "sprite": "monster_name",
  "exp_reward": 200,
  "min_level": 8
}
```

并在 `monsters.json` 的 `tile_mapping` 中添加：

```json
"monster_name": 103
```

---

## 10. 已知问题与限制

1. **Pygbag中文字体问题**：WebAssembly环境下中文字体显示有限
2. **地图尺寸限制**：当前地图为120x120，较大地图可能影响性能
3. **战斗系统简化**：战斗仅基于攻击力+防御力计算，无复杂战斗机制
4. **NPC系统缺失**：目前无NPC交互功能
5. **任务系统缺失**：无主线/支线任务系统

---

## 11. 代码规范

- **编码格式**：UTF-8
- **命名规范**：变量使用 snake_case，类使用 PascalCase
- **中文支持**：所有数据文件使用UTF-8编码，支持中文显示
- **注释规范**：关键函数和类提供中文文档字符串

---

## 12. 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | - | 初始版本，基础地图和角色系统 |
| v1.1 | - | 添加十字路网结构 |
| v1.2 | - | 添加战斗系统和怪物 |
| v1.3 | - | 添加装备系统和品质分级 |
| v1.4 | - | 添加剧情系统和地点等级限制 |
| v1.5 | - | 添加小地图和存档系统 |
