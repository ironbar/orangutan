"""
Functions for creating arenas for obstacles category
"""
import numpy as np
from animalai.envs.arena_config import Vector3, RGB, Item, Arena, ArenaConfig

from orangutan.arenas.utils import GRAY, PINK

DEFAULT_TIME_LIMIT = 500
DEFAULT_REWARD = 2

def create_arena_with_obstacles(t=DEFAULT_TIME_LIMIT):
    arena = Arena(t=t, items=[])
    _add_rewards_to_arena(arena)
    _add_obstacles_to_arena(arena)
    _add_badgoals_to_arena(arena)
    return arena

def _add_rewards_to_arena(arena):
    # TODO: add more complex goals
    for _ in range(DEFAULT_REWARD):
        item = Item(name='GoodGoalMulti', sizes=[Vector3(*[1]*3)])
        arena.items.append(item)

def _add_obstacles_to_arena(arena):
    for _ in range(10):
        _add_random_inmovable_object(arena)
        _add_random_movable_object(arena)

def _add_badgoals_to_arena(arena):
    for _ in range(5):
        item = Item(name='BadGoal', sizes=[Vector3(*[1]*3)])
        arena.items.append(item)

def _add_random_movable_object(arena):
    if np.random.randint(0, 2):
        _add_random_box(arena)
    else:
        _add_random_wooden_object(arena)

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

def _add_random_inmovable_object(arena):
    inmovable_objects = ['Wall', 'WallTransparent', 'Ramp', 'Cillinder', 'CillinderTransparent']
    name = str(np.random.choice(inmovable_objects))
    if name in ['Wall', 'Cillinder']:
        colors = [GRAY]
    elif name == 'Ramp':
        colors = [PINK]
    else:
        colors = []
    if 'Wall' in name or name == 'Ramp':
        sizes = [Vector3(*np.random.randint(1, 10, 3).tolist())]
    else:
        sizes = [Vector3(*np.random.randint(3, 10, 3).tolist())]
    item = Item(name=name, sizes=sizes, colors=colors)
    arena.items.append(item)
