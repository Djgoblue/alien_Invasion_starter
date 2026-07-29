import pygame
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class AlienFleet:
    """Manages the group of Alien sprites, including their layout and movement."""
    def __init__(self, game: 'AlienInvasion'):
        """Initalize the fleet and build the initial formation of aliens.

        Args:
            game: The AlienInvasion game instance.
        """
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed

        self.create_fleet()

    def create_fleet(self):
        """Calculate the fleet's size and offsets, then build the fleet."""
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h

        fleet_w, fleet_h = self.calculate_fleet_size(alien_w, screen_w, alien_h, screen_h)
        x_offset, y_offset = self.caclulate_offsets(alien_w, alien_h, screen_w, fleet_w, fleet_h)
         
        self._create_rectangle_fleet(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)

    def _create_rectangle_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
        """Create aliens in a rectangular grid pattern, skipping every other row/column.

        Args:
            alien_w: Width of an alien in pixels.
            alien_h: Height of an alien in pixels.
            fleet_w: Number of columns in the fleet grid.
            fleet_h: Number of rows in the fleet grid.
            x_offset: Horizontal pixel offset used to position the fleet.
            y_offset: Vertical pixel offset used to position the fleet.
        """
        for row in range(fleet_h):
            for col in range(fleet_w):
                current_x = alien_w * col + x_offset
                current_y = alien_h * row + y_offset
                if col % 2 == 0 or row % 2 == 0:
                    continue
                self._create_alien(current_x, current_y)

    def caclulate_offsets(self, alien_w, alien_h, screen_w, fleet_w, fleet_h):
        """Calculate the x/y offsets used to position the fleet on the screen.

        Args:
            alien_w: Width of an alien in pixels.
            alien_h: Height of an alien in pixels.
            fleet_w: Number of columns in the fleet grid.
            fleet_h: Number of rows in the fleet grid.

        Returns:
            tuple[int, int]: The (x_offset, y_offset) to use when placing aliens.
        """
        half_screen = self.settings.screen_h//2
        fleet_horizontal_space = fleet_w * alien_w
        fleet_vertical_space = fleet_h * alien_h
        x_offset = int((screen_w-fleet_horizontal_space)//2)
        y_offset = int((half_screen-fleet_vertical_space)//2)
        return x_offset,y_offset


    def calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h):
        """Calculate how many columns and rows of aliens fit in the fleet.

        Args:
            alien_w: Width of an alien in pixels.
            screen_w: Width of the game screen in pixels.
            alien_h: Height of an alien in pixels.
            screen_h: Height of the game screen in pixels.

        Returns:
            tuple[int, int]: The (fleet_w, fleet_h) colum and row counts.
        """
        fleet_w = (screen_w//alien_w)
        fleet_h = ((screen_h /2)//alien_h)

        if fleet_w % 2 == 0:
            fleet_w -=1
        else:
            fleet_w -= 2
        
        if fleet_h % 2 == 0:
            fleet_h -=1
        else:
            fleet_h -= 2


        return int(fleet_w), int(fleet_h)


    def _create_alien(self, current_x: int, current_y: int):
        """Create a single Alien at the given position and add it to the fleet.

        Args:
            current_x: The x-coordinate for the alien.
            current_y: The y-coordinate for the alien.
        """
        new_alien = Alien(self, current_x, current_y)

        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        """Check if any alien has reached a screen edge, if so, drop and reverse the direction of the fleet."""
        alien: Alien 
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break


    def _drop_alien_fleet(self):
        """Move every alien in the fleet down by the set drop speed"""
        for alien in self.fleet:
            alien.y += self.fleet_drop_speed


    def update_fleet(self):
        """Check the fleet's edges and direction and update the position of every alien."""
        self._check_fleet_edges()
        self.fleet.update()


    def draw(self):
        """Draw every alien in the fleet to the screen."""
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()

    def check_collisions(self, other_group):
        """Check for collisions between the fleet and another sprite group.

        Args:
            other_group: The sprite group to check collisions against

        Returns:
            dict: A map of collided aliens to the sprites they collided with.
        """
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)
    
    def check_fleet_bottom(self):
        """Check whether an alien has reach the bottom of the screen.

        Returns:
            bool: True if the alien has reached the bottom of the screen.
        """
        alien: Alien
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True
            return False
        
    def check_destroyed_status(self):
        """Check whether the entire fleet has been destroyed.

        Returns:
            bool: True if there are no aliens left in the fleet.
        """
        return not self.fleet