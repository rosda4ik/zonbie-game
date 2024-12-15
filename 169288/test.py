import pygame
import math
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Поворот, движение, стрельба и враги")

# Загрузка изображений
player_image = pygame.image.load("fbr.png")  # Замените на путь к вашему изображению игрока
player_image = pygame.transform.scale(player_image, (100, 100))  # Измените размер по необходимости
bullet_image = pygame.Surface((10, 10))  # Создаем простую пулю
bullet_image.fill((255, 0, 0))  # Красный цвет пули
enemy_image = pygame.image.load("izllom.png")  # Замените на путь к изображению врага
enemy_image = pygame.transform.scale(enemy_image, (150, 150))  # Измените размер по необходимости

# Начальная позиция персонажа
x, y = width // 2, height // 2
speed = 5  # Скорость перемещения
bullets = []  # Список для хранения пуль
enemies = []  # Список для хранения врагов

# Параметры стрельбы
last_shot_time = 0
shot_delay = 300  # Задержка между выстрелами в миллисекундах

# Функция для создания врагов
def create_enemy():
    enemy_x = random.randint(0, width - 50)
    enemy_y = random.randint(0, height - 50)
    enemies.append({'pos': [enemy_x, enemy_y]})

# Основной цикл игры
running = True
while running:
    current_time = pygame.time.get_ticks()  # Текущее время в миллисекундах
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Получаем позицию мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Вычисляем угол поворота
    angle = math.degrees(math.atan2(mouse_y - (y + 50), mouse_x - (x + 50)))

    # Движение персонажа
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        y -= speed
    if keys[pygame.K_s]:
        y += speed
    if keys[pygame.K_a]:
        x -= speed
    if keys[pygame.K_d]:
        x += speed

    # Стрельба с задержкой
    if keys[pygame.K_SPACE] and current_time - last_shot_time > shot_delay:
        # Создаем пулю
        bullet_dx = math.cos(math.radians(angle)) * 10  # Скорость по X
        bullet_dy = math.sin(math.radians(angle)) * 10  # Скорость по Y
        bullet = {'pos': [x + 50, y + 50], 'dx': bullet_dx, 'dy': bullet_dy}
        bullets.append(bullet)
        last_shot_time = current_time  # Обновляем время последнего выстрела

    # Обновление позиций пуль
    for bullet in bullets:
        bullet['pos'][0] += bullet['dx']
        bullet['pos'][1] += bullet['dy']

    # Создание врагов через определенные промежутки времени
    if random.randint(1, 50) == 1:  # Примерно 2% шанс появления врага на каждом кадре
        create_enemy()

    # Обновление позиций врагов
    for enemy in enemies:
        angle_to_player = math.degrees(math.atan2(y + 50 - enemy['pos'][1], x + 50 - enemy['pos'][0]))
        enemy_dx = math.cos(math.radians(angle_to_player)) * 0.3  # Скорость врага
        enemy_dy = math.sin(math.radians(angle_to_player)) * 0.3
        enemy['pos'][0] += enemy_dx
        enemy['pos'][1] += enemy_dy

    # Отрисовка
    screen.fill((255, 255, 255))  # Заливка фона белым
    rotated_image = pygame.transform.rotate(player_image, -angle)
    rect = rotated_image.get_rect(center=(x + 50, y + 50))
    screen.blit(rotated_image, rect.topleft)

    # Отрисовка пуль
    for bullet in bullets:
        bullet_rect = bullet_image.get_rect(center=(bullet['pos'][0], bullet['pos'][1]))
        screen.blit(bullet_image, bullet_rect.topleft)

    # Отрисовка врагов
    for enemy in enemies:
        enemy_rect = enemy_image.get_rect(center=(enemy['pos'][0], enemy['pos'][1]))
        screen.blit(enemy_image, enemy_rect.topleft)

    pygame.display.flip()

# Завершение
pygame.quit()