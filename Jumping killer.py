import pygame
import sys
import random

pygame.init()

# Window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Fortnite 2D")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# Colors
PLAYER_COLOR = (0, 200, 0)
ENEMY_COLOR = (200, 0, 0)
BULLET_COLOR = (255, 255, 0)
GROUND_COLOR = (50, 50, 50)
BG_COLOR = (100, 150, 255)
HEALTH_COLOR = (0, 255, 0)

# Player
player = pygame.Rect(100, 500, 40, 60)
player_speed = 5
player_vel_y = 0
gravity = 0.8
jump_power = -15
on_ground = False
player_health = 100

# Bullets
bullets = []
bullet_speed = 10

# Enemies
enemies = []
enemy_spawn_timer = 1
enemy_speed = 5

# Score
score = 0

# Game loop
running = True
while running:
    clock.tick(60)
    screen.fill(BG_COLOR)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                player_vel_y = jump_power
            if event.key == pygame.K_f:  # Shoot bullet
                bullets.append(pygame.Rect(player.right, player.centery - 5, 10, 5))

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    # Gravity
    player_vel_y += gravity
    player.y += player_vel_y
    if player.bottom >= HEIGHT - 40:
        player.bottom = HEIGHT - 40
        player_vel_y = 0
        on_ground = True
    else:
        on_ground = False

    # Spawn enemies
    enemy_spawn_timer += 1
    if enemy_spawn_timer > 90:
        enemies.append(pygame.Rect(WIDTH, HEIGHT - 100, 40, 60))
        enemy_spawn_timer = 0

    # Move enemies
    for e in enemies:
        e.x -= enemy_speed

    # Remove off-screen enemies
    enemies = [e for e in enemies if e.x > -50]

    # Move bullets
    for b in bullets:
        b.x += bullet_speed
    bullets = [b for b in bullets if b.x < WIDTH]

    # Collision detection (bullets hit enemies)
    for b in bullets:
        for e in enemies:
            if b.colliderect(e):
                if e in enemies:
                    enemies.remove(e)
                if b in bullets:
                    bullets.remove(b)
                score += 20

    # Collision detection (enemies hit player)
    for e in enemies:
        if player.colliderect(e):
            player_health -= 1
            if player_health <= 0:
                print("Game Over! Score:", score)
                pygame.quit()
                sys.exit()

    # Draw ground
    pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT - 40, WIDTH, 40))

    # Draw player
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    # Draw enemies
    for e in enemies:
        pygame.draw.rect(screen, ENEMY_COLOR, e)

    # Draw bullets
    for b in bullets:
        pygame.draw.rect(screen, BULLET_COLOR, b)

    # Draw health bar
    pygame.draw.rect(screen, (255,0,0), (10, 10, 104, 24))  # background red
    pygame.draw.rect(screen, HEALTH_COLOR, (12, 12, player_health, 20))

    # Draw score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (WIDTH - 120, 10))

    pygame.display.flip()