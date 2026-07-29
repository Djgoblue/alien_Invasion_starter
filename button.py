import pygame.font

from typing import TYPE_CHECKING

if TYPE_CHECKING:
        from alien_invasion import AlienInvasion

class Button:
    """A clickable rectangular button with text."""
    def __init__(self, game: 'AlienInvasion', msg): 
        """Create a button and text.

        Args:
            game: The AlienInvasion game instance.
            msg: The text to display on button.
        """
        self.game = game
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.settings = game.settings
        self.font = pygame.font.Font(self.settings.font_file,
            self.settings.button_font_size)
        self. rect = pygame.Rect(0,0, self.settings.button_w, self.settings.button_h)
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Create the text and center it within the button.

        Args:
            msg: The text to display on button.
        """
        self.msg_image = self.font.render(msg, True, self.settings.text_color, None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        """Draw the button's background and text to the screen."""
        self.screen.fill(self.settings.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_clicked(self, mouse_pos):
        """Check whether the button has been pressed.

        Args:
            mouse_pos: An (x,y) tuple representing the mouse click position.

        Returns:
            bool: True if the position is inside the button's shape.
        """
        return self.rect.collidepoint(mouse_pos)
        