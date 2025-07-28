import pygame
from player import Player
from enemy import Enemy
from settings import *
from particles import particle_manager

class Combat:
    def __init__(self, screen, font, small_font):
        self.screen = screen
        self.font = font
        self.small_font = small_font
        
        # Combat state
        self.state = "player_turn"  # player_turn, enemy_turn, game_over, victory
        self.player = Player()
        self.enemy = Enemy()
        
        # UI state
        self.message = ""
        self.message_timer = 0
        self.turn_transition_timer = 0
        
    def reset(self):
        """Reset combat for new fight"""
        self.state = "player_turn"
        self.player.reset()
        self.enemy.reset()
        self.message = ""
        self.message_timer = 0
        self.turn_transition_timer = 0
        
    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.KEYDOWN:
            if self.state == "player_turn":
                if event.key == pygame.K_LEFT and self.player.selected_action > 0:
                    self.player.selected_action -= 1
                elif event.key == pygame.K_RIGHT and self.player.selected_action < len(self.player.actions) - 1:
                    self.player.selected_action += 1
                elif event.key == pygame.K_z or event.key == pygame.K_RETURN:
                    self.execute_player_action()
    
    def update(self):
        """Update combat logic"""
        keys = pygame.key.get_pressed()
        
        # Update timers
        if self.message_timer > 0:
            self.message_timer -= 1
        if self.turn_transition_timer > 0:
            self.turn_transition_timer -= 1
        
        # Update player
        self.player.update()
        
        # Update particle effects
        particle_manager.update()
        
        # State machine
        if self.state == "player_turn":
            self.update_player_turn(keys)
        elif self.state == "enemy_turn":
            self.update_enemy_turn(keys)
        elif self.state == "turn_transition":
            self.update_turn_transition()
        
        # Check win/lose conditions
        if self.player.hp <= 0:
            self.state = "game_over"
        elif self.enemy.hp <= 0:
            self.state = "victory"
            self.show_message("Victory! Enemy defeated!", 180)
    
    def update_player_turn(self, keys):
        """Handle player's turn logic"""
        # Menu navigation is now handled in handle_event method
        pass
    
    def execute_player_action(self):
        """Execute the selected player action"""
        action = self.player.actions[self.player.selected_action]
        
        if action == "FIGHT":
            damage = 15  # Base damage
            # Add damage particle effect
            particle_manager.add_effect(SCREEN_WIDTH - 150, 80, "explosion")
            if self.enemy.take_damage(damage):
                self.show_message(f"You dealt {damage} damage! Enemy defeated!", 120)
                self.state = "victory"
            else:
                self.show_message(f"You dealt {damage} damage!", 120)
                self.start_enemy_turn()
        
        elif action == "ACT":
            # Add star effect
            particle_manager.add_effect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "stars")
            self.show_message("You try to reason with the enemy...", 120)
            self.start_enemy_turn()
        
        elif action == "ITEM":
            heal_amount = 20
            self.player.hp = min(self.player.max_hp, self.player.hp + heal_amount)
            # Add healing particle effect
            particle_manager.add_effect(self.player.rect.centerx, self.player.rect.centery, "heal")
            self.show_message(f"You healed {heal_amount} HP!", 120)
            self.start_enemy_turn()
        
        elif action == "MERCY":
            if self.enemy.hp < self.enemy.max_hp * 0.3:  # Can only spare when enemy is low HP
                self.show_message("Enemy spared! Victory!", 120)
                self.state = "victory"
            else:
                self.show_message("Enemy doesn't want mercy yet...", 120)
                self.start_enemy_turn()
    
    def start_enemy_turn(self):
        """Start enemy's attack phase"""
        self.state = "turn_transition"
        self.turn_transition_timer = 60  # 1 second transition
        self.show_message("Enemy attacks!", 60)
    
    def update_turn_transition(self):
        """Handle transition between turns"""
        if self.turn_transition_timer <= 0:
            self.state = "enemy_turn"
            self.enemy.start_attack()
    
    def update_enemy_turn(self, keys):
        """Handle enemy's turn (dodge phase)"""
        # Player can move to dodge
        self.player.handle_input_dodge(keys)
        
        # Update enemy attack
        self.enemy.update(self.player)
        
        # Check if attack is finished
        if self.enemy.attack_finished:
            self.state = "player_turn"
            self.player.made_move = False
            self.show_message("Your turn!", 60)
    
    def show_message(self, text, duration=120):
        """Show a message for a specified duration"""
        self.message = text
        self.message_timer = duration
    
    def draw(self):
        """Draw the combat scene"""
        if self.state == "player_turn":
            self.draw_player_turn()
        elif self.state == "enemy_turn" or self.state == "turn_transition":
            self.draw_enemy_turn()
        elif self.state == "victory":
            self.draw_victory()
        
        # Always draw HP bars
        self.player.draw_hp_bar(self.screen, self.small_font)
        self.enemy.draw(self.screen, self.small_font)
        
        # Draw particle effects
        particle_manager.draw(self.screen)
        
        # Draw message if active
        if self.message_timer > 0:
            self.draw_message()
    
    def draw_player_turn(self):
        """Draw UI for player's turn"""
        # Draw action menu
        self.player.draw_menu(self.screen, self.font)
        
        # Draw instructions
        instruction_text = self.small_font.render("Use LEFT/RIGHT arrows to select, Z/ENTER to confirm", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(instruction_text, instruction_rect)
        
        # Draw combat box (empty during menu)
        pygame.draw.rect(self.screen, WHITE, 
                        (COMBAT_BOX_X, COMBAT_BOX_Y, COMBAT_BOX_WIDTH, COMBAT_BOX_HEIGHT), 2)
    
    def draw_enemy_turn(self):
        """Draw UI for enemy's turn (dodge phase)"""
        # Draw player
        self.player.draw(self.screen)
        
        # Draw instructions
        instruction_text = self.small_font.render("Use WASD or arrow keys to dodge!", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(instruction_text, instruction_rect)
    
    def draw_victory(self):
        """Draw victory screen"""
        victory_text = self.font.render("VICTORY!", True, GREEN)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(victory_text, victory_rect)
        
        # Draw combat box
        pygame.draw.rect(self.screen, WHITE, 
                        (COMBAT_BOX_X, COMBAT_BOX_Y, COMBAT_BOX_WIDTH, COMBAT_BOX_HEIGHT), 2)
    
    def draw_message(self):
        """Draw current message"""
        if self.message:
            # Create a semi-transparent background
            message_surface = pygame.Surface((SCREEN_WIDTH, 60))
            message_surface.set_alpha(180)
            message_surface.fill((50, 50, 50))
            self.screen.blit(message_surface, (0, SCREEN_HEIGHT - 100))
            
            # Draw message text
            message_text = self.font.render(self.message, True, WHITE)
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70))
            self.screen.blit(message_text, message_rect)
