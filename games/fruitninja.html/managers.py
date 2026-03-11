"""
Game management classes for score, lives, difficulty, etc.
"""
import time
import random

class ScoreManager:
    """Manages the player's score and fruit slice count"""
    def __init__(self):
        self.score = 0
        self.fruits_sliced = 0
    
    def add_score(self, points):
        self.score += points
        self.fruits_sliced += 1
        
    def get_score(self):
        return self.score
    
    def get_fruits_sliced(self):
        return self.fruits_sliced
    
    def reset(self):
        self.score = 0
        self.fruits_sliced = 0


class LivesManager:
    """Manages the player's lives"""
    def __init__(self, initial_lives=5):
        self.lives = initial_lives
        self.max_lives = initial_lives
    
    def lose_life(self):
        self.lives -= 1
        
    def has_lives(self):
        return self.lives > 0
    
    def get_lives(self):
        return self.lives
    
    def reset(self):
        self.lives = self.max_lives


class DifficultyManager:
    """Manages game difficulty and speed scaling"""
    def __init__(self, initial_multiplier=1.0, max_multiplier=4.0, increment=0.05, fruits_per_level=10):
        self.speed_multiplier = initial_multiplier
        self.max_multiplier = max_multiplier
        self.increment = increment
        self.fruits_per_level = fruits_per_level
        self.last_level = 0
    
    def increase_difficulty(self, fruits_sliced):
        if fruits_sliced % self.fruits_per_level == 0:
            self.speed_multiplier = min(self.max_multiplier, self.speed_multiplier + self.increment)
    
    def get_speed_multiplier(self):
        return self.speed_multiplier
    
    def get_current_level(self):
        return int((self.speed_multiplier - 1.0) / self.increment)
    
    def reset(self):
        self.speed_multiplier = 1.0
        self.last_level = 0


class GameState:
    """Manages the overall game state"""
    def __init__(self):
        self.game_over = False
        self.game_over_time = 0
        self.restart_delay = 2  # Seconds to wait before allowing restart
    
    def set_game_over(self):
        self.game_over = True
        self.game_over_time = time.time()
    
    def is_game_over(self):
        return self.game_over
    
    def can_restart(self):
        return time.time() - self.game_over_time >= self.restart_delay
    
    def reset(self):
        self.game_over = False
        self.game_over_time = 0


class FruitSpawner:
    """Manages the spawning of fruits"""
    def __init__(self, spawn_interval=70):  # Slightly faster spawn rate
        self.spawn_timer = 0
        self.spawn_interval = spawn_interval
    
    def update(self):
        self.spawn_timer += 1
        should_spawn = False
        
        if self.spawn_timer >= self.spawn_interval:
            should_spawn = True
            self.spawn_timer = 0
            
        return should_spawn
    
    def get_spawn_count(self):
        # Always spawn 1 fruit at a time to prevent clustering
        return 1
    
    def reset(self):
        self.spawn_timer = 0
