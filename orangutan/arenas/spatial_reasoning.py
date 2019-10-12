"""
Spatial reasoning
"""
import numpy as np
from animalai.envs.arena_config import Vector3, RGB, Item, Arena, ArenaConfig

from orangutan.arenas.utils import GRAY, PINK, BLUE
from orangutan.arenas.geometry import detect_collisions, CollisionDetected
from orangutan.arenas.maze import Maze

DEFAULT_REWARD = 2

def create_arena_with_walls_maze(t):
    arena = Arena(t=t, items=[])
    _add_walls_maze(arena, n_cells=5, wall_thickness=1)
    return arena

def _add_walls_maze(arena, n_cells, wall_thickness):
    _add_wall_pillars_to_maze(arena, n_cells, wall_thickness)
    _add_walls(arena, n_cells, wall_thickness)

def _add_wall_pillars_to_maze(arena, n_cells, wall_thickness):
    positions = _get_pillars_positions(n_cells)
    sizes = [Vector3(wall_thickness, 5, wall_thickness)]*len(positions)
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
    print(maze)

    for cell in maze.cells:
        positions, sizes = _get_cell_walls_positions_and_sizes(
            cell, wall_thickness, n_cells)
        if positions:
            wall = Item(name='Wall', positions=positions, rotations=[0]*len(positions), sizes=sizes)
            arena.items.append(wall)

def _get_cell_walls_positions_and_sizes(cell, wall_thickness, n_cells):
    centers = np.linspace(0, 40, n_cells, endpoint=False)[1:].tolist()
    wall_length = (40 - n_cells*wall_thickness)/n_cells

    positions, sizes = [], []
    cell_x_idx = cell.x
    cell_z_idx = cell.y

    # horizontal walls
    if cell_z_idx < n_cells - 1 and 's' in cell.walls:
        sizes.append(Vector3(wall_length, 5, wall_thickness))
        if not cell_x_idx:
            x = centers[cell_x_idx] - wall_length/2 - wall_thickness/2
        else:
            x = centers[cell_x_idx - 1] + wall_length/2 + wall_thickness/2
        positions.append(Vector3(x, 0, centers[cell_z_idx]))

    # vertical walls
    if cell_x_idx < n_cells - 1 and 'e' in cell.walls:
        sizes.append(Vector3(wall_thickness, 5, wall_length))
        if not cell_z_idx:
            z = centers[cell_z_idx] - wall_length/2 - wall_thickness/2
        else:
            z = centers[cell_z_idx - 1] + wall_length/2 + wall_thickness/2
        positions.append(Vector3(centers[cell_x_idx], 0, z))
    return positions, sizes
