"""
Sprite management for loading and handling game sprites
"""
import pygame
import os
import random
from .constants import GameConstants

class SpriteManager:
    """Manages loading and accessing sprites from spritesheets"""
    
    def __init__(self):
        self.fruit_sprites = []
        self.sliced_fruit_sprites = []
        self.fruit_to_sliced_map = {}  # Maps fruit index to its specific sliced pair
        self.fruit_names = []  # Names of loaded fruits for reference
        self.load_sprites()
    
    def load_sprites(self):
        """Load all sprites from individual files"""
        try:
            # Load individual fruit images
            for fruit_name, fruit_data in GameConstants.FRUIT_IMAGES.items():
                # Skip magic bean
                if fruit_name == "magic_bean":
                    continue
                    
                # Load whole fruit
                whole_path = fruit_data["whole"]
                if os.path.exists(whole_path):
                    whole_image = pygame.image.load(whole_path).convert_alpha()
                    
                    # Special handling for frozen banana - make it smaller
                    if "FreezeBanana" in whole_path:
                        scaled_size = 70  # Smaller size for frozen banana
                    else:
                        # Scale to appropriate size if needed - reduced overall size
                        scaled_size = 80  # Further reduced from 100
                    
                    # Maintain aspect ratio
                    aspect_ratio = whole_image.get_width() / whole_image.get_height()
                    if aspect_ratio > 1:
                        new_width = scaled_size
                        new_height = int(scaled_size / aspect_ratio)
                    else:
                        new_width = int(scaled_size * aspect_ratio)
                        new_height = scaled_size
                    
                    whole_image = pygame.transform.smoothscale(whole_image, (new_width, new_height))
                    
                    # Add to fruit sprites
                    fruit_index = len(self.fruit_sprites)
                    self.fruit_sprites.append(whole_image)
                    self.fruit_names.append(fruit_name)
                    
                    # Load sliced fruit parts
                    sliced_images = []
                    for sliced_path in fruit_data["sliced"]:
                        if os.path.exists(sliced_path):
                            sliced_image = pygame.image.load(sliced_path).convert_alpha()
                            
                            # Special handling for banana slices - make them bigger
                            if "BananaTop" in sliced_path or "BananaBottom" in sliced_path:
                                scaled_size = 120  # Reduced from 150 but still larger than other fruits
                            elif "FreezeBanana" in sliced_path:
                                scaled_size = 70  # Smaller for frozen banana slices
                            else:
                                scaled_size = 80  # Reduced from 100
                            
                            # Maintain aspect ratio
                            aspect_ratio = sliced_image.get_width() / sliced_image.get_height()
                            if aspect_ratio > 1:
                                new_width = scaled_size
                                new_height = int(scaled_size / aspect_ratio)
                            else:
                                new_width = int(scaled_size * aspect_ratio)
                                new_height = scaled_size
                            
                            sliced_image = pygame.transform.smoothscale(sliced_image, (new_width, new_height))
                            sliced_images.append(sliced_image)
                    
                    # If we have at least one sliced image
                    if sliced_images:
                        # If we only have one sliced image, duplicate it for left and right halves
                        if len(sliced_images) == 1:
                            sliced_images.append(sliced_images[0])
                        
                        # Take the first two sliced images (in case there are more)
                        self.sliced_fruit_sprites.append((sliced_images[0], sliced_images[1]))
                        self.fruit_to_sliced_map[fruit_index] = fruit_index
            
            # If we couldn't load any fruits, fall back to the old method
            if not self.fruit_sprites:
                self._load_legacy_sprites()
            
            print(f"Loaded {len(self.fruit_sprites)} fruit sprites and {len(self.sliced_fruit_sprites)} sliced fruit pairs")
            print(f"Fruit types: {', '.join(self.fruit_names)}")
            
        except Exception as e:
            print(f"Error loading sprites: {e}")
            # Create fallback sprites if loading fails
            self._create_fallback_sprites()
    
    def _load_legacy_sprites(self):
        """Load sprites from spritesheets (legacy method)"""
        try:
            # Load whole fruit spritesheet
            whole_fruit_sheet = pygame.image.load(GameConstants.NEW_FRUITS_SPRITESHEET).convert_alpha()
            
            # Load sliced fruit spritesheet
            sliced_sheet = pygame.image.load(GameConstants.SLICED_FRUITS_SPRITESHEET).convert_alpha()
            
            # Extract whole fruits first
            fruit_width = whole_fruit_sheet.get_width() // 4  # Assuming 4 columns
            fruit_height = whole_fruit_sheet.get_height() // 4  # Assuming 4 rows
            
            # Extract all whole fruits
            for row in range(4):  # 4 rows
                for col in range(4):  # 4 columns
                    x = col * fruit_width
                    y = row * fruit_height
                    rect = pygame.Rect(x, y, fruit_width, fruit_height)
                    
                    # Extract the individual fruit
                    image = pygame.Surface((fruit_width, fruit_height), pygame.SRCALPHA)
                    image.blit(whole_fruit_sheet, (0, 0), rect)
                    
                    # Scale the image to a larger size for better visibility
                    scaled_size = 80  # Reduced from 100
                    scaled_image = pygame.transform.smoothscale(image, (scaled_size, scaled_size))
                    
                    # Check if the image has any non-transparent pixels
                    if pygame.mask.from_surface(scaled_image).count() > 100:  # Threshold to avoid empty sprites
                        self.fruit_sprites.append(scaled_image)
                        self.fruit_names.append(f"fruit_{len(self.fruit_sprites)}")
            
            # Now extract sliced fruit pairs
            sliced_width = 32  # Width of each sliced half
            sliced_height = 32  # Height of each sliced half
            
            sliced_sheet_width = sliced_sheet.get_width()
            sliced_sheet_height = sliced_sheet.get_height()
            
            # Calculate how many sliced fruit pairs we have
            cols = sliced_sheet_width // sliced_width
            rows = sliced_sheet_height // sliced_height
            
            # Extract each pair of sliced fruit halves
            for row in range(rows):
                for col in range(0, cols, 2):  # Step by 2 to get pairs
                    if col + 1 < cols:  # Make sure we have a pair
                        # Left half
                        left_x = col * sliced_width
                        left_y = row * sliced_height
                        left_rect = pygame.Rect(left_x, left_y, sliced_width, sliced_height)
                        left_image = pygame.Surface((sliced_width, sliced_height), pygame.SRCALPHA)
                        left_image.blit(sliced_sheet, (0, 0), left_rect)
                        
                        # Right half
                        right_x = (col + 1) * sliced_width
                        right_y = row * sliced_height
                        right_rect = pygame.Rect(right_x, right_y, sliced_width, sliced_height)
                        right_image = pygame.Surface((sliced_width, sliced_height), pygame.SRCALPHA)
                        right_image.blit(sliced_sheet, (0, 0), right_rect)
                        
                        # Scale the sliced pieces to match the larger fruit size
                        scaled_size = 80  # Reduced from 100
                        scaled_left = pygame.transform.smoothscale(left_image, (scaled_size, scaled_size))
                        scaled_right = pygame.transform.smoothscale(right_image, (scaled_size, scaled_size))
                        
                        self.sliced_fruit_sprites.append((scaled_left, scaled_right))
            
            # Create mappings between fruits and their sliced versions
            for i in range(len(self.fruit_sprites)):
                if i < len(self.sliced_fruit_sprites):
                    self.fruit_to_sliced_map[i] = i
                else:
                    # If we have more fruits than sliced pairs, cycle through available pairs
                    self.fruit_to_sliced_map[i] = i % len(self.sliced_fruit_sprites)
                    
        except Exception as e:
            print(f"Error loading legacy sprites: {e}")
            self._create_fallback_sprites()
    
    def _create_fallback_sprites(self):
        """Create simple colored circles as fallback sprites"""
        self.fruit_sprites = []
        self.sliced_fruit_sprites = []
        self.fruit_to_sliced_map = {}
        self.fruit_names = []
        
        # Create 8 colored fruit sprites
        for i, color in enumerate(GameConstants.FRUIT_COLORS):
            size = 80  # Reduced from 100
            image = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(image, color, (size//2, size//2), size//2 - 2)
            self.fruit_sprites.append(image)
            self.fruit_names.append(f"color_{i}")
            
            # Create matching sliced fruit pair - same size as whole fruit
            left_half = pygame.Surface((size, size), pygame.SRCALPHA)
            right_half = pygame.Surface((size, size), pygame.SRCALPHA)
            
            # Draw left half circle
            pygame.draw.circle(left_half, color, (size//2, size//2), size//2 - 2)
            # Make right side transparent
            mask = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.rect(mask, (255, 255, 255), (size//2, 0, size//2, size))
            left_half.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            # Draw right half circle
            pygame.draw.circle(right_half, color, (size//2, size//2), size//2 - 2)
            # Make left side transparent
            mask = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.rect(mask, (255, 255, 255), (0, 0, size//2, size))
            right_half.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            self.sliced_fruit_sprites.append((left_half, right_half))
            self.fruit_to_sliced_map[i] = i
    
    def get_random_fruit_sprite(self):
        """Get a random fruit sprite"""
        if not self.fruit_sprites:
            return None
        index = random.randint(0, len(self.fruit_sprites) - 1)
        return self.fruit_sprites[index], index
    
    def get_matching_sliced_sprite(self, fruit_index):
        """Get the matching sliced sprite pair for a fruit index"""
        if not self.sliced_fruit_sprites:
            return None
            
        # Use the mapping to get the correct sliced pair
        if fruit_index in self.fruit_to_sliced_map:
            sliced_index = self.fruit_to_sliced_map[fruit_index]
            if sliced_index < len(self.sliced_fruit_sprites):
                return self.sliced_fruit_sprites[sliced_index]
        
        # Fallback to the first sliced pair if no mapping exists
        return self.sliced_fruit_sprites[0] if self.sliced_fruit_sprites else None
    
    def get_fruit_count(self):
        """Get the number of available fruit sprites"""
        return len(self.fruit_sprites)
