"""
Functions for creating arenas for preferences category
"""
import numpy as np
from animalai.envs.arena_config import Vector3, RGB, Item, Arena, ArenaConfig

from orangutan.arenas.geometry import get_angle_looking_center, get_random_position, normalize_angle, get_position_in_front_of_agent, get_random_position_close_to_center
from orangutan.arenas.food import _create_agent_looking_center_at_random_position, _create_goal_in_front_of_agent

DEFAULT_TIME_LIMIT = 500
DEFAULT_REWARD = 2

def create_arena_with_different_sizes_green_goal_in_front_of_agent(t=DEFAULT_TIME_LIMIT):
    arena = Arena(t=t, items=[])
    agent, x, z, angle = _create_agent_looking_center_at_random_position()

    arena.items.append(agent)
    size_small = DEFAULT_REWARD
    size_big = DEFAULT_REWARD*2
    angle_big = angle + np.random.randint(-20, 21)
    angle_small = angle + np.random.randint(-20, 21)
    while abs(angle_big - angle_small) < 15:
        angle_small = angle + np.random.randint(-20, 21)

    arena.items.append(_create_goal_in_front_of_agent(
        x, z, angle_big, goal_type='GoodGoal',
        min_distance=5, max_distance=20, size=size_big))
    arena.items.append(_create_goal_in_front_of_agent(
        x, z, angle_small, goal_type='GoodGoal',
        min_distance=5, max_distance=20, size=size_small))
    return arena

def create_arena_with_same_size_one_close_and_one_farther_goal_in_front_of_agent(t=DEFAULT_TIME_LIMIT):
    arena = Arena(t=t, items=[])
    agent, x, z, angle = _create_agent_looking_center_at_random_position()

    arena.items.append(agent)
    size = DEFAULT_REWARD
    angle_close = angle + np.random.randint(-20, 21)
    angle_far = angle + np.random.randint(-20, 21)
    while abs(angle_close - angle_far) < 15:
        angle_far = angle + np.random.randint(-20, 21)

    arena.items.append(_create_goal_in_front_of_agent(
        x, z, angle_close, goal_type='GoodGoal',
        min_distance=5, max_distance=10, size=size))
    arena.items.append(_create_goal_in_front_of_agent(
        x, z, angle_far, goal_type='GoodGoal',
        min_distance=19, max_distance=40, size=size))
    return arena

def create_arena_with_different_sizes_green_goal_separated_by_wall(t=DEFAULT_TIME_LIMIT):
    arena = Arena(t=t, items=[])
    agent, x, z, angle = _create_agent_looking_center_at_random_position()

    arena.items.append(agent)
    size_small = DEFAULT_REWARD
    size_big = DEFAULT_REWARD*2
    angle_big = angle + np.random.randint(-20, 21)
    angle_small = angle + np.random.randint(-20, 21)
    while abs(angle_big - angle_small) < 15:
        angle_small = angle + np.random.randint(-20, 21)

    arena.items.append(_create_goal_in_front_of_agent(
        x, z, angle_big, goal_type='GoodGoal',
        min_distance=15, max_distance=20, size=size_big))


    arena.items.append(_create_wall_in_front_of_agent(
        x, z, angle, wall_type='WallTransparent', min_distance=11, max_distance=14))

    arena.items.append(_create_goal_in_front_of_agent(
        x, z, angle_small, goal_type='GoodGoal',
        min_distance=5, max_distance=10, size=size_small))
    return arena

def create_arena_with_same_size_green_goal_separated_by_wall(t=DEFAULT_TIME_LIMIT):
    arena = Arena(t=t, items=[])
    agent, x, z, angle = _create_agent_looking_center_at_random_position()

    arena.items.append(agent)
    size_small = DEFAULT_REWARD
    size_big = DEFAULT_REWARD
    angle_big = angle + np.random.randint(-20, 21)
    angle_small = angle + np.random.randint(-20, 21)
    while abs(angle_big - angle_small) < 15:
        angle_small = angle + np.random.randint(-20, 21)

    arena.items.append(_create_goal_in_front_of_agent(
        x, z, angle_big, goal_type='GoodGoal',
        min_distance=15, max_distance=20, size=size_big))


    arena.items.append(_create_wall_in_front_of_agent(
        x, z, angle, wall_type='WallTransparent', min_distance=11, max_distance=14))

    arena.items.append(_create_goal_in_front_of_agent(
        x, z, angle_small, goal_type='GoodGoal',
        min_distance=5, max_distance=10, size=size_small))
    return arena

def create_arena_with_yellow_goal_separated_by_wall(t=DEFAULT_TIME_LIMIT):
    arena = Arena(t=t, items=[])
    agent, x, z, angle = _create_agent_looking_center_at_random_position()

    arena.items.append(agent)
    size_small = DEFAULT_REWARD
    size_big = DEFAULT_REWARD
    angle_big = angle + np.random.randint(-20, 21)
    angle_small = angle + np.random.randint(-20, 21)
    while abs(angle_big - angle_small) < 15:
        angle_small = angle + np.random.randint(-20, 21)

    arena.items.append(_create_goal_in_front_of_agent(
        x, z, angle_big, goal_type='GoodGoalMulti',
        min_distance=15, max_distance=20, size=size_big))


    arena.items.append(_create_wall_in_front_of_agent(
        x, z, angle, wall_type='WallTransparent', min_distance=11, max_distance=14))

    arena.items.append(_create_goal_in_front_of_agent(
        x, z, angle_small, goal_type='GoodGoal',
        min_distance=5, max_distance=10, size=size_small))
    return arena

def _create_wall_in_front_of_agent(x, z, angle, wall_type='WallTransparent', min_distance=15, max_distance=20):
    size = 1
    while 1:
        distance = np.random.randint(min_distance, max_distance)
        x_new, z_new = get_position_in_front_of_agent(x, z, angle, distance)
        if x_new > 0 + size/2 and x_new < 40 - size/2 and z_new > 0 + size/2 and z_new < 40 - size/2:
            break
    height = np.random.uniform(5, 10)
    width = np.random.uniform(10, 20)
    thickness = np.random.uniform(1, 2)
    wall = Item(name=wall_type, positions=[Vector3(x_new, 0, z_new)], sizes=[Vector3(width, height, thickness)],
                rotations=[normalize_angle(angle)])
    return wall
