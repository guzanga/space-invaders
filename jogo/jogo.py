import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Player
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height - player_size - 10
player_speed = 300  # Pixels per second

# Bullet
bullet_size = 5
bullet_speed = 1000  # Pixels per second
bullet_state = "ready"  # "ready" - ready to fire, "fire" - bullet is moving
bullet_x = 0
bullet_y = 0

# Enemies
enemy_size = 50
enemies = []  # List to store enemy objects
enemy_speed = 120
enemy_spawn_delay = 1000  # Delay between enemy spawns in milliseconds
last_enemy_spawn_time = pygame.time.get_ticks()  # Time of the last enemy spawn

# Score
score = 0
font = pygame.font.Font(None, 36)

# Player life
player_life = 1

# Clock for managing the frame rate
clock = pygame.time.Clock()

# Function to create a new enemy object
def create_enemy():
    enemy = {
        "x": random.randint(0, width - enemy_size),
        "y": random.randint(50, 150),
        "speed": enemy_speed,
        "shoot_delay": random.randint(1000, 3000),  # Delay between enemy shots in milliseconds
        "last_shot_time": pygame.time.get_ticks(),  # Time of the last enemy shot
    }
    enemies.append(enemy)

# Function to check bullet-enemy collision
def check_collision(bullet_x, bullet_y, enemy_x, enemy_y, enemy_size):
    if (
        bullet_x >= enemy_x
        and bullet_x <= enemy_x + enemy_size
        and bullet_y >= enemy_y
        and bullet_y <= enemy_y + enemy_size
    ):
        return True
    return False

# Game loop
running = True
while running:
    # Limit the frame rate to 60 FPS
    delta_time = clock.tick(60) / 1000.0

    window.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player shooting
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and bullet_state == "ready":
            bullet_x = player_x + player_size // 2 - bullet_size // 2
            bullet_y = player_y
            bullet_state = "fire"

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed * delta_time
    if keys[pygame.K_RIGHT]:
        player_x += player_speed * delta_time
    if keys[pygame.K_UP]:
        player_y -= player_speed * delta_time
    if keys[pygame.K_DOWN]:
        player_y += player_speed * delta_time

    # Player movement boundaries
    if player_x < 0:
        player_x = 0
    elif player_x > width - player_size:
        player_x = width - player_size
    if player_y < 0:
        player_y = 0
    elif player_y > height - player_size:
        player_y = height - player_size

    # Bullet movement
    if bullet_state == "fire":
        bullet_y -= bullet_speed * delta_time
        pygame.draw.circle(window, GREEN, (bullet_x, bullet_y), bullet_size)

    # Bullet boundaries
    if bullet_y <= 0:
        bullet_state = "ready"

    # Enemy movement, collision detection, and shooting
    for enemy in enemies:
        enemy["x"] += enemy["speed"] * delta_time

        if check_collision(bullet_x, bullet_y, enemy["x"], enemy["y"], enemy_size):
            bullet_state = "ready"
            score += 1
            enemies.remove(enemy)

        if enemy["x"] <= 0 or enemy["x"] >= width - enemy_size:
            enemy["speed"] *= -1
            enemy["y"] += 20

        # Enemy shooting
        current_time = pygame.time.get_ticks()
        if current_time - enemy["last_shot_time"] >= enemy["shoot_delay"]:
            enemy_bullet_x = enemy["x"] + enemy_size // 2 - bullet_size // 2
            enemy_bullet_y = enemy["y"] + enemy_size
            pygame.draw.circle(window, GREEN, (enemy_bullet_x, enemy_bullet_y), bullet_size)
            enemy["last_shot_time"] = current_time

            # Check if enemy bullet hits the player
            if check_collision(enemy_bullet_x, enemy_bullet_y, player_x, player_y, player_size):
                player_life -= 1
                if player_life <= 0:
                    running = False

    # Spawn a new enemy if enough time has passed
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time >= enemy_spawn_delay:
        create_enemy()
        last_enemy_spawn_time = current_time

    # Draw player
    pygame.draw.polygon(
        window,
        WHITE,
        [
            (player_x, player_y),
            (player_x + player_size, player_y),
            (player_x + player_size // 2, player_y - player_size),
        ],
    )

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(window, WHITE, (enemy["x"], enemy["y"], enemy_size, enemy_size))

    # Display score and player life
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (10, 10))
    life_text = font.render("Life: " + str(player_life), True, WHITE)
    window.blit(life_text, (10, 50))

    # Enemy movement, collision detection, and shooting
    for enemy in enemies:
        enemy["x"] += enemy["speed"] * delta_time

        if check_collision(bullet_x, bullet_y, enemy["x"], enemy["y"], enemy_size):
            bullet_state = "ready"
            score += 1
            enemies.remove(enemy)

        if enemy["x"] <= 0 or enemy["x"] >= width - enemy_size:
            enemy["speed"] *= -1
            enemy["y"] += 20

        # Enemy shooting
        current_time = pygame.time.get_ticks()
        if current_time - enemy["last_shot_time"] >= enemy["shoot_delay"]:
            enemy_bullet_x = enemy["x"] + enemy_size // 2 - bullet_size // 2
            enemy_bullet_y = enemy["y"] + enemy_size
            pygame.draw.circle(window, GREEN, (enemy_bullet_x, enemy_bullet_y), bullet_size)
            enemy["last_shot_time"] = current_time

            # Check if enemy bullet hits the player
            if check_collision(enemy_bullet_x, enemy_bullet_y, player_x, player_y, player_size):
                player_life -= 1
                if player_life <= 0:
                    running = False

        # Check if enemy hits the player
        if check_collision(player_x, player_y, enemy["x"], enemy["y"], enemy_size):
            player_life -= 1
            if player_life <= 0:
                running = False

    pygame.display.update()


# Quit the game
pygame.quit()
