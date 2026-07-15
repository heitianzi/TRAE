#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate NPC sprites for the game.
NPCs: Monk, Old Farmer, Merchant, Scholar, General, Beggar, Herbalist, Child
Each: 32x32, single frame, 1 direction (front-facing)
"""

import pygame
import os

pygame.init()
screen = pygame.display.set_mode((1, 1))

TILE = 32

# Shared colors
SKIN = (230, 195, 160)
SKIN_D = (200, 165, 130)
HAIR_BLK = (40, 30, 25)
HAIR_GRY = (180, 175, 170)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# NPC colors
MONK_ROBE = (200, 160, 50)     # Yellow monk robe
MONK_ROBE_D = (160, 120, 30)
FARMER_C = (90, 110, 140)      # Blue-gray
FARMER_D = (65, 80, 105)
MERCHANT_C = (120, 60, 100)    # Purple
MERCHANT_D = (90, 40, 75)
SCHOLAR_C = (180, 180, 190)    # Light gray
SCHOLAR_D = (140, 140, 150)
GENERAL_C = (130, 30, 30)      # Red armor
GENERAL_D = (90, 20, 20)
BEGGAR_C = (110, 90, 60)       # Dirty brown
BEGGAR_D = (80, 65, 45)
HERBALIST_C = (60, 120, 70)    # Green
HERBALIST_D = (40, 90, 50)
CHILD_C = (200, 120, 80)       # Orange
CHILD_D = (160, 90, 55)


def dr(surf, x, y, w, h, c):
    pygame.draw.rect(surf, c, (x, y, w, h))


def dp(surf, x, y, c):
    surf.set_at((x, y), c)


def make_npc_sprite(colors, hair_color, has_hat, hat_color, hat_shape,
                    face_color=SKIN, extra=None):
    """Generate a 32x32 NPC sprite (front-facing).
    colors: (body, body_dark)
    hair_color: hair color
    has_hat: bool
    hat_color: hat color
    hat_shape: 'bun', 'cap', 'none', 'hood', 'straw', 'helmet', 'topknot'
    extra: optional dict for extra drawing params
    """
    body_c, body_d = colors
    surf = pygame.Surface((TILE, TILE))
    surf.fill((0, 255, 0))
    surf.set_colorkey((0, 255, 0))

    cx = TILE // 2  # 16

    # Head (y: 4-16)
    head_w = 12
    head_h = 12
    hx = cx - head_w // 2
    hy = 4
    dr(surf, hx, hy, head_w, head_h, face_color)
    dr(surf, hx, hy + head_h - 2, head_w, 2, SKIN_D)

    # Hair
    dr(surf, hx, hy, head_w, 3, hair_color)

    # Eyes
    dp(surf, cx - 3, hy + 6, BLACK)
    dp(surf, cx + 2, hy + 6, BLACK)

    # Mouth
    dp(surf, cx - 1, hy + 9, (150, 80, 60))
    dp(surf, cx, hy + 9, (150, 80, 60))

    # Hat / Hair style
    if has_hat and hat_shape == 'bun':
        # Topknot
        dr(surf, cx - 2, hy - 3, 5, 3, hair_color)
        dp(surf, cx, hy - 4, hair_color)
    elif has_hat and hat_shape == 'cap':
        # Scholar cap (方巾)
        dr(surf, hx - 1, hy - 4, head_w + 2, 4, hat_color)
        dr(surf, hx - 1, hy - 4, head_w + 2, 1, (200, 200, 200))
    elif has_hat and hat_shape == 'hood':
        # Monk hood (shaved head = no hair, yellow cap)
        dr(surf, hx, hy, head_w, 4, hat_color)
        dr(surf, hx - 2, hy - 1, head_w + 4, 3, hat_color)
    elif has_hat and hat_shape == 'straw':
        # Straw hat
        dr(surf, hx - 3, hy - 2, head_w + 6, 2, hat_color)
        dr(surf, cx - 3, hy - 5, 7, 3, (160, 130, 70))
    elif has_hat and hat_shape == 'helmet':
        # Helmet
        dr(surf, hx - 1, hy - 3, head_w + 2, 4, hat_color)
        dr(surf, cx - 3, hy - 4, 7, 2, hat_color)
        dr(surf, hx - 1, hy + 1, 2, 4, hat_color)
        dr(surf, hx + head_w - 1, hy + 1, 2, 4, hat_color)
    elif has_hat and hat_shape == 'topknot':
        # Large topknot
        dr(surf, cx - 3, hy - 4, 7, 4, hair_color)
        dp(surf, cx, hy - 5, hair_color)

    # Body (y: 16-28)
    body_w = 16
    bx = cx - body_w // 2
    by = 16
    body_h = 12
    dr(surf, bx, by, body_w, body_h, body_c)
    # Shading
    dr(surf, bx, by + body_h - 2, body_w, 2, body_d)
    # Collar
    dr(surf, cx - 3, by, 6, 2, body_d)
    dp(surf, cx - 1, by + 2, body_d)
    dp(surf, cx, by + 2, body_d)

    # Belt
    dr(surf, bx, by + 7, body_w, 1, body_d)

    # Arms
    dr(surf, bx - 2, by + 1, 3, 7, body_c)
    dr(surf, bx + body_w - 1, by + 1, 3, 7, body_c)
    # Hands
    dr(surf, bx - 2, by + 7, 3, 2, face_color)
    dr(surf, bx + body_w - 1, by + 7, 3, 2, face_color)

    # Extra features
    if extra and extra.get('beard'):
        # Beard
        dr(surf, cx - 3, hy + 10, 7, 3, hair_color)
    if extra and extra.get('staff'):
        # Walking staff
        dr(surf, bx + body_w, by - 2, 2, 18, (100, 70, 40))
    if extra and extra.get('fan'):
        # Fan in hand
        dr(surf, bx + body_w + 1, by + 5, 4, 3, (200, 180, 100))
    if extra and extra.get('beads'):
        # Prayer beads
        dr(surf, cx - 2, by + 4, 5, 1, (180, 140, 60))
    if extra and extra.get('medicine'):
        # Medicine basket
        dr(surf, bx - 4, by + 3, 4, 6, (120, 90, 50))

    # Legs/shoes
    dr(surf, cx - 5, 28, 4, 3, (50, 40, 30))
    dr(surf, cx + 1, 28, 4, 3, (50, 40, 30))

    return surf.convert_alpha()


# Generate all NPC sprites
npcs = [
    # (filename, colors, hair, has_hat, hat_color, hat_shape, face, extra)
    ('npc_monk.png', (MONK_ROBE, MONK_ROBE_D), HAIR_BLK, True, MONK_ROBE, 'hood', SKIN,
     {'beads': True, 'staff': True}),
    ('npc_farmer.png', (FARMER_C, FARMER_D), HAIR_BLK, True, (150, 130, 90), 'straw', SKIN,
     {'beard': False}),
    ('npc_merchant.png', (MERCHANT_C, MERCHANT_D), HAIR_BLK, True, (180, 140, 30), 'cap', SKIN,
     {'fan': True}),
    ('npc_scholar.png', (SCHOLAR_C, SCHOLAR_D), HAIR_BLK, True, (60, 50, 50), 'cap', SKIN,
     {}),
    ('npc_general.png', (GENERAL_C, GENERAL_D), HAIR_BLK, True, (140, 140, 150), 'helmet', SKIN,
     {}),
    ('npc_beggar.png', (BEGGAR_C, BEGGAR_D), HAIR_GRY, False, None, 'none', (180, 150, 120),
     {'beard': True, 'staff': True}),
    ('npc_herbalist.png', (HERBALIST_C, HERBALIST_D), HAIR_BLK, True, (80, 100, 60), 'topknot', SKIN,
     {'medicine': True, 'beard': True}),
    ('npc_child.png', (CHILD_C, CHILD_D), HAIR_BLK, False, None, 'topknot', SKIN,
     {}),
]

for fname, colors, hair, has_hat, hat_c, hat_shape, face, extra in npcs:
    sprite = make_npc_sprite(colors, hair, has_hat, hat_c, hat_shape, face, extra)
    pygame.image.save(sprite, fname)
    print(f"Generated: {fname}")

print("All NPC sprites generated!")
