import pygame as pg
import numpy as np
import pickle
from random import randrange, randint, uniform

pg.init()
font = pg.font.SysFont('dejavusansmono', 25)

Window_Height = 300
Window_Width = 300
screen = pg.display.set_mode((Window_Width, Window_Height))
Tile_Size = 50
clock = pg.time.Clock()
get_random_position = lambda: [randrange(1, (Window_Width // Tile_Size)) * Tile_Size, randrange(1, (Window_Height // Tile_Size)) * Tile_Size]

class SnakeAgent:
    def __init__(self):
        self.length = 1
        self.head = []
        self.positions = []
        self.direction = 0
        self.lastpositionbuff = []
        self.score = 0

    def generate_head_position(self):
        initial_x = Window_Width // 2
        initial_y = Window_Height // 2
        self.head = [(initial_x, initial_y)]
        self.positions = self.head[:]

    def move(self):
        self.lastpositionbuff = self.positions[-1]
        if self.direction == 0:
            new_head = (self.positions[0][0], self.positions[0][1] - Tile_Size)
        elif self.direction == 1:
            new_head = (self.positions[0][0] + Tile_Size, self.positions[0][1])
        elif self.direction == 2:
            new_head = (self.positions[0][0], self.positions[0][1] + Tile_Size)
        elif self.direction == 3:
            new_head = (self.positions[0][0] - Tile_Size, self.positions[0][1])
        
        self.positions = [new_head] + self.positions[:-1]

    def reset(self):
        self.length = 1
        self.head = []
        self.positions = []
        self.direction = 0
        self.lastpositionbuff = []
        self.generate_head_position()
        self.score = 0

    def drawScore(self):
        screen.blit(font.render(f'Score: {self.score}', True, (255, 255, 255)), (0, 0))

class Food: 
    def __init__(self):
        self.position = []

    def randomize_position(self):
        self.position = [(randrange(0, Window_Width, Tile_Size), randrange(0, Window_Height, Tile_Size))]

    def draw(self):
        pg.draw.rect(screen, 'red', (self.position[0][0], self.position[0][1], Tile_Size, Tile_Size))

def check_collision(snake, food):
    if snake.positions[0] == food.position[0]:
        snake.length += 1
        snake.positions.append(snake.lastpositionbuff)
        food.position = []
        food.randomize_position()
        snake.score += 1
    if snake.positions[0][0] >= Window_Width or snake.positions[0][0] < 0 or snake.positions[0][1] >= Window_Height or snake.positions[0][1] < 0:
        print('Game Over')
        return True
    if snake.length > 1 and any(snake.positions[0] == pos for pos in snake.positions[1:]):
        print('Game Over')
        return True
    return False

def draw_grid(snake, food):
    screen.fill((0, 0, 0))
    for x, y in snake.positions:
        color = 'green' if (x, y) == snake.positions[0] else 'blue'
        pg.draw.rect(screen, color, (x, y, Tile_Size, Tile_Size))
    food.draw()
    snake.drawScore()

class QLearningAgent:
    def __init__(self, state_size, action_size, alpha=0.1, gamma=0.95, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.q_table = {}

    def get_state(self, snake, food):
        return (self.calculate_relative_position(snake, food), self.calculate_relative_danger(snake), snake.direction)

    def calculate_relative_position(self, snake, food):
        head = snake.positions[0]
        food_pos = food.position[0]
        return (food_pos[0] - head[0], food_pos[1] - head[1])

    def calculate_relative_danger(self, snake):
        head = snake.positions[0]
        danger = [0, 0, 0, 0]  # up, right, down, left
        if head[1] - Tile_Size < 0 or (head[0], head[1] - Tile_Size) in snake.positions:
            danger[0] = 1
        if head[0] + Tile_Size >= Window_Width or (head[0] + Tile_Size, head[1]) in snake.positions:
            danger[1] = 1
        if head[1] + Tile_Size >= Window_Height or (head[0], head[1] + Tile_Size) in snake.positions:
            danger[2] = 1
        if head[0] - Tile_Size < 0 or (head[0] - Tile_Size, head[1]) in snake.positions:
            danger[3] = 1
        return tuple(danger)

    def choose_action(self, state):
        if uniform(0, 1) < self.epsilon:
            return randint(0, self.action_size - 1)
        else:
            return np.argmax(self.q_table.get(state, [0] * self.action_size))

    def learn(self, state, action, reward, next_state):
        old_value = self.q_table.get(state, [0] * self.action_size)[action]
        next_max = max(self.q_table.get(next_state, [0] * self.action_size))
        new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
        if state not in self.q_table:
            self.q_table[state] = [0] * self.action_size
        self.q_table[state][action] = new_value

    def update_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save_model(self, filename='q_learning_model2.pkl'):
        with open(filename, 'wb') as file:
            pickle.dump(self.q_table, file)

    def load_model(self, filename='q_learning_model2.pkl'):
        with open(filename, 'rb') as file:
            self.q_table = pickle.load(file)

def main():
    snake = SnakeAgent()
    snake.generate_head_position()
    food = Food()
    food.randomize_position()

    agent = QLearningAgent(state_size=5, action_size=4)
    agent.load_model()
    num_iterations = 250000

    for iteration in range(1, num_iterations + 1):
        state = agent.get_state(snake, food)
        action = agent.choose_action(state)
        snake.direction = action
        snake.move()
        next_state = agent.get_state(snake, food)

        if snake.positions[0] == food.position[0]:
            reward = 100
            food.randomize_position()
            snake.length += 1
            snake.score += 1
            snake.positions.append(snake.lastpositionbuff)
        else:
            reward = -1

        if check_collision(snake, food):
            reward = -100
            if snake.score > 5:
                print(f'Iteration: {iteration}, Score: {snake.score}')
            snake.reset()
            food.randomize_position()

        agent.learn(state, action, reward, next_state)
        agent.update_epsilon()

        draw_grid(snake, food)
        pg.display.flip()
        clock.tick(100)

    agent.save_model()
    print('Training completed')

if __name__ == '__main__':
    main()
