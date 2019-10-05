"""
Functions for creating arenas for obstacles category
"""
import numpy as np
from animalai.envs.arena_config import Vector3, RGB, Item, Arena, ArenaConfig

from orangutan.arenas.geometry import get_angle_looking_center, get_random_position, normalize_angle, get_position_in_front_of_agent, get_random_position_close_to_center
from orangutan.arenas.food import _create_agent_looking_center_at_random_position, _create_goal_in_front_of_agent

DEFAULT_TIME_LIMIT = 500
DEFAULT_REWARD = 2

def create_arena_with_obstacles(t=DEFAULT_TIME_LIMIT):
    arena = Arena(t=t, items=[])
    _add_rewards_to_arena(arena)
    _add_obstacles_to_arena(arena)
    _add_badgoals_to_arena(arena)
    return arena

def _add_rewards_to_arena(arena):
    pass

def _add_obstacles_to_arena(arena):
    for _ in range(5):
        _add_random_box(arena)
        _add_random_wooden_object(arena)

def _add_badgoals_to_arena(arena):
    pass

def _add_random_box(arena):
    movable_objects = ['Cardbox1', 'Cardbox2']
    name = str(np.random.choice(movable_objects))
    sizes = [Vector3(*np.random.randint(1, 6, 3).tolist())]
    item = Item(name=name, sizes=sizes)
    arena.items.append(item)

def _add_random_wooden_object(arena):
    movable_objects = ['UObject', 'LObject', 'LObject2']
    name = str(np.random.choice(movable_objects))
    sizes = [Vector3(-1, -1, float(np.random.randint(3, 10)))]
    item = Item(name=name, sizes=sizes)
    arena.items.append(item)