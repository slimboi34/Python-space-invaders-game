import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Player
player_width = 64
player_height = 20  # Reduced height for a more "space-ship" feel
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - 50
player_speed = 5

# Enemy
num_enemies = 6
enemy_rows = 3
enemy_width = 30
enemy_height = 20
enemy_list = []

for row in range(enemy_rows):
    for i in range(num_enemies):
        enemy_x = i * 80 + 50
        enemy_y = row * 60 + 50
        enemy_list.append({"x": enemy_x, "y": enemy_y, "speed": 2})

# Bullet
bullet_width = 5
bullet_height = 10
bullet_state = "ready"
bullet_x = 0
bullet_y = 0
bullet_speed = 10

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game Over
game_over_font = pygame.font.Font(None, 64)

# Functions
def player(x, y):
    pygame.draw.rect(screen, white, (x, y, player_width, player_height))  # Draw player rectangle

def enemy(x, y):
    pygame.draw.rect(screen, red, (x, y, enemy_width, enemy_height))  # Draw enemy rectangle

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    pygame.draw.rect(screen, white, (x, y, bullet_width, bullet_height))  # Draw bullet rectangle

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    # More precise collision detection using rects
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    bullet_rect = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
    return enemy_rect.colliderect(bullet_rect)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(black)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x -= player_speed
            if event.key == pygame.K_RIGHT:
                player_x += player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x + player_width // 2 - bullet_width // 2
                    bullet_y = player_y
                    fire_bullet(bullet_x, bullet_y)

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed
        if bullet_y <= 0:
            bullet_state = "ready"

    # Enemy movement
    for e in enemy_list:
        e["x"] += e["speed"]
        if e["x"] <= 0 or e["x"] >= screen_width - enemy_width:
            e["speed"] *= -1
            e["y"] += 20

    # Collision detection
    for e in enemy_list[:]:
        if is_collision(e["x"], e["y"], bullet_x, bullet_y):
            bullet_state = "ready"
            enemy_list.remove(e)
            score += 1

    # Check if all enemies are defeated
    if not enemy_list:
        running = False
        print("You Win!")

    # Check if enemies reach the player
    for e in enemy_list:
        if e["y"] > screen_height - 100:
            running = False
            break

    # Draw player
    player(player_x, player_y)

    # Draw enemies
    for e in enemy_list:
        enemy(e["x"], e["y"])

    # Draw score
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()