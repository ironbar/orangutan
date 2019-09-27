"""
Save first image from episode
"""
import sys
import argparse
import cv2
import os
import numpy as np
import glob
import time
from tqdm import tqdm

from animalai.envs import UnityEnvironment
from animalai.envs.arena_config import ArenaConfig
from animalai.envs.exception import UnityWorkerInUseException

ENVIRONMENT_FILEPATH = '/media/guillermo/Data/Dropbox/02 Inteligencia Artificial/31_animalai/AnimalAI-Olympics/env/AnimalAI.x86_64'

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    args = parse_args(args)
    save_first_frame(args)

def save_first_frame(args):
    env, arena_config = _create_environment(args.config_filepath)
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    keys = sorted(list(arena_config.arenas.keys()))
    for key in tqdm(keys):
        arena_config.arenas[0] = arena_config.arenas[key]
        info = env.reset(arena_config)['Learner']
        frame = info.visual_observations[0][0]
        frame = (frame*255).astype(np.uint8)[:, :, [2, 1, 0]]
        cv2.imwrite(os.path.join(args.output_path, '%03d.png' % key), frame)
    env.close()

def _create_environment(config_filepath):
    worker_id = 0
    while worker_id < 10:
        try:
            env = UnityEnvironment(
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
    return env, arena_config

def parse_args(args):
    epilog = """
    python record_games.py "/media/guillermo/Data/Dropbox/02 Inteligencia Artificial/31_animalai/AnimalAI-Olympics/examples/configs/1-Food.yaml" /media/guillermo/Data/Kaggle/animalai/gameplay
    """
    description = """
    Save first image from episode
    """
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=epilog)
    parser.add_argument('config_filepath', help='Path to the file with configuratino for playing')
    parser.add_argument('output_path', help='Path to folder where the games are going to be saved')
    return parser.parse_args(args)

if __name__ == '__main__':
    main()
