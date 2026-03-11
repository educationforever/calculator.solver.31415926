"""
Game constants and configuration values
"""
import os

class GameConstants:
    # Default window size (can be resized)
    DEFAULT_SCREEN_WIDTH = 800
    DEFAULT_SCREEN_HEIGHT = 600
    FPS = 60
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    MAGENTA = (255, 0, 255)
    CYAN = (0, 255, 255)
    FRUIT_COLORS = [RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN]
    
    # Asset paths
    ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    
    # Home screen background
    HOME_SCREEN_BACKGROUND = os.path.join(ASSETS_DIR, "homescreenbg.png")
    
    # Background images - define them explicitly
    BACKGROUND_IMAGES = [
        os.path.join(ASSETS_DIR, "res", "Background1.png"),
        os.path.join(ASSETS_DIR, "res", "Background2.png"),
        os.path.join(ASSETS_DIR, "res", "Background3.png"),
        os.path.join(ASSETS_DIR, "res", "Background4.jpg"),
        os.path.join(ASSETS_DIR, "res", "Background5.png"),
        os.path.join(ASSETS_DIR, "res", "Background6.png"),
        os.path.join(ASSETS_DIR, "res", "Background7.png"),
        os.path.join(ASSETS_DIR, "res", "Background8.png")
    ]
    
    MAIN_MENU_BACKGROUND = os.path.join(ASSETS_DIR, "res", "MainMenuBackground.jpg")
    
    # Fruit images
    FRUIT_IMAGES = {
        "banana": {
            "whole": os.path.join(ASSETS_DIR, "res", "Banana.png"),
            "sliced": [
                os.path.join(ASSETS_DIR, "res", "BananaTop.png"),
                os.path.join(ASSETS_DIR, "res", "BananaBottom.png")
            ]
        },
        "green_apple": {
            "whole": os.path.join(ASSETS_DIR, "res", "GreenApple.png"),
            "sliced": [
                os.path.join(ASSETS_DIR, "res", "GreenAppleSliced.png")
            ]
        },
        "orange": {
            "whole": os.path.join(ASSETS_DIR, "res", "Orange.png"),
            "sliced": [
                os.path.join(ASSETS_DIR, "res", "OrangeSliced.png")
            ]
        },
        "watermelon": {
            "whole": os.path.join(ASSETS_DIR, "res", "Watermelon.png"),
            "sliced": [
                os.path.join(ASSETS_DIR, "res", "WatermelonHalf.png"),
                os.path.join(ASSETS_DIR, "res", "WatermelonHalf.png")
            ]
        },
        "magic_bean": {
            "whole": os.path.join(ASSETS_DIR, "res", "MagicBean.png"),
            "sliced": [
                os.path.join(ASSETS_DIR, "res", "MagicBeanSliced.png")
            ]
        },
        "freeze_banana": {
            "whole": os.path.join(ASSETS_DIR, "res", "FreezeBanana.png"),
            "sliced": [
                os.path.join(ASSETS_DIR, "res", "FreezeBananaSliced.png")
            ]
        }
    }
    
    # Special items
    BOMB_IMAGE = os.path.join(ASSETS_DIR, "res", "Bomb.png")
    BOMB_SLICED_IMAGE = os.path.join(ASSETS_DIR, "res", "Bomb.png")  # Same image as we don't want to show sliced bomb
    MINUS_10_BOMB_IMAGE = os.path.join(ASSETS_DIR, "res", "-10Bomb.png")
    MINUS_10_BOMB_SLICED_IMAGE = os.path.join(ASSETS_DIR, "res", "-10BombSliced.png")
    
    # UI elements
    BACK_BUTTON = os.path.join(ASSETS_DIR, "res", "BackButton.png")
    PAUSE_BUTTON = os.path.join(ASSETS_DIR, "res", "PauseButton.png")
    RESUME_BUTTON = os.path.join(ASSETS_DIR, "res", "ResumeButton.png")
    RESET_BUTTON = os.path.join(ASSETS_DIR, "res", "ResetButton.png")
    SETTINGS_BUTTON = os.path.join(ASSETS_DIR, "res", "SettingsButton.png")
    SAVE_BUTTON = os.path.join(ASSETS_DIR, "res", "SaveButton.png")
    LOAD_BUTTON = os.path.join(ASSETS_DIR, "res", "LoadButton.png")
    ARCADE_MODE_BUTTON = os.path.join(ASSETS_DIR, "res", "ArcadeMode.png")
    CLASSIC_MODE_BUTTON = os.path.join(ASSETS_DIR, "res", "ClassicMode.png")
    CURSOR_IMAGE = os.path.join(ASSETS_DIR, "cursor", "sword.png")
    
    # Font
    GAME_FONT = os.path.join(ASSETS_DIR, "res", "fonts", "GangOfThree.ttf")
    
    # Sound effects - define them explicitly
    SOUNDS = {
        "fruit_slice": os.path.join(ASSETS_DIR, "sounds", "FruitSlice.wav"),
        "fruit_throw": os.path.join(ASSETS_DIR, "sounds", "FruitThrow.wav"),
        "bomb_explode": os.path.join(ASSETS_DIR, "sounds", "BombExplode.wav"),
        "bomb_throw": os.path.join(ASSETS_DIR, "sounds", "BombThrow.wav"),
        "button_click": os.path.join(ASSETS_DIR, "sounds", "Button.wav"),
        "combo": os.path.join(ASSETS_DIR, "sounds", "Combo.wav"),
        "extra_life": os.path.join(ASSETS_DIR, "sounds", "ExtraLife.wav"),
        "freeze_banana": os.path.join(ASSETS_DIR, "sounds", "FreezeBanana.wav"),
        "game_over": os.path.join(ASSETS_DIR, "sounds", "GameOver.wav"),
        "game_start": os.path.join(ASSETS_DIR, "sounds", "GameStart.wav"),
        "lose_life": os.path.join(ASSETS_DIR, "sounds", "LoseLife.wav"),
        "main_menu_exit": os.path.join(ASSETS_DIR, "sounds", "MainMenuExit.wav"),
        "main_theme": os.path.join(ASSETS_DIR, "sounds", "MainTheme.wav"),
        "new_background": os.path.join(ASSETS_DIR, "sounds", "NewBackground.wav"),
        "new_high_score": os.path.join(ASSETS_DIR, "sounds", "NewHighScore.wav"),
        "pause": os.path.join(ASSETS_DIR, "sounds", "Pause.wav"),
        "resume": os.path.join(ASSETS_DIR, "sounds", "Resume.wav"),
        "times_up": os.path.join(ASSETS_DIR, "sounds", "TimesUp.wav")
    }
    
    # Legacy paths (for backward compatibility)
    NEW_FRUITS_SPRITESHEET = os.path.join(ASSETS_DIR, "Fruits", "Asset", "Fruits.png")
    SLICED_FRUITS_SPRITESHEET = os.path.join(ASSETS_DIR, "sliced_fruits", "PACK", "sprites.png")
    WINDOW_ICON = os.path.join(ASSETS_DIR, "res", "GreenApple.png")
    
    # Sprite dimensions
    FRUIT_SPRITE_SIZE = 64
    NEW_FRUIT_SPRITE_SIZE = 64
    SLICED_FRUIT_SPRITE_SIZE = 32
