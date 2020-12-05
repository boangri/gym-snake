import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import pygame


class SnakeEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 4
    }

    def __init__(self, dim=20, size=20, fps=4):

        self.dim = dim
        self.size = size
        self.space = np.zeros((dim, dim))
        self.observation_space = spaces.Discrete(dim * dim)
        self.action_space = spaces.Discrete(4)
        self.apple = []
        self.snake = []
        self.total = 0
        self.steps = 0
        self.fps = fps
        self.ready = False # if pygame initialized

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        np.random.seed(seed)
        return [seed]

    def step(self, action):
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
                reward = -1
                self.snake.remove(self.snake[-1])
        else: # invalid move
            reward = -100
            done = True
            
        self.total += reward
        self.steps += 1
        if self.steps == 200:
            done = True
        self.score += reward
        return (self.snake[0][0], self.snake[0][1], self.apple[0], self.apple[1]), reward, done, {}

    def reset(self):
        h = np.random.randint(self.dim, size=2)
        X, Y = h[0], h[1]
        self.snake = [[X, Y]]
        self.new_apple()
        self.total = 0
        self.steps = 0
        self.score = 0
        return X, Y, self.apple[0], self.apple[1]

    def render(self, mode='human'):
        if not self.ready: # Initialization
            self.ready = True
            pygame.init()
            self.clock = pygame.time.Clock()
            self.font_score = pygame.font.SysFont('Arial', 26, bold=True)
            self.font_end = pygame.font.SysFont('Arial', 66, bold=True)
        self.surface = pygame.display.set_mode([self.dim*self.size, self.dim*self.size])
        [pygame.draw.rect(self.surface, pygame.Color('green'), (p[0]*self.size, p[1]*self.size, self.size - 1, self.size - 1)) for p in self.snake]
        pygame.draw.rect(self.surface, pygame.Color('red'), (self.apple[0]*self.size, self.apple[1]*self.size, self.size, self.size))
        # show score
        render_score = self.font_score.render(f'SCORE: {self.score}', 1, pygame.Color('orange'))
        self.surface.blit(render_score, (5, 5))
        pygame.display.flip()
        self.clock.tick(self.fps)
        a = pygame.surfarray.array3d(self.surface)
        return np.transpose(a, (1, 0, 2))

    def close(self):
        pygame.quit()

    def valid(self, x, y):
        if x < 0 or y < 0:
            return False
        if x >= self.dim or y >= self.dim:
            return False
        for p in self.snake:
            if x == p[0] and y == p[1]:
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
