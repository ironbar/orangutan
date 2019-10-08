"""
Functions for creating arenas for obstacles category
"""
import numpy as np
from animalai.envs.arena_config import Vector3, RGB, Item, Arena, ArenaConfig

from orangutan.arenas.utils import GRAY, PINK, BLUE
from orangutan.arenas.geometry import detect_collisions, CollisionDetected

DEFAULT_TIME_LIMIT = 500
DEFAULT_REWARD = 2

# TODO: add empty group of boxes
# TODO: add boxes surrounding goal


def create_arena_with_obstacles(t=DEFAULT_TIME_LIMIT):
    arena = Arena(t=t, items=[])
    _add_rewards_to_arena(arena)
    _add_obstacles_to_arena(arena, np.random.randint(5, 10))
    _add_badgoals_to_arena(arena, np.random.randint(2, 7))
    return arena

def _add_rewards_to_arena(arena):
    funcs = {
        0: _add_goal_on_top_of_platform,
        1: _add_goal_on_top_of_box,
        2: _add_goal_inside_cillinder,
        3: _add_simple_goal,
    }
    func_keys = np.short(np.random.randint(0, np.max(list(funcs.keys()))+1, 2))
    for key in func_keys:
        funcs[key](arena)
    if np.random.uniform() < 0.2:
        _add_goal_on_top_of_platform(arena, empty_platform=True)

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
            detect_collisions(box, arena.items)
            arena.items.append(box)
            break
        except CollisionDetected:
            pass
    goal = Item(name='GoodGoalMulti', sizes=[Vector3(*[1]*3)], positions=[Vector3(x, box.sizes[0].y, z)])
    arena.items.append(goal)

def _add_goal_on_top_of_platform(arena, empty_platform=False):
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
    if not empty_platform:
        goal = Item(name='GoodGoalMulti', sizes=[Vector3(*[1]*3)], positions=[Vector3(x, platform.sizes[0].y, z)])
        arena.items.append(goal)

def _add_goal_inside_cillinder(arena):
    while 1:
        try:
            cillinder = _create_random_cillinder()
            border_distance = np.max([cillinder.sizes[0].x, cillinder.sizes[0].z])*1.2
            x, z = np.random.uniform(border_distance, 40 -border_distance, 2).tolist()
            cillinder.positions = [Vector3(x, 0, z)]
            detect_collisions(cillinder, arena.items)
            arena.items.append(cillinder)
            break
        except CollisionDetected:
            pass
    goal = Item(name='GoodGoalMulti', sizes=[Vector3(*[1]*3)], positions=[Vector3(x, 0, z)])
    arena.items.append(goal)

def _add_obstacles_to_arena(arena, n_obstacles=5):
    for _ in range(n_obstacles):
        if np.random.randint(0, 2):
            _add_random_inmovable_object(arena)
        else:
            _add_random_movable_object(arena)

def _add_badgoals_to_arena(arena, n_badgoals=5):
    for _ in range(n_badgoals):
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

"""
More levels
"""

def create_center_blocked_arena(t):
    arena = Arena(t=t, items=[])
    _add_center_blocking_wall(arena)
    for _ in range(DEFAULT_REWARD):
        _add_simple_goal(arena)
    _add_badgoals_to_arena(arena, np.random.randint(2, 7))
    for _ in range(np.random.randint(2, 6)):
        _add_random_box(arena)
    if np.random.randint(0, 2):
        _add_random_wooden_object(arena)
    return arena

def _add_center_blocking_wall(arena):
    inmovable_objects = ['Wall', 'WallTransparent']
    name = str(np.random.choice(inmovable_objects))
    colors = [GRAY]
    sizes = [Vector3(float(np.random.randint(15, 25)),
                     float(np.random.randint(2, 10)),
                     float(np.random.randint(15, 25)))]
    positions = [Vector3(20, 0, 20)]
    item = Item(name=name, sizes=sizes, colors=colors, positions=positions)
    arena.items.append(item)

def create_arena_splitted_in_two(t):
    arena = Arena(t=t, items=[])
    _split_arena_in_two(arena)
    for _ in range(DEFAULT_REWARD):
        _add_simple_goal(arena)
    _add_badgoals_to_arena(arena, np.random.randint(2, 7))
    for _ in range(np.random.randint(2, 4)):
        _add_random_box(arena)
    for _ in range(np.random.randint(1, 3)):
        _add_random_wooden_object(arena)
    return arena

def _split_arena_in_two(arena, block_path=False):
    inmovable_objects = ['Wall', 'WallTransparent']
    name = str(np.random.choice(inmovable_objects))
    colors = [GRAY]
    wall_position = np.random.randint(10, 31)
    hole_position = np.random.randint(10, 31)
    hole_width = np.random.randint(2, 6)

    wall_1_width = hole_position - hole_width/2
    wall_2_width = 40 - hole_position - hole_width/2

    if np.random.randint(0, 2):
        sizes = [Vector3(float(wall_1_width),
                        float(np.random.randint(2, 10)),
                        float(np.random.randint(1, 5)))]
        positions = [Vector3( wall_1_width/2, 0, wall_position)]
        item = Item(name=name, sizes=sizes, colors=colors, positions=positions, rotations=[0])
        arena.items.append(item)

        sizes = [Vector3(float(wall_2_width),
                        float(np.random.randint(2, 10)),
                        float(np.random.randint(1, 5)))]
        positions = [Vector3(40 - wall_2_width/2, 0, wall_position) ]
        item = Item(name=name, sizes=sizes, colors=colors, positions=positions, rotations=[0])
        arena.items.append(item)
        if block_path:
            box = _create_random_box()
            box.sizes = [Vector3(hole_width-0.5, box.sizes[0].y, box.sizes[0].z)]
            box.positions = [Vector3( wall_1_width + hole_width/2, 0, wall_position)]
            box.rotations = [0]
            arena.items.append(box)

    else:
        sizes = [Vector3(float(np.random.randint(1, 5)),
                        float(np.random.randint(2, 10)),
                        float(wall_1_width))]
        positions = [Vector3(wall_position, 0, wall_1_width/2)]
        item = Item(name=name, sizes=sizes, colors=colors, positions=positions, rotations=[0])
        arena.items.append(item)

        sizes = [Vector3(float(np.random.randint(1, 5)),
                        float(np.random.randint(2, 10)),
                        float(wall_2_width))]
        positions = [Vector3(wall_position, 0, 40 - wall_2_width/2)]
        item = Item(name=name, sizes=sizes, colors=colors, positions=positions, rotations=[0])
        arena.items.append(item)
        if block_path:
            box = _create_random_box()
            box.sizes = [Vector3(box.sizes[0].x, box.sizes[0].y, hole_width-0.5)]
            box.positions = [Vector3( wall_position, 0, wall_1_width + hole_width/2)]
            box.rotations = [0]
            arena.items.append(box)

def create_arena_splitted_in_four(t):
    arena = Arena(t=t, items=[])
    _split_arena_in_four(arena)
    for _ in range(DEFAULT_REWARD):
        _add_simple_goal(arena)
    _add_badgoals_to_arena(arena, np.random.randint(2, 7))
    for _ in range(np.random.randint(2, 4)):
        _add_random_box(arena)
    for _ in range(np.random.randint(1, 3)):
        _add_random_wooden_object(arena)
    return arena

def _split_arena_in_four(arena):
    inmovable_objects = ['Wall', 'WallTransparent']
    name = str(np.random.choice(inmovable_objects))
    colors = [GRAY]

    wall_position = float(np.random.randint(13, 16))
    wall_width = float(np.random.randint(19, 22))
    wall_thickness = 1

    sizes = [Vector3(
        float(wall_width),
        float(np.random.randint(2, 10)),
        float(wall_thickness))]
    positions = [Vector3(wall_width/2, 0, wall_position)]
    item = Item(name=name, sizes=sizes, colors=colors, positions=positions, rotations=[0])
    arena.items.append(item)
    positions = [Vector3(40-wall_width/2, 0, 40-wall_position)]
    item = Item(name=name, sizes=sizes, colors=colors, positions=positions, rotations=[0])
    arena.items.append(item)

    sizes = [Vector3(
        float(wall_thickness),
        float(np.random.randint(2, 10)),
        float(wall_width))]
    positions = [Vector3(wall_position, 0, 40-wall_width/2)]
    item = Item(name=name, sizes=sizes, colors=colors, positions=positions, rotations=[0])
    arena.items.append(item)
    positions = [Vector3(40-wall_position, 0, wall_width/2)]
    item = Item(name=name, sizes=sizes, colors=colors, positions=positions, rotations=[0])
    arena.items.append(item)

def create_arena_splitted_in_two_with_path_blocked(t):
    arena = Arena(t=t, items=[])
    _split_arena_in_two(arena, block_path=True)
    for _ in range(DEFAULT_REWARD):
        _add_simple_goal(arena)
    _add_badgoals_to_arena(arena, np.random.randint(2, 7))
    for _ in range(np.random.randint(2, 4)):
        _add_random_box(arena)
    for _ in range(np.random.randint(1, 3)):
        _add_random_wooden_object(arena)
    return arena