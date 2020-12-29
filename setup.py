from setuptools import setup

setup(name='gym_snake',
      version='0.1.7',
      description='Gym Snake Env',
      url='https://github.com/boangri/gym-snake',
      author='Boris Gribovskiy',
      packages=['gym_snake', 'gym_snake.envs'],
      author_email='xinu@yandex.ru',
      license='MIT License',
      install_requires=['gym', 'numpy', 'pygame'],
      python_requires='>=3.6'
      )
