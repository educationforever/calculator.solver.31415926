"""
Input handling for the game
"""
import pygame
from pygame.locals import *

class InputHandler:
    """Handles user input"""
    def __init__(self):
        self.slicing = False
        self.slice_points = []
        self.max_slice_points = 15  # Reduced from 25 for faster disappearance
    
    def is_slicing(self):
        """Check if the player is currently slicing"""
        return self.slicing and len(self.slice_points) > 0
    
    def get_slice_points(self):
        """Get the current slice path points"""
        return self.slice_points
    
    def handle_event(self, event, game_state):
        """
        Process a pygame event
        Returns: 
        - True to continue the game
        - False to quit
        - "RESET" to reset the game
        - "HOME" to return to home screen
        """
        if event.type == QUIT:
            return False
        
        elif event.type == KEYDOWN:
            if event.key == K_r and game_state.is_game_over():
                # Only allow restart after delay
                if game_state.can_restart():
                    return "RESET"  # Signal to reset the game
            elif event.key == K_ESCAPE:
                return "HOME"  # Return to home screen
            elif event.key == K_p:
                return "PAUSE"  # Toggle pause
        
        elif event.type == MOUSEBUTTONDOWN:
            # Start slicing
            self.slicing = True
            self.slice_points = [pygame.mouse.get_pos()]
        
        elif event.type == MOUSEBUTTONUP:
            # End slicing
            self.slicing = False
            self.slice_points = []
        
        elif event.type == MOUSEMOTION and self.slicing:
            # Add point to slice path
            self.slice_points.append(pygame.mouse.get_pos())
            # Keep only the last N points for performance and to create a trailing effect
            if len(self.slice_points) > self.max_slice_points:
                self.slice_points = self.slice_points[-self.max_slice_points:]
        
        return True
