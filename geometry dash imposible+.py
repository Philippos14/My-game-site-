import pygame
import sys
import random

pygame.init()

# Window
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Geometry Dash Deluxe")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Colors
COLORS = [(255, 50, 50), (50, 255, 50), (50, 50, 255),
          (255, 255, 50), (255, 50, 255), (50, 255, 255)]

# Characters (different colors)
CHARACTERS = [(200, 0, 0), (0, 200, 0), (0, 0, 200), (200, 200, 0), (200, 0, 200)]

# Player
player_size = 40
player_color = CHARACTERS[0]
player = pygame.Rect(100, HEIGHT - 100, player_size, player_size)
player_vel_y = 0
gravity = 0.8
jump_power = -15
on_ground = False

# Obstacles
obstacles = []
obstacle_timer = 0
obstacle_speed = 100

# Score and Level
score = 0
level = 1
level_length = 100000  # How long each level lasts

# Game loop
running = True
while running:
    clock.tick(60)
    screen.fill(random.choice(COLORS))  # Random background color each frame
    
    #  Update Score
    score +=100 
    if score % level_length == 0:
        level += 1
        # Change character each level
        player_color = random.choice(CHARACTERS)
        obstacle_speed += 1  # Increase difficulty

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                player_vel_y = jump_power

    # Gravity
    player_vel_y += gravity
    player.y += player_vel_y

    # Ground collision
    if player.bottom >= HEIGHT - 40:
        player.bottom = HEIGHT - 40
        player_vel_y = 0
        on_ground = True
    else:
        on_ground = False

    # Spawn obstacles
    obstacle_timer += 1
    if obstacle_timer > 60:
        obstacles.append(pygame.Rect(WIDTH, HEIGHT - 80, 40, 40))
        obstacle_timer = 0

    # Move obstacles
    for obs in obstacles:
        obs.x -= obstacle_speed

    # Remove off-screen obstacles
    obstacles = [obs for obs in obstacles if obs.x > -50]

    # Collision
    for obs in obstacles:
        if player.colliderect(obs):
            print("Game Over! Score:", score)
            pygame.quit()
            sys.exit()

    # Draw ground
    pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT - 40, WIDTH, 40))
    
    # Draw player
    pygame.draw.rect(screen, player_color, player)
    
    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, random.choice(COLORS), obs)
    
    # Draw score and level
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    level_text = font.render(f"Level: {level}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - 150, 10))
    
    pygame.display.flip()   