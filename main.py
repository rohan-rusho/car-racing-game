import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Car Racing Game")
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 36)

# Constants
CAR_WIDTH, CAR_HEIGHT = 48, 96
ROAD_SPEED = 5
score_file = "best_score.txt"

# Load road image
road_img = pygame.image.load("assets/road.png")
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

# Load car images
player_car = pygame.transform.smoothscale(
    pygame.image.load("assets/car.png").convert_alpha(), (CAR_WIDTH, CAR_HEIGHT)
)

# Load enemy cars from car1.png to car5.png
enemy_car_filenames = [f"car{i}.png" for i in range(1, 6)]
enemy_car_images = [
    pygame.transform.smoothscale(
        pygame.image.load(f"assets/{filename}").convert_alpha(), (CAR_WIDTH, CAR_HEIGHT)
    )
    for filename in enemy_car_filenames
]

def load_best_score():
    if not os.path.exists(score_file):
        return 0
    with open(score_file, "r") as f:
        return int(f.read())

def save_best_score(score):
    with open(score_file, "w") as f:
        f.write(str(score))

def draw_text(text, font, color, surface, x, y, outline_color=(0, 0, 0)):
    outline = font.render(text, True, outline_color)
    text_surface = font.render(text, True, color)
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            surface.blit(outline, (x + dx, y + dy))
    surface.blit(text_surface, (x, y))

def show_menu(title_text, options):
    selected = 0
    while True:
        screen.fill((30, 30, 30))
        title = big_font.render(title_text, True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (200, 200, 200)
            option_rendered = font.render(option, True, color)
            screen.blit(option_rendered, (WIDTH // 2 - option_rendered.get_width() // 2, 200 + i * 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected > 0:
                    selected -= 1
                elif event.key == pygame.K_DOWN and selected < len(options) - 1:
                    selected += 1
                elif event.key == pygame.K_RETURN:
                    return options[selected]

def get_random_enemy_car():
    return random.choice(enemy_car_images)

def start_game(difficulty):
    speeds = {
        "Easy": (3, 0.1),
        "Normal": (5, 0.2),
        "Hard": (7, 0.3),
        "Impossible": (10, 0.5)
    }

    enemy_speed, speed_increase = speeds[difficulty]
    player_x = WIDTH // 2 - CAR_WIDTH // 2
    player_y = HEIGHT - 120
    enemy_x = random.randint(50, WIDTH - CAR_WIDTH - 50)
    enemy_y = -CAR_HEIGHT
    score = 0
    best_score = load_best_score()

    enemy_car = get_random_enemy_car()

    road_y1 = 0
    road_y2 = -HEIGHT

    running = True
    while running:
        clock.tick(FPS)

        # Scroll road
        road_y1 += ROAD_SPEED
        road_y2 += ROAD_SPEED
        if road_y1 >= HEIGHT:
            road_y1 = -HEIGHT
        if road_y2 >= HEIGHT:
            road_y2 = -HEIGHT
        screen.blit(road_img, (0, road_y1))
        screen.blit(road_img, (0, road_y2))

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 5
        if keys[pygame.K_RIGHT] and player_x < WIDTH - CAR_WIDTH:
            player_x += 5

        # Enemy movement
        enemy_y += enemy_speed
        if enemy_y > HEIGHT:
            enemy_y = -CAR_HEIGHT
            enemy_x = random.randint(50, WIDTH - CAR_WIDTH - 50)
            enemy_car = get_random_enemy_car()
            score += 1
            enemy_speed += speed_increase

        # Draw cars
        screen.blit(player_car, (player_x, player_y))
        screen.blit(enemy_car, (enemy_x, enemy_y))

        # Collision
        player_rect = pygame.Rect(player_x, player_y, CAR_WIDTH, CAR_HEIGHT)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, CAR_WIDTH, CAR_HEIGHT)
        if player_rect.colliderect(enemy_rect):
            if score > best_score:
                save_best_score(score)
            game_over(score, best_score)
            return

        # HUD
        draw_text(f"Score: {score}", font, (255, 255, 255), screen, 10, 10)
        draw_text(f"Best: {max(score, best_score)}", font, (255, 255, 0), screen, WIDTH - 140, 10)
        draw_text(f"Level: {difficulty}", font, (200, 200, 255), screen, WIDTH // 2 - 50, 10)

        pygame.display.update()

def game_over(score, best_score):
    while True:
        screen.fill((50, 0, 0))

        game_over_text = big_font.render("GAME OVER", True, (255, 0, 0))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        best_text = font.render(f"Best: {max(score, best_score)}", True, (255, 255, 0))
        restart_text = font.render("Press R to Restart", True, (200, 255, 200))
        quit_text = font.render("Press Q to return to Menu", True, (255, 255, 255))

        screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, 200))
        screen.blit(score_text, ((WIDTH - score_text.get_width()) // 2, 270))
        screen.blit(best_text, ((WIDTH - best_text.get_width()) // 2, 310))
        screen.blit(restart_text, ((WIDTH - restart_text.get_width()) // 2, 370))
        screen.blit(quit_text, ((WIDTH - quit_text.get_width()) // 2, 410))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return
                elif event.key == pygame.K_r:
                    return

# Game loop
while True:
    selected_level = show_menu("Select Difficulty", ["Easy", "Normal", "Hard", "Impossible", "Quit"])
    if selected_level == "Quit":
        pygame.quit()
        sys.exit()
    start_game(selected_level)
