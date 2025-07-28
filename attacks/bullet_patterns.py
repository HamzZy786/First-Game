"""
Advanced bullet patterns for more complex enemy attacks.
You can add more creative patterns here!
"""

import pygame
import random
import math
from settings import *

class BulletPatterns:
    @staticmethod
    def wave_pattern(bullets, timer, center_x, center_y):
        """Creates a wave pattern of bullets"""
        if timer % 10 == 0:
            for i in range(5):
                angle = (timer * 0.1) + (i * 0.5)
                x = center_x + math.sin(angle) * 100
                y = center_y - 150
                
                bullet = {
                    'rect': pygame.Rect(int(x), int(y), BULLET_SIZE, BULLET_SIZE),
                    'x': float(x),
                    'y': float(y),
                    'vx': 0,
                    'vy': 3,
                    'color': BLUE,
                    'damage': 10
                }
                bullets.append(bullet)
    
    @staticmethod
    def expanding_circle(bullets, timer, center_x, center_y):
        """Creates expanding circles of bullets"""
        if timer % 30 == 0:
            num_bullets = 12
            radius = 30
            
            for i in range(num_bullets):
                angle = (2 * math.pi * i) / num_bullets
                x = center_x + math.cos(angle) * radius
                y = center_y + math.sin(angle) * radius
                
                speed = 2
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                
                bullet = {
                    'rect': pygame.Rect(int(x), int(y), BULLET_SIZE, BULLET_SIZE),
                    'x': float(x),
                    'y': float(y),
                    'vx': vx,
                    'vy': vy,
                    'color': ORANGE,
                    'damage': 10
                }
                bullets.append(bullet)
    
    @staticmethod
    def laser_sweep(bullets, timer, center_x, center_y):
        """Creates a sweeping laser effect"""
        if timer % 5 == 0:
            angle = (timer * 0.05) % (2 * math.pi)
            distance = 200
            
            # Create multiple bullets along the laser line
            for i in range(10):
                t = i / 9.0  # 0 to 1
                x = center_x + math.cos(angle) * distance * t
                y = center_y + math.sin(angle) * distance * t
                
                bullet = {
                    'rect': pygame.Rect(int(x), int(y), BULLET_SIZE // 2, BULLET_SIZE // 2),
                    'x': float(x),
                    'y': float(y),
                    'vx': math.cos(angle) * 1,
                    'vy': math.sin(angle) * 1,
                    'color': RED,
                    'damage': 5
                }
                bullets.append(bullet)
    
    @staticmethod
    def zigzag_pattern(bullets, timer, center_x, center_y):
        """Creates zigzag pattern bullets"""
        if timer % 15 == 0:
            side = 1 if (timer // 15) % 2 == 0 else -1
            x = center_x + side * 150
            y = center_y - 100
            
            bullet = {
                'rect': pygame.Rect(int(x), int(y), BULLET_SIZE, BULLET_SIZE),
                'x': float(x),
                'y': float(y),
                'vx': -side * 2,
                'vy': 3,
                'color': PURPLE,
                'damage': 10,
                'pattern': 'zigzag',
                'zigzag_timer': 0
            }
            bullets.append(bullet)
    
    @staticmethod
    def update_special_bullets(bullets):
        """Update bullets with special movement patterns"""
        for bullet in bullets:
            if bullet.get('pattern') == 'zigzag':
                bullet['zigzag_timer'] = bullet.get('zigzag_timer', 0) + 1
                if bullet['zigzag_timer'] % 20 == 0:
                    bullet['vx'] *= -1  # Reverse horizontal direction
    
    @staticmethod
    def homing_bullets(bullets, timer, center_x, center_y, player_rect):
        """Creates bullets that slowly home in on the player"""
        if timer % 40 == 0:
            # Start from random edge
            edges = [
                (center_x - 100, center_y - 100),
                (center_x + 100, center_y - 100),
                (center_x - 100, center_y + 100),
                (center_x + 100, center_y + 100)
            ]
            
            start_x, start_y = random.choice(edges)
            
            bullet = {
                'rect': pygame.Rect(int(start_x), int(start_y), BULLET_SIZE, BULLET_SIZE),
                'x': float(start_x),
                'y': float(start_y),
                'vx': 0,
                'vy': 0,
                'color': (255, 100, 255),  # Pink
                'damage': 15,
                'pattern': 'homing',
                'target': player_rect
            }
            bullets.append(bullet)
    
    @staticmethod
    def update_homing_bullets(bullets):
        """Update homing bullets to track the player"""
        for bullet in bullets:
            if bullet.get('pattern') == 'homing':
                target = bullet.get('target')
                if target:
                    # Calculate direction to target
                    dx = target.centerx - bullet['x']
                    dy = target.centery - bullet['y']
                    distance = math.sqrt(dx*dx + dy*dy)
                    
                    if distance > 0:
                        # Slowly adjust velocity towards target
                        homing_strength = 0.1
                        target_vx = (dx / distance) * 2
                        target_vy = (dy / distance) * 2
                        
                        bullet['vx'] += (target_vx - bullet['vx']) * homing_strength
                        bullet['vy'] += (target_vy - bullet['vy']) * homing_strength
