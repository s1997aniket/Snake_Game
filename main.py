import pygame
import random

# Set up the game window
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize pygame
pygame.init()

# Set up the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')

# Set up the clock
clock = pygame.time.Clock()

# Define the Snake class
class Snake:
    def __init__(self):
        self.body = [(5, 5), (4, 5), (3, 5)]
        self.direction = 'right'
        self.is_alive = True

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == 'up':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'down':
            new_head = (head_x, head_y + 1)
        elif self.direction == 'left':
            new_head = (head_x - 1, head_y)
        else:
            new_head = (head_x + 1, head_y)
        self.body = [new_head] + self.body[:-1]

    def change_direction(self, direction):
        if direction == 'up' and self.direction != 'down':
            self.direction = 'up'
        elif direction == 'down' and self.direction != 'up':
            self.direction = 'down'
        elif direction == 'left' and self.direction != 'right':
            self.direction = 'left'
        elif direction == 'right' and self.direction != 'left':
            self.direction = 'right'

    def grow(self):
        tail_x, tail_y = self.body[-1]
        if self.direction == 'up':
            new_tail = (tail_x, tail_y + 1)
        elif self.direction == 'down':
            new_tail = (tail_x, tail_y - 1)
        elif self.direction == 'left':
            new_tail = (tail_x + 1, tail_y)
        else:
            new_tail = (tail_x - 1, tail_y)
        self.body.append(new_tail)

    def check_collision(self):
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            self.is_alive = False
        for body_part in self.body[1:]:
            if head_x == body_part[0] and head_y == body_part[1]:
                self.is_alive = False

    def draw(self):
        for cell in self.body:
            pygame.draw.rect(window, WHITE, (cell[0]*CELL_SIZE, cell[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Define the Food class
class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

    def draw(self):
        pygame.draw.rect(window, RED, (self.position[0]*CELL_SIZE, self.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Create the Snake and Food
snake = Snake()
food = Food()

# Set up the game loop
while snake.is_alive:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            snake.is_alive = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction('up')
            elif event.key == pygame.K_DOWN:
                snake.change_direction('down')
            elif event.key == pygame.K_LEFT:
                snake.change_direction('left')
            elif event.key == pygame.K_RIGHT:
                snake.change_direction('right')

    # Move the snake
    snake.move()

    # Check for collision with the food
    if snake.body[0] == food.position:
        snake.grow()
        food = Food()

    # Check for collision with the walls or with itself
    snake.check_collision()

    # Draw the game
    window.fill(BLACK)
    snake.draw()
    food.draw()
    pygame.display.update()

    # Set the game speed
    clock.tick(10)

# Clean up pygame
pygame.quit()
