"""
Main game class that orchestrates all components
"""
import pygame
import random
from .constants import GameConstants
from .fruit import FruitFactory
from .managers import ScoreManager, LivesManager, DifficultyManager, GameState, FruitSpawner
from .input_handler import InputHandler
from .renderer import UIRenderer
from .screens import HomeScreen, AboutScreen, HighScoreScreen
from .sprite_manager import SpriteManager
from .sound_manager import SoundManager
from .high_scores import HighScoreManager

class Game:
    """Main game class that orchestrates all components"""
    def __init__(self):
        # Initialize pygame if not already initialized
        if not pygame.get_init():
            pygame.init()
            
        # Create a resizable window
        self.screen_width = GameConstants.DEFAULT_SCREEN_WIDTH
        self.screen_height = GameConstants.DEFAULT_SCREEN_HEIGHT
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            pygame.RESIZABLE
        )
        pygame.display.set_caption('Fruit Slicer')
        self.clock = pygame.time.Clock()
        
        # Set window icon
        self.set_window_icon()
        
        # Load custom cursor
        self.load_custom_cursor()
        
        # Initialize sprite manager
        self.sprite_manager = SpriteManager()
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        
        # Initialize high score manager
        self.high_score_manager = HighScoreManager()
        
        # Load background images
        self.load_backgrounds()
        
        # Initialize components
        self.fruits = []
        self.score_manager = ScoreManager()
        self.lives_manager = LivesManager(5)
        self.difficulty_manager = DifficultyManager()
        self.input_handler = InputHandler()
        self.game_state = GameState()
        self.fruit_spawner = FruitSpawner()
        self.ui_renderer = UIRenderer()
        self.fruit_factory = FruitFactory(self.sprite_manager)
        
        # Game state
        self.current_screen = "HOME"  # HOME, GAME, ABOUT
        self.paused = False
        
        # Load UI buttons
        self.load_ui_buttons()
        
        # Initialize screens
        self.home_screen = HomeScreen(self.screen, self.home_background, self.high_score_manager)
        self.about_screen = AboutScreen(self.screen, self.home_background)
        self.high_score_screen = HighScoreScreen(self.screen, self.home_background, self.high_score_manager)
        
        # Start playing background music
        self.sound_manager.play_music("main_theme")
    
    def load_custom_cursor(self):
        """Load custom sword cursor"""
        try:
            # Load cursor image
            cursor_img = pygame.image.load(GameConstants.CURSOR_IMAGE).convert_alpha()
            
            # Get original dimensions
            original_width = cursor_img.get_width()
            original_height = cursor_img.get_height()
            
            # Calculate aspect ratio
            aspect_ratio = original_width / original_height
            
            # Set a target height and calculate width to maintain aspect ratio
            target_height = 60
            target_width = int(target_height * aspect_ratio)
            
            # Scale cursor while preserving aspect ratio
            self.cursor_img = pygame.transform.smoothscale(cursor_img, (target_width, target_height))
            
            # Set hotspot to the bottom edge of the sword (for slicing with the blade)
            # This will make the bottom edge of the sword the active point for the slice line
            self.cursor_hotspot = (target_width // 2, target_height - 5)
            
            # Hide the system cursor
            pygame.mouse.set_visible(False)
            
            self.use_custom_cursor = True
        except Exception as e:
            print(f"Error loading custom cursor: {e}")
            self.use_custom_cursor = False
            pygame.mouse.set_visible(True)
    
    def set_window_icon(self):
        """Set the window icon to a fruit image"""
        try:
            # Use the green apple as the window icon
            icon = pygame.image.load(GameConstants.WINDOW_ICON).convert_alpha()
            
            # Scale down to a good icon size if needed
            if icon.get_width() > 32 or icon.get_height() > 32:
                icon = pygame.transform.scale(icon, (32, 32))
            
            # Set as window icon
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"Could not set window icon: {e}")
    
    def load_backgrounds(self):
        """Load and scale all background images"""
        try:
            # Load home screen background
            home_bg_path = GameConstants.HOME_SCREEN_BACKGROUND
            self.home_background = pygame.image.load(home_bg_path).convert_alpha()
            
            # Scale to current window size while preserving aspect ratio
            bg_aspect = self.home_background.get_width() / self.home_background.get_height()
            screen_aspect = self.screen_width / self.screen_height
            
            if bg_aspect > screen_aspect:
                # Image is wider than screen, scale by height
                new_height = self.screen_height
                new_width = int(new_height * bg_aspect)
                scaled_bg = pygame.transform.smoothscale(self.home_background, (new_width, new_height))
                # Center horizontally
                x_offset = (new_width - self.screen_width) // 2
                self.home_background = scaled_bg.subsurface((x_offset, 0, self.screen_width, self.screen_height))
            else:
                # Image is taller than screen, scale by width
                new_width = self.screen_width
                new_height = int(new_width / bg_aspect)
                scaled_bg = pygame.transform.smoothscale(self.home_background, (new_width, new_height))
                # Center vertically
                y_offset = (new_height - self.screen_height) // 2
                self.home_background = scaled_bg.subsurface((0, y_offset, self.screen_width, self.screen_height))
            
            # Load all gameplay backgrounds with proper aspect ratio preservation
            self.game_backgrounds = []
            for bg_path in GameConstants.BACKGROUND_IMAGES:
                try:
                    bg = pygame.image.load(bg_path).convert_alpha()
                    
                    # Scale while preserving aspect ratio
                    bg_aspect = bg.get_width() / bg.get_height()
                    
                    if bg_aspect > screen_aspect:
                        # Image is wider than screen, scale by height
                        new_height = self.screen_height
                        new_width = int(new_height * bg_aspect)
                        scaled_bg = pygame.transform.smoothscale(bg, (new_width, new_height))
                        # Center horizontally
                        x_offset = (new_width - self.screen_width) // 2
                        scaled_bg = scaled_bg.subsurface((x_offset, 0, self.screen_width, self.screen_height))
                    else:
                        # Image is taller than screen, scale by width
                        new_width = self.screen_width
                        new_height = int(new_width / bg_aspect)
                        scaled_bg = pygame.transform.smoothscale(bg, (new_width, new_height))
                        # Center vertically
                        y_offset = (new_height - self.screen_height) // 2
                        scaled_bg = scaled_bg.subsurface((0, y_offset, self.screen_width, self.screen_height))
                    
                    self.game_backgrounds.append(scaled_bg)
                except Exception as e:
                    print(f"Error loading background {bg_path}: {e}")
                    # Use a fallback color if image can't be loaded
                    fallback_bg = pygame.Surface((self.screen_width, self.screen_height))
                    fallback_bg.fill(GameConstants.BLACK)
                    self.game_backgrounds.append(fallback_bg)
            
            # Start with the first background for gameplay
            self.current_bg_index = 0
            if self.game_backgrounds:
                self.background = self.game_backgrounds[self.current_bg_index]
            else:
                # Create a fallback background if no backgrounds were loaded
                self.background = pygame.Surface((self.screen_width, self.screen_height))
                self.background.fill(GameConstants.BLACK)
            
        except Exception as e:
            print(f"Warning: Could not load background images: {e}")
            self.home_background = None
            self.game_backgrounds = []
            self.background = None
    
    def load_ui_buttons(self):
        """Load UI button images"""
        try:
            # Load pause button
            self.pause_button_img = pygame.image.load(GameConstants.PAUSE_BUTTON).convert_alpha()
            self.pause_button_img = pygame.transform.smoothscale(self.pause_button_img, (50, 50))
            self.pause_button_rect = self.pause_button_img.get_rect(topright=(self.screen_width - 10, 10))
            
            # Load resume button
            self.resume_button_img = pygame.image.load(GameConstants.RESUME_BUTTON).convert_alpha()
            self.resume_button_img = pygame.transform.smoothscale(self.resume_button_img, (50, 50))
            self.resume_button_rect = self.resume_button_img.get_rect(topright=(self.screen_width - 10, 10))
        except Exception as e:
            print(f"Error loading UI buttons: {e}")
            self.pause_button_img = None
            self.resume_button_img = None
    
    def handle_resize(self, new_width, new_height):
        """Handle window resize event"""
        self.screen_width = max(400, new_width)  # Minimum width
        self.screen_height = max(300, new_height)  # Minimum height
        
        # Update screen
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            pygame.RESIZABLE
        )
        
        # Reload and rescale backgrounds
        self.load_backgrounds()
        
        # Update screens with new background
        self.home_screen = HomeScreen(self.screen, self.home_background, self.high_score_manager)
        self.about_screen = AboutScreen(self.screen, self.home_background)
        self.high_score_screen = HighScoreScreen(self.screen, self.home_background, self.high_score_manager)
        
        # Update UI button positions
        if hasattr(self, 'pause_button_img') and self.pause_button_img:
            self.pause_button_rect = self.pause_button_img.get_rect(topright=(self.screen_width - 10, 10))
            self.resume_button_rect = self.resume_button_img.get_rect(topright=(self.screen_width - 10, 10))
    
    def reset(self):
        """Reset the game to initial state"""
        self.fruits = []
        self.score_manager.reset()
        self.lives_manager.reset()
        self.difficulty_manager.reset()
        self.fruit_spawner.reset()
        self.game_state.reset()
        self.paused = False
        
        # Play game start sound
        self.sound_manager.play_sound("game_start")
    
    def spawn_fruits(self):
        """Spawn new fruits based on current difficulty"""
        num_fruits = self.fruit_spawner.get_spawn_count()
        speed_multiplier = self.difficulty_manager.get_speed_multiplier()
        
        for _ in range(num_fruits):
            self.fruits.append(self.fruit_factory.create_fruit(speed_multiplier))
            # Play fruit throw sound
            self.sound_manager.play_sound("fruit_throw", 0.3)
    
    def update_game(self):
        """Update game state for the current frame"""
        # Don't update if paused
        if self.paused:
            return
            
        # Check if we should spawn new fruits
        if self.fruit_spawner.update():
            self.spawn_fruits()
        
        # Update fruits
        for fruit in self.fruits[:]:
            fruit.update()
            
            # Check if fruit fell off screen without being sliced
            if fruit.is_removable():
                if not fruit.is_sliced():
                    self.lives_manager.lose_life()
                    # Play lose life sound
                    self.sound_manager.play_sound("lose_life")
                    if not self.lives_manager.has_lives():
                        self.game_state.set_game_over()
                        # Play game over sound
                        self.sound_manager.play_sound("game_over")
                        
                        # Check if this is a high score
                        final_score = self.score_manager.get_score()
                        if self.high_score_manager.is_high_score(final_score):
                            # Add to high scores
                            self.high_score_manager.add_score(final_score)
                            # Play high score sound
                            self.sound_manager.play_sound("new_high_score")
                self.fruits.remove(fruit)
        
        # Check for slicing
        if self.input_handler.is_slicing():
            slice_points = self.input_handler.get_slice_points()
            if len(slice_points) > 1:
                sliced_any = False
                for fruit in self.fruits:
                    if fruit.check_slice(slice_points):
                        sliced_any = True
                        self.score_manager.add_score(10)
                        fruits_sliced = self.score_manager.get_fruits_sliced()
                        self.difficulty_manager.increase_difficulty(fruits_sliced)
                        
                        # Check if we should change background based on score
                        self.check_background_change()
                
                # Play slice sound if any fruit was sliced
                if sliced_any:
                    self.sound_manager.play_sound("fruit_slice")
    
    def check_background_change(self):
        """Check if we should change the background based on score"""
        score = self.score_manager.get_score()
        
        # Change background based on score thresholds
        if score < 200:
            new_bg_index = 0  # Background1
        elif score < 500:
            new_bg_index = 1  # Background2
        elif score < 1000:
            new_bg_index = 2  # Background3
        elif score < 1500:
            new_bg_index = 3  # Background4
        elif score < 2000:
            new_bg_index = 4  # Background5
        elif score < 2500:
            new_bg_index = 5  # Background6
        elif score < 3000:
            new_bg_index = 6  # Background7
        else:
            new_bg_index = 7  # Background8
        
        # Increase speed significantly after level 2
        if new_bg_index >= 2 and self.difficulty_manager.get_speed_multiplier() < 2.0:
            self.difficulty_manager.speed_multiplier = 2.0
        
        if new_bg_index != self.current_bg_index and new_bg_index < len(self.game_backgrounds):
            self.current_bg_index = new_bg_index
            self.background = self.game_backgrounds[self.current_bg_index]
            # Play sound for background change
            self.sound_manager.play_sound("new_background")
    
    def render_game(self):
        """Render the current game state"""
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(GameConstants.BLACK)
        
        # Draw fruits
        for fruit in self.fruits:
            fruit.render(self.screen)
        
        # Draw slice line
        if self.input_handler.is_slicing():
            slice_points = self.input_handler.get_slice_points()
            if len(slice_points) > 1:
                # Draw a thinner line with a subtle glow effect
                # First draw a narrower, semi-transparent line for the glow
                pygame.draw.lines(self.screen, (255, 255, 255, 80), False, slice_points, 4)
                # Then draw the main line on top
                pygame.draw.lines(self.screen, GameConstants.WHITE, False, slice_points, 2)
        
        # Draw UI
        self.ui_renderer.render_ui(
            self.screen,
            self.score_manager.get_score(),
            self.lives_manager.get_lives(),
            self.difficulty_manager.get_speed_multiplier(),
            self.game_state,
            self.current_bg_index + 1  # Display current background number (1-based)
        )
        
        # Draw play/pause button
        self.render_play_pause_button()
        
        # Draw custom cursor
        self.render_custom_cursor()
    
    def render_custom_cursor(self):
        """Render the custom sword cursor"""
        if hasattr(self, 'use_custom_cursor') and self.use_custom_cursor and hasattr(self, 'cursor_img'):
            mouse_pos = pygame.mouse.get_pos()
            # Position cursor so the hotspot is at the mouse position
            cursor_pos = (mouse_pos[0] - self.cursor_hotspot[0], mouse_pos[1] - self.cursor_hotspot[1])
            self.screen.blit(self.cursor_img, cursor_pos)
    
    def render_play_pause_button(self):
        """Render the play/pause button"""
        if self.paused and self.resume_button_img:
            self.screen.blit(self.resume_button_img, self.resume_button_rect)
        elif not self.paused and self.pause_button_img:
            self.screen.blit(self.pause_button_img, self.pause_button_rect)
    
    def toggle_pause(self):
        """Toggle game pause state"""
        self.paused = not self.paused
        if self.paused:
            self.sound_manager.play_sound("pause")
            self.sound_manager.pause_music()
        else:
            self.sound_manager.play_sound("resume")
            self.sound_manager.unpause_music()
        return self.paused
    
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Handle window resize
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize(event.w, event.h)
            
            # Handle mouse clicks for pause/resume button
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.current_screen == "GAME" and not self.game_state.is_game_over():
                    if self.paused and self.resume_button_rect.collidepoint(mouse_pos):
                        self.toggle_pause()
                    elif not self.paused and self.pause_button_rect.collidepoint(mouse_pos):
                        self.toggle_pause()
                
            if self.current_screen == "HOME":
                action = self.home_screen.handle_event(event)
                if action == "PLAY":
                    self.current_screen = "GAME"
                    self.reset()  # Reset game state when starting a new game
                    # Play button sound
                    self.sound_manager.play_sound("button_click")
                elif action == "ABOUT":
                    self.current_screen = "ABOUT"
                    # Play button sound
                    self.sound_manager.play_sound("button_click")
                    
            elif self.current_screen == "ABOUT":
                action = self.about_screen.handle_event(event)
                if action == "HOME":
                    self.current_screen = "HOME"
                    # Play button sound
                    self.sound_manager.play_sound("button_click")
                    
            elif self.current_screen == "GAME":
                result = self.input_handler.handle_event(event, self.game_state)
                if result == "RESET":
                    self.reset()
                    # Play button sound
                    self.sound_manager.play_sound("button_click")
                elif result == "HOME":
                    self.current_screen = "HOME"
                    # Play button sound
                    self.sound_manager.play_sound("main_menu_exit")
                elif result == "PAUSE":
                    self.toggle_pause()
                    
        return True
    
    def update(self):
        """Update the current screen"""
        if self.current_screen == "HOME":
            self.home_screen.update()
        elif self.current_screen == "ABOUT":
            self.about_screen.update()
        elif self.current_screen == "GAME" and not self.game_state.is_game_over():
            self.update_game()
    
    def render(self):
        """Render the current screen"""
        if self.current_screen == "HOME":
            self.home_screen.draw()
            self.render_custom_cursor()  # Draw cursor on home screen too
        elif self.current_screen == "ABOUT":
            self.about_screen.draw()
            self.render_custom_cursor()  # Draw cursor on about screen too
        elif self.current_screen == "GAME":
            self.render_game()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update current screen
            self.update()
            
            # Render current screen
            self.render()
            
            pygame.display.flip()
            self.clock.tick(GameConstants.FPS)
            
        # Clean up
        pygame.quit()
