"""Rendering system for displaying game graphics."""

import pygame
from config import TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from map import (
    TILE_GRASS,
    TILE_WATER,
    TILE_MOUNTAIN,
    TILE_TREE,
    TILE_BUILDING,
    TILE_ROAD,
)


class Renderer:
    """Handles all game rendering."""

    def __init__(self, screen):
        """Initialize the renderer.

        Args:
            screen: Pygame display surface
        """
        self.screen = screen
        self.tile_colors = {
            TILE_GRASS: (34, 177, 76),  # Green
            TILE_WATER: (0, 119, 182),  # Blue
            TILE_MOUNTAIN: (128, 128, 128),  # Gray
            TILE_TREE: (0, 100, 0),  # Dark green
            TILE_BUILDING: (192, 192, 192),  # Light gray
            TILE_ROAD: (139, 69, 19),  # Brown
        }
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 16)

    def draw_map(self, game_map, camera_x, camera_y):
        """Draw the game map.

        Args:
            game_map: Map object to draw
            camera_x: Camera X position in tiles
            camera_y: Camera Y position in tiles
        """
        for y in range(20):
            for x in range(25):
                map_x = camera_x + x
                map_y = camera_y + y
                
                if 0 <= map_x < game_map.width and 0 <= map_y < game_map.height:
                    tile = game_map.get_tile(map_x, map_y)
                    color = self.tile_colors.get(tile, (255, 255, 255))
                    pygame.draw.rect(
                        self.screen,
                        color,
                        (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    )
                    pygame.draw.rect(
                        self.screen,
                        (0, 0, 0),
                        (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                        1,
                    )

    def draw_player(self, player_x, player_y):
        """Draw the player character.

        Args:
            player_x: Player X position in pixels (relative to screen)
            player_y: Player Y position in pixels (relative to screen)
        """
        # Draw simple pixel art player (red square with head)
        pygame.draw.rect(self.screen, (255, 0, 0), (player_x, player_y, TILE_SIZE, TILE_SIZE))
        pygame.draw.circle(self.screen, (255, 200, 0), (player_x + TILE_SIZE // 2, player_y + 8), 4)

    def draw_ui(self, player, pokemon=None):
        """Draw UI elements.

        Args:
            player: Player object
            pokemon: Current pokemon (optional)
        """
        # Draw money
        money_text = self.small_font.render(f"Money: ${player.get_money()}", True, (0, 0, 0))
        self.screen.blit(money_text, (10, 10))

        # Draw pokemon party size
        party_text = self.small_font.render(
            f"Pokemon: {len(player.get_party())}/6", True, (0, 0, 0)
        )
        self.screen.blit(party_text, (10, 30))

        # Draw current pokemon if in battle
        if pokemon:
            pokemon_info = self.small_font.render(
                f"{pokemon.name} - Lvl {pokemon.level}", True, (0, 0, 0)
            )
            self.screen.blit(pokemon_info, (WINDOW_WIDTH - 200, 10))

            hp_text = self.small_font.render(
                f"HP: {pokemon.current_hp}/{pokemon.max_hp}", True, (0, 0, 0)
            )
            self.screen.blit(hp_text, (WINDOW_WIDTH - 200, 30))

    def draw_text(self, text, x, y, color=(0, 0, 0), size="normal"):
        """Draw text on screen.

        Args:
            text: Text to draw
            x: X position
            y: Y position
            color: Text color
            size: Font size ("small" or "normal")
        """
        font = self.small_font if size == "small" else self.font
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_battle_screen(self, battle, selected_move=0):
        """Draw the battle screen.

        Args:
            battle: Battle object
            selected_move: Currently selected move index
        """
        # Draw background
        self.screen.fill((173, 216, 230))

        # Draw wild pokemon
        wild_pokemon = battle.wild_pokemon
        self.draw_text(f"{wild_pokemon.name} - Lvl {wild_pokemon.level}", 50, 50)
        self.draw_text(
            f"HP: {wild_pokemon.current_hp}/{wild_pokemon.max_hp}", 50, 80, size="small"
        )

        # Draw player pokemon
        player_pokemon = battle.player_pokemon
        self.draw_text(f"{player_pokemon.name} - Lvl {player_pokemon.level}", 600, 400)
        self.draw_text(
            f"HP: {player_pokemon.current_hp}/{player_pokemon.max_hp}",
            600,
            430,
            size="small",
        )

        # Draw moves
        self.draw_text("Moves:", 50, 350)
        for i, move in enumerate(player_pokemon.moves):
            color = (255, 0, 0) if i == selected_move else (0, 0, 0)
            self.draw_text(f"  {i + 1}. {move.name}", 50, 380 + (i * 25), color=color, size="small")

        # Draw options
        self.draw_text("Options: [1-4] Move | [C] Catch | [F] Flee", 50, 530, size="small")

        # Draw battle log
        log = battle.get_battle_log()
        if log:
            last_message = log[-1]
            self.draw_text(last_message, 50, 500, size="small")

    def clear_screen(self, color=(255, 255, 255)):
        """Clear the screen.

        Args:
            color: Color to fill with
        """
        self.screen.fill(color)