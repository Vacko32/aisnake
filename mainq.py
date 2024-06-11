import pygame as pg 
import numpy as np 
from random import randrange
from random import randint
pg.init()
font = pg.font.SysFont('dejavusansmono', 25)

Window_Height = 1000
Window_Width = 1000
screen = pg.display.set_mode((Window_Width, Window_Height))
Tile_Size = 50
clock = pg.time.Clock()
random_range = (Tile_Size, (Window_Width // Tile_Size) - Tile_Size)
get_random_position = lambda: [randrange(1, (Window_Width // Tile_Size)) * Tile_Size, randrange(1, (Window_Height // Tile_Size)) * Tile_Size]
reward = 0


# reset 
# reward 
# play(action) returns direction
# frame, state, game iteration 
# is collision change



class SnakeAgent:
    def __init__(self):
        self.length = 1
        self.head = []
        self.positions = []
        self.direction = 0
        self.lastpositionbuff = []
        self.frameiteration = 0
        self.score = 0
        self.isrunning = True

    def random_head_position(self):
        self.head.append(((randrange(100, Window_Width, Tile_Size), randrange(100, Window_Height, Tile_Size))))
        self.positions = self.head
    def move(self):
        snake_len = len(self.positions) - 1
       
        self.lastpositionbuff = self.positions[snake_len]
        del self.positions[snake_len] 

        if snake_len == 0:
            if self.direction == 0: # up
                self.positions.insert(0, (self.lastpositionbuff[0], self.lastpositionbuff[1] - Tile_Size))
            if self.direction == 1: # right
                self.positions.insert(0, (self.lastpositionbuff[0] + Tile_Size, self.lastpositionbuff[1]))
            if self.direction == 2: # down
                self.positions.insert(0, (self.lastpositionbuff[0], self.lastpositionbuff[1] + Tile_Size))
            if self.direction == 3: # left
                self.positions.insert(0, (self.lastpositionbuff[0] - Tile_Size, self.lastpositionbuff[1]))
        else:
            if self.direction == 0:
                self.positions.insert(0, (self.positions[0][0], self.positions[0][1] - Tile_Size))
            if self.direction == 1:
                self.positions.insert(0, (self.positions[0][0] + Tile_Size, self.positions[0][1]))
            if self.direction == 2:
                self.positions.insert(0, (self.positions[0][0], self.positions[0][1] + Tile_Size))
            if self.direction == 3:
                self.positions.insert(0, (self.positions[0][0] - Tile_Size, self.positions[0][1]))
        self.frameiteration += 1
        
    def reset(self):
        self.length = 1
        self.head = []
        self.positions = []
        self.direction = 0
        self.lastpositionbuff = []
        self.random_head_position()
        self.move()
        self.score = 0
        self.frameiteration = 0

    def drawScore(self):
        screen.blit(font.render(f'Score: {self.score}', True, (255, 255, 255)), (0, 0))

class Food: 
    def __init__(self):
        self.position = []

    def randomize_position(self):
        self.position.append(((randrange(0, Window_Width, Tile_Size), randrange(0, Window_Height, Tile_Size))))
        for i in self.position:
            if i == 0 or i == 25:
                i = 50;

    def draw(self):
        pg.draw.rect(screen, 'red', (self.position[0], self.position[1], Tile_Size, Tile_Size))




def check_collision(snake, food):
    if snake.positions[0] == food.position[0]:
        snake.length += 1
        snake.positions.append(snake.lastpositionbuff)
        reward = 5
        food.position = []
        food.randomize_position()
        snake.score += 1
        snake.drawScore()
    if snake.positions[0][0] == Window_Width or snake.positions[0][0] == 0:
        print(snake.positions[0][0])
        print('Game Over')
        reward = -10
        snake.isrunning = False
        
    if snake.positions[0][1] == Window_Height or snake.positions[0][1] == 0:
        print(snake.positions[0][1])
        reward = -10
        print('Game Over')
        snake.isrunning = False
        
    if snake.length > 1:
        for i in snake.positions[1:]:
            if snake.positions[0] == i:
                print('Game Over')
                snake.isrunning = False
                reward = -10

        
    if snake.frameiteration > 100*len(snake.positions):
        print('Game Over')
        reward = -10
        snake.isrunning = False

    return reward, snake.score, snake.isrunning



def change_direction(snake, food, action):
    # action is a one hot encoded array passed by the agent 

    

    if np.array_equal(action, [1, 0, 0]):
        snake.direction = 0
    elif np.array_equal(action, [0, 1, 0]):
        snake.direction = 1
    elif np.array_equal(action, [0, 0, 1]):
        snake.direction = 2
    else:
        snake.direction = 3





    for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            

    draw_grid(snake, food)
    check_collision(snake, food)
    snake.move()
    draw_grid(snake, food)

def draw_grid(snake, food):
    screen.fill((0, 0, 0))
    counter_head = 0
    for x, y in snake.positions:
            print(snake.positions)
            if counter_head == 0:
                [pg.draw.rect(screen, 'green', (x, y, Tile_Size, Tile_Size))]
                counter_head += 1
            else:
                [pg.draw.rect(screen, 'blue', (x, y, Tile_Size, Tile_Size))]

    [pg.draw.rect(screen, 'red', (x, y, Tile_Size, Tile_Size)) for x, y in food.position]



    
def game_reset(snake, food):
    snake.reset()
    food.position = []
    food.randomize_position()
    snake.drawScore()
    draw_grid(snake, food)
    pg.display.flip()








def main():
    snake = SnakeAgent()
    SnakeAgent.random_head_position(snake)
    food = Food()
    snake.drawScore()
    Food.randomize_position(food)
    
    while True: 
        change_direction(snake, food)
        snake.drawScore()
        if snake.isrunning == False:
            break
        pg.display.flip()
        clock.tick(10)
    
if __name__ == '__main__':
    main()