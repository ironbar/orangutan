"""
Record games
"""
import sys
import argparse
import cv2
import os
import numpy as np
import glob
import time

from orangutan.env import EnvWrapper
from animalai.envs import UnityEnvironment
from animalai.envs.arena_config import ArenaConfig
from animalai.envs.exception import UnityWorkerInUseException

ENVIRONMENT_FILEPATH = '/media/guillermo/Data/Dropbox/02 Inteligencia Artificial/31_animalai/AnimalAI-Olympics/env/AnimalAI.x86_64'

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    args = parse_args(args)
    record_games(args)

def record_games(args):
    env = _create_environment(args.config_filepath)
    output_folder = _prepare_output_folder(args.config_filepath, args.output_path)

    info = env.reset()['Learner']
    level_idx = _get_initial_level_idx(output_folder)
    n_steps = 0
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    level_storage = LevelStorage()

    while 1:
        _update_window(info, level_idx, n_steps)
        action = _get_action_from_keyboard()
        if isinstance(action, str):
            if action == 'break':
                break
            elif action == 'reset':
                info = env.reset()['Learner']
                level_storage = LevelStorage()
                n_steps = 0
                _transition_between_levels()
                continue
            elif action == 'save':
                info = env.reset()['Learner']
                level_storage.save(os.path.join(output_folder, '%05d.npz' % level_idx))
                level_storage = LevelStorage()
                level_idx += 1
                n_steps = 0
                _transition_between_levels()
                continue


        info_next = env.step(vector_action=action)['Learner']
        level_storage.add(info, info_next, action)
        info = info_next

        n_steps += 1
        is_level_ended = info.max_reached[0] or info.local_done[0]
        if is_level_ended:
            reward = _unpack_info(info)[-1]
            if reward > 0:
                level_storage.save(os.path.join(output_folder, '%05d.npz' % level_idx))
                level_idx += 1
            else:
                msg = 'Not saving level because of negative reward'
                print(msg)
                cv2.displayOverlay('img', msg)
            level_storage = LevelStorage()
            n_steps = 0
            _transition_between_levels()

    cv2.destroyAllWindows()
    cv2.waitKey(1)
    env.close()

def _create_environment(config_filepath):
    worker_id = 0
    while worker_id < 10:
        try:
            env = EnvWrapper(
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

def _get_action_from_keyboard():
    key_to_action = {
        ord('d'): [0, 1],
        ord('a'): [0, 2],
        ord('w'): [1, 0],
        ord('s'): [2, 0],
        ord('o'): 'break',
        ord('k'): 'reset',
        ord('n'): 'save',
    }
    while 1:
        key = cv2.waitKey()
        if key in key_to_action:
            action = key_to_action[key]
            break
        else:
            print('Unknown key pressed')
    return action

class LevelStorage():
    def __init__(self):
        self.frame = []
        self.speed = []
        self.previous_action = []
        self.action = []
        self.reward = []

    def add(self, info, info_next, action):
        frame, speed, previous_action, _ = _unpack_info(info)
        _, _, _, reward = _unpack_info(info_next)
        self.frame.append(frame)
        self.speed.append(speed)
        self.previous_action.append(previous_action)
        self.action.append(action)
        self.reward.append(reward)

    def save(self, path):
        np.savez(path, frame=self.frame, speed=self.speed, reward=self.reward,
                 previous_action=self.previous_action, action=self.action)

def _prepare_output_folder(config_filepath, output_path):
    output_folder = os.path.join(output_path,
                                 os.path.splitext(os.path.basename(config_filepath))[0])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

def _update_window(info, level_idx, n_steps):
    frame, speed, previous_action, reward = _unpack_info(info)

    cv2.imshow('img', _add_hud(frame[:, :, [2, 1, 0]]))
    msg = 'Games played: %i     n_steps: %i   Reward: %.2f   Speed: %s Text observations: %s' % (
        level_idx,
        n_steps,
        reward,
        speed,
        info.text_observations[0])
    cv2.displayOverlay('img', msg)

def _add_hud(frame):
    frame = frame.copy()
    frame[:, 41:43] += 10/255
    return frame

def _unpack_info(info):
    frame = info.visual_observations[0][0]
    speed = info.vector_observations.round(2)
    previous_action = info.previous_vector_actions
    reward = info.rewards[0]
    return frame, speed, previous_action, reward

def _get_initial_level_idx(output_folder):
    saved_games = sorted(glob.glob(os.path.join(output_folder, '*.npz')))
    level_idx = 0
    if saved_games:
        level_idx = int(os.path.splitext(os.path.basename(saved_games[-1]))[0]) + 1
    return level_idx

def _transition_between_levels():
    cv2.imshow('img', np.zeros((84, 84, 3)))
    cv2.waitKey(1)
    for _ in range(5):
        time.sleep(0.1)
        cv2.waitKey(1)

def parse_args(args):
    epilog = """
    python record_games.py "/media/guillermo/Data/Dropbox/02 Inteligencia Artificial/31_animalai/AnimalAI-Olympics/examples/configs/1-Food.yaml" /media/guillermo/Data/Kaggle/animalai/gameplay
    """
    description = """
    Record games
    Use keys (w,a,s,d) to move.
    Press "o" to end the application.
    Press "k" to reset the level without saving the current game.
    The environment variable ENV_SEED can be used to modify the random seed that is 0 by default
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
