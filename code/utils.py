from code.Enemy import Enemy
from code.Entity import Entity
from code.Player import Player


class GetPlayer:
    def get_player_and_enemies(entity_list: list[Entity]) -> tuple[Player, list[Enemy]]:
        player = next((e for e in entity_list if isinstance(e, Player)), None)
        enemies = [e for e in entity_list if isinstance(e, Enemy)]
        return player, enemies