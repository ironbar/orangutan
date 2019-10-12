"""
Spatial reasoning
"""
import numpy as np
from animalai.envs.arena_config import Vector3, RGB, Item, Arena, ArenaConfig

from orangutan.arenas.utils import GRAY, PINK, BLUE
from orangutan.arenas.geometry import detect_collisions, CollisionDetected

DEFAULT_REWARD = 2

def create_arena_with_walls_maze(t):
    arena = Arena(t=t, items=[])
    _add_walls_maze(arena, n_cells=8, wall_thickness=1)
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
    centers = np.linspace(0, 40, n_cells, endpoint=False)[1:].tolist()
    wall_length = (40 - n_cells*wall_thickness)/n_cells
    for cell_x_idx in range(n_cells):
        for cell_z_idx in range(n_cells):
            if cell_z_idx < n_cells - 1 and np.random.randint(0, 2):
                sizes = [Vector3(wall_length, 5, wall_thickness)]
                if not cell_x_idx:
                    x = centers[cell_x_idx] - wall_length/2 - wall_thickness/2
                else:
                    x = centers[cell_x_idx - 1] + wall_length/2 + wall_thickness/2
                positions = [Vector3(x, 0, centers[cell_z_idx])]
                wall = Item(name='Wall', positions=positions, rotations=[0], sizes=sizes)
                arena.items.append(wall)

            if cell_x_idx < n_cells - 1 and np.random.randint(0, 2):
                sizes = [Vector3(wall_thickness, 5, wall_length)]
                if not cell_z_idx:
                    z = centers[cell_z_idx] - wall_length/2 - wall_thickness/2
                else:
                    z = centers[cell_z_idx - 1] + wall_length/2 + wall_thickness/2
                positions = [Vector3(centers[cell_x_idx], 0, z)]
                wall = Item(name='Wall', positions=positions, rotations=[0], sizes=sizes)
                arena.items.append(wall)
