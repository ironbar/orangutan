"""
Avoidance levels
"""
import numpy as np
from animalai.envs.arena_config import Vector3, RGB, Item, Arena, ArenaConfig

from orangutan.arenas.utils import GRAY, PINK, BLUE
from orangutan.arenas.geometry import detect_collisions, CollisionDetected
from orangutan.arenas.obstacles import (
    _add_obstacles_to_arena,
    _add_badgoals_to_arena,
    _add_goal_inside_cillinder,
    _add_goal_on_top_of_box,
    _add_goal_on_top_of_platform,
    _add_center_blocking_wall,
    _add_random_box,
    _add_random_wooden_object
)

DEFAULT_TIME_LIMIT = 500
DEFAULT_REWARD = 2

def create_arena_with_obstacles_and_deathzones(t=DEFAULT_TIME_LIMIT):
    arena = Arena(t=t, items=[])
    _add_rewards_to_arena(arena)
    _add_zones_to_arena(arena, np.random.randint(2, 5))
    _add_agent_to_arena(arena)
    _add_obstacles_to_arena(arena, np.random.randint(5, 10))
    _add_badgoals_to_arena(arena, np.random.randint(2, 7))
    return arena

def _add_rewards_to_arena(arena):
    funcs = {
        0: _add_goal_on_top_of_platform,
        1: _add_goal_on_top_of_box,
        2: _add_goal_inside_cillinder,
        3: _add_goal_above_hot_zone,
        4: _add_simple_goal,
    }
    func_keys = np.short(np.random.randint(0, np.max(list(funcs.keys()))+1, 2))
    for key in func_keys:
        funcs[key](arena)
    if np.random.uniform() < 0.2:
        _add_goal_on_top_of_platform(arena, empty_platform=True)
    # commented because the episode did not end because of that goal
    # if np.random.uniform() > 0.2:
    #     _add_goal_above_death_zone(arena)

def _add_simple_goal(arena):
    while 1:
        try:
            x, z = np.random.uniform(1, 39, 2).tolist()
            goal = Item(name='GoodGoalMulti', sizes=[Vector3(*[1]*3)], rotations=[0])
            goal.positions = [Vector3(x, 0, z)]
            detect_collisions(goal, arena.items)
            arena.items.append(goal)
            break
        except CollisionDetected:
            pass

def _add_goal_above_hot_zone(arena):
    while 1:
        try:
            zone = _create_random_zone(['HotZone'])
            border_distance = np.max([zone.sizes[0].x, zone.sizes[0].z])*1.2
            x, z = np.random.uniform(border_distance, 40 -border_distance, 2).tolist()
            zone.positions = [Vector3(x, 0, z)]
            detect_collisions(zone, arena.items)
            arena.items.append(zone)
            break
        except CollisionDetected:
            pass
    goal = Item(name='GoodGoalMulti', sizes=[Vector3(*[1]*3)], positions=[Vector3(x, 0, z)])
    arena.items.append(goal)

def _add_goal_above_death_zone(arena):
    while 1:
        try:
            zone = _create_random_zone(['DeathZone'])
            border_distance = np.max([zone.sizes[0].x, zone.sizes[0].z])*1.2
            x, z = np.random.uniform(border_distance, 40 -border_distance, 2).tolist()
            zone.positions = [Vector3(x, 0, z)]
            detect_collisions(zone, arena.items)
            arena.items.append(zone)
            break
        except CollisionDetected:
            pass
    name = str(np.random.choice(['GoodGoalMulti', 'GoodGoal']))
    goal = Item(name=name, sizes=[Vector3(*[1]*3)], positions=[Vector3(x, 0, z)])
    arena.items.append(goal)

def _add_zones_to_arena(arena, n_zones):
    for _ in range(n_zones):
        while 1:
            try:
                zone = _create_random_zone()
                border_distance = np.max([zone.sizes[0].x, zone.sizes[0].z])*1.2
                x, z = np.random.uniform(border_distance, 40 -border_distance, 2).tolist()
                zone.positions = [Vector3(x, 0, z)]
                detect_collisions(zone, arena.items)
                arena.items.append(zone)
                break
            except CollisionDetected:
                pass

def _create_random_zone(zone_types=None):
    if zone_types is None:
        zone_types = ['DeathZone', 'HotZone']
    name = str(np.random.choice(zone_types))
    sizes = [Vector3(*np.random.randint(2, 10, 3).tolist())]
    item = Item(name=name, sizes=sizes, rotations=[float(np.random.randint(0, 360))])
    return item

def _add_agent_to_arena(arena):
    while 1:
        try:
            x, z = np.random.uniform(1, 39, 2).tolist()
            goal = Item(name='Agent', sizes=[Vector3(*[1]*3)])
            goal.positions = [Vector3(x, 0, z)]
            detect_collisions(goal, arena.items)
            arena.items.append(goal)
            break
        except CollisionDetected:
            pass

"""
More levels
"""

def create_center_blocked_arena(t):
    arena = Arena(t=t, items=[])
    _add_center_blocking_wall(arena)
    for item in arena.items:
        item.name = 'DeathZone'
    _add_agent_to_arena(arena)
    for _ in range(DEFAULT_REWARD):
        _add_simple_goal(arena)
    _add_badgoals_to_arena(arena, np.random.randint(2, 7))
    for _ in range(np.random.randint(2, 6)):
        _add_random_box(arena)
    if np.random.randint(0, 2):
        _add_random_wooden_object(arena)
    return arena