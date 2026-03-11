"""
Abstract base classes and interfaces for the game
"""
from abc import ABC, abstractmethod

# Renderer interface
class Renderer(ABC):
    @abstractmethod
    def render(self, screen):
        """Render the object to the screen"""
        pass


# GameObject interface
class GameObject(ABC):
    @abstractmethod
    def update(self):
        """Update the object state"""
        pass
    
    @abstractmethod
    def is_removable(self):
        """Check if the object should be removed from the game"""
        pass


# Sliceable interface
class Sliceable(ABC):
    @abstractmethod
    def check_slice(self, slice_points):
        """Check if the object is sliced by the given slice points"""
        pass
    
    @abstractmethod
    def is_sliced(self):
        """Check if the object has been sliced"""
        pass
