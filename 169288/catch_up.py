import pygame
import random
import math
pygame.mixer.init()
# Загрузка звука
shoot_sound = pygame.mixer.Sound('demonstratsionnyiy-vyistrel-iz-melkokalibernoy-vintovki.wav')  # Замените на путь к вашему звуковому файлу
enemy_death_sound = pygame.mixer.Sound("popadanie-tochno-v-tsel.wav")  # Замените на путь к звуку смерти врага
reload_sound = pygame.mixer.Sound("upavshiy-patron-pri-perezaryadke.wav")  # Замените на путь к звуку перезарядки

# Загрузка изображения фона
background_image = pygame.image.load("1678414405_bogatyr-club-p-polyana-vid-sverkhu-foni-instagram-6.jpg")  # Замените на путь к вашему изображению фона
background_image = pygame.transform.scale(background_image, (1400, 800))  # Масштабируйте изображение под размер экрана


# Переменная для хранения счёта
score = 0

# Параметры стрельбы
last_shot_time = 0
shot_delay = 300  # Задержка между выстрелами в миллисекундах

bullet_image = pygame.Surface((10, 10))  # Создаем простую пулю
bullet_image.fill((255, 255, 0))  # жёлтый цвет пули

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Апокалипсис: Последний из города")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Игрок
player_size = 15
player_pos = [WIDTH // 2, HEIGHT // 2]
player_health = 100
reload_time = 3  # Время перезарядки в секундах
last_reload_time = 0  # Время последней перезаря

# Загрузка спрайтов для игрока
player_sprites = [pygame.image.load(f'fbr.png') for i in range(4)]  # Замените на свои изображения
player_frame = 0
player_animation_speed = 0.1

# Пули
bullets = []
bullet_speed = 30

enemy_image = pygame.image.load("izllom.png")  # Замените на путь к изображению врага
enemy_image = pygame.transform.scale(enemy_image, (300, 300))  # Измените размер по необходимости
enemies = []  # Список для хранения врагов

# Инициализация патронов
max_ammo = 30  # Максимальное количество патронов
current_ammo = max_ammo  # Текущие патроны

def create_enemy():
    # Генерируем случайные координаты для появления врага за пределами экрана
    if random.choice([True, False]):  # Случайно выбираем, появится ли враг слева или справа
        enemy_x = -150  # Появление слева (вне экрана)
    else:
        enemy_x = WIDTH  # Появление справа (вне экрана)
    
    # Генерируем случайное Y-координату для врага
    enemy_y = random.randint(0, HEIGHT - 150)

    enemies.append({'pos': [enemy_x, enemy_y]})


# Шрифты
font = pygame.font.SysFont(None, 36)
x, y = WIDTH // 2, HEIGHT // 2
speed = 5  # Скорость перемещения
# Главный игровой цикл
running = True
clock = pygame.time.Clock()

# Переменные для перезарядки
reload_time = 4500  # Время перезарядки в миллисекундах
last_reload_time = 0  # Время последней перезарядки
is_reloading = False  # Статус перезарядки

def show_menu():
    while True:
        screen.fill(WHITE)  # Заливка фона
        title_text = font.render('Шутер от третьего лица', True, BLACK)
        start_text = font.render('Нажмите "Enter" для начала игры', True, BLACK)
        exit_text = font.render('Нажмите "Esc" для выхода', True, BLACK)

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Начать игру
                    return  # Выход из меню
                if event.key == pygame.K_ESCAPE:  # Выход из игры
                    pygame.quit()
                    return

def game_over_screen():
    screen.fill(WHITE)  # Заливка фона
    game_over_text = font.render('Игра окончена', True, BLACK)
    restart_text = font.render('Нажмите "Enter" для перезапуска', True, BLACK)
    exit_text = font.render('Нажмите "Esc" для выхода', True, BLACK)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Перезапуск игры
                    main()  # Замените на функцию, которая запускает игру
                if event.key == pygame.K_ESCAPE:  # Выход из игры
                    pygame.quit()
                    return
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Перезапуск игры
                    main()  # Замените на функцию, которая запускает игру
                if event.key == pygame.K_ESCAPE:  # Выход из игры
                    pygame.quit()
                    return

# Вызов меню перед началом игры
show_menu()
# Игровая логика здесь
running = True

while running:
    current_time = pygame.time.get_ticks()  # Текущее время в миллисекундах
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Проверка на выход из игры
            running = False
    
    # Отрисовка фона
    screen.blit(background_image, (0, 0))

    # Управление игроком
    keys = pygame.key.get_pressed()
   
   
    # Стрельба с задержкой и проверка наличия патронов
    if keys[pygame.K_SPACE] and current_time - last_shot_time > shot_delay and current_ammo > 0 and not is_reloading:
         # Создаем пулю
        bullet_dx = math.cos(math.radians(angle)) * bullet_speed
        bullet_dy = math.sin(math.radians(angle)) * bullet_speed
        bullet = {'pos': [x + 35, y + 30], 'dx': bullet_dx, 'dy': bullet_dy}
        bullets.append(bullet)
        last_shot_time = current_time
        current_ammo -= 1  # Уменьшаем количество патронов на 1
        # Воспроизведение звука выстрела
        shoot_sound.play()

    # Обновление позиций пуль
    for bullet in bullets[:]:
        bullet['pos'][0] += bullet['dx']
        bullet['pos'][1] += bullet['dy']
        if bullet['pos'][0] < 0 or bullet['pos'][0] > WIDTH or bullet['pos'][1] < 0 or bullet['pos'][1] > HEIGHT:
            bullets.remove(bullet)  # Удаляем пулю, если она вышла за пределы экрана


    # Отрисовка пуль
    for bullet in bullets:
        bullet_rect = bullet_image.get_rect(center=(bullet['pos'][0], bullet['pos'][1]))
        screen.blit(bullet_image, bullet_rect.topleft)

        
    # Отрисовка врагов
    for enemy in enemies:
        enemy_rect = rotated_enemy_image.get_rect(center=(enemy['pos'][0], enemy['pos'][1]))
        screen.blit(rotated_enemy_image, enemy_rect.topleft)




    mouse_x, mouse_y = pygame.mouse.get_pos()

   
      # Создание врагов через определенные промежутки времени
    if random.randint(1, 25) == 1:  # Примерно 4% шанс появления врага на каждом кадре
        create_enemy()
    
    # Обновление позиций врагов
    for enemy in enemies:
        angle_to_player = math.degrees(math.atan2(y + 50 - enemy['pos'][1], x + 50 - enemy['pos'][0]))
        rotated_enemy_image = pygame.transform.rotate(enemy_image, -angle_to_player)
        enemy_dx = math.cos(math.radians(angle_to_player)) * 3  # Скорость врага
        enemy_dy = math.sin(math.radians(angle_to_player)) * 3
        enemy['pos'][0] += enemy_dx
        enemy['pos'][1] += enemy_dy
    # Проверка столкновения пуль с врага
    for bullet in bullets[:]:  # Используем срез для безопасной итерации
        bullet_rect = bullet_image.get_rect(center=(bullet['pos'][0], bullet['pos'][1]))
        for enemy in enemies[:]:  # Используем срез для врагов
            enemy_rect = enemy_image.get_rect(center=(enemy['pos'][0], enemy['pos'][1]))
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)  # Удаляем пулю
                enemies.remove(enemy)    # Удаляем врага
                score += 1  # Увеличиваем счёт
                enemy_death_sound.play()  # Воспроизводим звук смерти врага
                break  # Выход из внутреннего цикла
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Проверка столкновения врагов с игроком
    player_rect = pygame.Rect(x, y, player_size, player_size)  # Прямоугольник игрока
    for enemy in enemies[:]:  # Используем срез для безопасной итерации
        enemy_rect = enemy_image.get_rect(center=(enemy['pos'][0], enemy['pos'][1]))
        if player_rect.colliderect(enemy_rect):
            player_health -= 5  # Уменьшаем здоровье игрока на 5
            enemies.remove(enemy)  # Удаляем врага, если он касается игрока
            break  # Выход из внутреннего цикла

    # Проверка здоровья игрока
    if player_health <= 0:
        game_over_screen()  # Вызов экрана окончания игры

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

    # Поворачиваем изображение
    rotated_image = pygame.transform.rotate(player_sprites[0], -angle)

    # Вычисляем новый прямоугольник для изображения
    rect = rotated_image.get_rect(center=(x + 50, y + 50))


    screen.blit(rotated_image, rect.topleft)

    # Показ здоровья и патронов
    health_text = font.render(f'Здоровье: {player_health}', True, BLACK)
    screen.blit(health_text, (10, 10))
    # Отображение счёта на экране
    score_text = font.render(f'Было убито: {score}', True, BLACK)
    screen.blit(score_text, (10, 70))  # Устанавливаем положение счёта на экране
    # Отображение количества патронов и статуса перезарядки
    ammo_text = font.render(f'Патроны: {current_ammo}/{max_ammo}', True, BLACK)
    screen.blit(ammo_text, (10, 40))

    if is_reloading:
        reload_text = font.render('Перезарядка...', True, RED)
        screen.blit(reload_text, (10, 100))  # Показать статус перезарядки

    # Стрельба с задержкой и проверка наличия патронов
    if keys[pygame.K_SPACE] and current_time - last_shot_time > shot_delay and current_ammo > 0 and not is_reloading:
        # Создаем пулю
        bullet_dx = math.cos(math.radians(angle)) * bullet_speed
        bullet_dy = math.sin(math.radians(angle)) * bullet_speed
        bullet = {'pos': [x + 35, y + 30], 'dx': bullet_dx, 'dy': bullet_dy}
        bullets.append(bullet)
        last_shot_time = current_time
        current_ammo -= 1  # Уменьшаем количество патронов на 1

     # Перезарядка
    if keys[pygame.K_r] and current_ammo < max_ammo and not is_reloading:
        is_reloading = True
        last_reload_time = current_time
        reload_sound.play()  # Воспроизводим звук перезарядки

    if is_reloading:
        # Проверка времени перезарядки
        if current_time - last_reload_time >= reload_time:
            current_ammo = max_ammo  # Полная перезарядка
            is_reloading = False  # Завершаем перезарядку
    
    # Обновление экрана
    pygame.display.flip()
    clock.tick(30)

# Завершение работы Pygame
pygame.quit()
 