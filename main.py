import pygame
import random

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Runner')

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 50)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # Power-up color

# Constants
GROUND_HEIGHT = HEIGHT - 50

# Obstacle dimensions and positions
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50

LOW_OBSTACLE_WIDTH = 50
LOW_OBSTACLE_HEIGHT = 30
LOW_OBSTACLE_Y = GROUND_HEIGHT - LOW_OBSTACLE_HEIGHT  # Position just above the ground

HIGH_OBSTACLE_WIDTH = 50
HIGH_OBSTACLE_HEIGHT = 70
HIGH_OBSTACLE_Y = GROUND_HEIGHT - HIGH_OBSTACLE_HEIGHT - 100  # Elevated position for high obstacles

PLAYER_WIDTH, PLAYER_HEIGHT = 50, 60
ROLL_HEIGHT = 30
JUMPING_HEIGHT = 90
PLAYER_X = 100
player_y = GROUND_HEIGHT - PLAYER_HEIGHT
player_velocity_y = 0
GRAVITY = 0.5
JUMP_VELOCITY = -10        # Normal jump velocity
SUPER_JUMP_VELOCITY = -20  # Super jump velocity
DUCK_VELOCITY = 5
FPS = 60

# Image file paths
BACKGROUND_IMAGE_PATH = 'images/bg.png'
RUNNER_IMAGES_PATHS = [
    'images/runner1.png',
    'images/runner2.png',
    'images/runner3.png'
]
RUNNER_JUMP_IMAGE_PATH = 'images/runner_jump.png'
RUNNER_SLIDE_IMAGE_PATH = 'images/runner_slide.png'

HIGH_OBJECT_IMAGES = [
    'images/object_high1.png',
    'images/object_high2.png'
]

LONG_OBJECT_IMAGES = [
    'images/object_long1.png',
    'images/object_long2.png',
    'images/object_long3.png',
    'images/object_long4.png'
]

NORMAL_OBJECT_IMAGES = [
    'images/object1.png',
    'images/object2.png',
    'images/object3.png'
]

# Load and scale images
background = pygame.image.load(BACKGROUND_IMAGE_PATH)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

runner_images = [
    pygame.transform.scale(pygame.image.load(img), (PLAYER_WIDTH, PLAYER_HEIGHT))
    for img in RUNNER_IMAGES_PATHS
]
runner_jump_image = pygame.transform.scale(pygame.image.load(RUNNER_JUMP_IMAGE_PATH), (PLAYER_WIDTH, JUMPING_HEIGHT))
runner_slide_image = pygame.transform.scale(pygame.image.load(RUNNER_SLIDE_IMAGE_PATH), (PLAYER_WIDTH, ROLL_HEIGHT))

# Load and scale object images
high_object_images = [pygame.image.load(img) for img in HIGH_OBJECT_IMAGES]
long_object_images = [pygame.image.load(img) for img in LONG_OBJECT_IMAGES]
normal_object_images = [pygame.image.load(img) for img in NORMAL_OBJECT_IMAGES]

player_x = PLAYER_X
jumping = False
ducking = False
double_jumped = False
obstacles = []
power_ups = []
obstacle_frequency = 1500
power_up_frequency = 10000  # Reduced frequency
score = 0
invincible = False
invincible_start_time = 0
power_up_speed = 20  # Increased speed boost

clock = pygame.time.Clock()
runner_frame = 0

def draw_player(x, y, is_ducking, is_jumping):
    global runner_frame
    
    if is_jumping:
        screen.blit(runner_jump_image, (x, y))
    elif is_ducking:
        screen.blit(runner_slide_image, (x, y + (PLAYER_HEIGHT - ROLL_HEIGHT)))
    else:
        screen.blit(runner_images[runner_frame // 5], (x, y))
        runner_frame = (runner_frame + 1) % 15  # Change frame every 5 ticks (adjust for smoothness)

def draw_obstacle(x, y, image, width, height):
    image_scaled = pygame.transform.scale(image, (width, height))
    screen.blit(image_scaled, (x, y))

def draw_power_up(x, y, color):
    pygame.draw.circle(screen, color, (x + OBSTACLE_WIDTH // 2, y + OBSTACLE_HEIGHT // 2), 20)

def update_score():
    global score
    score += 1

def draw_score():
    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))

def handle_obstacle_collision(player_rect, obstacle_rect, obs_type):
    if player_rect.colliderect(obstacle_rect):
        if obs_type == 'low' and not ducking:
            return True
        elif obs_type == 'high' and not jumping:
            return True
    return False

def handle_power_up_collision(player_rect, power_up_rect):
    return player_rect.colliderect(power_up_rect)

def game_loop():
    global player_y, player_velocity_y, jumping, ducking, double_jumped
    global obstacles, power_ups, obstacle_frequency, power_up_frequency
    global score, invincible, invincible_start_time

    running = True
    last_obstacle_time = pygame.time.get_ticks()
    last_power_up_time = pygame.time.get_ticks()
    speed = DUCK_VELOCITY

    while running:
        dt = clock.tick(FPS)
        screen.blit(background, (0, 0))
        
        pygame.draw.rect(screen, GRAY, [0, GROUND_HEIGHT, WIDTH, HEIGHT - GROUND_HEIGHT])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        
        # Handle normal jump
        if keys[pygame.K_UP]:
            if not jumping:
                jumping = True
                player_velocity_y = JUMP_VELOCITY
        
        # Handle super jump
        if keys[pygame.K_SPACE]:
            if not jumping and not double_jumped:
                double_jumped = True
                jumping = True
                player_velocity_y = SUPER_JUMP_VELOCITY
        
        if keys[pygame.K_DOWN] and not jumping:
            ducking = True
        else:
            ducking = False
        
        if jumping:
            player_velocity_y += GRAVITY
            player_y += player_velocity_y
            if player_y >= GROUND_HEIGHT - PLAYER_HEIGHT:
                player_y = GROUND_HEIGHT - PLAYER_HEIGHT
                jumping = False
                double_jumped = False
                player_velocity_y = 0
        
        player_height = ROLL_HEIGHT if ducking else PLAYER_HEIGHT
        player_actual_y = player_y + (PLAYER_HEIGHT - ROLL_HEIGHT) if ducking else player_y
        player_rect = pygame.Rect(player_x, player_actual_y, PLAYER_WIDTH, player_height)
        
        if pygame.time.get_ticks() - last_obstacle_time > obstacle_frequency:
            obs_x = WIDTH
            obs_type = random.choice(['normal', 'low', 'high'])
            if obs_type == 'normal':
                obs_y = GROUND_HEIGHT - OBSTACLE_HEIGHT
                obs_width = OBSTACLE_WIDTH
                obs_height = OBSTACLE_HEIGHT
                obs_image = random.choice(normal_object_images)
            elif obs_type == 'low':
                obs_y = LOW_OBSTACLE_Y
                obs_width = LOW_OBSTACLE_WIDTH
                obs_height = LOW_OBSTACLE_HEIGHT
                obs_image = random.choice(long_object_images)
            else:
                obs_y = HIGH_OBSTACLE_Y
                obs_width = HIGH_OBSTACLE_WIDTH
                obs_height = HIGH_OBSTACLE_HEIGHT
                obs_image = random.choice(high_object_images)
            obstacles.append([obs_x, obs_y, obs_width, obs_height, obs_image, obs_type])
            last_obstacle_time = pygame.time.get_ticks()
        
        if pygame.time.get_ticks() - last_power_up_time > power_up_frequency:
            pu_x = WIDTH
            pu_y = GROUND_HEIGHT - OBSTACLE_HEIGHT - 200  # Higher y for double jump
            power_ups.append([pu_x, pu_y])
            last_power_up_time = pygame.time.get_ticks()

        obstacles = [[x - speed, y, w, h, img, obs_type] for x, y, w, h, img, obs_type in obstacles if x > -OBSTACLE_WIDTH]
        power_ups = [[x - speed, y] for x, y in power_ups if x > -20]

        for obs_x, obs_y, obs_width, obs_height, obs_image, obs_type in obstacles:
            obstacle_rect = pygame.Rect(obs_x, obs_y, obs_width, obs_height)
            draw_obstacle(obs_x, obs_y, obs_image, obs_width, obs_height)
            if handle_obstacle_collision(player_rect, obstacle_rect, obs_type) and not invincible:
                running = False
        
        for pu_x, pu_y in power_ups:
            power_up_rect = pygame.Rect(pu_x, pu_y, 40, 40)  # Power-up size
            draw_power_up(pu_x, pu_y, YELLOW)
            if handle_power_up_collision(player_rect, power_up_rect):
                invincible = True
                invincible_start_time = pygame.time.get_ticks()
                speed = power_up_speed
                power_ups.remove([pu_x, pu_y])
        
        if invincible and pygame.time.get_ticks() - invincible_start_time > 5000:
            invincible = False
            speed = DUCK_VELOCITY
        
        update_score()
        draw_score()
        
        draw_player(player_x, player_y, ducking, jumping)
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    game_loop()
