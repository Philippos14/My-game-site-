import pygame
import sys
import random
import math

pygame.init()

# Window
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PS5-Style Mini Battle Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 28, bold=True)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (50, 200, 255)
ENEMY_COLOR = (255, 50, 50)
BULLET_COLOR = (255, 255, 0)
PARTICLE_COLOR = (255, 200, 50)
UI_BG = (20, 20, 20)
HEALTH_COLOR = (0, 255, 0)

# Background layers (parallax)
bg_layers = [pygame.Surface((WIDTH, HEIGHT)) for _ in range(3)]
bg_layers[0].fill((30, 30, 60))  # Far sky
bg_layers[1].fill((50, 50, 100))  # Mid mountains
bg_layers[2].fill((80, 80, 160))  # Foreground

bg_offsets = [0, 0, 0]

# Player
player = pygame.Rect(100, HEIGHT - 120, 50, 70)
player_speed = 6
player_vel_y = 0
gravity = 1
jump_power = -18
on_ground = False
player_health = 100
max_health = 100

# Bullets
bullets = []
bullet_speed = 15

# Enemies
enemies = []
enemy_timer = 0
enemy_spawn_rate = 90
enemy_speed = 4

# Particles
particles = []

# Score
score = 0

# Functions
def spawn_enemy():
    x = WIDTH + 50
    y = HEIGHT - 120
    enemies.append(pygame.Rect(x, y, 50, 70))

def spawn_particles(x, y, count=10):
    for _ in range(count):
        particles.append({
            "pos": [x, y],
            "vel": [random.uniform(-2, 2), random.uniform(-5, -1)],
            "life": random.randint(20, 40)
        })

# Game loop
running = True
while running:
    dt = clock.tick(60)
    screen.fill(BLACK)

    # Parallax background
    for i, layer in enumerate(bg_layers):
        speed = (i+1) * 0.5
        bg_offsets[i] -= speed
        if bg_offsets[i] <= -WIDTH:
            bg_offsets[i] = 0
        screen.blit(layer, (bg_offsets[i], 0))
        screen.blit(layer, (bg_offsets[i]+WIDTH, 0))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                player_vel_y = jump_power
            if event.key == pygame.K_f:
                bullets.append(pygame.Rect(player.right, player.centery-5, 15, 5))

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    # Gravity
    player_vel_y += gravity
    player.y += player_vel_y
    if player.bottom >= HEIGHT - 50:
        player.bottom = HEIGHT - 50
        player_vel_y = 0
        on_ground = True
    else:
        on_ground = False

    # Spawn enemies
    enemy_timer += 1
    if enemy_timer >= enemy_spawn_rate:
        spawn_enemy()
        enemy_timer = 0

    # Move enemies
    for e in enemies:
        e.x -= enemy_speed

    # Move bullets
    for b in bullets:
        b.x += bullet_speed

    # Collision bullets vs enemies
    for b in bullets:
        for e in enemies:
            if b.colliderect(e):
                if e in enemies:
                    enemies.remove(e)
                if b in bullets:
                    bullets.remove(b)
                spawn_particles(e.centerx, e.centery)
                score += 10

    # Collision enemies vs player
    for e in enemies:
        if player.colliderect(e):
            player_health -= 1
            if player_health <= 0:
                print("Game Over! Score:", score)
                pygame.quit()
                sys.exit()

    # Draw player
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    # Draw enemies
    for e in enemies:
        pygame.draw.rect(screen, ENEMY_COLOR, e)

    # Draw bullets
    for b in bullets:
        pygame.draw.rect(screen, BULLET_COLOR, b)

    # Draw particles
    for p in particles[:]:
        pygame.draw.circle(screen, PARTICLE_COLOR, (int(p["pos"][0]), int(p["pos"][1])), 3)
        p["pos"][0] += p["vel"][0]
        p["pos"][1] += p["vel"][1]
        p["vel"][1] += 0.2  # gravity
        p["life"] -= 1
        if p["life"] <= 0:
            particles.remove(p)

    # Draw ground
    pygame.draw.rect(screen, (50, 50, 50), (0, HEIGHT - 50, WIDTH, 50))

    # Draw UI
    pygame.draw.rect(screen, UI_BG, (10, 10, 210, 34))
    pygame.draw.rect(screen, (255, 0, 0), (12, 12, 206, 30))  # red background
    pygame.draw.rect(screen, HEALTH_COLOR, (12, 12, int(206*player_health/max_health), 30))  # green health

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 15))

    pygame.display.flip()