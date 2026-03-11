"""
Sound management for the game
"""
import pygame
from .constants import GameConstants

class SoundManager:
    """Manages loading and playing sounds"""
    
    def __init__(self):
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        self.sounds = {}
        self.music_playing = False
        self.sound_enabled = True
        self.music_enabled = True
        self.load_sounds()
    
    def load_sounds(self):
        """Load all sound effects"""
        try:
            for sound_name, sound_path in GameConstants.SOUNDS.items():
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                except Exception as e:
                    print(f"Could not load sound {sound_name}: {e}")
            
            print(f"Loaded {len(self.sounds)} sound effects")
        except Exception as e:
            print(f"Error loading sounds: {e}")
    
    def play_sound(self, sound_name, volume=1.0):
        """Play a sound effect"""
        if not self.sound_enabled:
            return
            
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(volume)
            self.sounds[sound_name].play()
    
    def play_music(self, music_name="main_theme", loops=-1):
        """Play background music"""
        if not self.music_enabled:
            return
            
        try:
            if music_name in GameConstants.SOUNDS:
                pygame.mixer.music.load(GameConstants.SOUNDS[music_name])
                pygame.mixer.music.set_volume(0.5)  # Lower volume for background music
                pygame.mixer.music.play(loops)
                self.music_playing = True
        except Exception as e:
            print(f"Error playing music {music_name}: {e}")
    
    def stop_music(self):
        """Stop the currently playing music"""
        pygame.mixer.music.stop()
        self.music_playing = False
    
    def pause_music(self):
        """Pause the currently playing music"""
        if self.music_playing:
            pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Unpause the currently playing music"""
        if self.music_playing:
            pygame.mixer.music.unpause()
    
    def toggle_sound(self):
        """Toggle sound effects on/off"""
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled
    
    def toggle_music(self):
        """Toggle music on/off"""
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            if not self.music_playing:
                self.play_music()
        else:
            self.stop_music()
        return self.music_enabled
