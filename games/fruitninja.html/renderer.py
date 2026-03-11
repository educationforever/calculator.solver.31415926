"""
Rendering classes for the game
"""
import pygame
from .constants import GameConstants

class UIRenderer:
    """Renders the game UI elements"""
    def __init__(self):
        # Use custom game font if available
        try:
            self.font = pygame.font.Font(GameConstants.GAME_FONT, 36)
            self.small_font = pygame.font.Font(GameConstants.GAME_FONT, 24)
        except:
            # Fall back to SysFont if Font fails
            self.font = pygame.font.SysFont(None, 36)
            self.small_font = pygame.font.SysFont(None, 24)
    
    def render_ui(self, screen, score, lives, speed_multiplier, game_state, bg_number=1):
        # Get current screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Draw score with antialiasing
        score_text = self.font.render(f'Score: {score}', True, GameConstants.WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw lives as X's
        lives_text = self.font.render('Lives: ' + 'X' * lives, True, GameConstants.WHITE)
        screen.blit(lives_text, (10, 50))
        
        # Draw speed multiplier
        speed_text = self.font.render(f'Speed: x{speed_multiplier:.2f}', True, GameConstants.WHITE)
        screen.blit(speed_text, (10, 90))
        
        # Calculate and draw level number (based on score)
        level = bg_number  # Level corresponds to background number
        level_text = self.small_font.render(f'Level: {level}', True, GameConstants.WHITE)
        screen.blit(level_text, (10, 130))
        
        # Draw game over message
        if game_state.is_game_over():
            game_over_text = self.font.render('GAME OVER', True, GameConstants.RED)
            final_score_text = self.font.render(f'Final Score: {score}', True, GameConstants.WHITE)
            
            # Center align game over text
            game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
            final_score_rect = final_score_text.get_rect(center=(screen_width // 2, screen_height // 2))
            
            screen.blit(game_over_text, game_over_rect)
            screen.blit(final_score_text, final_score_rect)
            
            # Only show restart message after delay
            if game_state.can_restart():
                restart_text = self.font.render('Press R to restart', True, GameConstants.WHITE)
                back_text = self.font.render('Press ESC for menu', True, GameConstants.WHITE)
                
                # Center align instruction texts
                restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 40))
                back_rect = back_text.get_rect(center=(screen_width // 2, screen_height // 2 + 80))
                
                screen.blit(restart_text, restart_rect)
                screen.blit(back_text, back_rect)
