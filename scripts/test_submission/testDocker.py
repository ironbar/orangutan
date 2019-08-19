"""
Script for testing and evaluating the docker
"""
import glob
import os
import sys
import json
import time
import importlib.util
import numpy as np
import yaml

from animalai.envs.gym.environment import AnimalAIEnv
from animalai.envs.arena_config import ArenaConfig

N_EPISODES = 30
GRAY_FRAMES = 5

def main():
    # Load the agent from the submission
    print('Loading your agent')
    try:
        spec = importlib.util.spec_from_file_location('agent_module', '/aaio/agent.py')
        agent_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(agent_module)
        submitted_agent = agent_module.Agent()
    except Exception as e:
        print('Your agent could not be loaded, make sure all the paths are absolute, error thrown:')
        raise e
    print('Agent successfully loaded')

    env = AnimalAIEnv(
        environment_filename='/aaio/test/env/AnimalAI',
        seed=7777,
        retro=False,
        n_arenas=1,
        worker_id=1,
        docker_training=True,
    )

    _remove_previous_frames()
    with open('/aaio/test/test_config.yaml', 'r') as stream:
        test_config = yaml.safe_load(stream)
    rewards = []
    elapsed_time = time.time()
    for key in test_config:
        config_filepath = os.path.join('/aaio/test/configs', key)
        rewards.append(evaluate_config(config_filepath, env, submitted_agent,
                                       n_episodes=test_config[key]['n_tests'],
                                       threshold=test_config[key]['threshold']))
    elapsed_time = time.time() - elapsed_time
    _summarize_rewards(rewards, test_config.keys(), elapsed_time)
    print('SUCCESS')

def evaluate_config(config_filepath, env, submitted_agent, n_episodes, threshold):
    arena_config_in = ArenaConfig(config_filepath)
    env.reset(arenas_configurations=arena_config_in)
    obs, reward, done, info = env.step([0, 0])
    print('█'*120)
    print('\t%s' % os.path.basename(config_filepath))
    rewards, steps = [], []
    episode_frames = []
    initial_frame = None
    for k in range(n_episodes):
        _reset_agent(submitted_agent, arena_config_in)
        cumulated_reward = 0
        #episode_frames = []
        try:
            for t in range(arena_config_in.arenas[0].t+1):
                action = submitted_agent.step(obs, reward, done, info)
                episode_frames.append(info['brain_info'].visual_observations[0][0])
                obs, reward, done, info = env.step(action)
                cumulated_reward += reward
                if done:
                    # # _save_frames(episode_frames, config_filepath, k)
                    for _ in range(GRAY_FRAMES):
                        episode_frames.append(np.ones((84, 84, 3), dtype=np.float32)*0.5)
                    _reset_agent(submitted_agent, arena_config_in)
                    break
        except Exception as e:
            print('Episode {} failed'.format(k))
            raise e
        if not done:
            print('Warning level not done.')
        msg = 'Episode %i reward: %.2f\tsteps: %i' % (k, cumulated_reward, t)
        if cumulated_reward >= threshold:
            _print_green(msg)
        else:
            _print_red(msg)
        rewards.append(cumulated_reward)
        steps.append(t)
        sys.stdout.flush()
    _print_config_summary(rewards, steps)
    _save_frames(episode_frames, config_filepath, None)
    return rewards

def _print_config_summary(rewards, steps):
    print('\tMean reward: %.2f (std: %.2f)' % (np.mean(rewards), np.std(rewards)))
    print('\tMean steps: %.2f (std: %.2f)' % (np.mean(steps), np.std(steps)))

def _reset_agent(agent, arena):
    try:
        agent.reset(t=arena.arenas[0].t)
    except Exception as e:
        print('Your agent could not be reset:')
        raise e

def _summarize_rewards(rewards, config_filepaths, elapsed_time):
    print('\nRewards summary')
    data = {'elapsed_time': elapsed_time}
    for reward, config_filepath in zip(rewards, config_filepaths):
        key = os.path.splitext(os.path.basename(config_filepath))[0]
        score = np.mean(reward)
        data['level_%s' % key] = score
        print('%.2f\t %s' % (score, key))
    data['mean_score'] = np.mean([np.mean(reward) for reward in rewards])
    print('Mean reward: %.2f' % data['mean_score'])
    with open('/aaio/test/summary.json', 'w') as f:
        json.dump(data, f)

def _save_frames(episode_frames, config_filepath, episode_idx):
    episode_frames = np.array(episode_frames)
    episode_frames = (episode_frames*255).astype(np.uint8)
    if episode_idx is not None:
        filepath = os.path.join('/aaio/test/frames', '%s_%03d.npz' % (
            os.path.splitext(os.path.basename(config_filepath))[0], episode_idx))
    else:
        filepath = os.path.join('/aaio/test/frames', '%s.npz' % (
            os.path.splitext(os.path.basename(config_filepath))[0]))
    np.savez(filepath, frame=episode_frames)

def _remove_previous_frames():
    filepaths = glob.glob('/aaio/test/frames/*.npz')
    [os.remove(filepath) for filepath in filepaths]

def _print_red(text):
    print("\x1b[31m" + text + "\x1b[0m")

def _print_green(text):
    print("\x1b[32m" + text + "\x1b[0m")

def _print_yellow(text):
    print("\x1b[33m" + text + "\x1b[0m")

if __name__ == '__main__':
    main()
