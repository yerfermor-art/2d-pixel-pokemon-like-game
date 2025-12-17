"""Pokemon class for creatures and battle mechanics."""

from config import (
    MAX_POKEMON_PARTY,
    BASE_HP,
    BASE_ATTACK,
    BASE_DEFENSE,
    BASE_SPEED,
    EXP_TO_LEVEL_UP,
)

# Pokemon types
TYPE_NORMAL = "normal"
TYPE_FIRE = "fire"
TYPE_WATER = "water"
TYPE_GRASS = "grass"
TYPE_ELECTRIC = "electric"
TYPE_ICE = "ice"
TYPE_FIGHTING = "fighting"
TYPE_POISON = "poison"
TYPE_GROUND = "ground"
TYPE_FLYING = "flying"
TYPE_PSYCHIC = "psychic"
TYPE_BUG = "bug"
TYPE_ROCK = "rock"
TYPE_GHOST = "ghost"
TYPE_DRAGON = "dragon"
TYPE_DARK = "dark"
TYPE_STEEL = "steel"
TYPE_FAIRY = "fairy"

# Type effectiveness chart
TYPE_EFFECTIVENESS = {
    TYPE_FIRE: {TYPE_GRASS: 1.5, TYPE_ICE: 1.5, TYPE_BUG: 1.5, TYPE_WATER: 0.5},
    TYPE_WATER: {TYPE_FIRE: 1.5, TYPE_GROUND: 1.5, TYPE_ROCK: 1.5, TYPE_GRASS: 0.5},
    TYPE_GRASS: {TYPE_WATER: 1.5, TYPE_GROUND: 1.5, TYPE_ROCK: 1.5, TYPE_FIRE: 0.5},
    TYPE_ELECTRIC: {TYPE_WATER: 1.5, TYPE_FLYING: 1.5, TYPE_GROUND: 0.0},
    # Add more type matchups as needed
}


class Pokemon:
    """Represents a Pokemon creature."""

    def __init__(
        self,
        name,
        pokemon_type,
        level=1,
        hp=None,
        attack=None,
        defense=None,
        speed=None,
    ):
        """Initialize a Pokemon.

        Args:
            name: Pokemon name
            pokemon_type: Pokemon type (from TYPE_* constants)
            level: Pokemon level (default 1)
            hp: Health points (calculated from base if None)
            attack: Attack stat (calculated from base if None)
            defense: Defense stat (calculated from base if None)
            speed: Speed stat (calculated from base if None)
        """
        self.name = name
        self.pokemon_type = pokemon_type
        self.level = level
        self.experience = 0
        self.experience_to_level = EXP_TO_LEVEL_UP

        # Calculate base stats if not provided
        self.base_hp = hp if hp is not None else BASE_HP
        self.base_attack = attack if attack is not None else BASE_ATTACK
        self.base_defense = defense if defense is not None else BASE_DEFENSE
        self.base_speed = speed if speed is not None else BASE_SPEED

        # Calculate actual stats with level modifier
        self.max_hp = self._calculate_stat(self.base_hp)
        self.current_hp = self.max_hp
        self.attack = self._calculate_stat(self.base_attack)
        self.defense = self._calculate_stat(self.base_defense)
        self.speed = self._calculate_stat(self.base_speed)

        self.moves = []  # List of moves the pokemon can use
        self.status = None  # Status condition (burned, poisoned, etc.)

    def _calculate_stat(self, base_stat):
        """Calculate a stat based on level.

        Args:
            base_stat: Base stat value

        Returns:
            Calculated stat value
        """
        return int(base_stat + (base_stat * 0.1 * (self.level - 1)))

    def add_move(self, move):
        """Add a move to the pokemon's moveset.

        Args:
            move: Move object to add

        Returns:
            Boolean indicating success (False if 4 moves already known)
        """
        if len(self.moves) < 4:
            self.moves.append(move)
            return True
        return False

    def remove_move(self, move):
        """Remove a move from the pokemon's moveset.

        Args:
            move: Move object to remove
        """
        if move in self.moves:
            self.moves.remove(move)

    def gain_experience(self, exp_amount):
        """Add experience to the pokemon.

        Args:
            exp_amount: Amount of experience to gain

        Returns:
            Boolean indicating if pokemon leveled up
        """
        self.experience += exp_amount
        if self.experience >= self.experience_to_level:
            self.level_up()
            return True
        return False

    def level_up(self):
        """Level up the pokemon and recalculate stats."""
        self.level += 1
        self.experience = 0
        self.experience_to_level = int(EXP_TO_LEVEL_UP * (self.level * 0.1))

        # Recalculate stats
        self.max_hp = self._calculate_stat(self.base_hp)
        self.current_hp = self.max_hp
        self.attack = self._calculate_stat(self.base_attack)
        self.defense = self._calculate_stat(self.base_defense)
        self.speed = self._calculate_stat(self.base_speed)

    def take_damage(self, damage):
        """Reduce pokemon's health.

        Args:
            damage: Amount of damage to take

        Returns:
            Boolean indicating if pokemon fainted
        """
        self.current_hp = max(0, self.current_hp - damage)
        return self.current_hp == 0

    def heal(self, amount):
        """Heal the pokemon.

        Args:
            amount: Amount to heal
        """
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def is_fainted(self):
        """Check if pokemon is fainted.

        Returns:
            Boolean indicating if pokemon is fainted
        """
        return self.current_hp == 0

    def get_stats(self):
        """Get all pokemon stats.

        Returns:
            Dictionary of stats
        """
        return {
            "name": self.name,
            "type": self.pokemon_type,
            "level": self.level,
            "experience": self.experience,
            "hp": self.current_hp,
            "max_hp": self.max_hp,
            "attack": self.attack,
            "defense": self.defense,
            "speed": self.speed,
        }

    def __str__(self):
        """Return string representation of the pokemon."""
        return f"{self.name} (Lvl {self.level}) - HP: {self.current_hp}/{self.max_hp}"
