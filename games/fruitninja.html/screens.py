"""
Game screens (home screen, about screen, etc.)
"""
import pygame
from .constants import GameConstants

class Button:
    """Interactive button class for UI screens"""
    def __init__(self, x, y, width, height, text, font, text_color=GameConstants.BLACK, 
                 bg_color=GameConstants.WHITE, hover_color=(220, 220, 220)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.is_hovered = False
        
        # Pre-render text with antialiasing
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        
    def update(self, mouse_pos):
        """Update button state based on mouse position"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def draw(self, screen):
        """Draw the button on the screen"""
        # Draw button background
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.text_color, self.rect, 2)  # Border
        
        # Draw button text
        screen.blit(self.text_surface, self.text_rect)
        
    def is_clicked(self, event):
        """Check if button was clicked"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_hovered
        return False


class HomeScreen:
    """Home screen with play and about buttons"""
    def __init__(self, screen, background_image=None, high_score_manager=None):
        self.screen = screen
        self.background = background_image
        self.high_score_manager = high_score_manager
        
        # Get current screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Use custom game font if available
        try:
            self.font_large = pygame.font.Font(GameConstants.GAME_FONT, 72)
            self.font_medium = pygame.font.Font(GameConstants.GAME_FONT, 48)
            self.font_small = pygame.font.Font(GameConstants.GAME_FONT, 24)
        except:
            # Fall back to SysFont if Font fails
            self.font_large = pygame.font.SysFont(None, 72)
            self.font_medium = pygame.font.SysFont(None, 48)
            self.font_small = pygame.font.SysFont(None, 24)
        
        # Create title with antialiasing
        self.title_text = self.font_large.render("FRUIT SLICER", True, GameConstants.WHITE)
        self.title_rect = self.title_text.get_rect(center=(screen_width // 2, 150))
        
        # Create high score text
        self.high_score = 0
        if high_score_manager and high_score_manager.get_high_scores():
            # Get the highest score
            self.high_score = high_score_manager.get_high_scores()[0]["score"]
        
        self.high_score_text = self.font_small.render(f"High Score: {self.high_score}", True, GameConstants.WHITE)
        self.high_score_rect = self.high_score_text.get_rect(topleft=(10, 10))
        
        # Create buttons
        button_width = 200
        button_height = 60
        button_y_start = 300
        button_spacing = 80
        
        self.play_button = Button(
            screen_width // 2 - button_width // 2,
            button_y_start,
            button_width,
            button_height,
            "PLAY",
            self.font_medium
        )
        
        self.about_button = Button(
            screen_width // 2 - button_width // 2,
            button_y_start + button_spacing,
            button_width,
            button_height,
            "ABOUT",
            self.font_medium
        )
        
    def handle_event(self, event):
        """Handle events for the home screen"""
        if self.play_button.is_clicked(event):
            return "PLAY"
        elif self.about_button.is_clicked(event):
            return "ABOUT"
        return None
        
    def update(self):
        """Update home screen state"""
        mouse_pos = pygame.mouse.get_pos()
        self.play_button.update(mouse_pos)
        self.about_button.update(mouse_pos)
        
        # Update high score if needed
        if self.high_score_manager and self.high_score_manager.get_high_scores():
            new_high_score = self.high_score_manager.get_high_scores()[0]["score"]
            if new_high_score != self.high_score:
                self.high_score = new_high_score
                self.high_score_text = self.font_small.render(f"High Score: {self.high_score}", True, GameConstants.WHITE)
        
    def draw(self):
        """Draw the home screen"""
        # Get current screen dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Draw background
        if self.background:
            # Scale background to fit current screen size if needed
            if (self.background.get_width() != screen_width or 
                self.background.get_height() != screen_height):
                scaled_bg = pygame.transform.smoothscale(self.background, (screen_width, screen_height))
                self.screen.blit(scaled_bg, (0, 0))
            else:
                self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(GameConstants.BLACK)
            
        # Draw high score in top left corner
        self.screen.blit(self.high_score_text, self.high_score_rect)
            
        # Update title position for current screen size
        self.title_rect.center = (screen_width // 2, 150)
        self.screen.blit(self.title_text, self.title_rect)
        
        # Update button positions for current screen size
        button_width = 200
        button_y_start = screen_height // 2 - 50
        button_spacing = 80
        
        self.play_button.rect.x = screen_width // 2 - button_width // 2
        self.play_button.rect.y = button_y_start
        self.play_button.text_rect.center = self.play_button.rect.center
        
        self.about_button.rect.x = screen_width // 2 - button_width // 2
        self.about_button.rect.y = button_y_start + button_spacing
        self.about_button.text_rect.center = self.about_button.rect.center
        
        # Draw buttons
        self.play_button.draw(self.screen)
        self.about_button.draw(self.screen)


class AboutScreen:
    """About screen with game information"""
    def __init__(self, screen, background_image=None):
        self.screen = screen
        self.background = background_image
        
        # Get current screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Use custom game font if available
        try:
            self.font_large = pygame.font.Font(GameConstants.GAME_FONT, 48)
            self.font_medium = pygame.font.Font(GameConstants.GAME_FONT, 32)
            self.font_small = pygame.font.Font(GameConstants.GAME_FONT, 24)
        except:
            # Fall back to SysFont if Font fails
            self.font_large = pygame.font.SysFont(None, 48)
            self.font_medium = pygame.font.SysFont(None, 32)
            self.font_small = pygame.font.SysFont(None, 24)
        
        # Create title with antialiasing
        self.title_text = self.font_large.render("ABOUT", True, GameConstants.WHITE)
        self.title_rect = self.title_text.get_rect(center=(screen_width // 2, 100))
        
        # Create about text
        self.about_lines = [
            "Fruit Slicer is Fruit Ninja Clone",
            "Slice fruits with your mouse to score points!",
            "Don't let fruits fall off the screen or you'll lose lives.",
            "",
            "Controls:",
            "- Click and drag to slice fruits",
            "- Press R to restart after game over",
            "- Press ESC to return to menu",
            "",
            "Developer: Aditya Manoj Shinde"
        ]
        
        # Pre-render text surfaces for better performance and quality
        self.text_surfaces = []
        for line in self.about_lines:
            self.text_surfaces.append(self.font_small.render(line, True, GameConstants.WHITE))
        
        # Create back button
        self.back_button = Button(
            screen_width // 2 - 100,
            screen_height - 100,
            200,
            50,
            "BACK",
            self.font_medium
        )
        
    def handle_event(self, event):
        """Handle events for the about screen"""
        if self.back_button.is_clicked(event):
            return "HOME"
        return None
        
    def update(self):
        """Update about screen state"""
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.update(mouse_pos)
        
    def draw(self):
        """Draw the about screen"""
        # Get current screen dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Draw background
        if self.background:
            # Scale background to fit current screen size if needed
            if (self.background.get_width() != screen_width or 
                self.background.get_height() != screen_height):
                scaled_bg = pygame.transform.smoothscale(self.background, (screen_width, screen_height))
                self.screen.blit(scaled_bg, (0, 0))
            else:
                self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(GameConstants.BLACK)
            
        # Update title position for current screen size
        self.title_rect.center = (screen_width // 2, 100)
        self.screen.blit(self.title_text, self.title_rect)
        
        # Draw about text - left aligned
        left_margin = screen_width // 8
        y_offset = 180
        line_spacing = 30
        
        # Use pre-rendered text surfaces
        for text_surface in self.text_surfaces:
            text_rect = text_surface.get_rect(left=left_margin, top=y_offset)
            self.screen.blit(text_surface, text_rect)
            y_offset += line_spacing
        
        # Update back button position
        self.back_button.rect.x = screen_width // 2 - 100
        self.back_button.rect.y = screen_height - 100
        self.back_button.text_rect.center = self.back_button.rect.center
        
        # Draw back button
        self.back_button.draw(self.screen)


class HighScoreScreen:
    """Screen to display high scores"""
    def __init__(self, screen, background_image, high_score_manager):
        self.screen = screen
        self.background = background_image
        self.high_score_manager = high_score_manager
        
        # Get current screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Use custom game font if available
        try:
            self.font_large = pygame.font.Font(GameConstants.GAME_FONT, 48)
            self.font_medium = pygame.font.Font(GameConstants.GAME_FONT, 32)
            self.font_small = pygame.font.Font(GameConstants.GAME_FONT, 24)
        except:
            # Fall back to SysFont if Font fails
            self.font_large = pygame.font.SysFont(None, 48)
            self.font_medium = pygame.font.SysFont(None, 32)
            self.font_small = pygame.font.SysFont(None, 24)
        
        # Create title
        self.title_text = self.font_large.render("HIGH SCORES", True, GameConstants.WHITE)
        self.title_rect = self.title_text.get_rect(center=(screen_width // 2, 100))
        
        # Create back button
        self.back_button = Button(
            screen_width // 2 - 100,
            screen_height - 100,
            200,
            50,
            "BACK",
            self.font_medium
        )
        
    def handle_event(self, event):
        """Handle events for the high score screen"""
        if self.back_button.is_clicked(event):
            return "HOME"
        return None
        
    def update(self):
        """Update high score screen state"""
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.update(mouse_pos)
        
    def draw(self):
        """Draw the high score screen"""
        # Get current screen dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Draw background
        if self.background:
            # Scale background to fit current screen size if needed
            if (self.background.get_width() != screen_width or 
                self.background.get_height() != screen_height):
                scaled_bg = pygame.transform.smoothscale(self.background, (screen_width, screen_height))
                self.screen.blit(scaled_bg, (0, 0))
            else:
                self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(GameConstants.BLACK)
            
        # Draw title
        self.screen.blit(self.title_text, self.title_rect)
        
        # Draw high scores
        scores = self.high_score_manager.get_high_scores()
        
        if not scores:
            # No scores yet
            no_scores_text = self.font_medium.render("No high scores yet!", True, GameConstants.WHITE)
            no_scores_rect = no_scores_text.get_rect(center=(screen_width // 2, screen_height // 2))
            self.screen.blit(no_scores_text, no_scores_rect)
        else:
            # Draw column headers
            rank_header = self.font_medium.render("Rank", True, GameConstants.YELLOW)
            name_header = self.font_medium.render("Name", True, GameConstants.YELLOW)
            score_header = self.font_medium.render("Score", True, GameConstants.YELLOW)
            date_header = self.font_medium.render("Date", True, GameConstants.YELLOW)
            
            # Position headers
            header_y = 180
            rank_x = screen_width // 8
            name_x = screen_width // 4
            score_x = screen_width // 2
            date_x = 3 * screen_width // 4
            
            self.screen.blit(rank_header, (rank_x, header_y))
            self.screen.blit(name_header, (name_x, header_y))
            self.screen.blit(score_header, (score_x, header_y))
            self.screen.blit(date_header, (date_x, header_y))
            
            # Draw scores
            row_height = 40
            start_y = header_y + 50
            
            for i, score in enumerate(scores):
                # Rank
                rank_text = self.font_small.render(f"{i+1}", True, GameConstants.WHITE)
                self.screen.blit(rank_text, (rank_x, start_y + i * row_height))
                
                # Name
                name_text = self.font_small.render(score["name"], True, GameConstants.WHITE)
                self.screen.blit(name_text, (name_x, start_y + i * row_height))
                
                # Score
                score_text = self.font_small.render(str(score["score"]), True, GameConstants.WHITE)
                self.screen.blit(score_text, (score_x, start_y + i * row_height))
                
                # Date
                date_text = self.font_small.render(score["date"], True, GameConstants.WHITE)
                self.screen.blit(date_text, (date_x, start_y + i * row_height))
        
        # Update back button position
        self.back_button.rect.x = screen_width // 2 - 100
        self.back_button.rect.y = screen_height - 100
        self.back_button.text_rect.center = self.back_button.rect.center
        
        # Draw back button
        self.back_button.draw(self.screen)
