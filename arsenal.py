import pygame
from bullet import Bullet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Arsenal:
    """Manages the arsenal of bullets fired by the ship."""
    def __init__(self, game: 'AlienInvasion'):
        """Initialize an empty arsenal to hold the ship's bullets.

        Args:
            game: The AlienInvasion game instance.
        """
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()
    
    def update_arsenal(self):
        """Update the position of every bullet and remove any that leave the screen."""
        self.arsenal.update()
        self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self):
        """Remove bullets from the arsenal once the move past the top of the screen."""
        for bullet in self.arsenal.copy():
            if bullet.rect.bottom <= 0:
                self.arsenal.remove(bullet)

    def draw(self):
        """Draw every bullet in the arsenal to the screen."""
        for bullet in self.arsenal:
            bullet.draw_bullet()
    
    def fire_bullet(self):
        """Fire a new bullet if the arsenal has not reached capacity.

        Returns:
            bool: True if a bullet was fired, False if the arsenal is full.
        """
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False
