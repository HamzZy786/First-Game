import pygame
import os
from settings import *

class SpriteManager:
    def __init__(self):
        self.sprites = {}
        self.load_sprites()
    
    def load_sprites(self):
        """Load all sprite images"""
        # Create basic sprites programmatically if image files don't exist
        self.create_basic_sprites()
    
    def create_basic_sprites(self):
        """Create basic sprites programmatically using pygame surfaces"""
        
        # Player heart sprite (red heart with outline)
        heart_surface = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        self.draw_heart(heart_surface, RED, PLAYER_SIZE)
        self.sprites['player_heart'] = heart_surface
        
        # Player heart damaged (darker red with flicker effect)
        heart_damaged = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        self.draw_heart(heart_damaged, (150, 0, 0), PLAYER_SIZE)
        self.sprites['player_heart_damaged'] = heart_damaged
        
        # Enemy sprite (simple monster face)
        enemy_surface = pygame.Surface((64, 64), pygame.SRCALPHA)
        self.draw_enemy(enemy_surface)
        self.sprites['enemy_basic'] = enemy_surface
        
        # Bullet sprites with different shapes
        self.create_bullet_sprites()
        
        # UI elements
        self.create_ui_sprites()
    
    def draw_heart(self, surface, color, size):
        """Draw a heart shape on the given surface"""
        # Simple heart using circles and triangle
        center_x, center_y = size // 2, size // 2
        
        # Two circles for the top of the heart
        radius = size // 4
        pygame.draw.circle(surface, color, (center_x - radius//2, center_y - radius//2), radius)
        pygame.draw.circle(surface, color, (center_x + radius//2, center_y - radius//2), radius)
        
        # Triangle for the bottom of the heart
        points = [
            (center_x - radius, center_y),
            (center_x + radius, center_y),
            (center_x, center_y + radius + 2)
        ]
        pygame.draw.polygon(surface, color, points)
        
        # Add white outline
        pygame.draw.circle(surface, WHITE, (center_x - radius//2, center_y - radius//2), radius, 2)
        pygame.draw.circle(surface, WHITE, (center_x + radius//2, center_y - radius//2), radius, 2)
        pygame.draw.polygon(surface, WHITE, points, 2)
    
    def draw_enemy(self, surface):
        """Draw a simple enemy sprite"""
        width, height = surface.get_size()
        center_x, center_y = width // 2, height // 2
        
        # Body (dark purple circle)
        pygame.draw.circle(surface, (80, 0, 80), (center_x, center_y), 28)
        pygame.draw.circle(surface, WHITE, (center_x, center_y), 28, 2)
        
        # Eyes (red glowing)
        pygame.draw.circle(surface, RED, (center_x - 8, center_y - 8), 4)
        pygame.draw.circle(surface, RED, (center_x + 8, center_y - 8), 4)
        
        # Mouth (simple line)
        pygame.draw.line(surface, WHITE, (center_x - 6, center_y + 6), (center_x + 6, center_y + 6), 2)
    
    def create_bullet_sprites(self):
        """Create different bullet sprites"""
        bullet_size = BULLET_SIZE
        
        # Standard bullet (circle)
        bullet_circle = pygame.Surface((bullet_size, bullet_size), pygame.SRCALPHA)
        pygame.draw.circle(bullet_circle, YELLOW, (bullet_size//2, bullet_size//2), bullet_size//2)
        pygame.draw.circle(bullet_circle, WHITE, (bullet_size//2, bullet_size//2), bullet_size//2, 1)
        self.sprites['bullet_circle'] = bullet_circle
        
        # Diamond bullet
        bullet_diamond = pygame.Surface((bullet_size, bullet_size), pygame.SRCALPHA)
        points = [
            (bullet_size//2, 0),
            (bullet_size, bullet_size//2),
            (bullet_size//2, bullet_size),
            (0, bullet_size//2)
        ]
        pygame.draw.polygon(bullet_diamond, BLUE, points)
        pygame.draw.polygon(bullet_diamond, WHITE, points, 1)
        self.sprites['bullet_diamond'] = bullet_diamond
        
        # Star bullet
        bullet_star = pygame.Surface((bullet_size, bullet_size), pygame.SRCALPHA)
        self.draw_star(bullet_star, ORANGE, bullet_size//2, bullet_size//2, bullet_size//2)
        self.sprites['bullet_star'] = bullet_star
        
        # Square bullet
        bullet_square = pygame.Surface((bullet_size, bullet_size), pygame.SRCALPHA)
        pygame.draw.rect(bullet_square, PURPLE, (0, 0, bullet_size, bullet_size))
        pygame.draw.rect(bullet_square, WHITE, (0, 0, bullet_size, bullet_size), 1)
        self.sprites['bullet_square'] = bullet_square
    
    def draw_star(self, surface, color, center_x, center_y, radius):
        """Draw a star shape"""
        import math
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                r = radius
            else:
                r = radius // 2
            x = center_x + r * math.cos(angle - math.pi/2)
            y = center_y + r * math.sin(angle - math.pi/2)
            points.append((x, y))
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, WHITE, points, 1)
    
    def create_ui_sprites(self):
        """Create UI element sprites"""
        # Menu button background
        button_bg = pygame.Surface((200, 40), pygame.SRCALPHA)
        pygame.draw.rect(button_bg, (50, 50, 100, 200), (0, 0, 200, 40))
        pygame.draw.rect(button_bg, WHITE, (0, 0, 200, 40), 2)
        self.sprites['button_bg'] = button_bg
        
        # Menu button hover
        button_hover = pygame.Surface((200, 40), pygame.SRCALPHA)
        pygame.draw.rect(button_hover, (100, 100, 150, 220), (0, 0, 200, 40))
        pygame.draw.rect(button_hover, YELLOW, (0, 0, 200, 40), 2)
        self.sprites['button_hover'] = button_hover
    
    def get_sprite(self, name):
        """Get a sprite by name"""
        return self.sprites.get(name, None)
    
    def get_bullet_sprite(self, bullet_type):
        """Get bullet sprite based on type"""
        sprite_map = {
            'circle': 'bullet_circle',
            'diamond': 'bullet_diamond', 
            'star': 'bullet_star',
            'square': 'bullet_square'
        }
        sprite_name = sprite_map.get(bullet_type, 'bullet_circle')
        return self.get_sprite(sprite_name)

# Global sprite manager instance
sprite_manager = None

def get_sprite_manager():
    """Get the global sprite manager instance"""
    global sprite_manager
    if sprite_manager is None:
        sprite_manager = SpriteManager()
    return sprite_manager
