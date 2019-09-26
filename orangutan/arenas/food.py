"""
Functions for creating arenas for food category
"""
import numpy as np
from animalai.envs.arena_config import Vector3, RGB, Item, Arena, ArenaConfig

from orangutan.arenas.geometry import get_angle_looking_center, get_random_position, normalize_angle, get_position_in_front_of_agent, get_random_position_close_to_center

DEFAULT_TIME_LIMIT = 500
DEFAULT_REWARD = 2

def create_arena_with_green_and_yellow_goal_in_front_of_agent(t=DEFAULT_TIME_LIMIT):
    arena = Arena(t=t, items=[])
    agent, x, z, angle = _create_agent_looking_center_at_random_position()

    arena.items.append(agent)
    size = np.random.uniform(0.5, DEFAULT_REWARD - 0.5)
    arena.items.append(_create_goal_in_front_of_agent(
        x, z, angle + np.random.randint(-20, 21), goal_type='GoodGoalMulti',
        min_distance=5, max_distance=20, size=size))
    size = DEFAULT_REWARD - size
    arena.items.append(_create_goal_in_front_of_agent(
        x, z, angle + np.random.randint(-20, 21), goal_type='GoodGoal',
        min_distance=5, max_distance=20, size=size))
    return arena

def create_arena_with_red_goal_coming(t=DEFAULT_TIME_LIMIT):
    arena = Arena(t=t, items=[])
    agent, x, z, angle = _create_agent_looking_center_closer_to_center()

    arena.items.append(agent)
    arena.items.append(_create_goal_in_front_of_agent(
        x, z, angle, goal_type='BadGoalBounce', min_distance=15, max_distance=20))
    arena = _add_reward_to_arena(arena)
    return arena

def _create_agent_looking_center_at_random_position():
    x, z = get_random_position()
    angle = get_angle_looking_center(x, z)
    agent = Item(name='Agent', positions=[Vector3(x, 0, z)], rotations=[angle])
    return agent, x, z, angle

def _create_agent_looking_center_closer_to_center():
    x, z = get_random_position_close_to_center()
    angle = get_angle_looking_center(x, z)
    agent = Item(name='Agent', positions=[Vector3(x, 0, z)], rotations=[angle])
    return agent, x, z, angle

def _create_goal_in_front_of_agent(x, z, angle, goal_type='BadGoalBounce', min_distance=15, max_distance=20, size=-1):
    distance = np.random.randint(min_distance, max_distance)
    x, z = get_position_in_front_of_agent(x, z, angle, distance)
    goal = Item(name=goal_type, positions=[Vector3(x, 0, z)], sizes=[Vector3(size, size, size)],
                rotations=[normalize_angle(angle+180)])
    return goal

def _add_reward_to_arena(arena, reward=DEFAULT_REWARD):
    remaining_reward = reward
    while remaining_reward:
        new_reward = np.random.uniform(0, remaining_reward)
        if new_reward < 0.5:
            new_reward = 0.5
        if remaining_reward - new_reward < 0.5:
            new_reward = remaining_reward
        remaining_reward -= new_reward
        goal = Item(name='GoodGoalMulti', sizes=[Vector3(new_reward, new_reward, new_reward)])
        arena.items.append(goal)
    return arena
