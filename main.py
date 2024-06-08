import pygame as pg 
from random import randrange
from random import randint

Window_Height = 1000
Window_Width = 1250
screen = pg.display.set_mode((Window_Width, Window_Height))
Tile_Size = 25
clock = pg.time.Clock()
random_range = (Tile_Size, (Window_Width // Tile_Size) - Tile_Size)
get_random_position = lambda: [randrange(1, (Window_Width // Tile_Size)) * Tile_Size, randrange(1, (Window_Height // Tile_Size)) * Tile_Size]

class Snake:
    def __init__(self):
        self.length = 1
        self.head = []
        self.positions = []
        self.direction = 0
        self.lastpositionbuff = []

    def random_head_position(self):
        self.head.append(((randrange(0, Window_Width, Tile_Size), randrange(0, Window_Height, Tile_Size))))
        for i in self.head:
            if i == 0 or i == 25:
                i = 50;
        self.positions = self.head

    def move(self):
        snake_len = len(self.positions) - 1
       
        self.lastpositionbuff = self.positions[snake_len]
        del self.positions[snake_len] 

        if snake_len == 0:
            if self.direction == 0:
                self.positions.insert(0, (self.lastpositionbuff[0], self.lastpositionbuff[1] - Tile_Size))
            if self.direction == 1:
                self.positions.insert(0, (self.lastpositionbuff[0] + Tile_Size, self.lastpositionbuff[1]))
            if self.direction == 2:
                self.positions.insert(0, (self.lastpositionbuff[0], self.lastpositionbuff[1] + Tile_Size))
            if self.direction == 3:
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
        food.position = []
        food.randomize_position()
    if snake.positions[0][0] == Window_Width or snake.positions[0][0] == 0:
        print('Game Over')
        pg.quit()
        quit()
    if snake.positions[0][1] == Window_Height or snake.positions[0][1] == 0:
        print('Game Over')
        pg.quit()
        quit()
    if snake.length > 1:
        for i in snake.positions[1:]:
            if snake.positions[0] == i:
                print('Game Over')
                pg.quit()
                quit()
        
    







def main():
    snake = Snake()
    Snake.random_head_position(snake)
    food = Food()
    Food.randomize_position(food)
    while True: 
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    snake.direction = 0
                if event.key == pg.K_RIGHT:
                    snake.direction = 1
                if event.key == pg.K_DOWN:
                    snake.direction = 2
                if event.key == pg.K_LEFT:
                    snake.direction = 3
                if event.key == pg.K_w:
                    snake.direction = 0
                if event.key == pg.K_d:
                    snake.direction = 1
                if event.key == pg.K_s:
                    snake.direction = 2
                if event.key == pg.K_a:
                    snake.direction = 3
        screen.fill((0, 0, 0))
        
        counter_head = 0
        
        check_collision(snake, food)
        snake.move()
        for x, y in snake.positions:
            print(snake.positions)
            if counter_head == 0:
                [pg.draw.rect(screen, 'green', (x, y, Tile_Size, Tile_Size))]
                counter_head += 1
            else:
                [pg.draw.rect(screen, 'blue', (x, y, Tile_Size, Tile_Size))]


        [pg.draw.rect(screen, 'red', (x, y, Tile_Size, Tile_Size)) for x, y in food.position]
        
        pg.display.flip()
        clock.tick(10)

if __name__ == '__main__':
    main()