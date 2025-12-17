"""Battle system for Pokemon encounters."""

import random
from move import Move
from pokemon import TYPE_EFFECTIVENESS


class Battle:
    """Represents a Pokemon battle."""

    def __init__(self, player_pokemon, wild_pokemon):
        """Initialize a battle.

        Args:
            player_pokemon: Pokemon from player's party
            wild_pokemon: Wild pokemon encountered
        """
        self.player_pokemon = player_pokemon
        self.wild_pokemon = wild_pokemon
        self.turn = 0
        self.battle_log = []
        self.is_finished = False
        self.winner = None

    def calculate_move_order(self, player_move, wild_move):
        """Determine who goes first based on priority and speed.

        Args:
            player_move: Move chosen by player
            wild_move: Move chosen by wild pokemon

        Returns:
            Tuple (bool: player goes first, bool: wild goes first)
        """
        player_priority = player_move.priority
        wild_priority = wild_move.priority

        if player_priority != wild_priority:
            return (player_priority > wild_priority, wild_priority > player_priority)
        else:
            # Same priority, use speed stat
            player_first = (
                self.player_pokemon.speed > self.wild_pokemon.speed
                or random.random() < 0.5
            )
            return (player_first, not player_first)

    def execute_move(self, attacker, defender, move):
        """Execute a move in battle.

        Args:
            attacker: Pokemon using the move
            defender: Pokemon being attacked
            move: Move to execute

        Returns:
            Boolean indicating if move hit
        """
        # Check accuracy
        if random.random() * 100 > move.accuracy:
            self.battle_log.append(f"{attacker.name}'s {move.name} missed!")
            return False

        # Calculate damage
        damage = move.calculate_damage(attacker, defender)
        defender.take_damage(damage)

        self.battle_log.append(
            f"{attacker.name} used {move.name}! {defender.name} took {damage} damage!"
        )

        if defender.is_fainted():
            self.battle_log.append(f"{defender.name} fainted!")
            self.is_finished = True
            self.winner = attacker.name

        return True

    def player_turn(self, move_index):
        """Execute player's turn.

        Args:
            move_index: Index of move to use (0-3)

        Returns:
            Boolean indicating if action was valid
        """
        if move_index < len(self.player_pokemon.moves):
            player_move = self.player_pokemon.moves[move_index]
            wild_move = random.choice(self.wild_pokemon.moves)

            player_first, wild_first = self.calculate_move_order(player_move, wild_move)

            if player_first:
                self.execute_move(self.player_pokemon, self.wild_pokemon, player_move)
                if not self.is_finished:
                    self.execute_move(self.wild_pokemon, self.player_pokemon, wild_move)
            else:
                self.execute_move(self.wild_pokemon, self.player_pokemon, wild_move)
                if not self.is_finished:
                    self.execute_move(self.player_pokemon, self.wild_pokemon, player_move)

            self.turn += 1
            return True
        return False

    def player_catch(self):
        """Attempt to catch the wild pokemon.

        Returns:
            Boolean indicating if catch was successful
        """
        # Simple catch rate based on wild pokemon's HP percentage
        catch_rate = 1 - (self.wild_pokemon.current_hp / self.wild_pokemon.max_hp)
        
        if random.random() < catch_rate:
            self.battle_log.append(f"You caught {self.wild_pokemon.name}!")
            self.is_finished = True
            self.winner = "player"
            return True
        else:
            self.battle_log.append("The Pokemon broke free!")
            return False

    def player_flee(self):
        """Attempt to flee from battle.

        Returns:
            Boolean indicating if flee was successful
        """
        if random.random() < 0.5:
            self.battle_log.append("Successfully fled from battle!")
            self.is_finished = True
            self.winner = "fled"
            return True
        else:
            self.battle_log.append("Failed to flee!")
            return False

    def get_battle_log(self):
        """Get the battle log.

        Returns:
            List of battle log entries
        """
        return self.battle_log

    def __str__(self):
        """Return string representation of the battle."""
        return f"Battle between {self.player_pokemon.name} and {self.wild_pokemon.name}"