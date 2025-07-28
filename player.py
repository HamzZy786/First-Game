import pygame
from settings import *

class Player:
    def __init__(self):
        # Player position (heart/soul)
        self.rect = pygame.Rect(
            COMBAT_BOX_X + COMBAT_BOX_WIDTH // 2 - PLAYER_SIZE // 2,
            COMBAT_BOX_Y + COMBAT_BOX_HEIGHT // 2 - PLAYER_SIZE // 2,
            PLAYER_SIZE,
            PLAYER_SIZE
        )
        self.speed = PLAYER_SPEED
        self.hp = PLAYER_HP
        self.max_hp = PLAYER_HP
        
        # Combat state
        self.made_move = False
        self.selected_action = 0  # 0=Fight, 1=Act, 2=Item, 3=Mercy
        self.actions = ["FIGHT", "ACT", "ITEM", "MERCY"]
        
        # Invincibility frames after getting hit
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 60  # 1 second at 60fps
        
    def reset(self):
        """Reset player for new combat"""
        self.rect.x = COMBAT_BOX_X + COMBAT_BOX_WIDTH // 2 - PLAYER_SIZE // 2
        self.rect.y = COMBAT_BOX_Y + COMBAT_BOX_HEIGHT // 2 - PLAYER_SIZE // 2
        self.hp = self.max_hp
        self.made_move = False
        self.selected_action = 0
        self.invincible = False
        self.invincible_timer = 0
    
    def handle_input_menu(self, keys):
        """Handle input during menu selection"""
        if keys[pygame.K_LEFT] and self.selected_action > 0:
            self.selected_action -= 1
        elif keys[pygame.K_RIGHT] and self.selected_action < len(self.actions) - 1:
            self.selected_action += 1
        elif keys[pygame.K_z] or keys[pygame.K_RETURN]:  # Z or Enter to confirm
            self.made_move = True
            return True
        return False
    
    def handle_input_dodge(self, keys):
        """Handle input during dodge phase"""
        old_x, old_y = self.rect.x, self.rect.y
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        
        # Keep player within combat box
        if self.rect.left < COMBAT_BOX_X:
            self.rect.left = COMBAT_BOX_X
        if self.rect.right > COMBAT_BOX_X + COMBAT_BOX_WIDTH:
            self.rect.right = COMBAT_BOX_X + COMBAT_BOX_WIDTH
        if self.rect.top < COMBAT_BOX_Y:
            self.rect.top = COMBAT_BOX_Y
        if self.rect.bottom > COMBAT_BOX_Y + COMBAT_BOX_HEIGHT:
            self.rect.bottom = COMBAT_BOX_Y + COMBAT_BOX_HEIGHT
    
    def update(self):
        """Update player state"""
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
    
    def take_damage(self, damage=10):
        """Take damage if not invincible"""
        if not self.invincible:
            self.hp -= damage
            self.invincible = True
            self.invincible_timer = self.invincible_duration
            return True
        return False
    
    def draw_menu(self, screen, font):
        """Draw action selection menu"""
        menu_y = SCREEN_HEIGHT - 150
        box_width = 150
        box_height = 50
        
        for i, action in enumerate(self.actions):
            x = 100 + i * (box_width + 20)
            
            # Draw selection box
            color = WHITE if i == self.selected_action else (100, 100, 100)
            pygame.draw.rect(screen, color, (x, menu_y, box_width, box_height), 2)
            
            # Draw action text
            text = font.render(action, True, WHITE)
            text_rect = text.get_rect(center=(x + box_width // 2, menu_y + box_height // 2))
            screen.blit(text, text_rect)
    
    def draw_hp_bar(self, screen, font):
        """Draw HP bar"""
        hp_text = font.render(f"HP: {self.hp}/{self.max_hp}", True, WHITE)
        screen.blit(hp_text, (20, 20))
        
        # HP bar
        bar_width = 200
        bar_height = 20
        bar_x = 20
        bar_y = 50
        
        # Background
        pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        # Current HP
        hp_percentage = self.hp / self.max_hp
        current_width = int(bar_width * hp_percentage)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, current_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
    
    def draw(self, screen):
        """Draw the player (heart/soul)"""
        # Flicker if invincible
        if self.invincible and self.invincible_timer % 10 < 5:
            return
            
        pygame.draw.rect(screen, RED, self.rect)
        # Draw a simple heart shape (optional)
        # For now, just a red square representing the soul
