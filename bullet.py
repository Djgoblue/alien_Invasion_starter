import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Bullet(Sprite):
    """A single bullet fired from the ship, moving upward until it leaves the screen."""
    def __init__(self, game: 'AlienInvasion'):
        """Create a bullet position at the top of the ship.

        Args:
            game: The AlienInvasion game instance.
        """
        super().__init__()

        self.screen = game.screen
        self.settings = game.settings
        
        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image, (self.settings.bullet_w, self.settings.bullet_h))
        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet upward based on the set speed"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
    
    def draw_bullet(self):
        """Draw the bullet at its current position."""
        self.screen.blit(self.image, self.rect)