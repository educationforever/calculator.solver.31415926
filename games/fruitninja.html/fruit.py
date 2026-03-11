"""
Fruit classes and factory
"""
import random
import pygame
from .constants import GameConstants
from .interfaces import GameObject, Sliceable, Renderer
from .utils import CollisionDetector

class BaseFruit(GameObject, Sliceable, Renderer):
    """Base class for all fruit types"""
    def __init__(self, x, y, vx, vy, radius, sprite=None, sprite_index=0, sliced_sprites=None, points=10, is_special=False):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.gravity = 0.15
        self._sliced = False
        self._remove = False
        
        # Sprite properties
        self.sprite = sprite
        self.sprite_index = sprite_index
        self.sliced_sprites = sliced_sprites
        
        # Point value and special status
        self.points = points
        self.is_special = is_special
        
        # Slice pieces properties (initialized when sliced)
        self.left_piece_x = 0
        self.left_piece_y = 0
        self.right_piece_x = 0
        self.right_piece_y = 0
        self.left_vx = 0
        self.left_vy = 0
        self.right_vx = 0
        self.right_vy = 0
        
        # Rotation properties
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)
        self.left_rotation = 0
        self.right_rotation = 0
        self.left_rotation_speed = 0
        self.right_rotation_speed = 0
    
    def update(self):
        if not self._sliced:
            # Apply gravity to vertical velocity
            self.vy += self.gravity
            
            # Update position
            self.x += self.vx
            self.y += self.vy
            
            # Update rotation
            self.rotation += self.rotation_speed
            
            # Get current screen dimensions
            screen_width, screen_height = pygame.display.get_surface().get_size()
            
            # Bounce off walls with energy preservation
            if self.x < self.radius:
                self.x = self.radius
                self.vx = abs(self.vx) * 0.9
            elif self.x > screen_width - self.radius:
                self.x = screen_width - self.radius
                self.vx = -abs(self.vx) * 0.9
            
            # Mark for removal if it falls off screen
            if self.y > screen_height + self.radius and self.vy > 0:
                self._remove = True
        else:
            # Update sliced pieces
            # Left piece
            self.left_vy += self.gravity
            self.left_piece_x += self.left_vx
            self.left_piece_y += self.left_vy
            self.left_rotation += self.left_rotation_speed
            
            # Right piece
            self.right_vy += self.gravity
            self.right_piece_x += self.right_vx
            self.right_piece_y += self.right_vy
            self.right_rotation += self.right_rotation_speed
            
            # Get current screen dimensions
            screen_width, screen_height = pygame.display.get_surface().get_size()
            
            # Mark for removal if both pieces fall off screen
            if (self.left_piece_y > screen_height + self.radius and 
                self.right_piece_y > screen_height + self.radius):
                self._remove = True
    
    def is_removable(self):
        return self._remove
    
    def is_sliced(self):
        return self._sliced
    
    def get_points(self):
        """Get the point value of this fruit"""
        return self.points
    
    def is_special_fruit(self):
        """Check if this is a special fruit"""
        return self.is_special
    
    def check_slice(self, slice_points):
        if self._sliced:
            return False
            
        # Check if any line segment of the slice intersects the fruit
        for i in range(len(slice_points) - 1):
            p1 = slice_points[i]
            p2 = slice_points[i + 1]
            
            # Simple distance-based collision detection
            distance = CollisionDetector.point_to_line_distance(
                self.x, self.y, p1[0], p1[1], p2[0], p2[1]
            )
            if distance < self.radius:
                self._sliced = True
                
                # Calculate slice direction vector
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                
                # Normalize the vector
                length = (dx**2 + dy**2)**0.5
                if length > 0:
                    dx /= length
                    dy /= length
                
                # Initialize slice pieces with positions and velocities
                # Position them further apart for larger slices
                self.left_piece_x = self.x - 15
                self.left_piece_y = self.y
                self.right_piece_x = self.x + 15
                self.right_piece_y = self.y
                
                # Set velocities for pieces based on slice direction and original velocity
                slice_force = 4.0  # Increased force for better separation
                self.left_vx = self.vx - dy * slice_force
                self.left_vy = self.vy + dx * slice_force
                self.right_vx = self.vx + dy * slice_force
                self.right_vy = self.vy - dx * slice_force
                
                # Set rotation speeds for the pieces
                self.left_rotation_speed = random.uniform(-5, -2)
                self.right_rotation_speed = random.uniform(2, 5)
                
                return True
        
        return False


class SpriteFruit(BaseFruit):
    """Fruit implementation using sprites"""
    def render(self, screen):
        if not self.sprite:
            # Fallback to colored circle if no sprite
            if not self._sliced:
                pygame.draw.circle(screen, GameConstants.RED, (int(self.x), int(self.y)), self.radius)
            else:
                pygame.draw.circle(screen, GameConstants.RED, (int(self.left_piece_x), int(self.left_piece_y)), self.radius // 2)
                pygame.draw.circle(screen, GameConstants.RED, (int(self.right_piece_x), int(self.right_piece_y)), self.radius // 2)
            return
            
        if not self._sliced:
            # Draw whole fruit sprite with rotation
            rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
            sprite_rect = rotated_sprite.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(rotated_sprite, sprite_rect)
        else:
            # Draw sliced fruit sprites
            if self.sliced_sprites and len(self.sliced_sprites) == 2:
                left_half, right_half = self.sliced_sprites
                
                # Make sure we have valid surfaces
                if left_half and right_half:
                    try:
                        # Rotate the sliced pieces
                        rotated_left = pygame.transform.rotate(left_half, self.left_rotation)
                        rotated_right = pygame.transform.rotate(right_half, self.right_rotation)
                        
                        # Draw the sliced pieces - using the same size as the original fruit
                        left_rect = rotated_left.get_rect(center=(int(self.left_piece_x), int(self.left_piece_y)))
                        right_rect = rotated_right.get_rect(center=(int(self.right_piece_x), int(self.right_piece_y)))
                        
                        screen.blit(rotated_left, left_rect)
                        screen.blit(rotated_right, right_rect)
                    except Exception as e:
                        print(f"Error rendering sliced fruit: {e}")
                        self._render_fallback_slices(screen)
                else:
                    # Fallback if sliced sprites are invalid
                    self._render_fallback_slices(screen)
            else:
                # Fallback if sliced sprites aren't available
                self._render_fallback_slices(screen)
    
    def _render_fallback_slices(self, screen):
        """Render fallback sliced pieces if the proper sprites aren't available"""
        # Use the original fruit color for the fallback slices
        color = GameConstants.RED
        if self.sprite:
            # Try to get the dominant color from the sprite
            try:
                # Get center pixel color as a fallback
                center_x = self.sprite.get_width() // 2
                center_y = self.sprite.get_height() // 2
                color = self.sprite.get_at((center_x, center_y))
            except:
                pass
        
        half_radius = self.radius // 2
        pygame.draw.circle(screen, color, (int(self.left_piece_x), int(self.left_piece_y)), half_radius)
        pygame.draw.circle(screen, color, (int(self.right_piece_x), int(self.right_piece_y)), half_radius)


class FruitFactory:
    """Factory for creating different types of fruits"""
    def __init__(self, sprite_manager):
        self.sprite_manager = sprite_manager
        self.special_fruit_chance = 0.05  # 5% chance for special fruit (frozen banana)
    
    def create_fruit(self, speed_multiplier=1.0, current_level=1):
        radius = random.randint(35, 45)  # Further reduced radius from previous 40-50
        
        # Determine if this should be a special fruit (frozen banana)
        is_special = random.random() < self.special_fruit_chance
        
        # Get a random fruit sprite and its index, or specifically get the frozen banana
        if is_special:
            # Find the frozen banana in the sprite manager
            frozen_banana_index = None
            for i, name in enumerate(self.sprite_manager.fruit_names):
                if name == "freeze_banana":
                    frozen_banana_index = i
                    break
            
            if frozen_banana_index is not None:
                sprite = self.sprite_manager.fruit_sprites[frozen_banana_index]
                sprite_index = frozen_banana_index
            else:
                # If frozen banana not found, get a random fruit
                is_special = False
                sprite, sprite_index = self.sprite_manager.get_random_fruit_sprite()
        else:
            # Get a random regular fruit
            sprite, sprite_index = self.sprite_manager.get_random_fruit_sprite()
        
        sliced_sprites = self.sprite_manager.get_matching_sliced_sprite(sprite_index)
        
        # Get current screen dimensions
        screen_width, screen_height = pygame.display.get_surface().get_size()
        
        # Spawn fruits at random positions along the width
        x = random.randint(radius, screen_width - radius)
        
        # Random spawn height between bottom and middle of screen
        spawn_height = random.randint(screen_height // 2, screen_height)
        y = spawn_height
        
        # Initial velocities - reduce for first 3 levels
        base_speed = speed_multiplier
        if current_level <= 3:
            base_speed *= 0.8  # 20% slower for first 3 levels
        
        vx = random.uniform(-1.5, 1.5) * base_speed
        vy = random.uniform(-8, -6) * base_speed
        
        # Calculate points based on level and special status
        points = 10  # Base points
        
        # Increase points based on level
        if current_level > 1:
            points += (current_level - 1) * 5  # +5 points per level above 1
        
        # Double points for special fruits
        if is_special:
            points *= 2
        
        # Create a new fruit with the whole fruit sprite
        return SpriteFruit(x, y, vx, vy, radius, sprite, sprite_index, sliced_sprites, points, is_special)
