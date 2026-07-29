import pygame
from typing import TYPE_CHECKING
from arsenal import Arsenal

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Ship:
    """THe play controlled ship, which can move horizontally and fire bullets."""
    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal'):
        """Intialize the ship's image, position, and arsenal.

        Args:
            game: The AlienInvasion game instance
            arsenal: The Arsenal instance used to manage the ship's bullets.
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.ship_w, self.settings.ship_h)
            )
        
        self.rect = self.image.get_rect()
        self._center_ship()
        self.moving_right = False
        self.moving_left = False
        
        self.arsenal = arsenal

    def _center_ship(self):
        """Reposition the ship to the horizontal center at the bottom of the screen."""
        self.rect.midbottom = self.boundaries.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """Update the ship's movement and its arsenal."""
        #Update the position of the ship
        self._update_ship_movement()
        self.arsenal.update_arsenal()
        
    def _update_ship_movement(self):
        """Move the ship left or right based on input, staying within the screen boundaries."""
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def draw(self):
        """Draw the ship at its current position."""
        self.screen.blit(self.image, self.rect)

    def fire(self):
        """Attempt to fire a bullet from the arsenal.

        Returns:
            bool: True if a bullet was fired successfully.
        """
        return self.arsenal.fire_bullet()
    
    def check_collisions(self, other_group):
        """Check for a collision between the ship and a sprite group, recentering on hit.

        Args:
            other_group: THe sprite group to check collisions against

        Returns:
            bool: True if the ship collided with any sprite in the group.
        """
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False