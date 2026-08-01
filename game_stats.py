from pathlib import Path
import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class GameStats():
    """Tracks stats for the game."""
    def __init__(self, game: 'AlienInvasion'):
        """Initialize game stats.

        Args:
            game: The AlienInvasion game instance.
        """
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self):
        """Load the saved high score or create a new file if none."""
        self.path = self.settings.scores_file
        if self.path.exists() and self.path.stat.__sizeof__() > 20:
            contents = self.path.read_text()
            scores = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)
        else:
            self.hi_score = 0
            self.save_scores()
            #save the file

    def save_scores(self):
        """Write the current high score to scores file as JSON."""
        scores = {
            'hi_score': self.hi_score
        }
        contents = json.dumps(scores, indent=4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f'File Not Found; {e}')


    def reset_stats(self):
        """Reset per-game stats to their starting values."""
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1

    def update(self, collisions):
        """Update score, max score, and high score after alien collisions.

        Args:
            collisions: A dictionary of collided alens mapped to the sprites they collided with.
        """
        # update score
        self._update_score(collisions)
        # update max_score
        self._update_max_score()
        # update hi_score
        self._update_hi_score()

    def _update_max_score(self):
        """Update the max score if the current score is higher."""
        if self.score > self.max_score:
            self.max_score = self.score
        #print(f'Max: {self.max_score}')

    def _update_hi_score(self):
            """Update the high score if the current score is higher."""
            if self.score > self.hi_score:
                self.hi_score = self.score
            #print(f'Hi: {self.hi_score}')

    def _update_score(self, collisions):
        """Increase the score based on the number of aliens destroyed.

        Args:
            collisions: A dictionary of collided alens mapped to the sprites they collided with.
        """
        for alien in collisions.values():
            self.score += self.settings.alien_points
        #print(f'Basic: {self.score}')

    def update_level(self):
        """Increment the level by one."""
        self.level +=1
        print(self.level)
