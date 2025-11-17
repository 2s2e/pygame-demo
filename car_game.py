# A simple car game using pygame
import pygame
import random
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Game")

# Function to draw a car
def draw_car(screen, x, y, width, height, color):
    # Car body
    pygame.draw.rect(screen, color, (x, y + height * 0.2, width, height * 0.6), border_radius=5)
    # Car top (cabin)
    pygame.draw.rect(screen, color, (x + width * 0.15, y, width * 0.7, height * 0.5), border_radius=8)
    # Windows
    window_color = (150, 200, 255)
    pygame.draw.rect(screen, window_color, (x + width * 0.2, y + height * 0.05, width * 0.25, height * 0.3))
    pygame.draw.rect(screen, window_color, (x + width * 0.55, y + height * 0.05, width * 0.25, height * 0.3))
    # Wheels
    wheel_color = (30, 30, 30)
    pygame.draw.circle(screen, wheel_color, (int(x + width * 0.25), int(y + height * 0.85)), int(width * 0.15))
    pygame.draw.circle(screen, wheel_color, (int(x + width * 0.75), int(y + height * 0.85)), int(width * 0.15))
    # Wheel rims
    pygame.draw.circle(screen, (100, 100, 100), (int(x + width * 0.25), int(y + height * 0.85)), int(width * 0.08))
    pygame.draw.circle(screen, (100, 100, 100), (int(x + width * 0.75), int(y + height * 0.85)), int(width * 0.08))
    # Headlights/taillights
    light_color = (255, 255, 0) if color == (0, 0, 255) else (255, 100, 100)
    pygame.draw.circle(screen, light_color, (int(x + width * 0.15), int(y + height * 0.9)), int(width * 0.08))
    pygame.draw.circle(screen, light_color, (int(x + width * 0.85), int(y + height * 0.9)), int(width * 0.08))

def draw_car_with_tilt(screen, x, y, width, height, color, target_x, current_x):
    """Draw car with slight tilt when changing lanes"""
    # Calculate tilt based on direction of movement
    tilt_offset = 0
    if current_x < target_x:
        tilt_offset = 2  # Tilting right
    elif current_x > target_x:
        tilt_offset = -2  # Tilting left
    
    # Draw car with slight vertical offset to simulate tilt
    draw_car(screen, x, y + tilt_offset, width, height, color)

# ------------------------------------------------------------
# Helpers: road drawing and game state management
# ------------------------------------------------------------
def draw_road(screen):
    """Draw background, road surface, dashed center line, and edges."""
    screen.fill(BACKGROUND_COLOR)
    # Road surface
    pygame.draw.rect(screen, ROAD_COLOR, (road_x, 0, road_width, screen_height))
    # Dashed center line (moving downward)
    center_line_x = road_x + lane_width
    y = line_offset
    while y < screen_height:
        pygame.draw.rect(screen, LINE_COLOR, (center_line_x - 2, y, 4, line_dash_height))
        y += line_dash_height + line_dash_gap
    # Road edges
    pygame.draw.rect(screen, LINE_COLOR, (road_x - 5, 0, 5, screen_height))
    pygame.draw.rect(screen, LINE_COLOR, (road_x + road_width, 0, 5, screen_height))

def create_obstacles(count=2, spacing=400):
    """Create a list of obstacle rects spaced vertically by `spacing`."""
    rects = []
    for i in range(count):
        lane_choice = random.choice([left_lane_center, right_lane_center])
        y_pos = -OBSTACLE_HEIGHT - (i * spacing)
        rects.append(pygame.Rect(lane_choice - OBSTACLE_WIDTH // 2, y_pos, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
    return rects

def reset_game():
    """Reset dynamic game state for a new run."""
    global game_over, score, obstacle_speed, current_lane, car_rect, target_x, obstacles
    game_over = False
    score = 0
    obstacle_speed = base_obstacle_speed
    current_lane = 0
    car_rect.x = left_lane_center - CAR_WIDTH // 2
    target_x = car_rect.x
    obstacles = create_obstacles(count=2, spacing=400)

# Simple sound effects using basic frequencies
# These create basic beep sounds without requiring external sound files
def play_score_sound():
    """Play a sound when scoring a point"""
    try:
        # Create a short high-pitched beep
        sound = pygame.mixer.Sound(buffer=bytes([
            int(128 + 127 * ((i % 20) < 10)) for i in range(2205)
        ]))
        sound.set_volume(0.3)
        sound.play()
    except:
        pass  # Sound not available

def play_crash_sound():
    """Play a sound when crashing"""
    try:
        # Create a longer low-pitched sound
        sound = pygame.mixer.Sound(buffer=bytes([
            int(128 + 127 * ((i % 50) < 25)) for i in range(6615)
        ]))
        sound.set_volume(0.5)
        sound.play()
    except:
        pass  # Sound not available

BACKGROUND_COLOR = (200, 200, 200)
ROAD_COLOR = (50, 50, 50)
LINE_COLOR = (255, 255, 255)
CAR_COLOR = (0, 0, 255)
OBSTACLE_COLOR = (255, 0, 0)
CAR_WIDTH = 50
CAR_HEIGHT = 100
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 100
# Road and lane settings
road_width = 400
road_x = (screen_width - road_width) // 2
lane_width = road_width // 2
left_lane_center = road_x + lane_width // 2
right_lane_center = road_x + lane_width + lane_width // 2
line_dash_height = 40
line_dash_gap = 20
line_offset = 0
car_rect = pygame.Rect(left_lane_center - CAR_WIDTH // 2, screen_height - CAR_HEIGHT - 10, CAR_WIDTH, CAR_HEIGHT)
# Start obstacles in random lanes - now using a list for multiple obstacles
obstacles = []
# Create initial obstacles with varying starting positions
for i in range(2):
    lane_choice = random.choice([left_lane_center, right_lane_center])
    y_pos = -OBSTACLE_HEIGHT - (i * 400)  # More space between obstacles
    obstacles.append(pygame.Rect(lane_choice - OBSTACLE_WIDTH // 2, y_pos, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

current_lane = 0  # 0 for left lane, 1 for right lane
target_x = car_rect.x  # Target x position for smooth movement
lane_switch_speed = 8  # Speed of lane switching animation
car_speed = 20
base_obstacle_speed = 20
obstacle_speed = base_obstacle_speed
boost_multiplier = 2.0  # Speed multiplier when boosting
score = 0

font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)
clock = pygame.time.Clock()
running = True
game_over = False

# Button rectangles for game over screen
play_again_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 100, 200, 50)
exit_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 170, 200, 50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle mouse clicks on game over buttons
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = event.pos
            if play_again_button.collidepoint(mouse_pos):
                # Reset game via helper
                reset_game()
            elif exit_button.collidepoint(mouse_pos):
                running = False
    
    if not game_over:
        keys = pygame.key.get_pressed()
        # Switch lanes with left/right arrow keys - set target position
        if keys[pygame.K_LEFT] and current_lane == 1:
            current_lane = 0
            target_x = left_lane_center - CAR_WIDTH // 2
        if keys[pygame.K_RIGHT] and current_lane == 0:
            current_lane = 1
            target_x = right_lane_center - CAR_WIDTH // 2
        
        # Smoothly move car towards target position
        if car_rect.x < target_x:
            car_rect.x = min(car_rect.x + lane_switch_speed, target_x)
        elif car_rect.x > target_x:
            car_rect.x = max(car_rect.x - lane_switch_speed, target_x)
        
        # Apply boost when up arrow is pressed
        current_speed = obstacle_speed
        if keys[pygame.K_UP]:
            current_speed = obstacle_speed * boost_multiplier
        
        # Animate the center line
        line_offset += current_speed
        if line_offset > line_dash_height + line_dash_gap:
            line_offset = 0
    
    if not game_over:
        # Use boosted speed if up arrow is pressed
        keys = pygame.key.get_pressed()
        current_speed = obstacle_speed
        if keys[pygame.K_UP]:
            current_speed = obstacle_speed * boost_multiplier
        
        # Update all obstacles
        for obstacle_rect in obstacles:
            obstacle_rect.y += current_speed
            
            # Reset obstacle if it goes off screen
            if obstacle_rect.top > screen_height:
                score += 1
                play_score_sound()  # Play sound when scoring
                # Increase speed every 5 points (less aggressive)
                obstacle_speed = base_obstacle_speed + (score // 5) * 1
                lane_choice = random.choice([left_lane_center, right_lane_center])
                obstacle_rect.x = lane_choice - OBSTACLE_WIDTH // 2
                obstacle_rect.y = -OBSTACLE_HEIGHT - random.randint(50, 200)  # More spacing
            
            # Check collision with any obstacle
            if car_rect.colliderect(obstacle_rect):
                game_over = True
                play_crash_sound()  # Play sound when crashing
                break
    # Draw static road elements
    draw_road(screen)
    
    # Draw cars
    draw_car_with_tilt(screen, car_rect.x, car_rect.y, CAR_WIDTH, CAR_HEIGHT, CAR_COLOR, target_x, car_rect.x)
    # Draw all obstacle cars
    for obstacle_rect in obstacles:
        draw_car(screen, obstacle_rect.x, obstacle_rect.y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_COLOR)
    
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    # Show boost indicator when boosting
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            boost_text = font.render("BOOST!", True, (255, 165, 0))
            screen.blit(boost_text, (10, 50))
    
    # Display Game Over screen
    if game_over:
        # Semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(game_over_text, game_over_rect)
        
        # Final score text
        final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        final_score_rect = final_score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 30))
        screen.blit(final_score_text, final_score_rect)
        
        # Get mouse position for button hover effect
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw Play Again button
        play_again_color = (0, 200, 0) if play_again_button.collidepoint(mouse_pos) else (0, 150, 0)
        pygame.draw.rect(screen, play_again_color, play_again_button, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), play_again_button, 3, border_radius=10)
        play_again_text = font.render("Play Again", True, (255, 255, 255))
        play_again_text_rect = play_again_text.get_rect(center=play_again_button.center)
        screen.blit(play_again_text, play_again_text_rect)
        
        # Draw Exit button
        exit_color = (200, 0, 0) if exit_button.collidepoint(mouse_pos) else (150, 0, 0)
        pygame.draw.rect(screen, exit_color, exit_button, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), exit_button, 3, border_radius=10)
        exit_text = font.render("Exit", True, (255, 255, 255))
        exit_text_rect = exit_text.get_rect(center=exit_button.center)
        screen.blit(exit_text, exit_text_rect)
    
    pygame.display.flip()
    clock.tick(30)  # Limit to 30 frames per second (lower = slower)
pygame.quit()
