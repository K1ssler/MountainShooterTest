import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT, KNOCKBACK_DISTANCE
from code.Enemy import Enemy
from code.Entity import Entity
from code.Player import Player
from code.Point import Point


class EntityMediator:

    @staticmethod
    def __verify_collision_window(ent: Entity):
        if isinstance(ent, Enemy):
            if ent.rect.right <= 0:
                ent.health = 0  # inimigo saiu da tela, morre

    @staticmethod
    def __verify_collision_entity(player: Player, enemy: Enemy):
        knockback_distance = KNOCKBACK_DISTANCE  # ajuste o valor para ficar mais natural
        collision_sound = pygame.mixer.Sound('./asset/Collision.wav')
        collision_sound.set_volume(0.5)  # opcional: define volume de 0.0 a 1.0

        if player.invincibility_timer == 0:

            if player.rect.colliderect(enemy.rect):
                collision_sound.play()
                player.health -= enemy.damage
                player.last_dmg = enemy.name
                player.invincibility_timer = 1000  # 5 segundos de invencibilidade

                dx = player.rect.centerx - enemy.rect.centerx
                dy = player.rect.centery - enemy.rect.centery

                distance = max((dx ** 2 + dy ** 2) ** 0.5, 1)  # evita divisão por zero
                norm_dx = dx / distance
                norm_dy = dy / distance

                # calcula nova posição com knockback
                new_x = player.rect.x + int(norm_dx * knockback_distance)
                new_y = player.rect.y + int(norm_dy * knockback_distance)

                # limita para dentro da tela (ajuste WIN_WIDTH/HEIGHT conforme seu jogo)
                new_x = max(0, min(new_x, WIN_WIDTH - player.rect.width))
                new_y = max(0, min(new_y, WIN_HEIGHT - player.rect.height))

                player.rect.x = new_x
                player.rect.y = new_y

    @staticmethod
    def __verify_collision_point(player: Player, point: Point):

        if point.name == 'Point':
            collision_sound = pygame.mixer.Sound('./asset/Coin.wav')
        else:
            collision_sound = pygame.mixer.Sound('./asset/Diamond.wav')
        collision_sound.set_volume(0.5)  # opcional: define volume de 0.0 a 1.0

        if player.rect.colliderect(point.rect):
            collision_sound.play()
            player.score += point.score
            point.health -= player.damage



    @staticmethod
    def __give_score(enemy: Enemy, player: Player):
        player.score += enemy.score

    @staticmethod
    def verify_collision(player: Player, enemies: list[Enemy], points: list[Point]):
        for enemy in enemies:
            EntityMediator.__verify_collision_window(enemy)
            EntityMediator.__verify_collision_entity(player, enemy)

        for point in points:
            EntityMediator.__verify_collision_window(point)
            EntityMediator.__verify_collision_point(player, point)


    @staticmethod
    def verify_health(player: Player, enemies: list[Enemy], points: list[Point], entity_list: list[Entity]):
        # Verifica se o player morreu
        if player.health <= 0 and player in entity_list:
            entity_list.remove(player)

        for enemy in enemies[:]:  # cria uma cópia da lista para evitar erro ao remover
            if enemy.health <= 0:
                EntityMediator.__give_score(enemy, player)
                enemies.remove(enemy)
                if enemy in entity_list:
                    entity_list.remove(enemy)

        for point in points[:]:
            if point.health <= 0:
                points.remove(point)
                if point in entity_list:
                    entity_list.remove(point)

    '''
    @staticmethod
    def __verify_collision_window(ent: Entity):
        if isinstance(ent, Enemy):
            if ent.rect.right <= 0:
                ent.health = 0
        if isinstance(ent, PlayerShot):
            if ent.rect.left >= WIN_WIDTH:
                ent.health = 0
        if isinstance(ent, EnemyShot):
            if ent.rect.right <= 0:
                ent.health = 0

    @staticmethod
    def __verify_collision_entity(ent1, ent2):
        valid_interaction = False
        if isinstance(ent1, Enemy) and isinstance(ent2, PlayerShot):
            valid_interaction = True
        elif isinstance(ent1, PlayerShot) and isinstance(ent2, Enemy):
            valid_interaction = True
        elif isinstance(ent1, Player) and isinstance(ent2, EnemyShot):
            valid_interaction = True
        elif isinstance(ent1, EnemyShot) and isinstance(ent2, Player):
            valid_interaction = True

        if valid_interaction:  # if valid_interaction == True:
            if (ent1.rect.right >= ent2.rect.left and
                    ent1.rect.left <= ent2.rect.right and
                    ent1.rect.bottom >= ent2.rect.top and
                    ent1.rect.top <= ent2.rect.bottom):
                ent1.health -= ent2.damage
                ent2.health -= ent1.damage
                ent1.last_dmg = ent2.name
                ent2.last_dmg = ent1.name


    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):
        if enemy.last_dmg == 'Player1Shot':
            for ent in entity_list:
                if ent.name == 'Player1':
                    ent.score += enemy.score
        elif enemy.last_dmg == 'Player2Shot':
            for ent in entity_list:
                if ent.name == 'Player2':
                    ent.score += enemy.score

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            EntityMediator.__verify_collision_window(entity1)
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.__verify_collision_entity(entity1, entity2)

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        for ent in entity_list:
            if ent.health <= 0:
                if isinstance(ent, Enemy):
                    EntityMediator.__give_score(ent, entity_list)
                entity_list.remove(ent)
    '''