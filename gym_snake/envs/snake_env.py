import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np


class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, dim=6):

        self.dim = dim
        self.space = np.zeros((dim, dim))
        self.observation_space = spaces.Discrete(dim * dim)
        self.action_space = spaces.Discrete(4)
        self.apple = []
        self.snake = []
        self.total = 0
        self.steps = 0

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        reward = -1
        done = False
        x = self.snake[0][0]
        y = self.snake[0][1]
        if action == 0:  # left
            y = self.snake[0][1] - 1
        elif action == 1:  # up
            x = self.snake[0][0] - 1
        elif action == 2:  # right
            y = self.snake[0][1] + 1
        elif action == 3:  # down
            x = self.snake[0][0] + 1
        if self.valid(x, y):
            self.snake.insert(0, [x, y])
            if [x, y] == self.apple:
                reward = 100  # съели яблоко, делаем новое
                self.new_apple()
            else:
                self.snake.remove(self.snake[-1])
        else: # invalid move
            reward = -2
        self.total += reward
        self.steps += 1
        if self.total < -200 or self.steps == 200:
            done = True
        return (self.snake[0][0], self.snake[0][1], self.apple[0], self.apple[1]), reward, done, {}

    def reset(self):
        h = np.random.randint(self.dim, size=2)
        X, Y = h[0], h[1]
        self.snake = [[X, Y]]
        self.new_apple()
        self.total = 0
        self.steps = 0
        return X, Y, self.apple[0], self.apple[1]

    def render(self, mode='human'):
        x, y = self.apple[0], self.apple[1]
#         print("Head at %d,%d length:%d Apple at %d,%d" % (
#             self.snake[0][0], self.snake[0][1], len(self.snake), x, y))
        a = np.zeros((self.dim, self.dim))
        a[x][y] = 3 # apple
        head = True
        for s in self.snake:
            if head:
                a[s[0], s[1]] = 1 # snake head
                head = False
            else:
                a[s[0], s[1]] = 2 # snake tail
        for i in range(self.dim):
            for j in range(self.dim):
                if a[i, j] == 0:
                    print(". ", end='')
                elif a[i, j] == 1:
                    print("O ", end='')
                elif a[i, j] == 2:
                    print("o ", end='')
                elif a[i, j] == 3:
                    print("A ", end='')
            print('')

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

    def in_snake(self, x, y):
        """Check if x, y, belongs to the snake
        """
        for i, (X, Y) in enumerate(self.snake):
            if x == X and y == Y:
                return True
        return False

    def new_apple(self):
        """Place the apple randomly"""
        a = np.random.randint(self.dim, size=2)
        x, y = a[0], a[1]
        while self.in_snake(x, y):  # apple must not occupy the same cell as the snake
            a = np.random.randint(self.dim, size=2)
            x, y = a[0], a[1]
        self.apple = [x, y]
