#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate player sprite sheets for different character stages:
1. Peasant (Level 1-4): Simple clothes, straw hat
2. Soldier (Level 5-9): Light armor, headband
3. Red Robe (Level 10+): Imperial red robe, crown

Each sprite sheet: 4 directions x 3 frames = 128x144
Directions: down(0), left(1), right(2), up(3)
Frame size: 32x48
"""

import pygame
import os

pygame.init()
screen = pygame.display.set_mode((1, 1))  # Need a display for convert_alpha

TILE_W = 32
TILE_H = 48
FRAMES = 3
DIRECTIONS = 4

# Colors
SKIN = (230, 195, 160)
SKIN_DARK = (200, 165, 130)
HAIR_BLACK = (40, 30, 25)
HAIR_DARK = (60, 45, 35)

# Peasant colors - Ancient Chinese farmer (短打/交领)
P_CLOTHES = (90, 110, 140)      # Blue-gray rough cloth (粗布短打)
P_CLOTHES_DARK = (65, 80, 105)
P_CLOTHES_LIGHT = (115, 135, 165)
P_PANTS = (70, 60, 50)          # Dark brown loose pants
P_PANTS_DARK = (50, 42, 35)
P_SASH = (160, 140, 80)         # Cloth sash belt (布腰带)
P_WRAP = (120, 100, 70)         # Leg wraps (绑腿)
P_SHOES = (45, 38, 30)          # Cloth shoes (布鞋)
P_HAIR_BUN = (35, 28, 22)       # Hair topknot (发髻)
P_HEADCLOTH = (150, 130, 90)    # Head cloth (巾)

# Soldier colors
S_ARMOR = (140, 140, 150)      # Light iron armor
S_ARMOR_DARK = (100, 100, 110)
S_BAND = (180, 50, 40)         # Red headband
S_PANTS = (70, 60, 55)
S_BOOTS = (40, 35, 30)

# Red robe (emperor) colors
R_ROBE = (160, 30, 30)         # Imperial red
R_ROBE_DARK = (120, 20, 20)
R_ROBE_LIGHT = (200, 50, 40)
R_GOLD = (255, 200, 50)        # Gold trim
R_CROWN = (220, 180, 40)
R_CROWN_DARK = (180, 140, 20)
R_BELT = (200, 160, 30)
R_INNER = (240, 220, 180)      # Inner robe white


def draw_pixel(surface, x, y, color):
    surface.set_at((x, y), color)


def draw_rect_s(surface, x, y, w, h, color):
    pygame.draw.rect(surface, color, (x, y, w, h))


def draw_char_frame(surf, ox, oy, direction, frame, stage):
    """Draw one character frame at offset (ox, oy)
    direction: 0=down, 1=left, 2=right, 3=up
    frame: 0,1,2 (walking animation)
    stage: 'peasant', 'soldier', 'robe'
    """
    cx = ox + TILE_W // 2  # center x
    # Walking offset
    leg_offset = 0
    if frame == 1:
        leg_offset = 1  # mid step
    elif frame == 0 or frame == 2:
        leg_offset = 2 if frame == 0 else -1

    is_side = direction in (1, 2)  # left/right
    is_up = direction == 3

    # ===== Choose colors by stage =====
    if stage == 'peasant':
        clothes = P_CLOTHES
        clothes_d = P_CLOTHES_DARK
        pants = P_PANTS
        shoes = P_SHOES
        headband = None
    elif stage == 'soldier':
        clothes = S_ARMOR
        clothes_d = S_ARMOR_DARK
        hat_color = None
        headband = S_BAND
        pants = S_PANTS
        shoes = S_BOOTS
    else:  # robe
        clothes = R_ROBE
        clothes_d = R_ROBE_DARK
        hat_color = None
        headband = None
        pants = R_ROBE_DARK
        shoes = (80, 30, 20)

    # ===== Head (same for all, y: 8-20) =====
    head_y = 8
    head_h = 12
    head_w = 14
    head_x = cx - head_w // 2

    # Face/skin
    draw_rect_s(surf, head_x, head_y, head_w, head_h, SKIN)
    # Skin shading
    draw_rect_s(surf, head_x, head_y + head_h - 2, head_w, 2, SKIN_DARK)

    # Hair (top of head)
    draw_rect_s(surf, head_x, head_y, head_w, 3, HAIR_BLACK)

    # Eyes (depend on direction)
    if direction == 0:  # down - face viewer
        draw_pixel(surf, cx - 3, head_y + 6, HAIR_BLACK)
        draw_pixel(surf, cx + 2, head_y + 6, HAIR_BLACK)
        # Mouth
        draw_pixel(surf, cx - 1, head_y + 9, (150, 80, 60))
        draw_pixel(surf, cx, head_y + 9, (150, 80, 60))
    elif direction == 3:  # up - back of head
        draw_rect_s(surf, head_x, head_y, head_w, 5, HAIR_BLACK)
    elif direction == 1:  # left
        draw_pixel(surf, head_x + 1, head_y + 6, HAIR_BLACK)
        draw_rect_s(surf, head_x, head_y, 3, 4, HAIR_BLACK)
    elif direction == 2:  # right
        draw_pixel(surf, head_x + head_w - 2, head_y + 6, HAIR_BLACK)
        draw_rect_s(surf, head_x + head_w - 3, head_y, 3, 4, HAIR_BLACK)

    # ===== Hat / Crown =====
    if stage == 'peasant':
        # Ancient Chinese peasant: hair topknot + cloth headwrap (巾帻)
        # Hair topknot (发髻) on top of head
        bun_y = head_y - 3
        draw_rect_s(surf, cx - 2, bun_y, 5, 3, P_HAIR_BUN)
        draw_pixel(surf, cx, bun_y - 1, P_HAIR_BUN)

        # Cloth headwrap (巾) around forehead
        band_y = head_y + 1
        draw_rect_s(surf, head_x - 1, band_y, head_w + 2, 2, P_HEADCLOTH)
        # Headwrap knot on side
        if direction == 1:  # left
            draw_rect_s(surf, head_x - 2, band_y, 2, 4, P_HEADCLOTH)
        elif direction == 2:  # right
            draw_rect_s(surf, head_x + head_w, band_y, 2, 4, P_HEADCLOTH)

    elif stage == 'soldier':
        # Red headband
        band_y = head_y + 1
        draw_rect_s(surf, head_x - 1, band_y, head_w + 2, 3, S_BAND)
        # Band tail (side)
        if direction == 1:  # left
            draw_rect_s(surf, head_x - 3, band_y, 3, 4, S_BAND)
        elif direction == 2:  # right
            draw_rect_s(surf, head_x + head_w, band_y, 3, 4, S_BAND)
    elif stage == 'robe':
        # Imperial crown
        crown_y = head_y - 4
        crown_w = 16
        crown_x = cx - crown_w // 2
        # Base
        draw_rect_s(surf, crown_x, crown_y, crown_w, 4, R_CROWN)
        # Points
        for i in range(4):
            px = crown_x + i * 4 + 1
            draw_pixel(surf, px, crown_y - 1, R_CROWN)
            draw_pixel(surf, px + 1, crown_y - 2, R_CROWN)
        # Gold gems
        draw_pixel(surf, cx - 2, crown_y + 1, R_GOLD)
        draw_pixel(surf, cx + 1, crown_y + 1, R_GOLD)

    # ===== Body / Torso (y: 20-36) =====
    body_y = 20
    body_h = 14
    body_w = 16 if is_side else 18
    body_x = cx - body_w // 2

    if stage == 'robe':
        # Wide flowing robe
        body_w = 20
        body_x = cx - body_w // 2
        draw_rect_s(surf, body_x, body_y, body_w, body_h, R_ROBE)
        # Robe shading
        draw_rect_s(surf, body_x, body_y + body_h - 3, body_w, 3, R_ROBE_DARK)
        # Gold trim down the middle
        if not is_side:
            draw_rect_s(surf, cx - 1, body_y, 2, body_h, R_GOLD)
        # Inner collar
        draw_rect_s(surf, cx - 3, body_y, 6, 2, R_INNER)
        # Belt
        draw_rect_s(surf, body_x, body_y + 8, body_w, 2, R_BELT)
    elif stage == 'soldier':
        # Armor
        draw_rect_s(surf, body_x, body_y, body_w, body_h, S_ARMOR)
        # Armor plates
        draw_rect_s(surf, body_x, body_y + 4, body_w, 1, S_ARMOR_DARK)
        draw_rect_s(surf, body_x, body_y + 9, body_w, 1, S_ARMOR_DARK)
        # Shoulder guards
        draw_rect_s(surf, body_x - 1, body_y, 2, 4, S_ARMOR_DARK)
        draw_rect_s(surf, body_x + body_w - 1, body_y, 2, 4, S_ARMOR_DARK)
    else:
        # Ancient peasant: cross-collar short jacket (交领短打)
        draw_rect_s(surf, body_x, body_y, body_w, body_h, P_CLOTHES)
        # Cross collar (交领) - V-shape at top
        if not is_side:
            # Left lapel
            draw_rect_s(surf, cx - 4, body_y, 4, 4, P_CLOTHES_DARK)
            # Right lapel overlapping
            draw_rect_s(surf, cx, body_y, 4, 4, P_CLOTHES_LIGHT)
            # Inner shirt
            draw_rect_s(surf, cx - 1, body_y + 2, 3, 5, (200, 190, 170))
        else:
            # Side view: collar line
            draw_rect_s(surf, body_x, body_y, 2, 5, P_CLOTHES_DARK)
        # Bottom hem shading
        draw_rect_s(surf, body_x, body_y + body_h - 2, body_w, 2, P_CLOTHES_DARK)
        # Cloth sash belt (布腰带)
        draw_rect_s(surf, body_x - 1, body_y + 8, body_w + 2, 2, P_SASH)
        # Sash knot
        if not is_side:
            draw_pixel(surf, cx, body_y + 8, (120, 100, 60))

    # Arms (simple)
    if is_side:
        # One arm visible
        arm_x = body_x + body_w - 2 if direction == 2 else body_x
        draw_rect_s(surf, arm_x, body_y + 1, 3, 8, clothes)
        # Hand
        draw_rect_s(surf, arm_x, body_y + 8, 3, 2, SKIN)
    else:
        # Both arms
        draw_rect_s(surf, body_x - 2, body_y + 1, 3, 8, clothes)
        draw_rect_s(surf, body_x + body_w - 1, body_y + 1, 3, 8, clothes)
        # Hands
        draw_rect_s(surf, body_x - 2, body_y + 8, 3, 2, SKIN)
        draw_rect_s(surf, body_x + body_w - 1, body_y + 8, 3, 2, SKIN)

    # ===== Legs / Lower body (y: 34-48) =====
    leg_y = 34
    leg_h = 12

    if stage == 'robe':
        # Long robe covers legs
        robe_bottom = 44
        # Wide robe bottom
        robe_w = 22
        robe_x = cx - robe_w // 2
        draw_rect_s(surf, robe_x, leg_y, robe_w, robe_bottom - leg_y, R_ROBE_DARK)
        # Gold hem
        draw_rect_s(surf, robe_x, robe_bottom - 2, robe_w, 2, R_GOLD)
        # Shoes peeking out
        shoe_offset = leg_offset
        draw_rect_s(surf, cx - 4 + shoe_offset, robe_bottom, 4, 3, shoes)
        draw_rect_s(surf, cx + shoe_offset, robe_bottom, 4, 3, shoes)
    else:
        # Ancient peasant: loose pants + leg wraps (绑腿) + cloth shoes
        if is_side:
            # One leg visible
            draw_rect_s(surf, body_x + 2, leg_y, 8, leg_h - 5, P_PANTS)
            # Leg wrap (绑腿) - lighter band around shin
            draw_rect_s(surf, body_x + 2, leg_y + leg_h - 6, 8, 2, P_WRAP)
            # Cloth shoe
            shoe_y = leg_y + leg_h - 3
            draw_rect_s(surf, body_x + 2, shoe_y, 8, 3, P_SHOES)
            if frame == 1:
                draw_rect_s(surf, body_x + 2, shoe_y - 1, 8, 1, P_SHOES)
        else:
            # Two legs with walking offset
            left_offset = leg_offset if frame != 1 else 0
            right_offset = -leg_offset if frame != 1 else 0

            # Left leg - loose pants
            draw_rect_s(surf, cx - 6 + left_offset, leg_y, 5, leg_h - 5, P_PANTS)
            # Leg wrap (绑腿)
            draw_rect_s(surf, cx - 6 + left_offset, leg_y + leg_h - 6, 5, 2, P_WRAP)
            # Cloth shoe
            draw_rect_s(surf, cx - 6 + left_offset, leg_y + leg_h - 3, 5, 3, P_SHOES)

            # Right leg
            draw_rect_s(surf, cx + 1 + right_offset, leg_y, 5, leg_h - 5, P_PANTS)
            draw_rect_s(surf, cx + 1 + right_offset, leg_y + leg_h - 6, 5, 2, P_WRAP)
            draw_rect_s(surf, cx + 1 + right_offset, leg_y + leg_h - 3, 5, 3, P_SHOES)


def generate_sprite_sheet(stage, filename):
    """Generate a complete sprite sheet for one stage"""
    sheet_w = TILE_W * DIRECTIONS  # 128
    sheet_h = TILE_H * FRAMES      # 144

    # Use SRCALPHA for proper per-pixel transparency (no colorkey needed)
    sheet = pygame.Surface((sheet_w, sheet_h), pygame.SRCALPHA)

    for d in range(DIRECTIONS):
        for f in range(FRAMES):
            ox = d * TILE_W
            oy = f * TILE_H
            draw_char_frame(sheet, ox, oy, d, f, stage)

    sheet = sheet.convert_alpha()

    pygame.image.save(sheet, filename)
    print(f"Generated: {filename} ({sheet_w}x{sheet_h})")


# Generate all three stages
generate_sprite_sheet('peasant', 'sprite_peasant.png')
generate_sprite_sheet('soldier', 'sprite_soldier.png')
generate_sprite_sheet('robe', 'sprite_robe.png')

# Also copy peasant as default player_sprite.png
import shutil
shutil.copy('sprite_peasant.png', 'player_sprite.png')
print("Copied peasant sprite to player_sprite.png")
print("All sprites generated successfully!")
