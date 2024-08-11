import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Runner')

WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 50)
BLUE = (0, 0, 255)

GROUND_HEIGHT = HEIGHT - 50
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
LOW_OBSTACLE_HEIGHT = 30
LOW_OBSTACLE_Y = GROUND_HEIGHT - 80
HIGH_OBSTACLE_HEIGHT = 70

PLAYER_WIDTH, PLAYER_HEIGHT = 50, 60
ROLL_HEIGHT = 30
PLAYER_X = 100
player_y = GROUND_HEIGHT - PLAYER_HEIGHT
player_velocity_y = 0
GRAVITY = 0.5
JUMP_VELOCITY = -10
DUCK_VELOCITY = 5
FPS = 60

background = pygame.image.load('images/bg.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

player_x = PLAYER_X
jumping = False
ducking = False
obstacles = []
obstacle_frequency = 1500
score = 0

clock = pygame.time.Clock()

def draw_player(x, y, is_ducking):
    height = ROLL_HEIGHT if is_ducking else PLAYER_HEIGHT
    pygame.draw.rect(screen, WHITE, [x, y + (PLAYER_HEIGHT - height) if is_ducking else y, PLAYER_WIDTH, height])

def draw_obstacle(x, y, width, height, color):
    pygame.draw.rect(screen, color, [x, y, width, height])

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

def game_loop():
    global player_y, player_velocity_y, jumping, ducking
    global obstacles, obstacle_frequency, score

    running = True
    last_obstacle_time = pygame.time.get_ticks()
    
    while running:
        dt = clock.tick(FPS)
        screen.blit(background, (0, 0))
        
        pygame.draw.rect(screen, GRAY, [0, GROUND_HEIGHT, WIDTH, HEIGHT - GROUND_HEIGHT])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP] and not jumping and not ducking:
            jumping = True
            player_velocity_y = JUMP_VELOCITY
        
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
                player_velocity_y = 0
        
        player_height = ROLL_HEIGHT if ducking else PLAYER_HEIGHT
        player_actual_y = player_y + (PLAYER_HEIGHT - ROLL_HEIGHT) if ducking else player_y
        player_rect = pygame.Rect(player_x, player_actual_y, PLAYER_WIDTH, player_height)
        
        if pygame.time.get_ticks() - last_obstacle_time > obstacle_frequency:
            obs_x = WIDTH
            obs_type = random.choice(['normal', 'low', 'high'])
            if obs_type == 'normal':
                obs_y = GROUND_HEIGHT - OBSTACLE_HEIGHT
                obs_height = OBSTACLE_HEIGHT
                obs_color = RED
            elif obs_type == 'low':
                obs_y = LOW_OBSTACLE_Y
                obs_height = LOW_OBSTACLE_HEIGHT
                obs_color = GREEN
            else:
                obs_y = GROUND_HEIGHT - HIGH_OBSTACLE_HEIGHT
                obs_height = HIGH_OBSTACLE_HEIGHT
                obs_color = BLUE
            obstacles.append([obs_x, obs_y, obs_height, obs_color, obs_type])
            last_obstacle_time = pygame.time.get_ticks()
        
        obstacles = [[x - DUCK_VELOCITY, y, h, color, obs_type] for x, y, h, color, obs_type in obstacles if x > -OBSTACLE_WIDTH]
        
        for obs_x, obs_y, obs_height, obs_color, obs_type in obstacles:
            obstacle_rect = pygame.Rect(obs_x, obs_y, OBSTACLE_WIDTH, obs_height)
            draw_obstacle(obs_x, obs_y, OBSTACLE_WIDTH, obs_height, obs_color)
            if handle_obstacle_collision(player_rect, obstacle_rect, obs_type):
                running = False
        
        update_score()
        draw_score()
        
        draw_player(player_x, player_y, ducking)
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    game_loop()
