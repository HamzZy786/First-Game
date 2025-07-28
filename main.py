import pygame
import sys
from combat import Combat
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
        self.combat = Combat(self.screen, self.font, self.small_font)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if self.state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.state = "combat"
                        self.combat.reset()
            
            elif self.state == "combat":
                self.combat.handle_event(event)
                
                # Check if combat is over
                if self.combat.state == "game_over":
                    self.state = "game_over"
            
            elif self.state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.state = "menu"
                    elif event.key == pygame.K_ESCAPE:
                        return False
                        
        return True
    
    def update(self):
        if self.state == "combat":
            self.combat.update()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "combat":
            self.combat.draw()
        elif self.state == "game_over":
            self.draw_game_over()
            
        pygame.display.flip()
    
    def draw_menu(self):
        title_text = self.font.render("UNDERTALE-STYLE COMBAT", True, WHITE)
        start_text = self.small_font.render("Press SPACE to start", True, WHITE)
        
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        
        self.screen.blit(title_text, title_rect)
        self.screen.blit(start_text, start_rect)
    
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
