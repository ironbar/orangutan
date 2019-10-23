import pytest
import os

from animalai.envs.arena_config import ArenaConfig
from animalai.envs.exception import UnityWorkerInUseException
from orangutan.env import EnvWrapper, MapEnv

RESOURCES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')
ENVIRONMENT_FILEPATH = '/media/guillermo/Data/Dropbox/02 Inteligencia Artificial/31_animalai/AnimalAI-Olympics/env/AnimalAI.x86_64'


def _create_environment(config_filepath, env_class):
    worker_id = 0
    while worker_id < 10:
        try:
            env = env_class(
                file_name=ENVIRONMENT_FILEPATH,   # Path to the environment
                worker_id=worker_id,                # Unique ID for running the environment (used for connection)
                seed=int(os.getenv('ENV_SEED', 0)),                     # The random seed
                docker_training=False,      # Whether or not you are training inside a docker
                n_arenas=1,                 # Number of arenas in your environment
                play=False,                 # Set to False for training
                inference=False,            # Set to true to watch your agent in action
                resolution=None             # Int: resolution of the agent's square camera (in [4,512], default 84)
            )
            break
        except UnityWorkerInUseException:
            worker_id += 1
            print('Increasing worker_id: %i' % worker_id)
    arena_config = ArenaConfig(config_filepath)
    env.reset(arenas_configurations=arena_config, train_mode=True)
    return env

def test_env_wrapper():
    env = _create_environment(os.path.join(RESOURCES_PATH, 'death_maze.yaml'), EnvWrapper)
    for _ in range(10):
        env.step([1, 0])
    env.close()

def test_map_wrapper():
    env = _create_environment(os.path.join(RESOURCES_PATH, 'death_maze.yaml'), MapEnv)
    for _ in range(10):
        env.step([1, 0])
    env.close()
