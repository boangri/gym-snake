import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np


class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, dim=5):

        self.dim = dim
        self.space = np.zeros((dim, dim))
        self.observation_space = spaces.Discrete(dim*dim)
        self.action_space = spaces.Discrete(4)
        self.apple = [None, None]
        self.snake = []

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        reward = -1
        done = False
        if action == 0:  # up
            x = self.head[0][0]
            y = self.head[0][1] - 1
        elif action == 1:  # left
            x = self.head[0][0] - 1
            y = self.head[0][1]
        elif action == 2:  # down
            x = self.head[0][0]
            y = self.head[0][1] + 1
        elif action == 3:  # right
            x = self.head[0][0] + 1
            y = self.head[0][1]
        if self.valid(x, y):
            self.snake.insert(0, [x, y])
            if [x, y] == self.apple:
                reward = 100  # съели яблоко, делаем новое
                apple = np.random.randint(self.dim, size=2)
                while apple in self.snake:  # apple must not occupy the same cell as the snake
                    apple = np.random.randint(self.dim, size=2)
                self.apple = [apple[0], apple[1]]
            else:
                self.snake.remove(self.snake[-1])

        return (self.snake[0][0], self.snake[0][1], self.apple[0], self.apple[1]), reward, done, {}

    def reset(self):
        head = np.random.randint(self.dim, size=2)
        self.snake = [[head[0], head[1]]]
        apple = np.random.randint(self.dim, size=2)
        while apple in self.snake:  # apple must not occupy the same cell as the snake
            apple = np.random.randint(self.dim, size=2)
        self.apple = [apple[0], apple[1]]
        return self.head[0][0], self.head[0][1], self.apple[0], self.apple[1]

    def render(self, mode='human'):
        print("Head at %d,%d length:%d Apple at %d,%d" % (self.snake[0][0], self.snake[0][1], len(self.snake), self.apple[0], self.apple[1]))

    def close(self):
        pass

    def valid(self, x, y):
        if x < 0 or y < 0:
            return False
        if x >= self.dim or y >= self.dim:
            return False
        if [x, y] in self.snake:
            return False
        return True
