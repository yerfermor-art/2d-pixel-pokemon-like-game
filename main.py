"""Main game loop and entry point."""

import pygame
import sys
import random
from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    FPS,
    TILE_SIZE,
    MAP_WIDTH,
    MAP_HEIGHT,
)
from player import Player
from map import Map
from pokemon import Pokemon, TYPE_NORMAL, TYPE_FIRE, TYPE_WATER, TYPE_GRASS
from move import Move
from battle import Battle
from renderer import Renderer


class Game:
    """Main game class."""

    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = FPS

        # Initialize game objects
        self.player = Player()
        self.game_map = Map()
        self.renderer = Renderer(self.screen)
        self.battle = None
        self.in_battle = False

        # Initialize player's starting pokemon
        self._init_starter_pokemon()

    def _init_starter_pokemon(self):
        """Initialize starter pokemon for the player."""
        # Create starter pokemon
        starters = [
            ("Bulbasaur", TYPE_GRASS, 5, 45, 49, 49, 45),
            ("Charmander", TYPE_FIRE, 5, 39, 52, 43, 60),
            ("Squirtle", TYPE_WATER, 5, 44, 48, 65, 43),
        ]

        name, ptype, level, hp, attack, defense, speed = random.choice(starters)
        starter = Pokemon(name, ptype, level, hp, attack, defense, speed)

        # Add starter moves
        starter.add_move(Move("Tackle", TYPE_NORMAL, 40, 100))
        starter.add_move(Move("Growl", TYPE_NORMAL, 0, 100))

        self.player.add_pokemon(starter)
        self.player.add_money(100)

    def handle_events(self):
        """Handle input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.in_battle:
                    self._handle_battle_input(event.key)
                else:
                    self._handle_exploration_input(event.key)

    def _handle_exploration_input(self, key):
        """Handle input during exploration.

        Args:
            key: Pygame key constant
        """
        if key == pygame.K_UP or key == pygame.K_w:
            self.player.move_up()
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.player.move_down()
        elif key == pygame.K_LEFT or key == pygame.K_a:
            self.player.move_left()
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.player.move_right()

    def _handle_battle_input(self, key):
        """Handle input during battle.

        Args:
            key: Pygame key constant
        """
        if key == pygame.K_1:
            self.battle.player_turn(0)
        elif key == pygame.K_2:
            self.battle.player_turn(1)
        elif key == pygame.K_3:
            self.battle.player_turn(2)
        elif key == pygame.K_4:
            self.battle.player_turn(3)
        elif key == pygame.K_c:
            self.battle.player_catch()
        elif key == pygame.K_f:
            self.battle.player_flee()

        if self.battle.is_finished:
            self.in_battle = False
            self.battle = None

    def update(self):
        """Update game state."""
        if not self.in_battle:
            # Check for pokemon encounter
            if random.random() < 0.01:  # Low encounter chance per frame
                self._start_encounter()

    def _start_encounter(self):
        """Start a random pokemon encounter."""
        if not self.player.get_party():
            return

        # Create random wild pokemon
        wild_pokemon_data = [
            ("Pidgeot", TYPE_NORMAL, 3, 40, 50, 40, 35),
            ("Bulbasaur", TYPE_GRASS, 3, 45, 49, 49, 45),
            ("Charmander", TYPE_FIRE, 3, 39, 52, 43, 60),
        ]

        name, ptype, level, hp, attack, defense, speed = random.choice(wild_pokemon_data)
        wild_pokemon = Pokemon(name, ptype, level, hp, attack, defense, speed)
        wild_pokemon.add_move(Move("Tackle", TYPE_NORMAL, 40, 100))

        # Start battle
        player_pokemon = self.player.get_party()[0]
        self.battle = Battle(player_pokemon, wild_pokemon)
        self.in_battle = True

    def render(self):
        """Render the game."""
        self.renderer.clear_screen()

        if self.in_battle:
            self.renderer.draw_battle_screen(self.battle)
        else:
            # Calculate camera position
            camera_x = max(0, min(self.player.x - 12, MAP_WIDTH - 25))
            camera_y = max(0, min(self.player.y - 9, MAP_HEIGHT - 18))

            # Draw map
            self.renderer.draw_map(self.game_map, camera_x, camera_y)

            # Draw player
            player_screen_x = (self.player.x - camera_x) * TILE_SIZE
            player_screen_y = (self.player.y - camera_y) * TILE_SIZE
            self.renderer.draw_player(player_screen_x, player_screen_y)

            # Draw UI
            self.renderer.draw_ui(self.player)

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()