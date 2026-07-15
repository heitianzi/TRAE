import pygame
import sys
import os
import json
import asyncio
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ming Dynasty - Rise of Zhu Yuanzhang")

clock = pygame.time.Clock()

CHINESE_FONT = None
font_paths = [
    "fonts/STHeiti Light.ttc",
    "fonts/PingFang.ttc",
    "fonts/Arial Unicode.ttf",
    "fonts/Hiragino Sans GB.ttc"
]
for font_path in font_paths:
    if os.path.exists(font_path):
        try:
            CHINESE_FONT = pygame.font.Font(font_path, 24)
            break
        except:
            continue

if CHINESE_FONT is None:
    try:
        CHINESE_FONT = pygame.font.SysFont("simhei", 24)
    except:
        try:
            CHINESE_FONT = pygame.font.SysFont("arial", 24)
        except:
            CHINESE_FONT = pygame.font.Font(None, 24)
# Fallback: if SysFont returned an empty/invalid font, use default
try:
    CHINESE_FONT.render("Test", True, (0, 0, 0))
except:
    CHINESE_FONT = pygame.font.Font(None, 24)

tile_images = {}
tiles_dir = "tiles"

def load_tiles():
    import glob
    tile_pattern = os.path.join(tiles_dir, "*.png")
    tile_files = glob.glob(tile_pattern)
    
    for filepath in tile_files:
        filename = os.path.basename(filepath)
        tile_name = os.path.splitext(filename)[0]
        try:
            image = pygame.image.load(filepath).convert()
            tile_images[tile_name] = image
        except Exception as e:
            print(f"Failed to load tile: {filepath}, error: {e}")
    
    print(f"Loaded {len(tile_images)} tiles")

map_data = None
tile_map = None
locations = None

def load_map(map_name):
    global map_data, tile_map, locations

    map_file = "maps.json"
    if not os.path.exists(map_file):
        print(f"Map file {map_file} not found")
        return False

    try:
        with open(map_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if map_name not in data.get('maps', {}):
            print(f"Map {map_name} not found")
            return False

        map_info = data['maps'][map_name]
        map_data = map_info['data']
        locations = map_info.get('locations', {})

        string_mapping = data.get('tile_mapping', {})
        tile_map = {int(k): v for k, v in string_mapping.items()}

        return True
    except Exception as e:
        print(f"Failed to load map: {e}")
        return False

def get_current_location_name(player_x, player_y):
    if not locations:
        return "Unknown"
    
    for loc_id, loc_info in locations.items():
        loc_x = loc_info["x"]
        loc_y = loc_info["y"]
        if abs(loc_x - player_x) <= 2 and abs(loc_y - player_y) <= 2:
            return loc_info["name"]
    
    return "Path of Rise"

def get_current_location_id(player_x, player_y):
    """Get current location ID"""
    if not locations:
        return None
    
    for loc_id, loc_info in locations.items():
        loc_x = loc_info["x"]
        loc_y = loc_info["y"]
        if abs(loc_x - player_x) <= 2 and abs(loc_y - player_y) <= 2:
            return loc_id
    
    return None

def get_location_min_level(player_x, player_y):
    """Get minimum entry level for location"""
    if not locations:
        return 1
    
    for loc_id, loc_info in locations.items():
        loc_x = loc_info["x"]
        loc_y = loc_info["y"]
        if abs(loc_x - player_x) <= 2 and abs(loc_y - player_y) <= 2:
            return loc_info.get("min_level", 1)
    
    return 1

load_map('main_map')

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = 48
        self.direction = 'down'
        self.frame = 0
        self.frame_count = 0

        self.speed = 150
        self.target_x = x
        self.target_y = y
        self.is_moving = False
        self.moving_timer = 3

        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 100
        self.skin_stage = 'peasant'  # peasant / soldier / robe
        
        self.name = "Zhu Yuanzhang"
        self.base_attack = 10
        self.base_defense = 5
        self.attack = self.base_attack
        self.defense = self.base_defense
        
        # HP system
        self.base_hp = 100
        self.max_hp = self.base_hp
        self.hp = self.max_hp
        
        # Stamina system
        self.base_stamina = 100
        self.max_stamina = self.base_stamina
        self.stamina = self.max_stamina
        self.stamina_regen = 5  # Recovers 5 stamina per second
        
        # Food system
        self.food = 0
        self.max_food = 20

        # Gold system
        self.gold = 50  # Starting gold
        
        # Equipment system
        self.equipment = {
            "weapon": "Bowl",
            "wrist_guard": "",
            "necklace": "",
            "amulet": "",
            "ring": "",
            "helmet": "",
            "gauntlet": "",
            "shoulder": "",
            "belt": "",
            "boots": ""
        }
        
        # Equipment data
        self.equipment_data = self.load_equipment_data()
        
        # Auto-farming state
        self.auto_farming = True

        self.load_sprite()
        
    def load_equipment_data(self):
        """Load equipment data"""
        try:
            with open('equipment.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('equipment', [])
        except:
            return []
    
    def calculate_stats(self):
        """Calculate current stats"""
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.max_hp = self.base_hp
        self.max_stamina = self.base_stamina
        
        for eq_type, eq_name in self.equipment.items():
            if eq_name:
                for eq in self.equipment_data:
                    if eq['name'] == eq_name:
                        self.attack += eq['attack']
                        self.defense += eq['defense']
                        break
        
        # Adjust HP if exceeds max HP
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        
        # Adjust stamina if exceeds max stamina
        if self.stamina > self.max_stamina:
            self.stamina = self.max_stamina
    
    def consume_stamina(self, amount):
        """Consume stamina"""
        self.stamina = max(0, self.stamina - amount)
        return self.stamina
    
    def add_food(self, amount):
        """Add food"""
        self.food = min(self.max_food, self.food + amount)
        return self.food
    
    def eat_food(self):
        """Eat food to recover stamina"""
        if self.food > 0:
            self.food -= 1
            self.stamina = min(self.max_stamina, self.stamina + 30)
            return True
        return False
    
    def get_equipment_by_type(self, eq_type):
        """Get equipment by type"""
        return [eq for eq in self.equipment_data if eq['type'] == eq_type]
    
    def toggle_auto_farming(self):
        """Toggle auto-farming state"""
        self.auto_farming = not self.auto_farming
        return self.auto_farming

    def load_sprite(self):
        # Load all skin stages
        self.sprite_sheets = {}
        skin_files = {
            'peasant': 'sprite_peasant.png',
            'soldier': 'sprite_soldier.png',
            'robe': 'sprite_robe.png'
        }
        for stage, path in skin_files.items():
            if os.path.exists(path):
                self.sprite_sheets[stage] = pygame.image.load(path).convert_alpha()
            else:
                # Fallback to player_sprite.png for peasant
                if stage == 'peasant' and os.path.exists('player_sprite.png'):
                    self.sprite_sheets[stage] = pygame.image.load('player_sprite.png').convert_alpha()

        self.sprite_sheet = self.sprite_sheets.get(self.skin_stage)
        if self.sprite_sheet is None:
            self.color = (255, 0, 0)

    def gain_exp(self, amount):
        self.exp += amount
        while self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        if self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level += 1
            self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
            self.update_skin()
            return True
        return False

    def update_skin(self):
        """Update player skin based on level"""
        old_stage = self.skin_stage
        if self.level >= 10:
            self.skin_stage = 'robe'
        elif self.level >= 5:
            self.skin_stage = 'soldier'
        else:
            self.skin_stage = 'peasant'

        if old_stage != self.skin_stage:
            self.sprite_sheet = self.sprite_sheets.get(self.skin_stage)
            print(f"Skin changed: {old_stage} -> {self.skin_stage}")
            return True
        return False

    def get_level(self):
        return self.level

    def try_move(self, dx, dy):
        if self.is_moving:
            return

        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < len(map_data[0]) and 0 <= new_y < len(map_data):
            tile_type = map_data[new_y][new_x]
            # Allow movement on passable terrain like roads, grass, farmland
            if tile_type not in [26]:  # Only water (26) is impassable
                self.target_x = new_x
                self.target_y = new_y
                self.is_moving = True
                self.moving_timer = 0

                if dx < 0:
                    self.direction = 'left'
                elif dx > 0:
                    self.direction = 'right'
                elif dy < 0:
                    self.direction = 'up'
                elif dy > 0:
                    self.direction = 'down'
                
                # Check if entered new location after moving
                return True
        return False

    def update(self, dt):
        # Gain exp from auto-farming
        if self.auto_farming:
            self.gain_exp(2 * dt)  # Gain 2 exp per second
        
        # Stamina regeneration
        if self.stamina < self.max_stamina:
            self.stamina = min(self.max_stamina, self.stamina + self.stamina_regen * dt)
        
        if self.is_moving:
            self.moving_timer += dt
            pixels_to_move = TILE_SIZE
            move_duration = pixels_to_move / self.speed
            progress = min(self.moving_timer / move_duration, 1.0)
            self.x = self.target_x - (self.target_x - self.x) * (1.0 - progress)
            self.y = self.target_y - (self.target_y - self.y) * (1.0 - progress)

            if progress >= 1.0:
                self.x = self.target_x
                self.y = self.target_y
                self.is_moving = False
                return True  # Returns True when movement complete

            self.frame_count += 1
            if self.frame_count >= 6:
                self.frame = (self.frame + 1) % 3
                self.frame_count = 0
        
        return False

    def draw(self, surface, camera_x, camera_y):
        screen_x = int(self.x * TILE_SIZE - camera_x)
        screen_y = int(self.y * TILE_SIZE - camera_y - 16)

        if self.sprite_sheet:
            direction_idx = {'down': 0, 'left': 1, 'right': 2, 'up': 3}[self.direction]
            sprite_x = direction_idx * TILE_SIZE
            sprite_y = self.frame * 48
            sprite_rect = pygame.Rect(sprite_x, sprite_y, TILE_SIZE, 48)
            sprite = self.sprite_sheet.subsurface(sprite_rect)
            surface.blit(sprite, (screen_x, screen_y))
        else:
            pygame.draw.rect(surface, self.color, (screen_x, screen_y, self.width, self.height))

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, rect):
        return rect.move(-self.camera.x, -self.camera.y)

    def update(self, target):
        x = target.x * TILE_SIZE - self.width // 2 + TILE_SIZE // 2
        y = target.y * TILE_SIZE - self.height // 2 + TILE_SIZE // 2

        x = max(0, min(x, len(map_data[0]) * TILE_SIZE - self.width))
        y = max(0, min(y, len(map_data) * TILE_SIZE - self.height))

        self.camera = pygame.Rect(int(x), int(y), self.width, self.height)


class NPC:
    """NPC class for non-player characters with dialogue system."""
    def __init__(self, npc_id, data):
        self.id = npc_id
        self.name = data.get("name", "Unknown")
        self.x = data.get("x", 0)
        self.y = data.get("y", 0)
        self.location = data.get("location", "")
        self.color = tuple(data.get("color", [200, 200, 200]))
        self.dialogues = data.get("dialogues", ["..."])
        self.dialogue_index = 0
        self.sprite = None
        sprite_file = data.get("sprite", "")
        if sprite_file and os.path.exists(sprite_file):
            self.sprite = pygame.image.load(sprite_file).convert_alpha()

    def talk(self):
        """Return current dialogue and advance index."""
        if not self.dialogues:
            return "..."
        text = self.dialogues[self.dialogue_index]
        self.dialogue_index = (self.dialogue_index + 1) % len(self.dialogues)
        return text

    def draw(self, surface, camera_x, camera_y):
        """Draw NPC on the map."""
        screen_x = self.x * TILE_SIZE - camera_x
        screen_y = self.y * TILE_SIZE - camera_y

        # Cull if off-screen
        if screen_x < -TILE_SIZE or screen_x > SCREEN_WIDTH or screen_y < -TILE_SIZE or screen_y > SCREEN_HEIGHT:
            return

        if self.sprite:
            surface.blit(self.sprite, (screen_x, screen_y))
        else:
            pygame.draw.rect(surface, self.color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))

        # Name tag above NPC
        # (drawn by Game class with font)


class Game:
    def __init__(self):
        # State machine: TITLE (title screen) or PLAYING (game exploration)
        self.state = "TITLE"
        self.title_timer = 0.0       # Time spent on title screen (for animations)
        self.transition_timer = 0.0  # Fade transition timer
        self.transitioning = False   # Whether currently transitioning TITLE -> PLAYING

        self.player = Player(60, 60)
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.font = CHINESE_FONT
        # Create smaller font supporting Chinese (reuse same font file, smaller size)
        if CHINESE_FONT:
            try:
                font_path = None
                for fp in ["fonts/STHeiti Light.ttc", "fonts/PingFang.ttc",
                           "fonts/Arial Unicode.ttf", "fonts/Hiragino Sans GB.ttc"]:
                    if os.path.exists(fp):
                        font_path = fp
                        break
                if font_path:
                    self.small_font = pygame.font.Font(font_path, 16)
                else:
                    self.small_font = pygame.font.Font(None, 16)
            except:
                self.small_font = pygame.font.Font(None, 16)
        else:
            self.small_font = pygame.font.Font(None, 16)
        self.scene_name = get_current_location_name(self.player.x, self.player.y)
        
        # Equipment drop related
        self.show_equipment_drop = False
        self.dropped_equipment = None
        
        # Equipment panel toggle state
        self.equipment_panel_visible = True
        
        # Chopping system
        self.chopping_tree = False
        self.chopping_progress = 0
        self.chopping_max = 5.0  # 5 seconds chopping time
        self.chopping_timer = 0
        self.auto_equip_timer = 0
        self.auto_equip_max = 3.0  # 3 seconds auto action time
        
        # Battle system
        self.in_battle = False
        self.battle_progress = 0
        self.battle_max = 5.0  # 5 seconds battle time
        self.battle_timer = 0
        self.current_monster = None
        self.battle_result = None  # "win" or "lose"
        self.battle_result_timer = 0
        self.battle_result_max = 3.0  # Show result for 3 seconds
        
        # Load monster data
        self.monsters_data = self.load_monsters_data()
        
        # Monster positions
        self.monsters = self.load_monsters()
        
        # Story system
        self.stories_data = self.load_stories_data()
        self.visited_locations = set()  # Records visited locations
        
        # Load map data
        self.maps_data = self.load_maps_data()
        self.showing_story = False
        self.current_story = None
        self.story_text = ""
        self.story_display_text = ""
        self.story_timer = 0
        self.story_char_delay = 0.05  # Interval per character (seconds)
        self.story_char_index = 0
        
        self.load_resources()
        
        # Quality color mapping
        self.quality_colors = {
            "white": (255, 255, 255),
            "green": (0, 255, 0),
            "blue": (0, 191, 255),
            "purple": (148, 0, 211),
            "orange": (255, 165, 0)
        }
        
        # Quality name mapping
        self.quality_names = {
            "white": "White",
            "green": "Green",
            "blue": "Blue",
            "purple": "Purple",
            "orange": "Orange"
        }
        
        # Village and well recovery cooldown timers
        self.village_timer = 0
        self.well_timer = 0
        self.village_cooldown = 1.0  # 1 second cooldown
        self.well_cooldown = 1.0  # 1 second cooldown
        
        # Current status display
        self.current_status = ""
        self.status_timer = 0
        
        # Minimap system
        self.minimap_visible = False       # World Map (toggled with M)
        self.minimap_scale = 2
        self.minimap_width = 500
        self.minimap_height = 500
        self.corner_minimap_visible = True # Corner realtime minimap (always shown)
        self.corner_minimap_size = 150     # Corner minimap size
        self.progress_panel_visible = False # Exploration progress panel (toggled with Tab)
        self.save_notification = ""        # Save notification text
        self.save_notification_timer = 0

        # NPC and dialogue system
        self.npcs = self.load_npcs()
        self.active_npc = None             # NPC currently being talked to
        self.dialogue_text = ""            # Current dialogue text
        self.dialogue_display_text = ""    # Typewriter effect text
        self.dialogue_char_index = 0       # Typewriter char position
        self.dialogue_timer = 0            # Typewriter timer
        self.dialogue_char_delay = 0.03    # Delay per character
        self.dialogue_done = False         # Whether full text is shown

        # Shop system
        self.shop_data = self.load_shop_data()
        self.shop_visible = False
        self.shop_npc_id = None            # Which NPC's shop is open
        self.shop_items = []               # Current shop item list
        self.shop_cursor = 0               # Selected item index
        self.shop_mode = "buy"             # "buy" or "sell"
        self.shop_message = ""             # Transaction feedback message
        self.shop_message_timer = 0

        # Equipment codex (bestiary/gallery for equipment)
        self.codex_visible = False
        self.codex_scroll = 0              # Scroll offset
        self.codex_filter = "all"          # all / weapon / armor / accessory
        # Quality color mapping for codex display
        self.quality_colors = {
            "white": (220, 220, 220),
            "green": (80, 200, 80),
            "blue": (80, 140, 240),
            "purple": (180, 80, 220),
            "orange": (255, 160, 40)
        }
    
    def load_npcs(self):
        """Load NPC data from npcs.json."""
        try:
            with open('npcs.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            npcs = {}
            for npc_id, npc_data in data.items():
                npcs[npc_id] = NPC(npc_id, npc_data)
            print(f"Loaded {len(npcs)} NPCs")
            return npcs
        except FileNotFoundError:
            print("npcs.json not found, no NPCs loaded")
            return {}
        except Exception as e:
            print(f"Failed to load NPCs: {e}")
            return {}

    def get_nearby_npc(self, px, py, radius=2):
        """Find the nearest NPC within radius tiles of the player."""
        for npc_id, npc in self.npcs.items():
            dist = abs(npc.x - px) + abs(npc.y - py)
            if dist <= radius:
                return npc
        return None

    def start_dialogue(self, npc):
        """Start a dialogue with an NPC."""
        self.active_npc = npc
        self.dialogue_text = npc.talk()
        self.dialogue_display_text = ""
        self.dialogue_char_index = 0
        self.dialogue_timer = 0
        self.dialogue_done = False
        print(f"Talking to {npc.name}")

    def advance_dialogue(self):
        """Advance dialogue: finish typewriter or go to next line."""
        if not self.active_npc:
            return
        if not self.dialogue_done:
            # Skip typewriter, show full text
            self.dialogue_display_text = self.dialogue_text
            self.dialogue_char_index = len(self.dialogue_text)
            self.dialogue_done = True
        else:
            # Next dialogue or end
            if self.active_npc.dialogue_index == 0:
                # Cycled back to start, end dialogue
                self.end_dialogue()
            else:
                self.dialogue_text = self.active_npc.talk()
                self.dialogue_display_text = ""
                self.dialogue_char_index = 0
                self.dialogue_timer = 0
                self.dialogue_done = False

    def end_dialogue(self):
        """End the current dialogue."""
        self.active_npc = None
        self.dialogue_text = ""
        self.dialogue_display_text = ""
        self.dialogue_char_index = 0
        self.dialogue_done = False

    def update_dialogue(self, dt):
        """Update dialogue typewriter effect."""
        if not self.active_npc or self.dialogue_done:
            return
        self.dialogue_timer += dt
        if self.dialogue_timer >= self.dialogue_char_delay:
            self.dialogue_timer = 0
            if self.dialogue_char_index < len(self.dialogue_text):
                self.dialogue_display_text += self.dialogue_text[self.dialogue_char_index]
                self.dialogue_char_index += 1
            else:
                self.dialogue_done = True

    def draw_npcs(self, surface):
        """Draw all NPCs on the map."""
        for npc_id, npc in self.npcs.items():
            npc.draw(surface, self.camera.camera.x, self.camera.camera.y)
            # Draw name tag
            screen_x = npc.x * TILE_SIZE - self.camera.camera.x
            screen_y = npc.y * TILE_SIZE - self.camera.camera.y
            if -TILE_SIZE <= screen_x <= SCREEN_WIDTH and -TILE_SIZE <= screen_y <= SCREEN_HEIGHT:
                name = self.small_font.render(npc.name, True, (255, 255, 100))
                name_bg = pygame.Surface((name.get_width() + 4, name.get_height() + 1), pygame.SRCALPHA)
                name_bg.fill((0, 0, 0, 180))
                surface.blit(name_bg, (screen_x + TILE_SIZE // 2 - name.get_width() // 2 - 2, screen_y - 14))
                surface.blit(name, (screen_x + TILE_SIZE // 2 - name.get_width() // 2, screen_y - 13))

                # Interaction hint when nearby
                dist = abs(npc.x - int(self.player.x)) + abs(npc.y - int(self.player.y))
                if dist <= 2 and not self.active_npc:
                    hint = self.small_font.render("[T] Talk", True, (100, 255, 100))
                    surface.blit(hint, (screen_x + TILE_SIZE // 2 - hint.get_width() // 2, screen_y + TILE_SIZE + 2))

    def draw_dialogue_box(self, surface):
        """Draw the dialogue box at the bottom of the screen."""
        if not self.active_npc:
            return

        box_h = 110
        box_w = SCREEN_WIDTH - 80
        box_x = 40
        box_y = SCREEN_HEIGHT - box_h - 20

        # Background
        bg = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        bg.fill((20, 20, 30, 230))
        surface.blit(bg, (box_x, box_y))
        pygame.draw.rect(surface, (200, 180, 100), (box_x, box_y, box_w, box_h), 2, border_radius=6)

        # NPC portrait area (left side)
        portrait_w = 70
        pygame.draw.rect(surface, (40, 40, 50), (box_x + 6, box_y + 6, portrait_w, box_h - 12), border_radius=4)

        # Draw NPC sprite as portrait
        if self.active_npc.sprite:
            portrait = pygame.transform.scale(self.active_npc.sprite, (64, 64))
            surface.blit(portrait, (box_x + 9, box_y + 10))
        else:
            pygame.draw.rect(surface, self.active_npc.color, (box_x + 10, box_y + 10, 60, 60))

        # NPC name
        name_text = self.font.render(self.active_npc.name, True, (255, 215, 0))
        surface.blit(name_text, (box_x + 9, box_y + box_h - 20))

        # Location
        loc_text = self.small_font.render(self.active_npc.location, True, (150, 200, 255))
        surface.blit(loc_text, (box_x + 9 + name_text.get_width() + 8, box_y + box_h - 18))

        # Dialogue text area
        text_x = box_x + portrait_w + 18
        text_y = box_y + 14
        text_w = box_w - portrait_w - 30

        # Wrap and render dialogue text
        if self.dialogue_display_text:
            words = self.dialogue_display_text.split(' ')
            lines = []
            current_line = ""
            for word in words:
                test = current_line + (" " if current_line else "") + word
                rendered = self.font.render(test, True, WHITE)
                if rendered.get_width() > text_w:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
                else:
                    current_line = test
            if current_line:
                lines.append(current_line)

            for i, line in enumerate(lines[:3]):
                line_surf = self.font.render(line, True, WHITE)
                surface.blit(line_surf, (text_x, text_y + i * 26))

        # Hint at bottom right
        if self.dialogue_done:
            hint = self.small_font.render("[Space] Next / [Esc] Close", True, (150, 200, 150))
            surface.blit(hint, (box_x + box_w - hint.get_width() - 12, box_y + box_h - 18))
        else:
            hint = self.small_font.render("[Space] Skip", True, (150, 200, 150))
            surface.blit(hint, (box_x + box_w - hint.get_width() - 12, box_y + box_h - 18))

    def load_shop_data(self):
        """Load shop data from shop.json."""
        try:
            with open('shop.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            print("shop.json not found")
            return {"shops": {}, "npc_shops": {}}

    def get_npc_shop_id(self, npc_id):
        """Get shop type for an NPC."""
        npc_shops = self.shop_data.get("npc_shops", {})
        return npc_shops.get(npc_id)

    def open_shop(self, npc_id):
        """Open shop for a merchant NPC."""
        shop_id = self.get_npc_shop_id(npc_id)
        if not shop_id:
            return False
        shops = self.shop_data.get("shops", {})
        shop = shops.get(shop_id)
        if not shop:
            return False

        self.shop_visible = True
        self.shop_npc_id = npc_id
        self.shop_mode = "buy"
        self.shop_cursor = 0
        self.shop_message = ""
        self.shop_items = shop.get("items", [])
        return True

    def close_shop(self):
        """Close the shop."""
        self.shop_visible = False
        self.shop_npc_id = None
        self.shop_items = []
        self.shop_cursor = 0
        self.shop_message = ""

    def get_sellable_items(self):
        """Get items the player can sell (equipped equipment with value)."""
        sellable = []
        for eq_type, eq_name in self.player.equipment.items():
            if eq_name and eq_name != "Bowl":
                # Find price from shop data or equipment data
                sell_price = 5  # Default
                for eq in self.player.equipment_data:
                    if eq['name'] == eq_name:
                        quality = eq.get('quality', 'white')
                        atk = eq.get('attack', 0)
                        deff = eq.get('defense', 0)
                        sell_price = max(5, (atk + deff) * 3)
                        break
                sellable.append({"name": eq_name, "type": eq_type, "sell_price": sell_price, "desc": f"{eq_type}"})
        return sellable

    def buy_item(self, item):
        """Buy an item from the shop."""
        price = item.get("buy_price", 0)
        if self.player.gold < price:
            self.shop_message = "Not enough gold!"
            self.shop_message_timer = 0
            return

        item_type = item.get("type")
        item_name = item.get("name")

        if item_type == "consumable":
            if item_name == "Food":
                self.player.add_food(1)
            elif item_name == "HP Potion":
                self.player.hp = min(self.player.max_hp, self.player.hp + 50)
            elif item_name == "Stamina Potion":
                self.player.stamina = min(self.player.max_stamina, self.player.stamina + 50)
        elif item_type in self.player.equipment:
            self.player.equipment[item_type] = item_name
            self.player.calculate_stats()

        self.player.gold -= price
        self.shop_message = f"Bought {item_name} for {price} gold!"
        self.shop_message_timer = 0
        print(f"Bought {item_name} for {price} gold")

    def sell_item(self, item):
        """Sell an item."""
        item_name = item.get("name")
        sell_price = item.get("sell_price", 5)

        # Remove from equipment
        for eq_type, eq_name in list(self.player.equipment.items()):
            if eq_name == item_name:
                self.player.equipment[eq_type] = ""
                self.player.calculate_stats()
                break

        self.player.gold += sell_price
        self.shop_message = f"Sold {item_name} for {sell_price} gold!"
        self.shop_message_timer = 0
        print(f"Sold {item_name} for {sell_price} gold")

    def draw_shop(self, surface):
        """Draw the shop interface."""
        if not self.shop_visible:
            return

        # Dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        panel_w = 560
        panel_h = 460
        px = (SCREEN_WIDTH - panel_w) // 2
        py = (SCREEN_HEIGHT - panel_h) // 2

        # Panel background
        bg = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        bg.fill((30, 25, 20, 240))
        surface.blit(bg, (px, py))
        pygame.draw.rect(surface, (200, 180, 100), (px, py, panel_w, panel_h), 2, border_radius=8)

        # Title
        shop_name = "Shop"
        if self.shop_npc_id and self.shop_npc_id in self.npcs:
            shop_name = self.npcs[self.shop_npc_id].name + "'s Shop"
        title = self.font.render(shop_name, True, (255, 215, 0))
        surface.blit(title, (px + (panel_w - title.get_width()) // 2, py + 12))

        # Gold display
        gold_text = self.font.render(f"Gold: {self.player.gold}", True, (255, 200, 50))
        surface.blit(gold_text, (px + panel_w - gold_text.get_width() - 16, py + 14))

        # Mode tabs
        tab_y = py + 45
        tab_w = 100
        buy_tab_x = px + 30
        sell_tab_x = px + 140

        buy_color = (200, 180, 100) if self.shop_mode == "buy" else (80, 70, 50)
        sell_color = (200, 180, 100) if self.shop_mode == "sell" else (80, 70, 50)
        pygame.draw.rect(surface, buy_color, (buy_tab_x, tab_y, tab_w, 26), border_radius=4)
        pygame.draw.rect(surface, sell_color, (sell_tab_x, tab_y, tab_w, 26), border_radius=4)
        buy_text = self.font.render("[B] Buy", True, (255, 255, 255) if self.shop_mode == "buy" else (150, 150, 150))
        sell_text = self.font.render("[N] Sell", True, (255, 255, 255) if self.shop_mode == "sell" else (150, 150, 150))
        surface.blit(buy_text, (buy_tab_x + (tab_w - buy_text.get_width()) // 2, tab_y + 4))
        surface.blit(sell_text, (sell_tab_x + (tab_w - sell_text.get_width()) // 2, tab_y + 4))

        # Items list
        list_y = py + 85
        line_h = 48
        max_lines = 7

        if self.shop_mode == "buy":
            display_items = self.shop_items
        else:
            display_items = self.get_sellable_items()

        if not display_items:
            empty = self.font.render("No items to sell", True, (150, 150, 150))
            surface.blit(empty, (px + (panel_w - empty.get_width()) // 2, list_y + 40))
        else:
            for i, item in enumerate(display_items[:max_lines]):
                item_y = list_y + i * line_h
                is_selected = (i == self.shop_cursor)
                is_hovered = is_selected

                # Highlight selected row
                if is_hovered:
                    hl = pygame.Surface((panel_w - 24, line_h - 4), pygame.SRCALPHA)
                    hl.fill((80, 60, 30, 200))
                    surface.blit(hl, (px + 12, item_y - 2))
                    pygame.draw.rect(surface, (200, 180, 100), (px + 12, item_y - 2, panel_w - 24, line_h - 4), 1, border_radius=4)

                item_name = item.get("name", "?")
                item_desc = item.get("desc", "")

                if self.shop_mode == "buy":
                    price = item.get("buy_price", 0)
                    can_afford = self.player.gold >= price
                    name_color = (255, 255, 255) if can_afford else (180, 80, 80)
                    price_text = f"{price}G"
                    price_color = (255, 200, 50) if can_afford else (200, 80, 80)
                else:
                    price = item.get("sell_price", 5)
                    name_color = (255, 255, 255)
                    price_text = f"{price}G"
                    price_color = (100, 255, 100)

                # Item name
                name_surf = self.font.render(item_name, True, name_color)
                surface.blit(name_surf, (px + 22, item_y + 2))

                # Description
                desc_surf = self.small_font.render(item_desc, True, (180, 180, 180))
                surface.blit(desc_surf, (px + 22, item_y + 24))

                # Price (right aligned)
                price_surf = self.font.render(price_text, True, price_color)
                surface.blit(price_surf, (px + panel_w - price_surf.get_width() - 22, item_y + 8))

                # Action hint on selected
                if is_hovered:
                    if self.shop_mode == "buy":
                        action = "[Enter] Buy"
                    else:
                        action = "[Enter] Sell"
                    act_surf = self.small_font.render(action, True, (100, 255, 100))
                    surface.blit(act_surf, (px + panel_w - act_surf.get_width() - 22, item_y + 28))

        # Message
        if self.shop_message:
            msg_color = (255, 100, 100) if "Not enough" in self.shop_message else (100, 255, 100)
            msg_surf = self.font.render(self.shop_message, True, msg_color)
            surface.blit(msg_surf, (px + (panel_w - msg_surf.get_width()) // 2, py + panel_h - 50))

        # Controls hint
        hints = "[Up/Down] Select  [B] Buy  [N] Sell  [Enter] Trade  [Esc] Close"
        hint_surf = self.small_font.render(hints, True, (180, 180, 180))
        surface.blit(hint_surf, (px + (panel_w - hint_surf.get_width()) // 2, py + panel_h - 22))

    def get_codex_items(self):
        """Get equipment list filtered by current codex filter, sorted by quality then attack."""
        items = self.player.equipment_data
        if self.codex_filter == "weapon":
            items = [e for e in items if e.get("type") == "weapon"]
        elif self.codex_filter == "armor":
            # Armor: wrist_guard, helmet, gauntlet, shoulder, belt, boots
            armor_types = {"wrist_guard", "helmet", "gauntlet", "shoulder", "belt", "boots"}
            items = [e for e in items if e.get("type") in armor_types]
        elif self.codex_filter == "accessory":
            acc_types = {"necklace", "amulet", "ring"}
            items = [e for e in items if e.get("type") in acc_types]
        # Sort by quality rank, then attack+defense
        quality_rank = {"white": 0, "green": 1, "blue": 2, "purple": 3, "orange": 4}
        items = sorted(items, key=lambda e: (quality_rank.get(e.get("quality", "white"), 0), e.get("attack", 0) + e.get("defense", 0)))
        return items

    def draw_codex(self, surface):
        """Draw the equipment codex (gallery) overlay."""
        if not self.codex_visible:
            return

        # Dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        panel_w = 680
        panel_h = 500
        px = (SCREEN_WIDTH - panel_w) // 2
        py = (SCREEN_HEIGHT - panel_h) // 2

        # Panel background
        bg = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        bg.fill((25, 22, 30, 245))
        surface.blit(bg, (px, py))
        pygame.draw.rect(surface, (180, 160, 90), (px, py, panel_w, panel_h), 2, border_radius=8)

        # Title
        title = self.font.render("Equipment Codex", True, (255, 215, 0))
        surface.blit(title, (px + (panel_w - title.get_width()) // 2, py + 12))

        # Count display
        total = len(self.player.equipment_data)
        count_text = self.small_font.render(f"Total: {total}", True, (180, 180, 180))
        surface.blit(count_text, (px + panel_w - count_text.get_width() - 16, py + 16))

        # Filter tabs
        tab_y = py + 46
        tabs = [("all", "All"), ("weapon", "Weapons"), ("armor", "Armor"), ("accessory", "Accessory")]
        tab_x = px + 20
        for tkey, tlabel in tabs:
            is_active = (self.codex_filter == tkey)
            tab_color = (180, 160, 90) if is_active else (60, 55, 45)
            tab_w = 110
            pygame.draw.rect(surface, tab_color, (tab_x, tab_y, tab_w, 24), border_radius=4)
            label_color = (255, 255, 255) if is_active else (150, 150, 150)
            t_surf = self.small_font.render(tlabel, True, label_color)
            surface.blit(t_surf, (tab_x + (tab_w - t_surf.get_width()) // 2, tab_y + 5))
            tab_x += tab_w + 6

        # Column headers
        list_y = py + 80
        col_name_x = px + 24
        col_type_x = px + 250
        col_stat_x = px + 360
        col_qual_x = px + 480

        hdr_color = (200, 180, 100)
        surface.blit(self.small_font.render("Name", True, hdr_color), (col_name_x, list_y))
        surface.blit(self.small_font.render("Slot", True, hdr_color), (col_type_x, list_y))
        surface.blit(self.small_font.render("Stats", True, hdr_color), (col_stat_x, list_y))
        surface.blit(self.small_font.render("Quality", True, hdr_color), (col_qual_x, list_y))
        pygame.draw.line(surface, (100, 90, 60), (px + 20, list_y + 20), (px + panel_w - 20, list_y + 20), 1)

        # Items list (scrollable)
        items = self.get_codex_items()
        line_h = 32
        max_lines = 11
        start_idx = self.codex_scroll
        visible_items = items[start_idx:start_idx + max_lines]

        for i, eq in enumerate(visible_items):
            row_y = list_y + 28 + i * line_h
            quality = eq.get("quality", "white")
            q_color = self.quality_colors.get(quality, (220, 220, 220))

            # Row hover background (alternating)
            if i % 2 == 0:
                row_bg = pygame.Surface((panel_w - 40, line_h - 2), pygame.SRCALPHA)
                row_bg.fill((50, 45, 60, 120))
                surface.blit(row_bg, (px + 20, row_y - 1))

            # Quality color bar on left
            pygame.draw.rect(surface, q_color, (px + 20, row_y, 3, line_h - 4))

            # Name (colored by quality)
            name_surf = self.small_font.render(eq.get("name", "?"), True, q_color)
            surface.blit(name_surf, (col_name_x, row_y + 6))

            # Slot type
            slot_text = eq.get("slot", eq.get("type", ""))
            slot_surf = self.small_font.render(slot_text, True, (180, 180, 180))
            surface.blit(slot_surf, (col_type_x, row_y + 6))

            # Stats
            atk = eq.get("attack", 0)
            deff = eq.get("defense", 0)
            stat_parts = []
            if atk > 0:
                stat_parts.append(f"ATK+{atk}")
            if deff > 0:
                stat_parts.append(f"DEF+{deff}")
            stat_text = " ".join(stat_parts) if stat_parts else "-"
            stat_color = (255, 220, 100) if atk > 0 else (100, 200, 255)
            stat_surf = self.small_font.render(stat_text, True, stat_color)
            surface.blit(stat_surf, (col_stat_x, row_y + 6))

            # Quality label (colored)
            qual_label = quality.capitalize()
            qual_surf = self.small_font.render(qual_label, True, q_color)
            surface.blit(qual_surf, (col_qual_x, row_y + 6))

        # Scroll indicators
        if start_idx > 0:
            up_hint = self.small_font.render("▲ more above", True, (150, 150, 150))
            surface.blit(up_hint, (px + (panel_w - up_hint.get_width()) // 2, list_y + 8))
        if start_idx + max_lines < len(items):
            down_hint = self.small_font.render("▼ more below", True, (150, 150, 150))
            surface.blit(down_hint, (px + (panel_w - down_hint.get_width()) // 2, py + panel_h - 40))

        # Controls hint
        hints = "[1/2/3/4] Filter  [Up/Down] Scroll  [G/Esc] Close"
        hint_surf = self.small_font.render(hints, True, (180, 180, 180))
        surface.blit(hint_surf, (px + (panel_w - hint_surf.get_width()) // 2, py + panel_h - 22))

    def start_transition(self):
        """Begin the fade transition from TITLE to PLAYING."""
        if not self.transitioning:
            self.transitioning = True
            self.transition_timer = 0.0

    def draw_title_screen(self, surface):
        """Draw the title screen overlay."""
        import math
        t = self.title_timer

        # Background gradient (dark -> deep red-brown)
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(20 + ratio * 40)
            g = int(12 + ratio * 18)
            b = int(8 + ratio * 12)
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Decorative star/dust particles (deterministic, drift downward)
        for i in range(40):
            px = int((i * 137 + t * 20) % SCREEN_WIDTH)
            py = int((i * 89 + t * 15) % SCREEN_HEIGHT)
            alpha = int(120 + 80 * math.sin(t * 1.5 + i))
            alpha = max(60, min(200, alpha))
            pt = pygame.Surface((2, 2), pygame.SRCALPHA)
            pt.fill((212, 165, 116, alpha))
            surface.blit(pt, (px, py))

        # Title entrance animation (fade + slide up)
        title_alpha = min(1.0, t / 1.2)
        title_offset_y = int((1.0 - title_alpha) * 40)

        title_text = "She Ji Gui Xu Zhuan"
        subtitle_text = "Ming Dynasty - Rise of Zhu Yuanzhang"

        # Render title with glow
        title_surf = self.font.render(title_text, True, (212, 165, 116))
        title_w = title_surf.get_width()
        title_x = (SCREEN_WIDTH - title_w) // 2
        title_y = 150 + title_offset_y

        # Glow layers
        if title_alpha > 0.3:
            glow_surf = self.font.render(title_text, True, (255, 200, 100))
            for layer in range(4, 0, -1):
                glow_alpha = int(40 * title_alpha / layer)
                g_surf = pygame.Surface((title_w + layer * 8, title_surf.get_height() + layer * 8), pygame.SRCALPHA)
                g_surf.blit(glow_surf, (layer * 4, layer * 4))
                g_surf.set_alpha(glow_alpha)
                surface.blit(g_surf, (title_x - layer * 4, title_y - layer * 4))

        title_surf.set_alpha(int(255 * title_alpha))
        surface.blit(title_surf, (title_x, title_y))

        # Subtitle (appears after title)
        sub_alpha = max(0.0, min(1.0, (t - 0.8) / 0.8))
        if sub_alpha > 0:
            sub_surf = self.small_font.render(subtitle_text, True, (200, 180, 140))
            sub_surf.set_alpha(int(255 * sub_alpha))
            sub_x = (SCREEN_WIDTH - sub_surf.get_width()) // 2
            surface.blit(sub_surf, (sub_x, title_y + 50))

        # Decorative divider line
        if t > 1.5:
            line_alpha = min(1.0, (t - 1.5) / 0.6)
            line_w = int(300 * line_alpha)
            line_x = (SCREEN_WIDTH - line_w) // 2
            line_y = title_y + 90
            div_surf = pygame.Surface((line_w, 2), pygame.SRCALPHA)
            div_surf.fill((212, 165, 116, int(180 * line_alpha)))
            surface.blit(div_surf, (line_x, line_y))

        # Press to start prompt (blinking)
        if t > 2.2:
            prompt_alpha = 0.5 + 0.5 * math.sin(t * 2.5)
            prompt_text = "Press ENTER or Click to Begin"
            prompt_surf = self.font.render(prompt_text, True, (255, 230, 180))
            prompt_surf.set_alpha(int(255 * prompt_alpha))
            prompt_x = (SCREEN_WIDTH - prompt_surf.get_width()) // 2
            prompt_y = 340
            surface.blit(prompt_surf, (prompt_x, prompt_y))

        # Controls preview
        if t > 2.8:
            ctrl_alpha = min(1.0, (t - 2.8) / 0.8)
            controls = [
                "WASD  - Move",
                "T     - Talk to NPC",
                "B/N   - Shop Buy/Sell",
                "G     - Equipment Codex",
                "M     - World Map",
                "S/L   - Save / Load",
                "ESC   - Exit"
            ]
            ctrl_y = 400
            for i, line in enumerate(controls):
                c_surf = self.small_font.render(line, True, (180, 165, 130))
                c_surf.set_alpha(int(200 * ctrl_alpha))
                c_x = (SCREEN_WIDTH - c_surf.get_width()) // 2
                surface.blit(c_surf, (c_x, ctrl_y + i * 20))

        # Footer quote
        if t > 3.5:
            quote_alpha = min(1.0, (t - 3.5) / 1.0)
            quote = '"I was but a clothed peasant of Huaiyou, yet chaos brought me to greatness."'
            q_surf = self.small_font.render(quote, True, (150, 130, 100))
            q_surf.set_alpha(int(180 * quote_alpha))
            q_x = (SCREEN_WIDTH - q_surf.get_width()) // 2
            surface.blit(q_surf, (q_x, SCREEN_HEIGHT - 40))

    def draw_transition(self, surface):
        """Draw fade overlay during TITLE -> PLAYING transition."""
        if not self.transitioning:
            return
        # Transition lasts 0.6s: fade to black (0->0.3s) then fade out (0.3->0.6s)
        duration = 0.6
        progress = self.transition_timer / duration
        if progress >= 1.0:
            self.transitioning = False
            self.state = "PLAYING"
            return

        if progress < 0.5:
            alpha = int(255 * (progress / 0.5))
        else:
            alpha = int(255 * (1.0 - (progress - 0.5) / 0.5))

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        surface.blit(overlay, (0, 0))

    def toggle_minimap(self):
        """Toggle world map display"""
        self.minimap_visible = not self.minimap_visible

    def draw_corner_minimap(self, surface):
        """Draw corner minimap (always shown, real-time player position)"""
        if not self.corner_minimap_visible:
            return

        size = self.corner_minimap_size
        # Bottom right
        mm_x = SCREEN_WIDTH - size - 10
        mm_y = SCREEN_HEIGHT - size - 10

        # Semi-transparent background
        bg = pygame.Surface((size + 4, size + 4), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 180))
        surface.blit(bg, (mm_x - 2, mm_y - 2))

        # Border
        pygame.draw.rect(surface, (150, 150, 150), (mm_x - 2, mm_y - 2, size + 4, size + 4), 1)

        if map_data is None:
            return

        map_w = len(map_data[0]) if map_data else 0
        map_h = len(map_data) if map_data else 0
        if map_w == 0 or map_h == 0:
            return

        scale = size / max(map_w, map_h)

        # Draw simplified map (only key terrain)
        for y in range(0, map_h, 2):  # Skip rows for performance
            for x in range(0, map_w, 2):
                tile_id = map_data[y][x]
                tile_name = tile_map.get(tile_id, "grass")

                if tile_name in ["stone_road", "asphalt_road", "farm_path"]:
                    color = (160, 140, 80)
                elif tile_name in ["water", "calm_river", "shallow_water", "deep_water"]:
                    color = (50, 100, 200)
                elif tile_name in ["mountain", "barren_mountain", "active_volcano"]:
                    color = (100, 100, 100)
                elif tile_name in ["tree", "tree2", "forest"]:
                    color = (30, 100, 30)
                elif tile_name in ["snow_field"]:
                    color = (220, 220, 240)
                elif tile_name in ["desert"]:
                    color = (210, 190, 130)
                elif tile_name in ["house1", "house2", "town", "village"]:
                    color = (180, 130, 60)
                else:
                    color = (60, 100, 60)

                mx = mm_x + x * scale
                my = mm_y + y * scale
                pygame.draw.rect(surface, color, (mx, my, max(1, scale * 2), max(1, scale * 2)))

        # Draw visited locations (green dots)
        for loc_id, loc_info in locations.items():
            if "x" in loc_info and "y" in loc_info:
                mx = mm_x + loc_info["x"] * scale
                my = mm_y + loc_info["y"] * scale
                if loc_id in self.visited_locations:
                    pygame.draw.circle(surface, (0, 255, 0), (int(mx), int(my)), 2)
                else:
                    pygame.draw.circle(surface, (150, 150, 150), (int(mx), int(my)), 1)

        # Draw player position (red blinking dot)
        px = mm_x + self.player.x * scale
        py = mm_y + self.player.y * scale
        # Outer ring
        pygame.draw.circle(surface, (255, 255, 0), (int(px), int(py)), 4, 1)
        # Inner dot
        pygame.draw.circle(surface, (255, 50, 50), (int(px), int(py)), 2)

        # Draw player view range
        view_radius = 6 * scale
        pygame.draw.circle(surface, (255, 255, 100), (int(px), int(py)), int(view_radius), 1)

        # Title
        title = self.small_font.render("Minimap (M to enlarge)", True, (200, 200, 200))
        surface.blit(title, (mm_x, mm_y - 16))

    def draw_progress_panel(self, surface):
        """Draw exploration progress panel"""
        if not self.progress_panel_visible:
            return

        panel_w = 360
        panel_h = 420
        px = (SCREEN_WIDTH - panel_w) // 2
        py = (SCREEN_HEIGHT - panel_h) // 2

        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        # Panel background
        panel_bg = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel_bg.fill((30, 30, 40, 240))
        surface.blit(panel_bg, (px, py))
        pygame.draw.rect(surface, (200, 180, 100), (px, py, panel_w, panel_h), 2, border_radius=8)

        # Title
        title = self.font.render("Exploration Progress", True, (255, 215, 0))
        surface.blit(title, (px + (panel_w - title.get_width()) // 2, py + 15))

        total = len(locations)
        visited = len(self.visited_locations)
        progress_ratio = visited / total if total > 0 else 0

        # Progress bar
        bar_x = px + 30
        bar_y = py + 55
        bar_w = panel_w - 60
        bar_h = 20
        pygame.draw.rect(surface, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h), border_radius=4)
        pygame.draw.rect(surface, (0, 200, 100), (bar_x, bar_y, int(bar_w * progress_ratio), bar_h), border_radius=4)
        progress_text = self.font.render(f"{visited}/{total} ({int(progress_ratio*100)}%)", True, WHITE)
        surface.blit(progress_text, (px + (panel_w - progress_text.get_width()) // 2, bar_y + 2))

        # Location list (two columns)
        list_y = py + 90
        line_h = 22
        col_w = (panel_w - 40) // 2

        sorted_locs = sorted(locations.items(), key=lambda x: x[1].get("min_level", 1))

        for i, (loc_id, loc_info) in enumerate(sorted_locs):
            col = i % 2
            row = i // 2
            lx = px + 20 + col * col_w
            ly = list_y + row * line_h

            if ly + line_h > py + panel_h - 30:
                break

            # Visited/Unvisited markers
            if loc_id in self.visited_locations:
                pygame.draw.circle(surface, (0, 255, 0), (lx + 8, ly + 8), 4)
                color = (255, 255, 255)
            else:
                pygame.draw.circle(surface, (100, 100, 100), (lx + 8, ly + 8), 4, 1)
                color = (130, 130, 130)

            # Location name + level
            name = loc_info["name"]
            lvl = loc_info.get("min_level", 1)
            text = self.small_font.render(f"{name} (Lv.{lvl})", True, color)
            surface.blit(text, (lx + 18, ly + 1))

        # Hint
        hint = self.small_font.render("Tab to close | S to save | L to load", True, (180, 180, 180))
        surface.blit(hint, (px + (panel_w - hint.get_width()) // 2, py + panel_h - 22))
    
    def draw_minimap(self, surface):
        """Draw world map (toggled with M)"""
        if not self.minimap_visible:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        minimap_x = (SCREEN_WIDTH - self.minimap_width) // 2
        minimap_y = (SCREEN_HEIGHT - self.minimap_height) // 2
        
        # Map background
        pygame.draw.rect(surface, (20, 20, 20), (minimap_x - 4, minimap_y - 4, self.minimap_width + 8, self.minimap_height + 8), border_radius=8)
        pygame.draw.rect(surface, (200, 180, 100), (minimap_x - 4, minimap_y - 4, self.minimap_width + 8, self.minimap_height + 8), 2, border_radius=8)
        pygame.draw.rect(surface, (50, 50, 50), (minimap_x, minimap_y, self.minimap_width, self.minimap_height))
        
        if map_data is None:
            return
        
        map_width = len(map_data[0]) if map_data else 0
        map_height = len(map_data) if map_data else 0
        
        if map_width == 0 or map_height == 0:
            return
        
        scale_x = (self.minimap_width - 4) / map_width
        scale_y = (self.minimap_height - 4) / map_height
        
        # Draw terrain
        for y, row in enumerate(map_data):
            for x, tile_id in enumerate(row):
                tile_name = tile_map.get(tile_id, "grass")
                
                if tile_name in ["path", "path_corner", "path_t", "path_cross", "stone_road", "asphalt_road", "farm_path"]:
                    color = (160, 140, 80)
                elif tile_name in ["water", "water_wave", "water_shore", "calm_river", "shallow_water", "deep_water"]:
                    color = (50, 100, 200)
                elif tile_name in ["mountain", "mountain_peak", "barren_mountain", "active_volcano"]:
                    color = (100, 100, 100)
                elif tile_name in ["tree", "tree2", "tree_large", "forest"]:
                    color = (30, 100, 30)
                elif tile_name in ["house1", "house2", "house3", "town", "castle", "village"]:
                    color = (180, 130, 60)
                elif tile_name in ["farmland", "farmland_green", "wheat_field", "rice_field", "vegetable_field"]:
                    color = (100, 150, 50)
                elif tile_name in ["wolf", "tiger", "lion"]:
                    color = (200, 50, 50)
                elif tile_name in ["snow_field"]:
                    color = (220, 220, 240)
                elif tile_name in ["desert"]:
                    color = (210, 190, 130)
                elif tile_name in ["cave"]:
                    color = (60, 40, 40)
                elif tile_name in ["flowers"]:
                    color = (200, 150, 200)
                elif tile_name in ["ruins"]:
                    color = (140, 120, 80)
                else:
                    color = (60, 100, 60)
                
                mx = minimap_x + 2 + x * scale_x
                my = minimap_y + 2 + y * scale_y
                mw = max(1, scale_x)
                mh = max(1, scale_y)
                
                pygame.draw.rect(surface, color, (mx, my, mw, mh))
        
        # Draw location markers and names
        for loc_id, loc_info in locations.items():
            if "x" in loc_info and "y" in loc_info:
                mx = minimap_x + 2 + loc_info["x"] * scale_x
                my = minimap_y + 2 + loc_info["y"] * scale_y
                cx = int(mx + scale_x / 2)
                cy = int(my + scale_y / 2)

                # Visited=gold solid, Unvisited=gray hollow
                if loc_id in self.visited_locations:
                    pygame.draw.circle(surface, (0, 255, 100), (cx, cy), 5)
                    pygame.draw.circle(surface, (255, 255, 255), (cx, cy), 5, 1)
                    name_color = (0, 255, 100)
                else:
                    pygame.draw.circle(surface, (200, 200, 200), (cx, cy), 4, 2)
                    name_color = (200, 200, 200)

                # Location name (using Chinese font)
                name_text = self.font.render(loc_info["name"], True, name_color)
                name_bg = pygame.Surface((name_text.get_width() + 6, name_text.get_height() + 2), pygame.SRCALPHA)
                name_bg.fill((0, 0, 0, 180))
                surface.blit(name_bg, (cx - name_text.get_width() // 2 - 3, cy + 6))
                surface.blit(name_text, (cx - name_text.get_width() // 2, cy + 7))

                # Level label
                lvl = loc_info.get("min_level", 1)
                lvl_text = self.small_font.render(f"Lv.{lvl}", True, (255, 200, 100))
                surface.blit(lvl_text, (cx + 6, cy - 14))
        
        # Draw player position
        player_mx = minimap_x + 2 + self.player.x * scale_x
        player_my = minimap_y + 2 + self.player.y * scale_y
        pygame.draw.circle(surface, (255, 0, 0), (int(player_mx + scale_x/2), int(player_my + scale_y/2)), 6)
        pygame.draw.circle(surface, (255, 255, 0), (int(player_mx + scale_x/2), int(player_my + scale_y/2)), 6, 2)

        # Current location name
        current_loc = get_current_location_name(int(self.player.x), int(self.player.y))
        if current_loc and current_loc != "Path of Rise":
            loc_text = self.font.render(f"Current Location: {current_loc}", True, (255, 255, 0))
            surface.blit(loc_text, (minimap_x + 10, minimap_y + self.minimap_height + 8))

        # Progress info
        total = len(locations)
        visited = len(self.visited_locations)
        progress_str = f"Exploration: {visited}/{total} ({int(visited/total*100) if total > 0 else 0}%)"
        progress_text = self.font.render(progress_str, True, (0, 255, 100))
        surface.blit(progress_text, (minimap_x + self.minimap_width - progress_text.get_width() - 10, minimap_y + self.minimap_height + 8))

        # Legend
        legend_y = minimap_y + self.minimap_height + 35
        pygame.draw.circle(surface, (0, 255, 100), (minimap_x + 15, legend_y + 8), 4)
        surface.blit(self.small_font.render("Visited", True, (200, 200, 200)), (minimap_x + 25, legend_y + 1))
        pygame.draw.circle(surface, (200, 200, 200), (minimap_x + 90, legend_y + 8), 4, 2)
        surface.blit(self.small_font.render("Unvisited", True, (200, 200, 200)), (minimap_x + 100, legend_y + 1))
        pygame.draw.circle(surface, (255, 0, 0), (minimap_x + 165, legend_y + 8), 4)
        surface.blit(self.small_font.render("Player", True, (200, 200, 200)), (minimap_x + 175, legend_y + 1))

        # Title and hint
        title = self.font.render("World Map", True, (255, 215, 0))
        title_rect = title.get_rect(center=(minimap_x + self.minimap_width//2, minimap_y - 18))
        surface.blit(title, title_rect)

        hint = self.small_font.render("Press M to close | Tab for details", True, (200, 200, 200))
        hint_rect = hint.get_rect(center=(minimap_x + self.minimap_width//2, legend_y + 25))
        surface.blit(hint, hint_rect)
    
    def drop_equipment(self):
        """Randomly drop equipment"""
        import random
        equipment_list = self.player.equipment_data
        if equipment_list:
            # Get current map level
            current_location_level = get_location_min_level(int(self.player.x), int(self.player.y))
            
            # Determine droppable quality based on map level
            if current_location_level <= 1:
                # Low-level maps like Zhongli, only green and below
                available_equipment = [eq for eq in equipment_list if eq['quality'] in ['white', 'green']]
            elif current_location_level <= 5:
                # Mid-level maps, blue and below
                available_equipment = [eq for eq in equipment_list if eq['quality'] in ['white', 'green', 'blue']]
            elif current_location_level <= 10:
                # High-level maps, purple and below
                available_equipment = [eq for eq in equipment_list if eq['quality'] in ['white', 'green', 'blue', 'purple']]
            else:
                # Highest-level maps, all qualities
                available_equipment = equipment_list
            
            if available_equipment:
                # Randomly select one equipment
                self.dropped_equipment = random.choice(available_equipment)
                self.show_equipment_drop = True
                print(f"Equipment dropped: {self.dropped_equipment['name']} (quality: {self.dropped_equipment['quality']})")
            else:
                print("Cannot drop equipment at current map level")
    
    def replace_equipment(self):
        """Replace equipment"""
        if self.dropped_equipment:
            eq_type = self.dropped_equipment['type']
            self.player.equipment[eq_type] = self.dropped_equipment['name']
            # Recalculate stats
            self.player.calculate_stats()
            print(f"Equipped: {self.dropped_equipment['name']}")
            self.show_equipment_drop = False
            self.dropped_equipment = None
    
    def draw_equipment_drop(self, surface):
        """Draw equipment drop interface"""
        if not self.dropped_equipment:
            return
        
        # Calculate interface position
        width = 300
        height = 150
        x = (SCREEN_WIDTH - width) // 2
        y = (SCREEN_HEIGHT - height) // 2
        
        # Draw background
        pygame.draw.rect(surface, (50, 50, 50, 200), (x, y, width, height), border_radius=10)
        
        # Draw title
        title = self.font.render("Equipment Found", True, WHITE)
        title_rect = title.get_rect(center=(x + width//2, y + 20))
        surface.blit(title, title_rect)
        
        # Draw equipment info
        eq = self.dropped_equipment
        name_color = self.quality_colors.get(eq['quality'], WHITE)
        name_text = self.font.render(eq['name'], True, name_color)
        name_rect = name_text.get_rect(center=(x + width//2, y + 50))
        surface.blit(name_text, name_rect)
        
        # Draw slot info
        slot_text = self.small_font.render(f"Slot: {eq.get('slot', 'Unknown')}", True, (200, 200, 200))
        slot_rect = slot_text.get_rect(center=(x + width//2, y + 70))
        surface.blit(slot_text, slot_rect)
        
        # Draw stats
        attack_text = self.small_font.render(f"ATK: +{eq['attack']}", True, WHITE)
        defense_text = self.small_font.render(f"DEF: +{eq['defense']}", True, WHITE)
        quality_name = self.quality_names.get(eq['quality'], eq['quality'])
        quality_text = self.small_font.render(f"Quality: {quality_name}", True, name_color)
        
        surface.blit(attack_text, (x + 50, y + 80))
        surface.blit(defense_text, (x + 180, y + 80))
        surface.blit(quality_text, (x + 50, y + 100))
        
        # Draw action hint
        hint_text = self.small_font.render("Press R to equip, Q to discard", True, (200, 200, 200))
        hint_rect = hint_text.get_rect(center=(x + width//2, y + 130))
        surface.blit(hint_text, hint_rect)
    
    def update_chopping(self, dt):
        """Update chopping system"""
        # Check stamina
        if self.player.stamina <= 0:
            return
        
        # Check if near tree
        player_x, player_y = int(self.player.x), int(self.player.y)
        near_tree = self.is_near_tree(player_x, player_y)
        
        if near_tree:
            if not self.chopping_tree:
                # Start chopping
                self.chopping_tree = True
                self.chopping_progress = 0
                self.chopping_timer = 0
            else:
                # Chopping progress
                self.chopping_timer += dt
                self.chopping_progress = min(self.chopping_timer / self.chopping_max, 1.0)
                
                if self.chopping_progress >= 1.0:
                    # Chopping complete, drop equipment
                    self.drop_equipment()
                    # Chopping consumes stamina
                    self.player.consume_stamina(10)
                    self.chopping_tree = False
                    self.chopping_progress = 0
                    self.chopping_timer = 0
                    self.auto_equip_timer = 0
        else:
            # Not near tree, stop chopping
            self.chopping_tree = False
            self.chopping_progress = 0
            self.chopping_timer = 0
        
        # Auto-equip logic
        if self.show_equipment_drop:
            self.auto_equip_timer += dt
            if self.auto_equip_timer >= self.auto_equip_max:
                # Auto decide whether to equip
                self.auto_equip()
    
    def update_battle(self, dt):
        """Update battle system"""
        # Check stamina
        if self.player.stamina <= 0:
            return
        
        # If showing battle result
        if self.battle_result is not None:
            self.battle_result_timer += dt
            if self.battle_result_timer >= self.battle_result_max:
                self.battle_result = None
                self.battle_result_timer = 0
            return
        
        # Check if near monster
        player_x, player_y = int(self.player.x), int(self.player.y)
        near_monster = self.is_near_monster(player_x, player_y)
        
        if near_monster:
            if not self.in_battle:
                # Start battle
                self.in_battle = True
                self.battle_progress = 0
                self.battle_timer = 0
                self.current_monster = near_monster
            else:
                # Battle progress
                self.battle_timer += dt
                self.battle_progress = min(self.battle_timer / self.battle_max, 1.0)
                
                if self.battle_progress >= 1.0:
                    # Battle ended, determine win/lose
                    self.check_battle_result()
                    # Battle consumes stamina
                    self.player.consume_stamina(15)
        else:
            # Not near monster, stop battle
            self.in_battle = False
            self.battle_progress = 0
            self.battle_timer = 0
            self.current_monster = None
    
    def is_near_monster(self, x, y):
        """Check if near monster"""
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if (nx, ny) in self.monsters:
                    return self.monsters[(nx, ny)]
        return None
    
    def check_battle_result(self):
        """Determine battle result"""
        if not self.current_monster:
            return
        
        player_atk = self.player.attack
        player_def = self.player.defense
        monster_atk = self.current_monster['attack']
        monster_def = self.current_monster['defense']
        
        # Player power = ATK + DEF
        player_power = player_atk + player_def
        monster_power = monster_atk + monster_def
        
        if player_power >= monster_power:
            # Win
            self.battle_result = "win"
            exp_reward = self.current_monster['exp_reward']
            gold_reward = self.current_monster.get('gold_reward', random.randint(5, 15))
            self.player.gain_exp(exp_reward)
            self.player.gold += gold_reward
            print(f"Battle won! Gained {exp_reward} EXP and {gold_reward} gold")
        else:
            # Lose
            self.battle_result = "lose"
            print(f"Battle lost! ATK {player_atk}, DEF {player_def} not enough, keep trying!")
        
        self.in_battle = False
        self.battle_progress = 0
        self.battle_timer = 0
        self.battle_result_timer = 0
    
    def update_story(self, dt):
        """Update story system"""
        # Update story text display
        if self.showing_story:
            self.story_timer += dt
            if self.story_timer >= self.story_char_delay:
                self.story_timer = 0
                if self.story_char_index < len(self.story_text):
                    self.story_display_text += self.story_text[self.story_char_index]
                    self.story_char_index += 1
    
    def trigger_story(self, location_name):
        """Trigger story"""
        if location_name in self.stories_data:
            story_data = self.stories_data[location_name]
            self.current_story = story_data
            self.story_text = story_data['story']
            self.story_display_text = ""
            self.story_char_index = 0
            self.showing_story = True
            print(f"Story triggered: {story_data['name']} - {story_data['year']}")
    
    def check_new_location(self):
        """Check if entered new location"""
        current_location_id = self.get_current_location_id()
        if current_location_id and current_location_id not in self.visited_locations:
            self.visited_locations.add(current_location_id)
            self.trigger_story(current_location_id)
    
    def is_near_tree(self, x, y):
        """Check if near tree"""
        # Check surrounding 8 tiles
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(map_data[0]) and 0 <= ny < len(map_data):
                    tile_id = map_data[ny][nx]
                    # Check if it's a tree
                    if tile_id == 7 or tile_id == 8:  # tree and tree2
                        return True
        return False
    
    def is_near_farm(self, x, y):
        """Check if near farmland"""
        # Check surrounding 8 tiles
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(map_data[0]) and 0 <= ny < len(map_data):
                    tile_id = map_data[ny][nx]
                    # Check if it's farmland
                    if tile_id in [14, 15, 16]:  # wheat_field, rice_field, vegetable_field
                        return True
        return False
    
    def plant_crop(self):
        """Plant crop"""
        if self.player.stamina >= 20:
            self.player.consume_stamina(20)
            # Add food
            self.player.add_food(3)
            return True
        return False
    
    def is_near_village(self, x, y):
        """Check if near village"""
        # Check surrounding 8 tiles
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(map_data[0]) and 0 <= ny < len(map_data):
                    tile_id = map_data[ny][nx]
                    # Check if it's a village
                    if tile_id == 34:  # village
                        return True
        return False
    
    def is_near_well(self, x, y):
        """Check if near well"""
        # Check surrounding 8 tiles
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(map_data[0]) and 0 <= ny < len(map_data):
                    tile_id = map_data[ny][nx]
                    # Check if it's a well
                    if tile_id == 12 or tile_id == 13:  # well and well2
                        return True
        return False
    
    def draw_chopping_progress(self, surface):
        """Draw chopping progress bar"""
        width = 200
        height = 20
        x = (SCREEN_WIDTH - width) // 2
        y = SCREEN_HEIGHT - 100
        
        # Draw background
        pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height), border_radius=5)
        
        # Draw progress
        progress_width = int(width * self.chopping_progress)
        pygame.draw.rect(surface, (0, 255, 0), (x, y, progress_width, height), border_radius=5)
        
        # Draw text
        text = self.font.render("Chopping...", True, WHITE)
        text_rect = text.get_rect(center=(x + width//2, y - 20))
        surface.blit(text, text_rect)
    
    def draw_battle_progress(self, surface):
        """Draw battle progress bar"""
        width = 200
        height = 20
        x = (SCREEN_WIDTH - width) // 2
        y = SCREEN_HEIGHT - 150
        
        # Draw background
        pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height), border_radius=5)
        
        # Draw progress
        progress_width = int(width * self.battle_progress)
        pygame.draw.rect(surface, (255, 0, 0), (x, y, progress_width, height), border_radius=5)
        
        # Draw text
        if self.current_monster:
            monster_name = self.current_monster['name']
            text = self.font.render(f"Battle: {monster_name}", True, WHITE)
        else:
            text = self.font.render("Battling...", True, WHITE)
        text_rect = text.get_rect(center=(x + width//2, y - 20))
        surface.blit(text, text_rect)
    
    def draw_battle_result(self, surface):
        """Draw battle result"""
        width = 300
        height = 150
        x = (SCREEN_WIDTH - width) // 2
        y = (SCREEN_HEIGHT - height) // 2
        
        # Draw background
        pygame.draw.rect(surface, (50, 50, 50, 220), (x, y, width, height), border_radius=10)
        
        if self.battle_result == "win":
            # Win
            title = self.font.render("Battle Won!", True, (0, 255, 0))
            title_rect = title.get_rect(center=(x + width//2, y + 30))
            surface.blit(title, title_rect)
            
            if self.current_monster:
                exp_text = self.small_font.render(f"Gained {self.current_monster['exp_reward']} EXP", True, (255, 255, 0))
                exp_rect = exp_text.get_rect(center=(x + width//2, y + 70))
                surface.blit(exp_text, exp_rect)
        else:
            # Lose
            title = self.font.render("Battle Lost!", True, (255, 0, 0))
            title_rect = title.get_rect(center=(x + width//2, y + 30))
            surface.blit(title, title_rect)
            
            hint_text = self.small_font.render("ATK and DEF not enough", True, (200, 200, 200))
            hint_rect = hint_text.get_rect(center=(x + width//2, y + 60))
            surface.blit(hint_text, hint_rect)
            
            atk_text = self.small_font.render(f"Current ATK: {self.player.attack}", True, WHITE)
            def_text = self.small_font.render(f"Current DEF: {self.player.defense}", True, WHITE)
            surface.blit(atk_text, (x + 50, y + 85))
            surface.blit(def_text, (x + 50, y + 105))
    
    def draw_monsters(self, surface):
        """Draw monsters"""
        for (mx, my), monster in self.monsters.items():
            screen_x = mx * TILE_SIZE - self.camera.camera.x
            screen_y = my * TILE_SIZE - self.camera.camera.y
            
            sprite_name = monster['sprite']
            if sprite_name in self.monster_sprites:
                surface.blit(self.monster_sprites[sprite_name], (screen_x, screen_y))
    
    def draw_story(self, surface):
        """Draw story interface"""
        if not self.current_story:
            return
        
        # Draw semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        
        # Draw story box
        story_width = 600
        story_height = 300
        story_x = (SCREEN_WIDTH - story_width) // 2
        story_y = (SCREEN_HEIGHT - story_height) // 2
        
        pygame.draw.rect(surface, (50, 50, 50, 220), (story_x, story_y, story_width, story_height), border_radius=10)
        pygame.draw.rect(surface, (200, 200, 200), (story_x, story_y, story_width, story_height), 2, border_radius=10)
        
        # Draw title (location name and year)
        if self.current_story:
            title_text = self.font.render(f"{self.current_story['name']} - {self.current_story['year']}", True, (255, 215, 0))
            title_rect = title_text.get_rect(center=(story_x + story_width//2, story_y + 30))
            surface.blit(title_text, title_rect)
        
        # Draw story text (character by character)
        # Split text into multiple lines
        lines = []
        current_line = ""
        max_line_width = story_width - 40
        
        for char in self.story_display_text:
            test_line = current_line + char
            test_width = self.font.size(test_line)[0]
            if test_width <= max_line_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = char
        
        if current_line:
            lines.append(current_line)
        
        # Draw each line
        line_height = 30
        start_y = story_y + 60
        for i, line in enumerate(lines):
            if i >= 8:  # Max 8 lines
                break
            text = self.font.render(line, True, WHITE)
            text_rect = text.get_rect(topleft=(story_x + 20, start_y + i * line_height))
            surface.blit(text, text_rect)
        
        # Draw hint text
        hint_text = self.small_font.render("Press Enter to continue", True, (200, 200, 200))
        hint_rect = hint_text.get_rect(center=(story_x + story_width//2, story_y + story_height - 30))
        surface.blit(hint_text, hint_rect)
    
    def auto_equip(self):
        """Auto-equip logic"""
        if not self.dropped_equipment:
            return
        
        eq = self.dropped_equipment
        eq_type = eq['type']
        current_eq_name = self.player.equipment.get(eq_type, "")
        
        # Quality priority
        quality_order = {"white": 1, "green": 2, "blue": 3, "purple": 4, "orange": 5}
        
        if current_eq_name:
            # Find current equipment
            current_eq = None
            for item in self.player.equipment_data:
                if item['name'] == current_eq_name:
                    current_eq = item
                    break
            
            if current_eq:
                current_quality = quality_order.get(current_eq['quality'], 0)
                new_quality = quality_order.get(eq['quality'], 0)
                
                if new_quality > current_quality:
                    # New equipment better, auto-equip
                    self.player.equipment[eq_type] = eq['name']
                    self.player.calculate_stats()
                    print(f"Auto-equipped: {eq['name']}")
                else:
                    # New equipment worse, auto-discard
                    print(f"Auto-discarded: {eq['name']}")
        else:
            # No current equipment, auto-equip
            self.player.equipment[eq_type] = eq['name']
            self.player.calculate_stats()
            print(f"Auto-equipped: {eq['name']}")
        
        # Close equipment drop interface
        self.show_equipment_drop = False
        self.dropped_equipment = None

    def load_resources(self):
        load_tiles()
        self.load_monster_sprites()
    
    def load_monsters_data(self):
        """Load monster data"""
        try:
            with open('monsters.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('monsters', [])
        except:
            return []
    
    def load_monsters(self):
        """Load monster positions"""
        monsters = {}
        for y, row in enumerate(map_data):
            for x, tile_id in enumerate(row):
                if tile_id == 100:  # wolf
                    monsters[(x, y)] = self.get_monster_by_id(1)
                elif tile_id == 101:  # tiger
                    monsters[(x, y)] = self.get_monster_by_id(2)
                elif tile_id == 102:  # lion
                    monsters[(x, y)] = self.get_monster_by_id(3)
        return monsters
    
    def load_stories_data(self):
        """Load story data"""
        try:
            with open('stories.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('stories', {})
        except:
            return {}
    
    def load_maps_data(self):
        """Load map data"""
        try:
            with open('maps.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"maps": {}}
    
    def save_game(self):
        """Save game progress"""
        import datetime
        save_data = {
            "player": {
                "x": self.player.x,
                "y": self.player.y,
                "level": self.player.level,
                "exp": self.player.exp,
                "exp_to_next_level": self.player.exp_to_next_level,
                "hp": self.player.hp,
                "max_hp": self.player.max_hp,
                "stamina": self.player.stamina,
                "max_stamina": self.player.max_stamina,
                "food": self.player.food,
                "gold": self.player.gold,
                "attack": self.player.attack,
                "defense": self.player.defense,
                "equipment": self.player.equipment.copy()
            },
            "visited_locations": list(self.visited_locations),
            "scene_name": self.scene_name,
            "save_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "explore_progress": f"{len(self.visited_locations)}/{len(locations)}"
        }
        
        try:
            with open('savegame.json', 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            self.save_notification = f"Saved! {self.scene_name} | Exploration {len(self.visited_locations)}/{len(locations)}"
            self.save_notification_timer = 0
            print("Game saved!")
        except Exception as e:
            self.save_notification = f"Save failed: {e}"
            self.save_notification_timer = 0
            print(f"Save failed: {e}")
    
    def load_game(self):
        """Load game progress"""
        save_file = 'savegame.json'
        if not os.path.exists(save_file):
            print("No save file found, using defaults")
            return False
        
        try:
            with open(save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            player_data = save_data.get("player", {})
            self.player.x = player_data.get("x", 60)
            self.player.y = player_data.get("y", 60)
            self.player.target_x = self.player.x
            self.player.target_y = self.player.y
            self.player.level = player_data.get("level", 1)
            self.player.exp = player_data.get("exp", 0)
            self.player.exp_to_next_level = player_data.get("exp_to_next_level", 100)
            self.player.hp = player_data.get("hp", 100)
            self.player.max_hp = player_data.get("max_hp", 100)
            self.player.stamina = player_data.get("stamina", 100)
            self.player.max_stamina = player_data.get("max_stamina", 100)
            self.player.food = player_data.get("food", 0)
            self.player.gold = player_data.get("gold", 50)
            
            equipment = player_data.get("equipment", {})
            for eq_type, eq_name in equipment.items():
                if eq_type in self.player.equipment:
                    self.player.equipment[eq_type] = eq_name
            
            self.player.calculate_stats()
            self.player.update_skin()
            
            visited = save_data.get("visited_locations", [])
            self.visited_locations = set(visited)
            
            self.scene_name = save_data.get("scene_name", "Zhongli")
            
            save_time = save_data.get("save_time", "Unknown time")
            progress = save_data.get("explore_progress", f"{len(self.visited_locations)}/{len(locations)}")
            self.save_notification = f"Save loaded ({save_time}) | Exploration {progress}"
            self.save_notification_timer = 0
            
            print("Game loaded!")
            return True
        except Exception as e:
            print(f"Load failed: {e}")
            return False
    
    def get_current_location_id(self):
        """Get current location ID"""
        x, y = int(self.player.x), int(self.player.y)
        locations = self.maps_data['maps']['main_map']['locations']
        
        # Check if within a location's range
        for loc_id, loc_data in locations.items():
            loc_x, loc_y = loc_data['x'], loc_data['y']
            if abs(x - loc_x) <= 2 and abs(y - loc_y) <= 2:
                return loc_id
        
        return None
    
    def get_monster_by_id(self, monster_id):
        """Get monster data by ID"""
        for monster in self.monsters_data:
            if monster['id'] == monster_id:
                return monster.copy()
        return None
    
    def load_monster_sprites(self):
        """Load monster sprites"""
        self.monster_sprites = {}
        for monster in self.monsters_data:
            sprite_name = monster['sprite']
            sprite_path = f"tiles/{sprite_name}.png"
            if os.path.exists(sprite_path):
                img = pygame.image.load(sprite_path).convert_alpha()
                self.monster_sprites[sprite_name] = img
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # --- TITLE state: only handle Enter / click to start, or Esc to quit ---
            if self.state == "TITLE":
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self.start_transition()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.start_transition()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return False
                continue
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.shop_visible:
                        self.close_shop()
                        continue
                    elif self.codex_visible:
                        self.codex_visible = False
                        continue
                    elif self.active_npc:
                        self.end_dialogue()
                        continue
                    else:
                        return False
                elif event.key == pygame.K_RETURN and self.showing_story:
                    # Press Enter to end story
                    self.showing_story = False
                    self.current_story = None
                    self.story_text = ""
                    self.story_display_text = ""
                    self.story_char_index = 0
                elif event.key == pygame.K_a:
                    # Press A to toggle auto-farming
                    is_farming = self.player.toggle_auto_farming()
                    print(f"Auto-farming: {'ON' if is_farming else 'OFF'}")
                elif event.key == pygame.K_r and self.show_equipment_drop:
                    # Press R to replace equipment
                    self.replace_equipment()
                elif event.key == pygame.K_q and self.show_equipment_drop:
                    # Press Q to discard equipment
                    self.show_equipment_drop = False
                    self.dropped_equipment = None
                elif event.key == pygame.K_e:
                    # Press E to toggle equipment panel
                    self.equipment_panel_visible = not self.equipment_panel_visible
                elif event.key == pygame.K_s:
                    # Press S to save game
                    self.save_game()
                    print("Game saved!")
                elif event.key == pygame.K_l:
                    # Press L to load game
                    success = self.load_game()
                    if success:
                        print("Game loaded!")
                    else:
                        print("No save file found!")
                elif event.key == pygame.K_m:
                    # Press M to toggle world map
                    self.toggle_minimap()
                    print(f"World Map: {'ON' if self.minimap_visible else 'OFF'}")
                elif event.key == pygame.K_TAB:
                    # Press Tab to toggle exploration progress panel
                    self.progress_panel_visible = not self.progress_panel_visible
                elif event.key == pygame.K_t:
                    # Press T to talk to nearby NPC
                    if not self.active_npc:
                        npc = self.get_nearby_npc(int(self.player.x), int(self.player.y))
                        if npc:
                            self.start_dialogue(npc)
                elif event.key == pygame.K_SPACE:
                    # Press Space to advance dialogue
                    if self.active_npc:
                        self.advance_dialogue()
                elif event.key == pygame.K_b:
                    # Press B to open shop (near merchant) or switch to buy tab
                    if self.shop_visible:
                        self.shop_mode = "buy"
                        self.shop_cursor = 0
                        self.shop_message = ""
                    elif not self.active_npc:
                        npc = self.get_nearby_npc(int(self.player.x), int(self.player.y))
                        if npc and self.get_npc_shop_id(npc.id):
                            self.open_shop(npc.id)
                elif event.key == pygame.K_n:
                    # Press N to switch to sell tab in shop
                    if self.shop_visible:
                        self.shop_mode = "sell"
                        self.shop_cursor = 0
                        self.shop_message = ""
                elif event.key == pygame.K_UP and self.shop_visible:
                    if self.shop_cursor > 0:
                        self.shop_cursor -= 1
                elif event.key == pygame.K_DOWN and self.shop_visible:
                    max_items = len(self.shop_items if self.shop_mode == "buy" else self.get_sellable_items())
                    if self.shop_cursor < min(max_items, 7) - 1:
                        self.shop_cursor += 1
                elif event.key == pygame.K_UP and self.codex_visible:
                    if self.codex_scroll > 0:
                        self.codex_scroll -= 1
                elif event.key == pygame.K_DOWN and self.codex_visible:
                    items_count = len(self.get_codex_items())
                    if self.codex_scroll + 11 < items_count:
                        self.codex_scroll += 1
                elif event.key == pygame.K_RETURN and self.shop_visible:
                    if self.shop_mode == "buy":
                        if self.shop_items and self.shop_cursor < len(self.shop_items):
                            self.buy_item(self.shop_items[self.shop_cursor])
                    else:
                        sellable = self.get_sellable_items()
                        if sellable and self.shop_cursor < len(sellable):
                            self.sell_item(sellable[self.shop_cursor])
                elif event.key == pygame.K_p:
                    # Press P to plant crop
                    if self.is_near_farm(int(self.player.x), int(self.player.y)):
                        success = self.plant_crop()
                        if success:
                            print("Planted! Got 3 food!")
                        else:
                            print("Not enough stamina to plant!")
                    else:
                        print("No farm nearby!")
                elif event.key == pygame.K_f:
                    # Press F to eat food
                    success = self.player.eat_food()
                    if success:
                        print("Ate! Recovered 30 stamina!")
                    else:
                        print("No food left!")
                elif event.key == pygame.K_g:
                    # Press G to toggle equipment codex
                    self.codex_visible = not self.codex_visible
                    if self.codex_visible:
                        self.codex_scroll = 0
                        self.codex_filter = "all"
                elif self.codex_visible and event.key == pygame.K_1:
                    self.codex_filter = "all"
                    self.codex_scroll = 0
                elif self.codex_visible and event.key == pygame.K_2:
                    self.codex_filter = "weapon"
                    self.codex_scroll = 0
                elif self.codex_visible and event.key == pygame.K_3:
                    self.codex_filter = "armor"
                    self.codex_scroll = 0
                elif self.codex_visible and event.key == pygame.K_4:
                    self.codex_filter = "accessory"
                    self.codex_scroll = 0

        # No movement allowed while showing story, in dialogue, in shop, or in codex
        if self.showing_story or self.active_npc or self.shop_visible or self.codex_visible:
            return True

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1
        elif keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1

        if dx != 0 or dy != 0:
            if not self.player.auto_farming:
                # Calculate target position
                target_x = int(self.player.x) + dx
                target_y = int(self.player.y) + dy
                
                # Check current location level
                current_min_level = get_location_min_level(int(self.player.x), int(self.player.y))
                
                # Check target location level requirement
                target_min_level = get_location_min_level(target_x, target_y)
                
                # Allow movement if player is currently in high-level area (even if target is high-level)
                if current_min_level > self.player.level:
                    self.player.try_move(dx, dy)
                    self.scene_name = get_current_location_name(int(self.player.x), int(self.player.y))
                elif target_min_level > self.player.level:
                    print(f"Level too low! Need level {target_min_level} to enter this area")
                else:
                    self.player.try_move(dx, dy)
                    self.scene_name = get_current_location_name(int(self.player.x), int(self.player.y))

        return True

    def draw_map(self, surface):
        if map_data is None:
            return
        
        map_height = len(map_data)
        if map_height == 0:
            return
        
        map_width = len(map_data[0]) if map_data[0] else 0
        
        visible_tiles_x = SCREEN_WIDTH // TILE_SIZE + 2
        visible_tiles_y = SCREEN_HEIGHT // TILE_SIZE + 2
        
        start_x = max(0, int(self.camera.camera.x // TILE_SIZE) - 1)
        start_y = max(0, int(self.camera.camera.y // TILE_SIZE) - 1)
        end_x = min(map_width, start_x + visible_tiles_x)
        end_y = min(map_height, start_y + visible_tiles_y)
        
        for y in range(start_y, end_y):
            if y >= len(map_data):
                continue
            row = map_data[y]
            for x in range(start_x, end_x):
                if x >= len(row):
                    continue
                tile_id = row[x]
                tile_name = tile_map.get(tile_id, "grass")
                
                if tile_name in tile_images:
                    tile_image = tile_images[tile_name]
                else:
                    if "grass" in tile_images:
                        tile_image = tile_images["grass"]
                    else:
                        tile_image = None
                
                if tile_image:
                    screen_x = x * TILE_SIZE - self.camera.camera.x
                    screen_y = y * TILE_SIZE - self.camera.camera.y
                    surface.blit(tile_image, (screen_x, screen_y))
        
        for loc_id, loc_info in locations.items():
            loc_x = loc_info.get("x", 0)
            loc_y = loc_info.get("y", 0)
            
            if start_x <= loc_x < end_x and start_y <= loc_y < end_y:
                screen_x = loc_x * TILE_SIZE - self.camera.camera.x
                screen_y = loc_y * TILE_SIZE - self.camera.camera.y
                
                name_text = self.small_font.render(loc_info["name"], True, (255, 215, 0))
                name_rect = name_text.get_rect(center=(screen_x + TILE_SIZE//2, screen_y - 8))
                
                pygame.draw.rect(surface, (0, 0, 0, 180), 
                               (name_rect.x - 4, name_rect.y - 2, name_rect.width + 8, name_rect.height + 4))
                surface.blit(name_text, name_rect)

    def draw_ui(self, surface):
        self.scene_name = get_current_location_name(int(self.player.x), int(self.player.y))
        current_min_level = get_location_min_level(int(self.player.x), int(self.player.y))
        
        # Draw scene name
        text = self.font.render(self.scene_name, True, WHITE)
        text_rect = text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        pygame.draw.rect(surface, BLACK, (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10))
        surface.blit(text, text_rect)

        if current_min_level > 1:
            level_text = self.font.render(f"Entry Level: {current_min_level}", True, WHITE)
            level_rect = level_text.get_rect(topright=(SCREEN_WIDTH - 20, 50))
            pygame.draw.rect(surface, BLACK, (level_rect.x - 10, level_rect.y - 5, level_rect.width + 20, level_rect.height + 10))
            surface.blit(level_text, level_rect)

        # Draw detailed character stats interface
        player = self.player
        gui_width = 220
        gui_height = 240
        gui_x = 20
        gui_y = 20
        
        # Draw semi-transparent rounded rectangle background
        pygame.draw.rect(surface, (50, 50, 50, 180), (gui_x, gui_y, gui_width, gui_height), border_radius=10)
        
        # Draw character info
        stage_names = {'peasant': 'Peasant', 'soldier': 'Soldier', 'robe': 'Emperor'}
        stage_name = stage_names.get(player.skin_stage, 'Peasant')
        name_text = self.font.render(f"{player.name} [{stage_name}]", True, (255, 215, 0))
        level_text = self.font.render(f"Level: {player.level}", True, WHITE)
        exp_text = self.font.render(f"EXP: {int(player.exp)}/{player.exp_to_next_level}", True, WHITE)

        attack_text = self.font.render(f"ATK: {player.attack}", True, WHITE)
        defense_text = self.font.render(f"DEF: {player.defense}", True, WHITE)
        
        # Draw HP bar
        hp_ratio = min(player.hp / player.max_hp, 1.0)
        hp_bar_width = gui_width - 40
        hp_bar_height = 12
        hp_bar_x = gui_x + 20
        hp_bar_y = gui_y + 95
        
        # HP bar background
        pygame.draw.rect(surface, (80, 80, 80), (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), border_radius=3)
        # HP bar
        if hp_ratio > 0.5:
            hp_color = (0, 255, 0)
        elif hp_ratio > 0.25:
            hp_color = (255, 255, 0)
        else:
            hp_color = (255, 0, 0)
        pygame.draw.rect(surface, hp_color, (hp_bar_x, hp_bar_y, hp_bar_width * hp_ratio, hp_bar_height), border_radius=3)
        
        # Draw HP text
        hp_text = self.font.render(f"HP: {int(player.hp)}/{player.max_hp}", True, WHITE)
        surface.blit(hp_text, (hp_bar_x, hp_bar_y - 18))
        
        # Draw stamina bar
        stamina_ratio = min(player.stamina / player.max_stamina, 1.0)
        stamina_bar_width = gui_width - 40
        stamina_bar_height = 12
        stamina_bar_x = gui_x + 20
        stamina_bar_y = hp_bar_y + 30
        
        # Stamina bar background
        pygame.draw.rect(surface, (80, 80, 80), (stamina_bar_x, stamina_bar_y, stamina_bar_width, stamina_bar_height), border_radius=3)
        # Stamina bar
        if stamina_ratio > 0.5:
            stamina_color = (0, 128, 255)  # Blue
        elif stamina_ratio > 0.25:
            stamina_color = (0, 255, 255)  # Cyan
        else:
            stamina_color = (255, 165, 0)  # Orange
        pygame.draw.rect(surface, stamina_color, (stamina_bar_x, stamina_bar_y, stamina_bar_width * stamina_ratio, stamina_bar_height), border_radius=3)
        
        # Draw stamina text
        stamina_text = self.font.render(f"Stamina: {int(player.stamina)}/{player.max_stamina}", True, WHITE)
        surface.blit(stamina_text, (stamina_bar_x, stamina_bar_y - 18))
        
        # Draw food count
        food_text = self.font.render(f"Food: {player.food}/{player.max_food}", True, WHITE)
        surface.blit(food_text, (gui_x + 20, stamina_bar_y + 30))

        # Draw gold count
        gold_text = self.font.render(f"Gold: {player.gold}", True, (255, 200, 50))
        surface.blit(gold_text, (gui_x + 20, stamina_bar_y + 50))
        
        # Draw current status (Eating/Drinking)
        if self.current_status:
            status_text = self.font.render(self.current_status, True, (0, 255, 0))
            surface.blit(status_text, (gui_x + 20, stamina_bar_y + 55))
        
        # Draw EXP bar
        exp_ratio = min(player.exp / player.exp_to_next_level, 1.0)
        exp_bar_width = gui_width - 40
        exp_bar_height = 10
        exp_bar_x = gui_x + 20
        exp_bar_y = gui_y + 125
        
        pygame.draw.rect(surface, (80, 80, 80), (exp_bar_x, exp_bar_y, exp_bar_width, exp_bar_height), border_radius=3)
        pygame.draw.rect(surface, (0, 191, 255), (exp_bar_x, exp_bar_y, exp_bar_width * exp_ratio, exp_bar_height), border_radius=3)
        
        # Draw text
        surface.blit(name_text, (gui_x + 20, gui_y + 20))
        surface.blit(level_text, (gui_x + 20, gui_y + 45))
        surface.blit(exp_text, (gui_x + 20, gui_y + 65))
        surface.blit(attack_text, (gui_x + 20, gui_y + 145))
        surface.blit(defense_text, (gui_x + 20, gui_y + 170))
        
        # Draw equipment panel
        if self.equipment_panel_visible:
            equipment_gui_y = gui_y + gui_height + 10
            equipment_gui_width = 250
            equipment_gui_height = 220
            
            # Draw equipment panel background
            pygame.draw.rect(surface, (100, 150, 100, 180), (gui_x, equipment_gui_y, equipment_gui_width, equipment_gui_height), border_radius=10)
            
            # Draw title
            title_text = self.font.render("Equipment", True, WHITE)
            title_rect = title_text.get_rect(center=(gui_x + equipment_gui_width//2, equipment_gui_y + 20))
            surface.blit(title_text, title_rect)
            
            # Equipment categories - layout from reference image
            equipment_layout = [
                # Left side: weapons
                [("weapon", "Weapon"), ("wrist_guard", "Wrist"), ("necklace", "Necklace"), ("amulet", "Amulet"), ("ring", "Ring")],
                # Right side: armor
                [("helmet", "Helmet"), ("gauntlet", "Gauntlet"), ("shoulder", "Shoulder"), ("belt", "Belt"), ("boots", "Boots")]
            ]
            
            # Equipment stat bonuses
            equipment_stats = {
                "Bowl": "ATK+1"
            }
            
            # Get stats from equipment data
            for eq in self.player.equipment_data:
                stats = []
                if eq['attack'] > 0:
                    stats.append(f"ATK+{eq['attack']}")
                if eq['defense'] > 0:
                    stats.append(f"DEF+{eq['defense']}")
                if stats:
                    equipment_stats[eq['name']] = " ".join(stats)
            
            # Draw equipment slots
            for col, category in enumerate(equipment_layout):
                for row, (eq_key, eq_name) in enumerate(category):
                    slot_x = gui_x + 30 + col * 100
                    slot_y = equipment_gui_y + 50 + row * 30
                    slot_width = 80
                    slot_height = 25
                    
                    # Draw slot
                    pygame.draw.rect(surface, (50, 80, 50), (slot_x, slot_y, slot_width, slot_height), border_radius=3)
                    
                    # Draw equipment name and stats
                    eq_value = self.player.equipment[eq_key]
                    if eq_value:
                        # Show equipment name
                        eq_text = self.small_font.render(eq_value, True, WHITE)
                        text_rect = eq_text.get_rect(topleft=(slot_x + 5, slot_y + 2))
                        surface.blit(eq_text, text_rect)
                        
                        # Show equipment stats
                        if eq_value in equipment_stats:
                            stat_text = self.small_font.render(equipment_stats[eq_value], True, (255, 255, 0))  # Yellow
                            stat_rect = stat_text.get_rect(topleft=(slot_x + 5, slot_y + 12))
                            surface.blit(stat_text, stat_rect)
                    else:
                        # Show equipment slot name
                        eq_text = self.small_font.render(eq_name, True, (150, 150, 150))
                        text_rect = eq_text.get_rect(center=(slot_x + slot_width//2, slot_y + slot_height//2))
                        surface.blit(eq_text, text_rect)

    async def run(self):
        running = True
        last_time = pygame.time.get_ticks()
        while running:
            current_time = pygame.time.get_ticks()
            dt = (current_time - last_time) / 1000.0
            last_time = current_time

            running = self.handle_events()

            # --- TITLE state: render title screen, skip gameplay updates ---
            if self.state == "TITLE":
                self.title_timer += dt
                screen.fill(BLACK)
                self.draw_title_screen(screen)
                # If a transition was triggered, overlay fade
                if self.transitioning:
                    self.transition_timer += dt
                    self.draw_transition(screen)
                pygame.display.flip()
                clock.tick(FPS)
                await asyncio.sleep(0)
                continue

            # --- PLAYING state: normal gameplay ---
            move_completed = self.player.update(dt)
            
            # Check if stamina is 0
            if self.player.stamina <= 0:
                # Stamina is 0, teleport to Zhongli
                self.player.x = 60
                self.player.y = 60
                self.player.target_x = 60
                self.player.target_y = 60
                self.player.stamina = 50  # Recover some stamina
                print("Stamina depleted! Teleported to Zhongli!")
            
            # Check if near village (eating)
            if self.is_near_village(int(self.player.x), int(self.player.y)):
                self.village_timer += dt
                if self.village_timer >= self.village_cooldown:
                    self.village_timer = 0
                    if self.player.stamina < self.player.max_stamina:
                        old_stamina = self.player.stamina
                        self.player.stamina = min(self.player.max_stamina, self.player.stamina + 5)
                        if self.player.stamina > old_stamina:
                            self.current_status = "Eating"
                            self.status_timer = 0
            
            # Check if near well (drinking)
            if self.is_near_well(int(self.player.x), int(self.player.y)):
                self.well_timer += dt
                if self.well_timer >= self.well_cooldown:
                    self.well_timer = 0
                    if self.player.stamina < self.player.max_stamina:
                        old_stamina = self.player.stamina
                        self.player.stamina = min(self.player.max_stamina, self.player.stamina + 1)
                        if self.player.stamina > old_stamina:
                            self.current_status = "Drinking"
                            self.status_timer = 0
            
            # Update status display timer
            self.status_timer += dt
            if self.status_timer >= 1.0:
                self.current_status = ""
            
            # Update save notification timer
            if self.save_notification:
                self.save_notification_timer += dt
                if self.save_notification_timer >= 4.0:
                    self.save_notification = ""
            
            # Update chopping system
            self.update_chopping(dt)
            
            # Update battle system
            self.update_battle(dt)
            
            # Update story system
            if move_completed:
                self.check_new_location()
            self.update_story(dt)

            # Update dialogue typewriter
            self.update_dialogue(dt)
            
            self.camera.update(self.player)

            screen.fill(BLACK)
            self.draw_map(screen)
            self.draw_monsters(screen)
            self.draw_npcs(screen)
            self.player.draw(screen, self.camera.camera.x, self.camera.camera.y)
            self.draw_ui(screen)
            
            # Draw story interface
            if self.showing_story:
                self.draw_story(screen)
            
            # Draw chopping progress bar
            if self.chopping_tree:
                self.draw_chopping_progress(screen)
            
            # Draw battle progress bar
            if self.in_battle:
                self.draw_battle_progress(screen)
            
            # Draw battle result
            if self.battle_result is not None:
                self.draw_battle_result(screen)
            
            # Draw equipment drop interface
            if self.show_equipment_drop:
                self.draw_equipment_drop(screen)
            
            # Draw dialogue box (above other UI)
            self.draw_dialogue_box(screen)

            # Draw shop interface
            self.draw_shop(screen)

            # Draw equipment codex
            self.draw_codex(screen)

            # Draw world map
            self.draw_minimap(screen)
            
            # Draw exploration progress panel
            self.draw_progress_panel(screen)
            
            # Draw corner minimap (always shown)
            self.draw_corner_minimap(screen)
            
            # Draw save notification
            if self.save_notification:
                notif = self.font.render(self.save_notification, True, (0, 255, 100))
                notif_bg = pygame.Surface((notif.get_width() + 20, notif.get_height() + 10), pygame.SRCALPHA)
                notif_bg.fill((0, 0, 0, 200))
                notif_x = (SCREEN_WIDTH - notif.get_width()) // 2
                notif_y = 80
                screen.blit(notif_bg, (notif_x - 10, notif_y - 5))
                screen.blit(notif, (notif_x, notif_y))

            pygame.display.flip()
            clock.tick(FPS)
            
            await asyncio.sleep(0)

if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run())
