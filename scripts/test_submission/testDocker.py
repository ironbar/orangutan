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
import shutil

from animalai.envs.gym.environment import AnimalAIEnv
from animalai.envs.arena_config import ArenaConfig

N_EPISODES = 30
GRAY_FRAMES = 5
SAVE_FOLDER = '/aaio/test/_temp/%s' % sys.argv[1]

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

    _prepare_saving_folder()
    with open('/aaio/test/test_config.yaml', 'r') as stream:
        test_config = yaml.safe_load(stream)
    results = {}
    elapsed_time = time.time()
    for category, category_conf in test_config.items():
        print('█'*120)
        print('\t%s' % category)
        results[category] = {}
        for test_name, test_params in category_conf.items():
            config_filepath = os.path.join('/aaio/test/configs', category, test_name)
            if not 'partial_threshold' in test_params:
                test_params['partial_threshold'] = None
            results[category][test_name] = evaluate_config(
                config_filepath, env, submitted_agent, n_episodes=test_params['n_tests'],
                threshold=test_params['threshold'], partial_threshold=test_params['partial_threshold'],
                category=category)
    elapsed_time = time.time() - elapsed_time
    _summarize_results(results, elapsed_time)
    print('SUCCESS')

def evaluate_config(config_filepath, env, submitted_agent, n_episodes, threshold, partial_threshold, category):
    arena_config_in = ArenaConfig(config_filepath)
    env.reset(arenas_configurations=arena_config_in)
    obs, reward, done, info = env.step([0, 0])
    rewards, steps, results = [], [], []
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
        msg = 'Episode %i reward: %.2f\tsteps: %i\t%s' % (k, cumulated_reward, t, os.path.basename(config_filepath))
        if cumulated_reward >= threshold:
            _print_green(msg)
            results.append(1)
        elif partial_threshold is not None and cumulated_reward >= partial_threshold:
            _print_yellow(msg)
            results.append(0.5)
        else:
            _print_red(msg)
            results.append(0)
        rewards.append(cumulated_reward)
        steps.append(t)
        sys.stdout.flush()
    #_print_config_summary(rewards, steps)
    _save_frames(episode_frames, config_filepath, None, category=category)
    return dict(rewards=rewards, steps=steps, results=results)

def _print_config_summary(rewards, steps):
    print('\tMean reward: %.2f (std: %.2f)' % (np.mean(rewards), np.std(rewards)))
    print('\tMean steps: %.2f (std: %.2f)' % (np.mean(steps), np.std(steps)))

def _reset_agent(agent, arena):
    try:
        agent.reset(t=arena.arenas[0].t)
    except Exception as e:
        print('Your agent could not be reset:')
        raise e

def _summarize_results(results, elapsed_time):
    print('\nRewards summary')
    data = {'elapsed_time': elapsed_time, 'results': results}
    for category, category_results in results.items():
        category_score = np.mean([np.mean(result['results']) for result in category_results.values()])
        print('%.2f\t %s' % (category_score, category))
        data['level_%s' % category] = category_score
    data['mean_score'] = np.mean([data[key] for key in data if key.startswith('level_')])
    print('Mean reward: %.2f' % data['mean_score'])
    with open('%s/summary.json' % SAVE_FOLDER, 'w') as f:
        json.dump(data, f)

def _save_frames(episode_frames, config_filepath, episode_idx, category):
    episode_frames = np.array(episode_frames)
    episode_frames = (episode_frames*255).astype(np.uint8)
    if episode_idx is not None:
        filepath = os.path.join(SAVE_FOLDER, category, '%s_%03d.npz' % (
            os.path.splitext(os.path.basename(config_filepath))[0], episode_idx))
    else:
        filepath = os.path.join(SAVE_FOLDER, category, '%s.npz' % (
            os.path.splitext(os.path.basename(config_filepath))[0]))
    try:
        np.savez(filepath, frame=episode_frames)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(filepath))
        np.savez(filepath, frame=episode_frames)

def _prepare_saving_folder():
    if os.path.exists(SAVE_FOLDER):
        shutil.rmtree(SAVE_FOLDER)
    os.makedirs(SAVE_FOLDER)

def _print_red(text):
    print("\x1b[31m" + text + "\x1b[0m")

def _print_green(text):
    print("\x1b[32m" + text + "\x1b[0m")

def _print_yellow(text):
    print("\x1b[33m" + text + "\x1b[0m")

if __name__ == '__main__':
    main()
