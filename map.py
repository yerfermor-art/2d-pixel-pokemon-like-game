"""Map class for world generation and tile management."""

import random
from config import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE

# Tile types
TILE_GRASS = 0
TILE_WATER = 1
TILE_MOUNTAIN = 2
TILE_TREE = 3
TILE_BUILDING = 4
TILE_ROAD = 5

# Tile properties
TILE_PROPERTIES = {
    TILE_GRASS: {"name": "Grass", "walkable": True, "encounter_rate": 0.3},
    TILE_WATER: {"name": "Water", "walkable": False, "encounter_rate": 0.0},
    TILE_MOUNTAIN: {"name": "Mountain", "walkable": False, "encounter_rate": 0.0},
    TILE_TREE: {"name": "Tree", "walkable": False, "encounter_rate": 0.0},
    TILE_BUILDING: {"name": "Building", "walkable": False, "encounter_rate": 0.0},
    TILE_ROAD: {"name": "Road", "walkable": True, "encounter_rate": 0.0},
}


class Map:
    """Represents the game world map."""

    def __init__(self, width=MAP_WIDTH, height=MAP_HEIGHT):
        """Initialize the map.

        Args:
            width: Map width in tiles
            height: Map height in tiles
        """
        self.width = width
        self.height = height
        self.tiles = [[TILE_GRASS for _ in range(width)] for _ in range(height)]
        self.generate_world()

    def generate_world(self):
        """Generate a basic world layout using simple procedural generation."""
        # Create water bodies
        for _ in range(3):
            water_x = random.randint(0, self.width - 5)
            water_y = random.randint(0, self.height - 5)
            self._create_water_body(water_x, water_y, random.randint(3, 7))

        # Create mountains
        for _ in range(2):
            mountain_x = random.randint(0, self.width - 3)
            mountain_y = random.randint(0, self.height - 3)
            self._create_mountain_range(mountain_x, mountain_y, random.randint(2, 5))

        # Create roads
        self._create_road_h(1)  # Horizontal road
        self._create_road_v(5)  # Vertical road

        # Add some buildings/towns
        self.tiles[2][2] = TILE_BUILDING
        self.tiles[2][3] = TILE_BUILDING
        self.tiles[3][2] = TILE_BUILDING

    def _create_water_body(self, start_x, start_y, size):
        """Create a water body on the map.

        Args:
            start_x: Starting x position
            start_y: Starting y position
            size: Size of water body
        """
        for x in range(start_x, min(start_x + size, self.width)):
            for y in range(start_y, min(start_y + size, self.height)):
                if random.random() < 0.8:  # 80% chance to place water
                    self.tiles[y][x] = TILE_WATER

    def _create_mountain_range(self, start_x, start_y, size):
        """Create a mountain range on the map.

        Args:
            start_x: Starting x position
            start_y: Starting y position
            size: Size of mountain range
        """
        for x in range(start_x, min(start_x + size, self.width)):
            for y in range(start_y, min(start_y + size, self.height)):
                if random.random() < 0.7:  # 70% chance to place mountain
                    self.tiles[y][x] = TILE_MOUNTAIN

    def _create_road_h(self, y):
        """Create a horizontal road.

        Args:
            y: Y position of the road
        """
        for x in range(self.width):
            if self.tiles[y][x] not in [TILE_WATER, TILE_MOUNTAIN]:
                self.tiles[y][x] = TILE_ROAD

    def _create_road_v(self, x):
        """Create a vertical road.

        Args:
            x: X position of the road
        """
        for y in range(self.height):
            if self.tiles[y][x] not in [TILE_WATER, TILE_MOUNTAIN]:
                self.tiles[y][x] = TILE_ROAD

    def get_tile(self, x, y):
        """Get the tile type at a position.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Tile type constant
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return TILE_MOUNTAIN  # Out of bounds is treated as impassable

    def set_tile(self, x, y, tile_type):
        """Set the tile type at a position.

        Args:
            x: X coordinate
            y: Y coordinate
            tile_type: Tile type constant to set
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = tile_type

    def is_walkable(self, x, y):
        """Check if a tile is walkable.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Boolean indicating if tile is walkable
        """
        tile = self.get_tile(x, y)
        return TILE_PROPERTIES[tile]["walkable"]

    def get_encounter_rate(self, x, y):
        """Get the pokemon encounter rate for a tile.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Encounter rate as a decimal
        """
        tile = self.get_tile(x, y)
        return TILE_PROPERTIES[tile]["encounter_rate"]

    def get_tile_name(self, tile_type):
        """Get the name of a tile type.

        Args:
            tile_type: Tile type constant

        Returns:
            Name of the tile type
        """
        return TILE_PROPERTIES[tile_type]["name"]

    def __str__(self):
        """Return string representation of the map."""
        return f"Map {self.width}x{self.height}"
