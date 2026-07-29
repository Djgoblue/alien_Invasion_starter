import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien(Sprite):
    """An alien enemy sprite that moves as part of an alien fleet"""

    def __init__(self, fleet: 'AlienFleet', x: float, y: float):
        """Initialize an alien at the given position and load its image.

        Args:
            fleet: The AlienFleet instance the alien belongs to.
            x: The starting x coordinate for the alien.
            y: The starting y coordinate for the alien.
        """
        super().__init__()
        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings
        
        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.alien_w, self.settings.alien_h)
            )
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Update the alien's position based on the fleet's speed and direction."""
        temp_speed = self.settings.fleet_speed  
            
        self.x += temp_speed * self.fleet.fleet_direction
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self):
        """Check if the alien has reached the left or right screen boundary.

        Returns:
            bool: True if alien touches or passes either screen edge.
        """
        return (self.rect.right >= self.boundaries.right or self.rect.left <= self.boundaries.left)
    
    def draw_alien(self):
        """Draw the alien's image at its current position on the screen."""
        self.screen.blit(self.image, self.rect)