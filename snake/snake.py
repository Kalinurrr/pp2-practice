import pygame 
import random
import sys

pygame.init()

#Game settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 20

#THe wall uses one cell around the playing area
WALL_SIZE = CELL_SIZE

#Snake starts with speed:
FPS = 8

#Level increases after this speed
FOODS_PER_LEVEL = 4

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 0, 0)
BLUE = (0, 120, 255)
GRAY = (80, 80, 80)

#Create display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")

#Fonts, shape,type
font_small = pygame.font.SysFont("Verdana", 22)
font_big = pygame.font.SysFont("Verdana", 50)

# Clock controls the game speed
clock = pygame.time.Clock()

#Function to draw the border wall
def draw_walls():
    #Top wall
    pygame.draw.rect(screen, GRAY, (0, 0, SCREEN_WIDTH, WALL_SIZE))

    #Bottom wall
    pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT-WALL_SIZE,SCREEN_WIDTH, WALL_SIZE))
    
    #Left wall
    pygame.draw.rect(screen, GRAY, (0, 0, WALL_SIZE,SCREEN_HEIGHT))

    #Right wall
    pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH- WALL_SIZE,0 ,WALL_SIZE,SCREEN_HEIGHT))

#Function to generate food position
def generate_food(snake_body):
    while True:
        #Food is generated inside the walls only
        x = random.randrange(WALL_SIZE,SCREEN_WIDTH - WALL_SIZE, CELL_SIZE)
        y = random.randrange(WALL_SIZE,SCREEN_HEIGHT - WALL_SIZE, CELL_SIZE)
        food_position = [x, y]

        #food must not appear on the snake body
        if food_position not in snake_body:
            return food_position
        
#Function for game over
def game_over(score,level):
    screen.fill(RED)

    game_over_text = font_big.render("Game Over", True, BLACK)
    score_text = font_small.render("Score: " + str(score), True, BLACK)
    level_text = font_small.render("Level: " + str(level), True, BLACK)

    screen.blit(game_over_text, (140, 230))
    screen.blit(score_text, (235, 310))
    screen.blit(level_text, (235, 340))

    pygame.display.update()
    pygame.time.delay(2000)

    pygame.quit()
    sys.exit()

#SNake starting values
snake_position = [100, 100]
snake_body = [
    [100, 100],
    [80, 100],
    [60, 100],
]

#Snake starts by moving right
direction = "RIGHT"
next_direction = "RIGHT"

#Score and level counters
score = 0
level = 1
foods_eaten = 0

#First food position
food_position = generate_food(snake_body)

#MAIN GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exist()

        #read keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                next_direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                next_direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                next_direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                next_direction = "RIGHT"

    direction = next_direction

    #Moving snake head depending on direction
    if direction == "UP":
        snake_position[1] -= CELL_SIZE
    elif direction == "DOWN":
        snake_position[1] += CELL_SIZE
    elif direction == "LEFT":
        snake_position[0] -= CELL_SIZE
    elif direction == "RIGHT":
        snake_position[0] += CELL_SIZE

    # ADD new head position to snake body
    snake_body.insert(0, list(snake_position))

    #Chekking if snake eats food
    if snake_position == food_position:
        score += 1
        foods_eaten += 1

        #Generate new food in a safe random position
        food_position = generate_food(snake_body)

        #Increase level after every N foods
        if foods_eaten % FOODS_PER_LEVEL == 0:
            level +=1
            FPS +=2
    else:
        #Remove tail if food wan not eaten
        snake_body.pop()

    # Wall collision check
    if snake_position[0] < WALL_SIZE:
        game_over(score, level)

    if snake_position[0] >= SCREEN_WIDTH - WALL_SIZE:
        game_over(score, level)

    if snake_position[1] < WALL_SIZE:
        game_over(score, level)

    if snake_position[1] >= SCREEN_HEIGHT - WALL_SIZE:
        game_over(score, level)

    #Self collision check
    for block in snake_body[1:]:
        if snake_position == block:
            game_over(score, level)

    screen.fill(GREEN)
    draw_walls()

    #Draw snake
    for index, block in enumerate(snake_body):
        if index == 0:
             color =BLUE
        else:
            if index % 2== 0:
                color = DARK_GREEN
            else:
                color = GRAY

        

        pygame.draw.rect(screen, color, (block[0], block[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, DARK_GREEN, (block[0], block[1], CELL_SIZE, CELL_SIZE), 1)

    # Draw food
    pygame.draw.rect(screen, RED, (food_position[0], food_position[1], CELL_SIZE, CELL_SIZE))

    # Draw score and level counters
    score_text = font_small.render("Score: " + str(score), True, WHITE)
    level_text = font_small.render("Level: " + str(level), True, WHITE)
    speed_text = font_small.render("Speed: " + str(FPS), True, WHITE)

    screen.blit(score_text, (30, 25))
    screen.blit(level_text, (240, 25))
    screen.blit(speed_text, (430, 25))

    pygame.display.update()
    clock.tick(FPS)


