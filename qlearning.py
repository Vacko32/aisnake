import numpy as np
import random

# Define the environment
class GridWorld:
    def __init__(self, width, height, start, goal, obstacles):
        self.width = width
        self.height = height
        self.start = np.array(start)
        self.goal = np.array(goal)
        self.obstacles = [np.array(obstacle) for obstacle in obstacles]
        self.state = np.array(start)

    def reset(self):
        self.state = np.array(self.start)
        return self.state

    def step(self, action):
        next_state = self.state.copy()
        if action == 0:   # Up
            next_state[0] = max(0, self.state[0] - 1)
        elif action == 1: # Down
            next_state[0] = min(self.height - 1, self.state[0] + 1)
        elif action == 2: # Left
            next_state[1] = max(0, self.state[1] - 1)
        elif action == 3: # Right
            next_state[1] = min(self.width - 1, self.state[1] + 1)

        if any(np.array_equal(next_state, obstacle) for obstacle in self.obstacles):
            next_state = self.state

        self.state = next_state

        reward = -1
        done = False

        if np.array_equal(self.state, self.goal):
            reward = 0
            done = True

        return self.state, reward, done

    def get_state_space(self):
        return [np.array([i, j]) for i in range(self.height) for j in range(self.width) if not any(np.array_equal(np.array([i, j]), obstacle) for obstacle in self.obstacles)]

    def get_action_space(self):
        return [0, 1, 2, 3]

# Q-learning algorithm
def q_learning(env, episodes, alpha, gamma, epsilon):
    q_table = {}
    for state in env.get_state_space():
        q_table[tuple(state)] = [0, 0, 0, 0]

    for episode in range(episodes):
        state = env.reset()
        done = False

        while not done:
            if random.uniform(0, 1) < epsilon:
                action = random.choice(env.get_action_space())
            else:
                action = np.argmax(q_table[tuple(state)])

            next_state, reward, done = env.step(action)
            old_value = q_table[tuple(state)][action]
            next_max = np.max(q_table[tuple(next_state)])

            new_value = old_value + alpha * (reward + gamma * next_max - old_value)
            q_table[tuple(state)][action] = new_value

            state = next_state

    return q_table

# Initialize environment and parameters
width, height = 5, 5
start = [0, 0]
goal = [4, 4]
obstacles = [[1, 1], [2, 2], [3, 3]]
env = GridWorld(width, height, start, goal, obstacles)

episodes = 1000
alpha = 0.1
gamma = 0.6
epsilon = 0.1

# Train the agent
q_table = q_learning(env, episodes, alpha, gamma, epsilon)

# Display the Q-table
for state, actions in q_table.items():
    print(f"State {state}: {actions}")

# Test the agent
state = env.reset()
done = False
while not done:
    action = np.argmax(q_table[tuple(state)])
    state, reward, done = env.step(action)
    print(f"Moved to {state}")
