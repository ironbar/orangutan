"""
Functions for creating arenas for obstacles category
"""
import numpy as np
from animalai.envs.arena_config import Vector3, RGB, Item, Arena, ArenaConfig

from orangutan.arenas.utils import GRAY, PINK, BLUE
from orangutan.arenas.geometry import detect_collisions, CollisionDetected

DEFAULT_TIME_LIMIT = 500
DEFAULT_REWARD = 2

# TODO: add empty platforms
# TODO: add empty group of boxes
# TODO: add goal inside tunnel


def create_arena_with_obstacles(t=DEFAULT_TIME_LIMIT):
    arena = Arena(t=t, items=[])
    _add_rewards_to_arena(arena)
    # _add_obstacles_to_arena(arena)
    # _add_badgoals_to_arena(arena)
    return arena

def _add_rewards_to_arena(arena):
    # TODO: add more complex goals
    for _ in range(DEFAULT_REWARD):
        _add_goal_on_top_of_platform(arena)
        _add_goal_on_top_of_box(arena)
        _add_goal_inside_cillinder(arena)
        # _add_simple_goal(arena)

def _add_simple_goal(arena):
    item = Item(name='GoodGoalMulti', sizes=[Vector3(*[1]*3)])
    arena.items.append(item)

def _add_goal_on_top_of_box(arena):
    while 1:
        try:
            box = _create_random_box()
            border_distance = np.max([box.sizes[0].x, box.sizes[0].z])*1.2
            x, z = np.random.uniform(border_distance, 40 -border_distance, 2).tolist()
            box.positions = [Vector3(x, 0, z)]
            arena.items.append(box)
            break
        except CollisionDetected:
            pass
    goal = Item(name='GoodGoalMulti', sizes=[Vector3(*[1]*3)], positions=[Vector3(x, box.sizes[0].y, z)])
    arena.items.append(goal)

def _add_goal_on_top_of_platform(arena):
    while 1:
        try:
            platform = _create_random_platform()
            border_distance = np.max([platform.sizes[0].x, platform.sizes[0].z])*1.2
            x, z = np.random.uniform(border_distance, 40 -border_distance, 2).tolist()
            platform.positions = [Vector3(x, 0, z)]
            ramp = _create_ramp_for_platform(platform)
            detect_collisions(ramp, arena.items)
            detect_collisions(platform, arena.items)
            arena.items.append(platform)
            arena.items.append(ramp)
            break
        except CollisionDetected:
            pass
    goal = Item(name='GoodGoalMulti', sizes=[Vector3(*[1]*3)], positions=[Vector3(x, platform.sizes[0].y, z)])
    arena.items.append(goal)

def _add_goal_inside_cillinder(arena):
    while 1:
        try:
            cillinder = _create_random_cillinder()
            border_distance = np.max([cillinder.sizes[0].x, cillinder.sizes[0].z])*1.2
            x, z = np.random.uniform(border_distance, 40 -border_distance, 2).tolist()
            cillinder.positions = [Vector3(x, 0, z)]
            arena.items.append(cillinder)
            break
        except CollisionDetected:
            pass
    goal = Item(name='GoodGoalMulti', sizes=[Vector3(*[1]*3)], positions=[Vector3(x, 0, z)])
    arena.items.append(goal)

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
    arena.items.append(_create_random_box())

def _create_random_box():
    movable_objects = ['Cardbox1', 'Cardbox2']
    name = str(np.random.choice(movable_objects))
    sizes = [Vector3(*np.random.randint(1, 6, 3).tolist())]
    item = Item(name=name, sizes=sizes)
    return item

def _add_random_wooden_object(arena):
    movable_objects = ['UObject', 'LObject', 'LObject2']
    name = str(np.random.choice(movable_objects))
    sizes = [Vector3(-1, -1, float(np.random.randint(3, 10)))]
    item = Item(name=name, sizes=sizes)
    arena.items.append(item)

def _add_random_inmovable_object(arena):
    inmovable_objects = ['Wall', 'WallTransparent', 'Ramp', 'CylinderTunnelTransparent', 'CylinderTunnel']
    name = str(np.random.choice(inmovable_objects))
    if name in ['Wall', 'CylinderTunnel']:
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

def _create_random_platform():
    name = 'Wall'
    colors = [BLUE]
    x, z = np.random.randint(4, 8, 2).tolist()
    y = float(np.random.randint(1, 3))
    sizes = [Vector3(x, y, z)]
    item = Item(name=name, sizes=sizes, colors=colors, rotations=[0])
    return item

def _create_random_cillinder():
    inmovable_objects = ['CylinderTunnelTransparent', 'CylinderTunnel']
    name = str(np.random.choice(inmovable_objects))
    if name == 'CylinderTunnel':
        colors = [GRAY]
    else:
        colors = []
    sizes = [Vector3(*np.random.randint(3, 10, 3).tolist())]
    item = Item(name=name, sizes=sizes, colors=colors)
    return item

def _create_ramp_for_platform(platform, rotation=None):
    """
    Creates a ramp that allows to climb the platform

    Parameters
    ----------
    platform : Item
    rotation : int
        If given the ramp will be placed with that orientation, otherwise it will
        be randomly sampled from 0, 90, 180, 270
    """
    position = platform.positions[0]
    size = platform.sizes[0]
    if rotation is None:
        rotation = float(np.random.choice([0, 90, 180, 270]))
    else:
        assert rotation in [0, 90, 180, 270]
    sizes = platform.sizes
    ramp_length = size.y*np.random.uniform(1, 3)
    if rotation == 0:
        sizes = [Vector3(size.x, size.y, ramp_length)]
        displacement = (size.z + ramp_length)/2
        positions = [Vector3(position.x, position.y, position.z + displacement)]
    elif rotation == 180:
        sizes = [Vector3(size.x, size.y, ramp_length)]
        displacement = (size.z + ramp_length)/2
        positions = [Vector3(position.x, position.y, position.z - displacement)]
    elif rotation == 90:
        sizes = [Vector3(size.z, size.y, ramp_length)]
        displacement = (size.x + ramp_length)/2
        positions = [Vector3(position.x + displacement, position.y, position.z)]
    elif rotation == 270:
        sizes = [Vector3(size.z, size.y, ramp_length)]
        displacement = (size.x + ramp_length)/2
        positions = [Vector3(position.x - displacement, position.y, position.z)]
    item = Item(name='Ramp', sizes=sizes, colors=[PINK], rotations=[rotation], positions=positions)
    return item