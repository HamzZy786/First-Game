import pygame
import math
import random
from settings import *
from sprites import get_sprite_manager
from particles import particle_manager

class MainMenu:
    def __init__(self, screen, font, small_font):
        self.screen = screen
        self.font = font
        self.small_font = small_font
        
        # Menu options
        self.options = ["Start Game", "Instructions", "Settings", "Quit"]
        self.selected_option = 0
        
        # Animation variables
        self.title_pulse = 0
        self.option_hover_scale = [1.0] * len(self.options)
        self.background_stars = []
        self.menu_alpha = 255
        
        # Sub-menu states
        self.current_menu = "main"  # main, instructions, settings
        self.settings = {
            "difficulty": 0,  # 0=Easy, 1=Normal, 2=Hard
            "sound_volume": 0.7,
            "music_volume": 0.5
        }
        
        # Generate background stars
        self.generate_stars()
        
        # Sprite manager
        self.sprite_manager = get_sprite_manager()
        
    def generate_stars(self):
        """Generate twinkling background stars"""
        for _ in range(50):
            star = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'brightness': random.uniform(0.3, 1.0),
                'twinkle_speed': random.uniform(0.02, 0.08),
                'size': random.randint(1, 3)
            }
            self.background_stars.append(star)
    
    def handle_input(self, event):
        """Handle menu input events"""
        if event.type == pygame.KEYDOWN:
            if self.current_menu == "main":
                return self.handle_main_menu_input(event.key)
            elif self.current_menu == "instructions":
                return self.handle_instructions_input(event.key)
            elif self.current_menu == "settings":
                return self.handle_settings_input(event.key)
        return None
    
    def handle_main_menu_input(self, key):
        """Handle main menu navigation"""
        if key == pygame.K_UP and self.selected_option > 0:
            self.selected_option -= 1
            # Add selection particle effect
            particle_manager.add_effect(SCREEN_WIDTH // 2, 300 + self.selected_option * 60, "stars")
        elif key == pygame.K_DOWN and self.selected_option < len(self.options) - 1:
            self.selected_option += 1
            # Add selection particle effect
            particle_manager.add_effect(SCREEN_WIDTH // 2, 300 + self.selected_option * 60, "stars")
        elif key == pygame.K_RETURN or key == pygame.K_z:
            return self.execute_option()
        return None
    
    def handle_instructions_input(self, key):
        """Handle instructions screen input"""
        if key == pygame.K_ESCAPE or key == pygame.K_x:
            self.current_menu = "main"
        return None
    
    def handle_settings_input(self, key):
        """Handle settings menu input"""
        if key == pygame.K_ESCAPE or key == pygame.K_x:
            self.current_menu = "main"
        elif key == pygame.K_LEFT:
            if self.settings["difficulty"] > 0:
                self.settings["difficulty"] -= 1
        elif key == pygame.K_RIGHT:
            if self.settings["difficulty"] < 2:
                self.settings["difficulty"] += 1
        return None
    
    def execute_option(self):
        """Execute the selected menu option"""
        option = self.options[self.selected_option]
        
        if option == "Start Game":
            return "start_game"
        elif option == "Instructions":
            self.current_menu = "instructions"
        elif option == "Settings":
            self.current_menu = "settings"
        elif option == "Quit":
            return "quit"
        return None
    
    def update(self):
        """Update menu animations"""
        # Title pulse animation
        self.title_pulse += 0.05
        
        # Update option hover scales
        for i in range(len(self.option_hover_scale)):
            target_scale = 1.2 if i == self.selected_option else 1.0
            self.option_hover_scale[i] += (target_scale - self.option_hover_scale[i]) * 0.1
        
        # Update twinkling stars
        for star in self.background_stars:
            star['brightness'] += star['twinkle_speed']
            if star['brightness'] > 1.0:
                star['brightness'] = 1.0
                star['twinkle_speed'] *= -1
            elif star['brightness'] < 0.3:
                star['brightness'] = 0.3
                star['twinkle_speed'] *= -1
        
        # Update particle effects
        particle_manager.update()
    
    def draw(self):
        """Draw the current menu"""
        # Draw background
        self.draw_background()
        
        if self.current_menu == "main":
            self.draw_main_menu()
        elif self.current_menu == "instructions":
            self.draw_instructions()
        elif self.current_menu == "settings":
            self.draw_settings()
    
    def draw_background(self):
        """Draw animated background"""
        # Gradient background
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(20 * (1 - color_ratio) + 60 * color_ratio)
            g = int(20 * (1 - color_ratio) + 20 * color_ratio)
            b = int(50 * (1 - color_ratio) + 100 * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Draw twinkling stars
        for star in self.background_stars:
            brightness = int(255 * star['brightness'])
            color = (brightness, brightness, brightness)
            if star['size'] == 1:
                self.screen.set_at((int(star['x']), int(star['y'])), color)
            else:
                pygame.draw.circle(self.screen, color, 
                                 (int(star['x']), int(star['y'])), star['size'])
    
    def draw_main_menu(self):
        """Draw the main menu"""
        # Animated title
        pulse_scale = 1.0 + 0.1 * math.sin(self.title_pulse)
        title_text = "♥ SOUL COMBAT ♥"
        title_surface = self.font.render(title_text, True, WHITE)
        
        # Scale the title
        scaled_width = int(title_surface.get_width() * pulse_scale)
        scaled_height = int(title_surface.get_height() * pulse_scale)
        title_surface = pygame.transform.scale(title_surface, (scaled_width, scaled_height))
        
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle = self.small_font.render("An Undertale-Inspired Combat Experience", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Menu options
        start_y = 300
        for i, option in enumerate(self.options):
            # Option background box
            box_width = 200
            box_height = 40
            box_x = SCREEN_WIDTH // 2 - box_width // 2
            box_y = start_y + i * 60 - box_height // 2
            
            # Hover effect
            if i == self.selected_option:
                # Glowing border
                glow_color = (255, 255, 100)
                pygame.draw.rect(self.screen, glow_color, 
                               (box_x - 2, box_y - 2, box_width + 4, box_height + 4), 2)
                # Background highlight
                pygame.draw.rect(self.screen, (50, 50, 100, 100), 
                               (box_x, box_y, box_width, box_height))
            
            # Option border
            border_color = WHITE if i == self.selected_option else (100, 100, 100)
            pygame.draw.rect(self.screen, border_color, (box_x, box_y, box_width, box_height), 2)
            
            # Option text with scaling
            scale = self.option_hover_scale[i]
            text_color = YELLOW if i == self.selected_option else WHITE
            option_surface = self.small_font.render(option, True, text_color)
            
            if scale != 1.0:
                scaled_width = int(option_surface.get_width() * scale)
                scaled_height = int(option_surface.get_height() * scale)
                option_surface = pygame.transform.scale(option_surface, (scaled_width, scaled_height))
            
            option_rect = option_surface.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * 60))
            self.screen.blit(option_surface, option_rect)
        
        # Controls hint
        controls_text = self.small_font.render("↑↓ Navigate | ENTER/Z Select", True, (150, 150, 150))
        controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(controls_text, controls_rect)
        
        # Draw menu particle effects
        particle_manager.draw(self.screen)
    
    def draw_instructions(self):
        """Draw the instructions screen"""
        # Title
        title = self.font.render("HOW TO PLAY", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Instructions text
        instructions = [
            "COMBAT PHASES:",
            "",
            "1. PLAYER TURN:",
            "   • Use LEFT/RIGHT arrows to select action",
            "   • Press Z or ENTER to confirm",
            "   • FIGHT: Deal damage to enemy",
            "   • ACT: Interact with enemy",
            "   • ITEM: Heal yourself",
            "   • MERCY: Spare weakened enemies",
            "",
            "2. ENEMY TURN (DODGE PHASE):",
            "   • Control your red soul (♥)",
            "   • Use WASD or arrow keys to move",
            "   • Avoid colored bullets!",
            "   • Stay within the white combat box",
            "",
            "GOAL: Defeat enemies or show mercy!",
        ]
        
        y_offset = 150
        for line in instructions:
            if line.startswith("COMBAT PHASES:") or line.startswith("GOAL:"):
                color = YELLOW
                font = self.small_font
            elif line.startswith(("1.", "2.")):
                color = (100, 255, 100)
                font = self.small_font
            elif line.startswith("   •"):
                color = WHITE
                font = self.small_font
            else:
                color = (200, 200, 200)
                font = self.small_font
            
            if line.strip():  # Don't render empty lines
                text_surface = font.render(line, True, color)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                self.screen.blit(text_surface, text_rect)
            
            y_offset += 25
        
        # Back instruction
        back_text = self.small_font.render("Press ESC or X to go back", True, (150, 150, 150))
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(back_text, back_rect)
    
    def draw_settings(self):
        """Draw the settings screen"""
        # Title
        title = self.font.render("SETTINGS", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Difficulty setting
        difficulty_names = ["Easy", "Normal", "Hard"]
        difficulty_colors = [GREEN, YELLOW, RED]
        
        diff_label = self.small_font.render("Difficulty:", True, WHITE)
        diff_label_rect = diff_label.get_rect(center=(SCREEN_WIDTH // 2 - 100, 200))
        self.screen.blit(diff_label, diff_label_rect)
        
        diff_value = self.small_font.render(difficulty_names[self.settings["difficulty"]], 
                                          True, difficulty_colors[self.settings["difficulty"]])
        diff_value_rect = diff_value.get_rect(center=(SCREEN_WIDTH // 2 + 100, 200))
        self.screen.blit(diff_value, diff_value_rect)
        
        # Arrows for difficulty
        left_arrow = self.small_font.render("←", True, WHITE)
        right_arrow = self.small_font.render("→", True, WHITE)
        self.screen.blit(left_arrow, (SCREEN_WIDTH // 2 + 50, 185))
        self.screen.blit(right_arrow, (SCREEN_WIDTH // 2 + 150, 185))
        
        # Instructions
        instructions = [
            "Use LEFT/RIGHT arrows to change difficulty",
            "",
            "Easy: Slower bullets, more HP",
            "Normal: Balanced gameplay",
            "Hard: Faster bullets, less HP"
        ]
        
        y_offset = 280
        for line in instructions:
            color = WHITE if line.startswith("Use") else (180, 180, 180)
            text_surface = self.small_font.render(line, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 30
        
        # Back instruction
        back_text = self.small_font.render("Press ESC or X to go back", True, (150, 150, 150))
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(back_text, back_rect)
