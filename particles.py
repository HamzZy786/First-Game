import pygame
import random
import math
from settings import *

class ParticleEffect:
    def __init__(self, x, y, effect_type="stars"):
        self.x = x
        self.y = y
        self.effect_type = effect_type
        self.particles = []
        self.lifetime = 0
        
        if effect_type == "stars":
            self.create_star_particles()
        elif effect_type == "explosion":
            self.create_explosion_particles()
        elif effect_type == "heal":
            self.create_heal_particles()
        elif effect_type == "damage":
            self.create_damage_particles()
    
    def create_star_particles(self):
        """Create twinkling star particles"""
        for _ in range(20):
            particle = {
                'x': self.x + random.randint(-30, 30),
                'y': self.y + random.randint(-30, 30),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'life': random.randint(30, 60),
                'max_life': 60,
                'size': random.randint(1, 3),
                'color': random.choice([YELLOW, WHITE, (255, 255, 150)])
            }
            self.particles.append(particle)
    
    def create_explosion_particles(self):
        """Create explosion particles"""
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            particle = {
                'x': self.x,
                'y': self.y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.randint(20, 40),
                'max_life': 40,
                'size': random.randint(2, 4),
                'color': random.choice([RED, ORANGE, YELLOW])
            }
            self.particles.append(particle)
    
    def create_heal_particles(self):
        """Create healing particles"""
        for _ in range(12):
            particle = {
                'x': self.x + random.randint(-20, 20),
                'y': self.y,
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-2, -1),
                'life': random.randint(40, 60),
                'max_life': 60,
                'size': random.randint(2, 4),
                'color': random.choice([GREEN, (0, 255, 100), (100, 255, 100)])
            }
            self.particles.append(particle)
    
    def create_damage_particles(self):
        """Create damage particles"""
        for _ in range(10):
            angle = random.uniform(-math.pi/4, math.pi/4)  # Upward spread
            speed = random.uniform(1, 4)
            particle = {
                'x': self.x,
                'y': self.y,
                'vx': math.sin(angle) * speed,
                'vy': -math.cos(angle) * speed,
                'life': random.randint(15, 30),
                'max_life': 30,
                'size': random.randint(1, 3),
                'color': random.choice([RED, (255, 100, 100), (200, 0, 0)])
            }
            self.particles.append(particle)
    
    def update(self):
        """Update all particles"""
        self.lifetime += 1
        
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            # Apply gravity for some effects
            if self.effect_type in ["explosion", "damage"]:
                particle['vy'] += 0.1
            
            # Remove dead particles
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen):
        """Draw all particles"""
        for particle in self.particles:
            # Calculate alpha based on remaining life
            alpha_ratio = particle['life'] / particle['max_life']
            alpha = int(255 * alpha_ratio)
            
            # Create surface with alpha for transparency
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            color_with_alpha = (*particle['color'], alpha)
            
            if self.effect_type == "stars":
                # Draw twinkling star
                pygame.draw.circle(particle_surface, color_with_alpha, 
                                 (particle['size'], particle['size']), particle['size'])
            else:
                # Draw circle particle
                pygame.draw.circle(particle_surface, color_with_alpha, 
                                 (particle['size'], particle['size']), particle['size'])
            
            screen.blit(particle_surface, (int(particle['x'] - particle['size']), 
                                         int(particle['y'] - particle['size'])))
    
    def is_finished(self):
        """Check if the effect is finished"""
        return len(self.particles) == 0 and self.lifetime > 10

class ParticleManager:
    def __init__(self):
        self.effects = []
    
    def add_effect(self, x, y, effect_type="stars"):
        """Add a new particle effect"""
        effect = ParticleEffect(x, y, effect_type)
        self.effects.append(effect)
    
    def update(self):
        """Update all effects"""
        for effect in self.effects[:]:
            effect.update()
            if effect.is_finished():
                self.effects.remove(effect)
    
    def draw(self, screen):
        """Draw all effects"""
        for effect in self.effects:
            effect.draw(screen)
    
    def clear(self):
        """Clear all effects"""
        self.effects.clear()

# Global particle manager
particle_manager = ParticleManager()
