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
    angle_yellow = angle + np.random.randint(-20, 21)
    arena.items.append(_create_goal_in_front_of_agent(
        x, z, angle_yellow, goal_type='GoodGoalMulti',
        min_distance=5, max_distance=20, size=size))
    size = DEFAULT_REWARD - size
    angle_green = angle + np.random.randint(-20, 21)
    while abs(angle_yellow - angle_green) < 5:
        angle_green = angle + np.random.randint(-20, 21)
    arena.items.append(_create_goal_in_front_of_agent(
        x, z, angle_green, goal_type='GoodGoal',
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

def create_arena_with_red_wall(t=DEFAULT_TIME_LIMIT):
    arena = Arena(t=t, items=[])
    orientation = np.random.choice(['horizontal', 'vertical'])
    goal_size = np.random.choice([1, 2, 3])
    _add_wall_to_arena(arena, orientation='horizontal', position=np.random.randint(10, 30), goal_size=goal_size)
    if orientation == 'horizontal':
        arena.items.append(Item(name='GoodGoalMulti', sizes=[Vector3(1,1,1)]*2,
        positions=[Vector3(-1,0, np.random.randint(1, 7)), Vector3(-1,0, 40 - np.random.randint(1, 7))]))
    else:
        arena.items.append(Item(name='GoodGoalMulti', sizes=[Vector3(1,1,1)]*2,
        positions=[Vector3(np.random.randint(1, 7), 0, -1), Vector3(40 - np.random.randint(1, 7), 0, -1)]))
    return arena

def create_arena_with_red_houses(t=DEFAULT_TIME_LIMIT):
    arena = Arena(t=t, items=[])
    centers, radiuses = [], []

    for idx in range(4):
        not_good_center = True
        while not_good_center:
            not_good_center = False
            radius = np.random.uniform(2, 4)
            center = np.random.randint(5, 35, 2)
            for _center, _radius in zip(centers, radiuses):
                distance = np.sqrt(np.sum((center - _center)**2))
                if distance < radius + _radius + 4:
                    not_good_center = True
        centers.append(center)
        radiuses.append(radius)
        goal_size = np.random.uniform(1, 2)
        _add_red_circle_to_arena(arena, center=center, radius=radius, goal_size=goal_size)
        if idx < 2:
            arena.items.append(Item(name='GoodGoalMulti', sizes=[Vector3(1,1,1)],
                                    positions=[Vector3(center[0], 0, center[1])]))
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
    while 1:
        distance = np.random.randint(min_distance, max_distance)
        x_new, z_new = get_position_in_front_of_agent(x, z, angle, distance)
        if x_new > 0 + size/2 and x_new < 40 - size/2 and z_new > 0 + size/2 and z_new < 40 - size/2:
            break
    goal = Item(name=goal_type, positions=[Vector3(x_new, 0, z_new)], sizes=[Vector3(size, size, size)],
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

def _add_wall_to_arena(arena, orientation, position, goal_size):
    x_range = np.linspace(goal_size/2, 40 - goal_size/2, int((40 - goal_size)/(goal_size + 0.5))).tolist()
    x_range.pop(np.random.randint(len(x_range)))
    if orientation == 'horizontal':
        positions = [Vector3(position, 0, z) for z in x_range]
    elif orientation == 'vertical':
        positions = [Vector3(x, 0, position) for x in x_range]
    else:
        raise Exception('Unknown orientation: %s' % orientation)
    sizes = [Vector3(goal_size, goal_size, goal_size)]*len(positions)
    goal = Item(name='BadGoal', sizes=sizes, positions=positions)
    arena.items.append(goal)

def _add_red_circle_to_arena(arena, center, radius, goal_size):
    theta_range = np.linspace(0, np.pi*2, int((2*np.pi*radius)/(goal_size + 0.5)), endpoint=False)
    theta_range += np.random.uniform(0, np.pi)
    theta_range = theta_range.tolist()
    theta_range.pop(np.random.randint(len(theta_range)))
    positions = [Vector3(radius*np.cos(theta) + center[0], 0, radius*np.sin(theta)+ center[1]) for theta in theta_range]
    sizes = [Vector3(goal_size, goal_size, goal_size)]*len(positions)
    goal = Item(name='BadGoal', sizes=sizes, positions=positions)
    arena.items.append(goal)