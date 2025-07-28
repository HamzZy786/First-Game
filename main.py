import pygame
import sys
from combat import Combat
from menu import MainMenu
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Undertale-Style Combat Game")
        self.clock = pygame.time.Clock()
        
        # Initialize fonts
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        self.small_font = pygame.font.Font(None, SMALL_FONT_SIZE)
        
        # Game state
        self.state = "menu"  # menu, combat, game_over
        self.menu = MainMenu(self.screen, self.font, self.small_font)
        self.combat = Combat(self.screen, self.font, self.small_font)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if self.state == "menu":
                result = self.menu.handle_input(event)
                if result == "start_game":
                    self.state = "combat"
                    self.combat.reset()
                elif result == "quit":
                    return False
            
            elif self.state == "combat":
                self.combat.handle_event(event)
                
                # Check if combat is over
                if self.combat.state == "game_over":
                    self.state = "game_over"
            
            elif self.state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.state = "menu"
                        self.menu = MainMenu(self.screen, self.font, self.small_font)
                    elif event.key == pygame.K_ESCAPE:
                        return False
                        
        return True
    
    def update(self):
        if self.state == "menu":
            self.menu.update()
        elif self.state == "combat":
            self.combat.update()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.state == "menu":
            self.menu.draw()
        elif self.state == "combat":
            self.combat.draw()
        elif self.state == "game_over":
            self.draw_game_over()
            
        pygame.display.flip()
    
    def draw_game_over(self):
        game_over_text = self.font.render("GAME OVER", True, RED)
        restart_text = self.small_font.render("Press R to restart or ESC to quit", True, WHITE)
        
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
