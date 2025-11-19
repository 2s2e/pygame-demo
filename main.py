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
GRAVITY = 9.8 / FPS  # simulate gravity for falling objects
player_x = WIDTH // 2 - PLAYER_WIDTH // 2
player_y = HEIGHT - PLAYER_HEIGHT - 10
player_speed = 6

# --- Falling object settings ---
ITEM_WIDTH = 30
ITEM_HEIGHT = 30
START_HEIGHT = 100
DROP_TIME = 500  # milliseconds
MAX_X_SPEED = 10
MIN_X_SPEED = 5
drop_x = random.randint(0, WIDTH - ITEM_WIDTH)
drop_y = -ITEM_HEIGHT  # start above the screen
drop_speed = 5
drop_timer = 0
# spawn points for ingredients
spawn_points = [(0, START_HEIGHT), (WIDTH, START_HEIGHT)]

# ---Scoring---
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True


class Ingredient:
    def __init__(
        self, name, points, width=30, height=30, speed=5, start_x=None, start_y=None
    ):
        self.name = name
        self.points = points
        self.width = width
        self.height = height
        self.speed_x = speed
        self.speed_y = -3

        # Start at a random horizontal position, above the screen
        self.x = start_x if start_x is not None else random.randint(0, WIDTH - width)
        self.y = start_y if start_y is not None else -height

        # Pre-build a color (or you could set one based on name)
        self.color = (255, random.randint(100, 255), 0)  # default yellow-ish

    def update(self):
        """Move downward each frame."""
        self.speed_y += GRAVITY
        self.y += self.speed_y
        self.x += self.speed_x

        # If it falls off the bottom: reset to the top
        if self.y > HEIGHT:
            ingredients.remove(self)

    def get_rect(self):
        """Return a pygame.Rect for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())


# objects
ingredients = []


def spawn_ingredient(ingredients_list):
    # pick the ingredient
    ingredient = random.choice(INGREDIENTS)

    # pick the spawn point
    spawn_point = random.choice(spawn_points)

    # if its to the right, make it go left
    if spawn_point[0] > WIDTH // 2:
        speed_x = -random.randint(MIN_X_SPEED, MAX_X_SPEED)
    else:
        speed_x = random.randint(MIN_X_SPEED, MAX_X_SPEED)

    # create the ingredient object
    ingredient_obj = Ingredient(
        name=ingredient["name"],
        points=ingredient["points"],
        width=ITEM_WIDTH,
        height=ITEM_HEIGHT,
        speed=speed_x,
        start_x=spawn_point[0],
        start_y=spawn_point[1],
    )
    ingredients_list.append(ingredient_obj)


# when ingredients hit each other, they bounce off
def handle_collision(ing1, ing2):
    ing1.speed_x, ing2.speed_x = ing2.speed_x, ing1.speed_x


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

    # Fill the screen with background color
    screen.fill(BACKGROUND_COLOR)

    # update and draw ingredients
    for ingredient in ingredients[:]:
        ingredient.update()
        ingredient.draw(screen)

    # ---- Build rects for player  ----
    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)

    # ---- Do collision checks ----
    for ingredient in ingredients[:]:
        drop_rect = ingredient.get_rect()

        # ---- Collision check with player----
        if player_rect.colliderect(drop_rect):
            score += ingredient.points
            ingredients.remove(ingredient)
            continue  # Skip further checks for this ingredient

    # ---- Collision check with other ingredients----
    # This is a clever bit to show off
    for i in range(len(ingredients)):
        for j in range(i + 1, len(ingredients)):
            rect1 = ingredients[i].get_rect()
            rect2 = ingredients[j].get_rect()
            if rect1.colliderect(rect2):
                handle_collision(ingredients[i], ingredients[j])

    # Draw the player
    pygame.draw.rect(
        screen,
        (0, 180, 255),  # cyan-ish color
        (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT),
    )

    # Spawn falling object
    if drop_timer <= 0:
        spawn_ingredient(ingredients)
        drop_timer = random.randint(DROP_TIME - 500, DROP_TIME + 500)  # reset timer
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
