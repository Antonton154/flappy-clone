import pygame
import random
import sys

velocity = 0
gravity = 0.05
jump = -1.5

screen = pygame.display.set_mode((288, 512))

background = pygame.image.load("assets/background-day.png").convert()
background = pygame.transform.scale(background, (288,512))

floor = pygame.image.load("assets/base.png").convert()
floor_x = 0
floor_movement = -1

bird = pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()
bird_rect = bird.get_rect(center = (50,225))

game_over_screen = pygame.image.load("assets/gameover.png").convert_alpha()
game_over_rect = game_over_screen.get_rect(center = (144, 100))

message = pygame.image.load("assets/message.png").convert_alpha()
message_rect = game_over_screen.get_rect(center = (144, 60))

bottom_pipe_image = pygame.image.load("assets/pipe-green.png").convert()
top_pipe_image = pygame.transform.rotate(bottom_pipe_image, 180)
pipe_list = []

SPAWNPIPE = pygame.USEREVENT

pygame.display.set_caption("Flappy Bird")
pygame.display.set_icon(bird)

clock = pygame.time.Clock()

game_over = False
start = False

def spawnPipe():
    height  = random.randint(150, 350)
    bottom_pipe = bottom_pipe_image.get_rect(topleft = (288, height))
    top_pipe = top_pipe_image.get_rect(bottomleft = (288 , height-100))
    return bottom_pipe, top_pipe

def movePipes(pipes):
    for pipe_pair in pipes:
        for pipe in pipe_pair:
            pipe.centerx -= 1
    return pipes
 
def drawPipes(pipes):
    for pipe in pipes:
        screen.blit(top_pipe_image, pipe[1])
        screen.blit(bottom_pipe_image, pipe[0])

def check_collision(pipes):
    if bird_rect.bottom > 400:
        return True
    for pipe_pair in pipe_list:
        for pipe in pipe_pair:
            if bird_rect.colliderect(pipe):
                return True
    return False

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if (not start) and (event.key == pygame.K_SPACE):
                start = True
                pygame.time.set_timer(SPAWNPIPE, 1800)
            if (not game_over) and (event.key == pygame.K_SPACE):
                velocity = 0
                velocity += jump
        if not game_over and start and event.type == SPAWNPIPE:
            pipe_list.append(spawnPipe())

    screen.blit(background, (0,0))
    drawPipes(pipe_list)
    screen.blit(bird, bird_rect)
    screen.blit(floor, (floor_x, 400))

    if not start:
        screen.blit(message, message_rect)
    else:
        if not game_over:
            floor_x += floor_movement
            if floor_x == -48:
                floor_x = 0
            movePipes(pipe_list)
            velocity += gravity
            bird_rect.centery += velocity
            if bird_rect.top < 0:
                bird_rect.top = 0
                velocity = 0
            game_over = check_collision(pipe_list)
        else: 
            screen.blit(game_over_screen, game_over_rect)

    pygame.display.update()
    clock.tick(120)