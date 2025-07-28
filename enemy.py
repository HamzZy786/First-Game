import pygame
import random
import math
from settings import *

class Enemy:
    def __init__(self):
        self.name = "Test Enemy"
        self.hp = 50
        self.max_hp = 50
        
        # Attack system
        self.bullets = []
        self.attack_finished = False
        self.attack_timer = 0
        self.current_attack = 0
        self.attack_patterns = [
            self.rain_attack,
            self.spiral_attack,
            self.cross_attack,
            self.random_scatter
        ]
        
    def reset(self):
        """Reset enemy for new combat"""
        self.hp = self.max_hp
        self.bullets.clear()
        self.attack_finished = False
        self.attack_timer = 0
        self.current_attack = 0
    
    def start_attack(self):
        """Start a new attack pattern"""
        self.bullets.clear()
        self.attack_finished = False
        self.attack_timer = 0
        # Cycle through attack patterns or choose random
        self.current_attack = random.randint(0, len(self.attack_patterns) - 1)
        
    def update(self, player):
        """Update enemy and attack logic"""
        if not self.attack_finished:
            self.attack_timer += 1
            
            # Execute current attack pattern
            if self.current_attack < len(self.attack_patterns):
                self.attack_patterns[self.current_attack]()
            
            # Update bullets
            self.update_bullets(player)
            
            # End attack after duration
            if self.attack_timer >= ATTACK_DURATION:
                self.attack_finished = True
    
    def update_bullets(self, player):
        """Update all bullets and check collisions"""
        for bullet in self.bullets[:]:  # Copy list to avoid modification issues
            # Update bullet position
            bullet['x'] += bullet['vx']
            bullet['y'] += bullet['vy']
            bullet['rect'].x = int(bullet['x'])
            bullet['rect'].y = int(bullet['y'])
            
            # Remove bullets that are off screen
            if (bullet['rect'].right < 0 or bullet['rect'].left > SCREEN_WIDTH or
                bullet['rect'].bottom < 0 or bullet['rect'].top > SCREEN_HEIGHT):
                self.bullets.remove(bullet)
                continue
            
            # Check collision with player
            if bullet['rect'].colliderect(player.rect):
                if player.take_damage(bullet.get('damage', 10)):
                    # Remove bullet on hit (optional)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
    
    def rain_attack(self):
        """Bullets fall from the top like rain"""
        if self.attack_timer % 15 == 0:  # Spawn every 15 frames
            x = random.randint(COMBAT_BOX_X, COMBAT_BOX_X + COMBAT_BOX_WIDTH - BULLET_SIZE)
            y = COMBAT_BOX_Y - BULLET_SIZE
            bullet = {
                'rect': pygame.Rect(x, y, BULLET_SIZE, BULLET_SIZE),
                'x': float(x),
                'y': float(y),
                'vx': 0,
                'vy': random.uniform(2, 4),
                'color': YELLOW,
                'damage': 10
            }
            self.bullets.append(bullet)
    
    def spiral_attack(self):
        """Bullets spiral outward from center"""
        if self.attack_timer % 8 == 0:
            center_x = COMBAT_BOX_X + COMBAT_BOX_WIDTH // 2
            center_y = COMBAT_BOX_Y + COMBAT_BOX_HEIGHT // 2
            
            angle = (self.attack_timer * 0.2) % (2 * math.pi)
            speed = 3
            
            bullet = {
                'rect': pygame.Rect(center_x, center_y, BULLET_SIZE, BULLET_SIZE),
                'x': float(center_x),
                'y': float(center_y),
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': BLUE,
                'damage': 10
            }
            self.bullets.append(bullet)
    
    def cross_attack(self):
        """Bullets move in cross pattern"""
        if self.attack_timer % 20 == 0:
            center_x = COMBAT_BOX_X + COMBAT_BOX_WIDTH // 2
            center_y = COMBAT_BOX_Y + COMBAT_BOX_HEIGHT // 2
            speed = 3
            
            # Four directions
            directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left
            
            for dx, dy in directions:
                bullet = {
                    'rect': pygame.Rect(center_x, center_y, BULLET_SIZE, BULLET_SIZE),
                    'x': float(center_x),
                    'y': float(center_y),
                    'vx': dx * speed,
                    'vy': dy * speed,
                    'color': ORANGE,
                    'damage': 10
                }
                self.bullets.append(bullet)
    
    def random_scatter(self):
        """Random bullets from random positions"""
        if self.attack_timer % 12 == 0:
            # Random spawn position around the edges
            side = random.randint(0, 3)
            if side == 0:  # Top
                x = random.randint(COMBAT_BOX_X, COMBAT_BOX_X + COMBAT_BOX_WIDTH)
                y = COMBAT_BOX_Y - BULLET_SIZE
            elif side == 1:  # Right
                x = COMBAT_BOX_X + COMBAT_BOX_WIDTH
                y = random.randint(COMBAT_BOX_Y, COMBAT_BOX_Y + COMBAT_BOX_HEIGHT)
            elif side == 2:  # Bottom
                x = random.randint(COMBAT_BOX_X, COMBAT_BOX_X + COMBAT_BOX_WIDTH)
                y = COMBAT_BOX_Y + COMBAT_BOX_HEIGHT
            else:  # Left
                x = COMBAT_BOX_X - BULLET_SIZE
                y = random.randint(COMBAT_BOX_Y, COMBAT_BOX_Y + COMBAT_BOX_HEIGHT)
            
            # Aim roughly towards player area
            target_x = COMBAT_BOX_X + COMBAT_BOX_WIDTH // 2
            target_y = COMBAT_BOX_Y + COMBAT_BOX_HEIGHT // 2
            
            dx = target_x - x
            dy = target_y - y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                speed = 2.5
                vx = (dx / distance) * speed
                vy = (dy / distance) * speed
            else:
                vx, vy = 0, 0
            
            bullet = {
                'rect': pygame.Rect(x, y, BULLET_SIZE, BULLET_SIZE),
                'x': float(x),
                'y': float(y),
                'vx': vx,
                'vy': vy,
                'color': PURPLE,
                'damage': 10
            }
            self.bullets.append(bullet)
    
    def take_damage(self, damage):
        """Take damage and return True if defeated"""
        self.hp -= damage
        return self.hp <= 0
    
    def draw(self, screen, font):
        """Draw enemy info and bullets"""
        # Draw enemy name and HP
        name_text = font.render(self.name, True, WHITE)
        screen.blit(name_text, (SCREEN_WIDTH - 200, 20))
        
        hp_text = font.render(f"HP: {self.hp}/{self.max_hp}", True, WHITE)
        screen.blit(hp_text, (SCREEN_WIDTH - 200, 50))
        
        # Draw combat box
        pygame.draw.rect(screen, WHITE, 
                        (COMBAT_BOX_X, COMBAT_BOX_Y, COMBAT_BOX_WIDTH, COMBAT_BOX_HEIGHT), 2)
        
        # Draw bullets
        for bullet in self.bullets:
            pygame.draw.rect(screen, bullet['color'], bullet['rect'])
            # Optional: Add glow effect or different shapes
            pygame.draw.rect(screen, WHITE, bullet['rect'], 1)
