import pygame
import random
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Adventure")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

player_width, player_height = 50, 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_velocity = 5
jump_height = -15
gravity = 0.8
is_jumping = False
player_y_velocity = 0

object_width, object_height = 40, 40
object_velocity = 5

meteors = []
aliens = []
spaceship_parts = []

parts_collected = 0
current_level = 0
LEVELS = ["Aidala", "Jerdin bir jeri", "Baigaistan", "It olgen jer"]
backgrounds = ["bg1.jpeg", "bg2.jpeg", "bg3.jpeg", "bg4.jpeg"]

clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 30)

def load_image(filename, width, height, fallback_color):
    if os.path.exists(filename):
        img = pygame.image.load(filename)
        return pygame.transform.scale(img, (width, height))
    else:
        surface = pygame.Surface((width, height))
        surface.fill(fallback_color)
        return surface

player_img = load_image("player.png", player_width, player_height, WHITE)
meteor_img = load_image("meteor.png", object_width, object_height, (255, 0, 0))
alien_img = load_image("alien.png", object_width, object_height, (0, 255, 0))
part_img = load_image("part.png", 20, 20, (0, 0, 255))
backgrounds = [load_image(bg, WIDTH, HEIGHT, BLACK) for bg in backgrounds]

def draw_player():
    screen.blit(player_img, (player_x, player_y))

def draw_objects(objects, img):
    for obj in objects:
        screen.blit(img, (obj.x, obj.y))

def check_collision(obj1, obj2):
    return obj1.colliderect(obj2)

def reset_game():
    global meteors, aliens, spaceship_parts, player_x, player_y, is_jumping, player_y_velocity, parts_collected, current_level
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 10
    is_jumping = False
    player_y_velocity = 0
    meteors.clear()
    aliens.clear()
    spaceship_parts.clear()
    parts_collected = 0
    current_level = 0

running = True
while running:
    screen.blit(backgrounds[current_level], (0, 0))
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_velocity
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_velocity
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        player_y_velocity = jump_height

    player_y_velocity += gravity
    player_y += player_y_velocity

    if player_y >= HEIGHT - player_height:
        player_y = HEIGHT - player_height
        is_jumping = False
        player_y_velocity = 0

    if random.randint(1, 30) == 1:
        meteors.append(pygame.Rect(random.randint(0, WIDTH - object_width), -object_height, object_width, object_height))
    if random.randint(1, 50) == 1:
        aliens.append(pygame.Rect(random.randint(0, WIDTH - object_width), -object_height, object_width, object_height))
    if random.randint(1, 40) == 1:
        spaceship_parts.append(pygame.Rect(random.randint(0, WIDTH - 20), -20, 20, 20))

    for meteor in meteors[:]:
        meteor.y += object_velocity
        if meteor.y > HEIGHT:
            meteors.remove(meteor)
        elif check_collision(pygame.Rect(player_x, player_y, player_width, player_height), meteor):
            reset_game()

    for alien in aliens[:]:
        alien.y += object_velocity
        if alien.y > HEIGHT:
            aliens.remove(alien)
        elif check_collision(pygame.Rect(player_x, player_y, player_width, player_height), alien):
            reset_game()

    for part in spaceship_parts[:]:
        part.y += object_velocity
        if part.y > HEIGHT:
            spaceship_parts.remove(part)
        elif check_collision(pygame.Rect(player_x, player_y, player_width, player_height), part):
            spaceship_parts.remove(part)
            parts_collected += 1

            if parts_collected % 10 == 0 and current_level < len(LEVELS) - 1:
                current_level += 1

    draw_player()
    draw_objects(meteors, meteor_img)
    draw_objects(aliens, alien_img)
    draw_objects(spaceship_parts, part_img)

    score_text = font.render(f"Parts Collected: {parts_collected}", True, WHITE)
    level_text = font.render(f"Planet: {LEVELS[current_level]}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.update()

pygame.quit()
