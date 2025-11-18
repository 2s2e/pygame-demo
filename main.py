import random
import pygame
import sys


# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (30, 30, 30)
INGREDIENTS = [
    {"name": "Bok Choy", "points": 5},
    {"name": "Mushroom", "points": 3},
    {"name": "Enoki Mushroom", "points": 4},
    {"name": "Napa Cabbage", "points": 2},
    {"name": "Fish Cake", "points": 6},
    {"name": "Tofu", "points": 4},
    {"name": "Lotus Root", "points": 5},
    {"name": "Udon Noodles", "points": 3},
    {"name": "Beef Slice", "points": 7},
    {"name": "Shrimp", "points": 6},
    {"name": "Fish", "points": 5},
    {"name": "Fish Ball", "points": 4},
]

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Demo")

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# --- Player settings ---
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 20
player_x = WIDTH // 2 - PLAYER_WIDTH // 2
player_y = HEIGHT - PLAYER_HEIGHT - 10
player_speed = 6

# --- Falling object settings ---
DROP_WIDTH = 30
DROP_HEIGHT = 30
DROP_TIME = 1000  # milliseconds
drop_x = random.randint(0, WIDTH - DROP_WIDTH)
drop_y = -DROP_HEIGHT  # start above the screen
drop_speed = 5
drop_timer = 0

# ---Scoring---
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True


class Ingredient:
    def __init__(self, name, points, width=30, height=30, speed=5):
        self.name = name
        self.points = points
        self.width = width
        self.height = height
        self.speed = speed

        # Start at a random horizontal position, above the screen
        self.x = random.randint(0, WIDTH - width)
        self.y = -height

        # Pre-build a color (or you could set one based on name)
        self.color = (255, 200, 0)  # default yellow-ish

    def update(self):
        """Move downward each frame."""
        self.y += self.speed

        # If it falls off the bottom: reset to the top
        if self.y > HEIGHT:
            self.reset()

    def reset(self):
        """Move back to the top at a random x."""
        self.y = -self.height
        self.x = random.randint(0, WIDTH - self.width)

    def get_rect(self):
        """Return a pygame.Rect for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())


# objects
ingredients = []


# SHOWCASE
while running:
    # Handle events
    # SHOWCASE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Keep player inside screen bounds
    if player_x < 0:
        player_x = 0
    if player_x > WIDTH - PLAYER_WIDTH:
        player_x = WIDTH - PLAYER_WIDTH

    # ---- Drop movement ----
    # drop_y += drop_speed

    for ingredient in ingredients:
        ingredient.update()
        ingredient.draw(screen)

        # Remove ingredient if it goes off the bottom
        if ingredient.y > HEIGHT:
            ingredients.remove(ingredient)

    # Fill the screen with background color
    screen.fill(BACKGROUND_COLOR)

    # ---- Build rects for player  ----
    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)

    # ---- Build rects for ingredients
    # drop_rect = pygame.Rect(drop_x, drop_y, DROP_WIDTH, DROP_HEIGHT)
    for ingredient in ingredients:
        drop_rect = ingredient.get_rect()
        pygame.draw.rect(
            screen,
            ingredient.color,
            drop_rect,
        )
        # ---- Collision check ----
        if player_rect.colliderect(drop_rect):
            score += ingredient.points
            ingredients.remove(ingredient)

    # Draw the player
    pygame.draw.rect(
        screen,
        (0, 180, 255),  # cyan-ish color
        (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT),
    )

    # Spawn falling object
    if drop_timer <= 0:
        # reset the drop timer
        drop_timer = random.randint(DROP_TIME - 500, DROP_TIME + 500)  # reset timer
        ingredient = random.choice(INGREDIENTS)
        # create the ingredient object
        ingredient_obj = Ingredient(
            name=ingredient["name"],
            points=ingredient["points"],
            width=DROP_WIDTH,
            height=DROP_HEIGHT,
            speed=drop_speed,
        )
        ingredients.append(ingredient_obj)
    else:
        drop_timer -= clock.get_time()

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
