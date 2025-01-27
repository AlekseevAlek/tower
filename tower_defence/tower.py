import pygame
from bullet import Bullet
import math


class Tower(pygame.sprite.Sprite):
    '''Базовый класс для всех башен, его методы включают инициализацию, отрисовку, обновление, стрельбу, поворот к цели и поиск цели.'''
    def __init__(self, position, game):
        '''Инициализирует башню.'''
        super().__init__()
        self.position = pygame.math.Vector2(position)
        self.game = game

        self.image = None
        self.rect = None
        self.tower_range = 0
        self.damage = 0
        self.rate_of_fire = 0
        self.last_shot_time = pygame.time.get_ticks()
        self.level = 1
        self.original_image = self.image

    def upgrade_cost(self):
        '''Вычисляет стоимость улучшения башни на текущем уровне.'''

        return 100 * self.level

    def draw(self, screen):
        '''Отображает изображение башни на экране.'''
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovered(mouse_pos):
            level_text = self.game.font.render(f"Level: {self.level}", True, (255, 255, 255))
            upgrade_cost_text = self.game.font.render(f"Upgrade: ${self.upgrade_cost()  }", True, (255, 255, 255))

            level_text_pos = (self.position.x, self.position.y + 20)
            upgrade_cost_pos = (self.position.x, self.position.y + 40)

            screen.blit(level_text, level_text_pos)
            screen.blit(upgrade_cost_text, upgrade_cost_pos)

    def update(self, enemies, current_time, bullets_group):
        ''' Обновляет состояние башни.'''
        if current_time - self.last_shot_time > self.rate_of_fire:
            target = self.find_target(enemies)
            if target:
                self.rotate_towards_target(target)
                self.shoot(target, bullets_group)
                self.last_shot_time = current_time

    def is_hovered(self, mouse_pos):
        '''Проверяет, находится ли курсор мыши над башней.'''
        return self.rect.collidepoint(mouse_pos)

    def shoot(self, target, bullets_group):
        '''Метод для создания пули и добавления ее в группу пуль.'''
        pass

    def rotate_towards_target(self, target):
        '''Вращивает изображение башни к целевой точке.'''
        dx = target.position.x - self.position.x
        dy = target.position.y - self.position.y
        # Вычисляем угол в радианах
        angle_rad = math.atan2(dy, dx)
        # Преобразуем радианы в градусы
        angle_deg = math.degrees(angle_rad)
        angle_deg = -angle_deg - 90
        self.image = pygame.transform.rotate(self.original_image, angle_deg)
        self.rect = self.image.get_rect(center=self.position)

    def find_target(self, enemies):
        '''Найдет ближайшего врага в пределах диапазона башни.'''
        nearest_enemy = None
        min_distance = float('inf')
        for enemy in enemies:
            distance = self.position.distance_to(enemy.position)
            if distance < min_distance and distance <= self.tower_range:
                nearest_enemy = enemy
                min_distance = distance
        return nearest_enemy

    def upgrade(self):
        '''Увеличивает уровень башни.'''
        self.level += 1


class BasicTower(Tower):
    '''Конкретная реализация башен, расширяющие базовый класс.'''
    def __init__(self, position, game):
        '''Инициализирует базовую башню.'''
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/basic_tower.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 150
        self.damage = 20
        self.rate_of_fire = 1000

    def shoot(self, target, bullets_group):
        '''Создает новую пулю и добавляет ее в группу пуль.'''
        new_bullet = Bullet(self.position, target.position, self.damage, self.game)
        bullets_group.add(new_bullet)


class SniperTower(Tower):
    '''Снайперская башня имеет собственный алгоритм выбора цели.'''
    def __init__(self, position, game):
        '''Инициализирует снайперскую башню.'''
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/sniper_tower.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 300
        self.damage = 40
        self.rate_of_fire = 2000

    def find_target(self, enemies):
        '''Найдет врага с максимальным здоровьем в пределах диапазона.'''

        healthiest_enemy = None
        max_health = 0
        for enemy in enemies:
            if self.position.distance_to(enemy.position) <= self.tower_range and enemy.health > max_health:
                healthiest_enemy = enemy
                max_health = enemy.health
        return healthiest_enemy

    def shoot(self, target, bullets_group):
        '''Создает новую пулю и добавляет ее в группу пуль.'''
        new_bullet = Bullet(self.position, target.position, self.damage, self.game)
        bullets_group.add(new_bullet)
