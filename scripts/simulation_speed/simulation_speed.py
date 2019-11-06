"""
This is the trainMLAgents.py script copied and adapted to make random actions
"""
from animalai.envs import UnityEnvironment
from animalai.envs.exception import UnityEnvironmentException
from animalai.envs.arena_config import ArenaConfig
import random
import yaml
import sys
import argparse
from functools import partial
import numpy as np
import os
import glob
from tqdm import tqdm
import time

from animalai.envs.subprocess_environment import SubprocessUnityEnvironment
from orangutan.env import EnvWrapper, MapEnv


def train(args=None):
    if args is None:
        args = sys.argv[1:]
    args = parse_args(args)

    # ML-agents parameters for training
    env_path = '../../../AnimalAI-Olympics/env/AnimalAI'
    worker_id = random.randint(1, 100)
    seed = 10
    base_port = 5005
    sub_id = 1
    if args.verbose_id:
        run_id = '%s_%ienv_%iarenas' % (
            os.path.basename(os.path.dirname(os.path.dirname(args.trainer_config_path))),
            args.n_envs, args.n_arenas)
    else:
        run_id = os.path.basename(os.path.dirname(os.path.dirname(args.trainer_config_path)))
    if args.suffix:
        run_id += '_%s' % args.suffix
    save_freq = args.save_freq
    curriculum_file = None
    train_model = True
    keep_checkpoints = args.keep_checkpoints
    lesson = 0
    run_seed = 1
    docker_target_name = None
    no_graphics = False
    # model_path = '%s/%s' % (os.path.dirname(args.trainer_config_path), run_id)
    model_path = './models/%s' % (run_id)
    summaries_dir = './summaries'
    maybe_meta_curriculum = None

    if os.path.isdir(args.arena_config):
        arena_config_paths = glob.glob(os.path.join(args.arena_config, '*.yaml'))
        arena_config_in = [ArenaConfig(arena_config_path) for arena_config_path in tqdm(arena_config_paths, desc='loading arenas config')]
    else:
        arena_config_in = ArenaConfig(args.arena_config)
    trainer_config = load_config(args.trainer_config_path)
    trainer_config['Learner']['reset_steps'] = args.reset_steps
    if args.n_envs > 1:
        env_factory = partial(
            init_environment, docker_target_name=docker_target_name, no_graphics=no_graphics,
            env_path=env_path, n_arenas=args.n_arenas, trainer_config=trainer_config)
        env = SubprocessUnityEnvironment(env_factory, args.n_envs)
    else:
        env = init_environment(worker_id, env_path, docker_target_name, no_graphics,
                               n_arenas=args.n_arenas, trainer_config=trainer_config)
    env.reset(arena_config_in)
    time.sleep(1)
    t0 = time.time()
    for _ in tqdm(range(2000)):
        env.step(np.random.randint(0, 3, size=(args.n_envs*args.n_arenas, 2)))
    print('Elapsed time: %.2f' % (time.time() - t0))
    env.close()

def load_config(trainer_config_path):
    try:
        with open(trainer_config_path) as data_file:
            trainer_config = yaml.load(data_file)
            return trainer_config
    except IOError:
        raise UnityEnvironmentException('Parameter file could not be found '
                                        'at {}.'
                                        .format(trainer_config_path))
    except UnicodeDecodeError:
        raise UnityEnvironmentException('There was an error decoding '
                                        'Trainer Config from this path : {}'
                                        .format(trainer_config_path))

def init_environment(worker_id, env_path, docker_target_name, no_graphics, n_arenas, trainer_config):
    if env_path is not None:
        # Strip out executable extensions if passed
        env_path = (env_path.strip()
                    .replace('.app', '')
                    .replace('.exe', '')
                    .replace('.x86_64', '')
                    .replace('.x86', ''))
    docker_training = docker_target_name is not None

    return MapEnv(
        n_arenas=n_arenas,             # Change this to train on more arenas
        file_name=env_path,
        worker_id=worker_id,
        seed=worker_id,
        docker_training=docker_training,
        play=False,
        # TODO: make this more intelligent
        map_side=trainer_config['Learner']['model_architecture']['map_encoding']['map_side'],
    )

def parse_args(args):
    epilog = """
    python trainMLAgents.py /media/guillermo/Data/Kaggle/animalai/agents/012_even_more_memory/data/training_002.yaml /media/guillermo/Data/Kaggle/animalai/agents/012_even_more_memory/data/trainer_config.yaml --n_envs 8 --n_arenas 32
    """
    description = """
    Train using MLAgents and PPO algorithm
    """
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=epilog)
    parser.add_argument('arena_config', help='Path to the file with configuration for the arena')
    parser.add_argument('trainer_config_path', help='Path to the file with configuration for training')
    parser.add_argument('--n_envs', type=int, default=8, help='Number of environments to run')
    parser.add_argument('--n_arenas', type=int, default=32, help='Number of arenas on each environment')
    parser.add_argument('--load_model', action='store_true')
    parser.add_argument('--reset_steps', action='store_true')
    parser.add_argument('--save_freq', type=int, default=1000, help='Number of steps between each saving of the model.')
    parser.add_argument('--keep_checkpoints', type=int, default=5, help='Number of checkpoints that will be kept.')
    parser.add_argument('--verbose_id', action='store_true')
    parser.add_argument('--suffix', default='')
    return parser.parse_args(args)

if __name__ == '__main__':
    train()