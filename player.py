"""Player class for character movement and interaction."""

from config import (
    PLAYER_SPEED,
    PLAYER_SPRITE_WIDTH,
    PLAYER_SPRITE_HEIGHT,
    START_X,
    START_Y,
    TILE_SIZE,
    MAP_WIDTH,
    MAP_HEIGHT,
)


class Player:
    """Represents the player character in the game."""

    def __init__(self, x=START_X, y=START_Y):
        """Initialize the player.

        Args:
            x: Starting x position in tiles
            y: Starting y position in tiles
        """
        self.x = x
        self.y = y
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.speed = PLAYER_SPEED
        self.direction = "down"  # down, up, left, right
        self.pokemon_party = []  # List of Pokemon in party
        self.inventory = {}  # Items in inventory
        self.money = 0
        self.badges = 0  # Gym badges earned

    def move_up(self):
        """Move the player up."""
        if self.y > 0:
            self.y -= 1
            self.pixel_y = self.y * TILE_SIZE
            self.direction = "up"

    def move_down(self):
        """Move the player down."""
        if self.y < MAP_HEIGHT - 1:
            self.y += 1
            self.pixel_y = self.y * TILE_SIZE
            self.direction = "down"

    def move_left(self):
        """Move the player left."""
        if self.x > 0:
            self.x -= 1
            self.pixel_x = self.x * TILE_SIZE
            self.direction = "left"

    def move_right(self):
        """Move the player right."""
        if self.x < MAP_WIDTH - 1:
            self.x += 1
            self.pixel_x = self.x * TILE_SIZE
            self.direction = "right"

    def get_position(self):
        """Get the player's current tile position.

        Returns:
            Tuple of (x, y) tile coordinates
        """
        return (self.x, self.y)

    def get_pixel_position(self):
        """Get the player's pixel position.

        Returns:
            Tuple of (pixel_x, pixel_y) coordinates
        """
        return (self.pixel_x, self.pixel_y)

    def add_pokemon(self, pokemon):
        """Add a pokemon to the player's party.

        Args:
            pokemon: Pokemon object to add

        Returns:
            Boolean indicating success (False if party is full)
        """
        if len(self.pokemon_party) < 6:
            self.pokemon_party.append(pokemon)
            return True
        return False

    def remove_pokemon(self, pokemon):
        """Remove a pokemon from the player's party.

        Args:
            pokemon: Pokemon object to remove
        """
        if pokemon in self.pokemon_party:
            self.pokemon_party.remove(pokemon)

    def get_party(self):
        """Get the player's pokemon party.

        Returns:
            List of Pokemon objects
        """
        return self.pokemon_party

    def add_money(self, amount):
        """Add money to the player's funds.

        Args:
            amount: Amount of money to add
        """
        self.money += amount

    def spend_money(self, amount):
        """Spend money from the player's funds.

        Args:
            amount: Amount of money to spend

        Returns:
            Boolean indicating if transaction was successful
        """
        if self.money >= amount:
            self.money -= amount
            return True
        return False

    def get_money(self):
        """Get the player's current money.

        Returns:
            Current money amount
        """
        return self.money

    def __str__(self):
        """Return string representation of the player."""
        return f"Player at ({self.x}, {self.y}) with {len(self.pokemon_party)} pokemon"
