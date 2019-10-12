"""
Spatial reasoning
"""
import numpy as np
from animalai.envs.arena_config import Vector3, RGB, Item, Arena, ArenaConfig

from orangutan.arenas.utils import GRAY, PINK, BLUE
from orangutan.arenas.geometry import detect_collisions, CollisionDetected
from orangutan.arenas.maze import Maze
from orangutan.arenas.avoidance import _add_simple_goal as _add_goal_on_fixed_position
from orangutan.arenas.obstacles import _add_simple_goal
from orangutan.arenas.avoidance import _add_agent_to_arena

DEFAULT_REWARD = 2
WALL_HEIGHT = 5
PLATFORM_HEIGHT = 2

"""
Walls maze
"""

def create_arena_with_walls_maze(t):
    arena = Arena(t=t, items=[])
    _add_walls_maze(arena, n_cells=np.random.randint(4, 7), wall_thickness=1)
    _apply_color_to_wall_maze(arena)
    for _ in range(DEFAULT_REWARD):
        _add_simple_goal(arena)
    return arena

def _add_walls_maze(arena, n_cells, wall_thickness):
    _add_wall_pillars_to_maze(arena, n_cells, wall_thickness)
    _add_walls(arena, n_cells, wall_thickness)

def _add_wall_pillars_to_maze(arena, n_cells, wall_thickness):
    positions = _get_pillars_positions(n_cells)
    sizes = [Vector3(wall_thickness, WALL_HEIGHT, wall_thickness)]*len(positions)
    pillars = Item(name='Wall', positions=positions, rotations=[0]*len(positions), sizes=sizes)
    arena.items.append(pillars)

def _get_pillars_positions(n_cells):
    centers = np.linspace(0, 40, n_cells, endpoint=False)[1:].tolist()
    positions = []
    for x in centers:
        for z in centers:
            positions.append(Vector3(x, 0, z))
    return positions

def _add_walls(arena, n_cells, wall_thickness):
    maze = Maze()
    maze = maze.generate(n_cells, n_cells)
    for cell in maze.cells:
        positions, sizes = _get_cell_walls_positions_and_sizes(
            cell, wall_thickness, n_cells, WALL_HEIGHT)
        if positions:
            wall = Item(name='Wall', positions=positions, rotations=[0]*len(positions), sizes=sizes)
            arena.items.append(wall)

def _get_cell_walls_positions_and_sizes(cell, wall_thickness, n_cells, height):
    centers = np.linspace(0, 40, n_cells, endpoint=False)[1:].tolist()
    positions, sizes = [], []
    cell_x_idx = cell.x
    cell_z_idx = cell.y

    # horizontal walls
    if cell_z_idx < n_cells - 1 and 's' in cell.walls:
        wall_length = (40 - n_cells*wall_thickness)/n_cells
        if not cell_x_idx or cell_x_idx == n_cells -1:
            wall_length += wall_thickness/2
        sizes.append(Vector3(wall_length, height, wall_thickness))
        if not cell_x_idx:
            x = centers[cell_x_idx] - wall_length/2 - wall_thickness/2
        else:
            x = centers[cell_x_idx - 1] + wall_length/2 + wall_thickness/2
        positions.append(Vector3(x, 0, centers[cell_z_idx]))

    # vertical walls
    if cell_x_idx < n_cells - 1 and 'e' in cell.walls:
        wall_length = (40 - n_cells*wall_thickness)/n_cells
        if not cell_z_idx or cell_z_idx == n_cells -1:
            wall_length += wall_thickness/2
        sizes.append(Vector3(wall_thickness, height, wall_length))
        if not cell_z_idx:
            z = centers[cell_z_idx] - wall_length/2 - wall_thickness/2
        else:
            z = centers[cell_z_idx - 1] + wall_length/2 + wall_thickness/2
        positions.append(Vector3(centers[cell_x_idx], 0, z))
    return positions, sizes

def _apply_color_to_wall_maze(arena):
    option = np.random.choice(['random', 'transparent', 'gray'])
    for item in arena.items:
        if option == 'transparent':
            item.name = 'WallTransparent'
        elif option == 'gray':
            item.colors = [GRAY]*len(item.rotations)

"""
Death maze
"""

def create_arena_with_death_maze(t):
    arena = Arena(t=t, items=[])
    _add_walls_maze(arena, n_cells=np.random.randint(4, 6), wall_thickness=4)
    _replace_walls_by_death_zones(arena)
    for _ in range(DEFAULT_REWARD):
        _add_goal_on_fixed_position(arena)
    _add_agent_to_arena(arena)
    return arena

def _replace_walls_by_death_zones(arena):
    for item in arena.items:
        item.name = 'DeathZone'

"""
Platform maze
"""
def create_arena_with_platform_maze(t):
    arena = Arena(t=t, items=[])
    _add_platform_maze(arena, n_cells=np.random.randint(4, 6), wall_thickness=6)
    _apply_color_to_platform_maze(arena)
    for _ in range(DEFAULT_REWARD):
        _add_simple_goal(arena)
    return arena

def _add_platform_maze(arena, n_cells, wall_thickness):
    _add_platforms_to_maze(arena, n_cells, wall_thickness)

def _add_platforms_to_maze(arena, n_cells, wall_thickness):
    maze = Maze()
    maze = maze.generate(n_cells, n_cells)
    print(maze)
    for cell in maze.cells:
        positions, sizes = _get_cell_walls_positions_and_sizes(
            cell, wall_thickness, n_cells, PLATFORM_HEIGHT)
        if positions:
            wall = Item(name='Wall', positions=positions, rotations=[0]*len(positions), sizes=sizes)
            arena.items.append(wall)

def _get_cell_walls_positions_and_sizes(cell, wall_thickness, n_cells, height):
    centers = np.linspace(0, 40, n_cells, endpoint=False)[1:].tolist()
    positions, sizes = [], []
    cell_x_idx = cell.x
    cell_z_idx = cell.y
    # platform
    wall_length_x = (40 - n_cells*wall_thickness)/n_cells
    if not cell_x_idx or cell_x_idx == n_cells -1:
        wall_length_x += wall_thickness/2
    if not cell_x_idx:
        x = centers[cell_x_idx] - wall_length_x/2 - wall_thickness/2
    else:
        x = centers[cell_x_idx - 1] + wall_length_x/2 + wall_thickness/2
    wall_length_z = (40 - n_cells*wall_thickness)/n_cells
    if not cell_z_idx or cell_z_idx == n_cells -1:
        wall_length_z += wall_thickness/2
    if not cell_z_idx:
        z = centers[cell_z_idx] - wall_length_z/2 - wall_thickness/2
    else:
        z = centers[cell_z_idx - 1] + wall_length_z/2 + wall_thickness/2
    positions.append(Vector3(x, 0, z))
    sizes.append(Vector3(wall_length_x, height, wall_length_z))

    # horizontal walls
    if cell_z_idx < n_cells - 1 and 's' not in cell.walls:
        wall_length = (40 - n_cells*wall_thickness)/n_cells
        if not cell_x_idx or cell_x_idx == n_cells -1:
            wall_length += wall_thickness/2
        sizes.append(Vector3(wall_length, height, wall_thickness))
        if not cell_x_idx:
            x = centers[cell_x_idx] - wall_length/2 - wall_thickness/2
        else:
            x = centers[cell_x_idx - 1] + wall_length/2 + wall_thickness/2
        positions.append(Vector3(x, 0, centers[cell_z_idx]))

    # vertical walls
    if cell_x_idx < n_cells - 1 and 'e' not in cell.walls:
        wall_length = (40 - n_cells*wall_thickness)/n_cells
        if not cell_z_idx or cell_z_idx == n_cells -1:
            wall_length += wall_thickness/2
        sizes.append(Vector3(wall_thickness, height, wall_length))
        if not cell_z_idx:
            z = centers[cell_z_idx] - wall_length/2 - wall_thickness/2
        else:
            z = centers[cell_z_idx - 1] + wall_length/2 + wall_thickness/2
        positions.append(Vector3(centers[cell_x_idx], 0, z))
    return positions, sizes

def _apply_color_to_platform_maze(arena):
    option = np.random.choice(['random', 'blue'])
    for item in arena.items:
        if option == 'blue':
            item.colors = [BLUE]*len(item.rotations)