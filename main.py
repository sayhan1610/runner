import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Infinite Runner Game')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

GROUND_HEIGHT = HEIGHT - 50
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
JUMP_HEIGHT = 150
ROLL_WIDTH = 50
ROLL_HEIGHT = 30

player_width, player_height = 50, 60
player_x = 100
player_y = GROUND_HEIGHT - player_height
player_velocity_y = 0
gravity = 0.5
jumping = False
rolling = False

obstacles = []
obstacle_timer = 0
obstacle_frequency = 1500

clock = pygame.time.Clock()
FPS = 60

def draw_player(x, y):
    pygame.draw.rect(screen, BLACK, [x, y, player_width, player_height])

def draw_obstacle(x, y, width, height):
    pygame.draw.rect(screen, RED, [x, y, width, height])

def game_loop():
    global player_x, player_y, player_velocity_y, jumping, rolling
    global obstacles, obstacle_timer, obstacle_frequency

    running = True
    last_obstacle_time = pygame.time.get_ticks()
    
    while running:
        dt = clock.tick(FPS)
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE] and not jumping and not rolling:
            jumping = True
            player_velocity_y = -10
        
        if keys[pygame.K_DOWN] and not jumping and not rolling:
            rolling = True
        
        if jumping:
            player_velocity_y += gravity
            player_y += player_velocity_y
            if player_y >= GROUND_HEIGHT - player_height:
                player_y = GROUND_HEIGHT - player_height
                jumping = False
                player_velocity_y = 0
        
        if rolling:
            rolling = False
        
        if pygame.time.get_ticks() - last_obstacle_time > obstacle_frequency:
            obs_x = WIDTH
            obs_y = GROUND_HEIGHT - OBSTACLE_HEIGHT
            obstacles.append([obs_x, obs_y])
            last_obstacle_time = pygame.time.get_ticks()
        
        obstacles = [[x - 5, y] for x, y in obstacles if x > -OBSTACLE_WIDTH]
        
        for obs_x, obs_y in obstacles:
            draw_obstacle(obs_x, obs_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
            if player_x + player_width > obs_x and player_x < obs_x + OBSTACLE_WIDTH:
                if player_y + player_height > obs_y:
                    if not jumping and not rolling:
                        running = False
        
        draw_player(player_x, player_y)
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    game_loop()
