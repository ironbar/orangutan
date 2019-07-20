"""
Script for testing and evaluating the docker
"""
import glob
import os
import sys
import importlib.util
import numpy as np

from animalai.envs.gym.environment import AnimalAIEnv
from animalai.envs.arena_config import ArenaConfig


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

    config_filepaths = sorted(glob.glob('/aaio/test/configs/*.yaml'))
    rewards = []
    for config_filepath in config_filepaths:
        rewards.append(evaluate_config(config_filepath, env, submitted_agent))
    _summarize_rewards(rewards, config_filepaths)
    print('SUCCESS')

def evaluate_config(config_filepath, env, submitted_agent, n_episodes=10):
    arena_config_in = ArenaConfig(config_filepath)
    env.reset(arenas_configurations=arena_config_in)
    obs, reward, done, info = env.step([0, 0])

    print('\t%s' % os.path.basename(config_filepath))
    rewards = []
    for k in range(n_episodes):
        _reset_agent(submitted_agent, arena_config_in)
        cumulated_reward = 0
        try:
            for i in range(arena_config_in.arenas[0].t):
                action = submitted_agent.step(obs, reward, done, info)
                obs, reward, done, info = env.step(action)
                cumulated_reward += reward
                if done:
                    _reset_agent(submitted_agent, arena_config_in)
                    break
        except Exception as e:
            print('Episode {} failed'.format(k))
            raise e
        print('Episode %i: %.2f' % (k, cumulated_reward))
        rewards.append(cumulated_reward)
        sys.stdout.flush()
    return rewards

def _reset_agent(agent, arena):
    try:
        agent.reset(t=arena.arenas[0].t)
    except Exception as e:
        print('Your agent could not be reset:')
        raise e

def _summarize_rewards(rewards, config_filepaths):
    print('\nRewards summary')
    for reward, config_filepath in zip(rewards, config_filepaths):
        print('%.2f\t %s' % (np.mean(reward), os.path.basename(config_filepath)))
    print('Mean reward: %.2f' % np.mean(rewards))

if __name__ == '__main__':
    main()
