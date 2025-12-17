"""Move class for Pokemon attacks."""

class Move:
    """Represents a Pokemon move/attack."""

    def __init__(self, name, move_type, power, accuracy, priority=0):
        """Initialize a move.

        Args:
            name: Move name
            move_type: Type of move (should match pokemon type)
            power: Base power of the move (0-150)
            accuracy: Accuracy percentage (0-100)
            priority: Priority in battle (-7 to 5)
        """
        self.name = name
        self.move_type = move_type
        self.power = power
        self.accuracy = accuracy
        self.priority = priority
        self.pp = 20  # Power Points (uses per battle)
        self.max_pp = 20

    def use_pp(self):
        """Use one power point.

        Returns:
            Boolean indicating if move can be used
        """
        if self.pp > 0:
            self.pp -= 1
            return True
        return False

    def restore_pp(self):
        """Restore power points to maximum."""
        self.pp = self.max_pp

    def calculate_damage(self, attacker, defender):
        """Calculate damage dealt by this move.

        Args:
            attacker: Attacking pokemon
            defender: Defending pokemon

        Returns:
            Damage value
        """
        import random
        
        # Base damage calculation
        level = attacker.level
        power = self.power
        attack = attacker.attack
        defense = defender.defense
        
        damage = ((2 * level / 5 + 2) * power * attack / defense) / 50 + 2
        
        # Random factor (85-100%)
        damage *= random.uniform(0.85, 1.0)
        
        # Type effectiveness
        if self.move_type in defender.pokemon_type:
            damage *= 0.5  # Not very effective
        
        return int(max(1, damage))

    def __str__(self):
        """Return string representation of the move."""
        return f"{self.name} ({self.move_type}) - Power: {self.power}, PP: {self.pp}/{self.max_pp}"