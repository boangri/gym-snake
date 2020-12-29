from gym.envs.registration import register

register(
    id='Snake-v0',
    entry_point='gym_snake.envs:SnakeEnv',
)

print('gym-snake v0.1.7 29.12.2020')
