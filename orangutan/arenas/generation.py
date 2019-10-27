"""
Arenas generation

The main idea behind this module is that levels that are easier or shorter in duration
should have smaller weight when sampling. So each function has an asociated weight that
is used to create the arena configuration.

# Reference for choosing weights

## 1
create_arena_with_different_sizes_green_goal_in_front_of_agent
create_arena_with_same_size_one_close_and_one_farther_goal_in_front_of_agent
create_arena_with_same_size_green_goal_separated_by_wall
create_arena_with_green_and_yellow_goal_in_front_of_agent

## 2
create_arena_with_different_sizes_green_goal_separated_by_wall
create_arena_with_yellow_goal_separated_by_wall

## 4
create_arena_with_red_houses
create_arena_with_red_wall

## 8

"""
import numpy as np
from animalai.envs.arena_config import ArenaConfig

from orangutan.arenas.food import (
    create_arena_with_green_and_yellow_goal_in_front_of_agent,
    create_arena_with_red_goal_coming,
    create_arena_with_red_wall,
    create_arena_with_red_houses,
    create_arena_with_4_goodgoalmulti,
    create_arena_with_4_goodgoalmultibounce,
    create_arena_with_30_badgoal_labyrinth,
    create_arena_with_15_badgoal_labyrinth,
    create_arena_with_5_badgoalbounce_labyrinth,
    create_arena_with_10_badgoalbounce_labyrinth,
    create_arena_with_15_badgoalbounce_labyrinth,
)
from orangutan.arenas.preferences import (
    create_arena_with_different_sizes_green_goal_in_front_of_agent,
    create_arena_with_same_size_one_close_and_one_farther_goal_in_front_of_agent,
    create_arena_with_different_sizes_green_goal_separated_by_wall,
    create_arena_with_same_size_green_goal_separated_by_wall,
    create_arena_with_yellow_goal_separated_by_wall)
from orangutan.arenas.obstacles import (
    create_arena_with_obstacles,
    create_center_blocked_arena,
    create_arena_splitted_in_two,
    create_arena_splitted_in_four,
    create_arena_splitted_in_two_with_path_blocked,
    create_arena_with_goal_on_platform,
    create_arena_with_goal_on_top_of_box,
    create_arena_with_goal_inside_cillinder
)
from orangutan.arenas.generalization import remove_color_information
from orangutan.arenas.avoidance import (
    create_arena_with_obstacles_and_deathzones,
    create_center_blocked_arena_deathzone,
    create_arena_splitted_in_two_deathzone,
    create_arena_splitted_in_four_deathzone,
    create_arena_splitted_in_two_with_path_blocked_deathzone,
)
from orangutan.arenas.spatial_reasoning import (
    create_arena_with_death_maze,
    create_arena_with_platform_maze,
    create_arena_with_walls_maze,
)

FOOD_FUNC_WEIGHTS = [
        (create_arena_with_green_and_yellow_goal_in_front_of_agent, 1),
        (create_arena_with_red_goal_coming, 2),
        (create_arena_with_red_wall, 4),
        (create_arena_with_red_houses, 4),
        (create_arena_with_4_goodgoalmulti, 2),
        (create_arena_with_4_goodgoalmultibounce, 2),
        (create_arena_with_15_badgoal_labyrinth, 4),
        (create_arena_with_30_badgoal_labyrinth, 4),
        (create_arena_with_5_badgoalbounce_labyrinth, 4),
        (create_arena_with_10_badgoalbounce_labyrinth, 4),
        (create_arena_with_15_badgoalbounce_labyrinth, 4),
        (create_arena_with_small_goal, 4),
    ]

PREFERENCES_FUNC_WEIGHTS = [
        (create_arena_with_different_sizes_green_goal_in_front_of_agent, 1),
        (create_arena_with_same_size_one_close_and_one_farther_goal_in_front_of_agent, 1),
        (create_arena_with_different_sizes_green_goal_separated_by_wall, 2),
        (create_arena_with_same_size_green_goal_separated_by_wall, 1),
        (create_arena_with_yellow_goal_separated_by_wall, 2),
    ]

OBSTACLES_FUNC_WEIGHTS = [
    (create_arena_with_obstacles, 16),
    (create_center_blocked_arena, 8),
    (create_arena_splitted_in_two, 8),
    (create_arena_splitted_in_four, 8),
    (create_arena_splitted_in_two_with_path_blocked, 8),
    (create_arena_with_goal_on_platform, 8),
    (create_arena_with_goal_inside_cillinder, 4),
    (create_arena_with_goal_on_top_of_box, 4),
]

AVOIDANCE_FUNC_WEIGHTS = [
    (create_arena_with_obstacles_and_deathzones, 16),
    (create_center_blocked_arena_deathzone, 8),
    (create_arena_splitted_in_two_deathzone, 8),
    (create_arena_splitted_in_four_deathzone, 8),
    (create_arena_splitted_in_two_with_path_blocked_deathzone, 8),
]

SPATIAL_REASONING_FUNC_WEIGHTS = [
    (create_arena_with_death_maze, 12),
    (create_arena_with_platform_maze, 12),
    (create_arena_with_walls_maze, 12),
]

GENERALIZATION_FUNC_WEIGHTS = OBSTACLES_FUNC_WEIGHTS[:7] + AVOIDANCE_FUNC_WEIGHTS[:1]
INTERNAL_MODELS_FUNC_WEIGHTS = FOOD_FUNC_WEIGHTS + OBSTACLES_FUNC_WEIGHTS + AVOIDANCE_FUNC_WEIGHTS
INTERNAL_MODELS_FUNC_WEIGHTS = [(ret[0], int(ret[1]//4)) for ret in INTERNAL_MODELS_FUNC_WEIGHTS]

def generate_arena_config(t, n):
    """
    Creates an ArenaConfig object

    Parameters
    ----------
    t : int
        Max number of steps on the level
    n : int
        Controls the size of the generated arena, the bigger n the bigger the number of arenas
    """
    _summarize_funcs_weights()
    arena_config = ArenaConfig()
    _add_arenas_using_functions_and_weights(arena_config, FOOD_FUNC_WEIGHTS, t, n)
    _add_arenas_using_functions_and_weights(arena_config, PREFERENCES_FUNC_WEIGHTS, t, n)
    _add_arenas_using_functions_and_weights(arena_config, OBSTACLES_FUNC_WEIGHTS, t, n)
    _add_arenas_using_functions_and_weights(arena_config, AVOIDANCE_FUNC_WEIGHTS, t, n)
    _add_arenas_using_functions_and_weights(arena_config, SPATIAL_REASONING_FUNC_WEIGHTS, t, n)
    _add_arenas_using_functions_and_weights(arena_config, GENERALIZATION_FUNC_WEIGHTS, t, n,
                                            remove_color=True)
    _add_arenas_using_functions_and_weights(arena_config, INTERNAL_MODELS_FUNC_WEIGHTS, t, n,
                                            add_blackouts=True)
    _shuffle_arenas(arena_config)
    return arena_config

def _shuffle_arenas(arena_config):
    arenas_copy = arena_config.arenas.copy()
    keys = list(arena_config.arenas.keys())
    np.random.shuffle(keys)
    for key, new_key in zip(arena_config.arenas, keys):
        arena_config.arenas[key] = arenas_copy[new_key]

def _add_arenas_using_functions_and_weights(arena_config, funcs_weights, t, n,
                                            remove_color=False, add_blackouts=False):
    for func, weight in funcs_weights:
        for _ in range(weight*n):
            idx = len(arena_config.arenas)
            arena = func(t=t)
            if remove_color:
                remove_color_information(arena)
            if add_blackouts:
                _add_blackouts_to_arena(arena)
            arena_config.arenas[idx] = arena

def _summarize_funcs_weights():
    print('Food: %i' % sum([weight for func, weight in FOOD_FUNC_WEIGHTS]))
    print('Preferences: %i' % sum([weight for func, weight in PREFERENCES_FUNC_WEIGHTS]))
    print('Obstacles: %i' % sum([weight for func, weight in OBSTACLES_FUNC_WEIGHTS]))
    print('Avoidance: %i' % sum([weight for func, weight in AVOIDANCE_FUNC_WEIGHTS]))
    print('Spatial reasoning: %i' % sum([weight for func, weight in SPATIAL_REASONING_FUNC_WEIGHTS]))
    print('Generalization: %i' % sum([weight for func, weight in GENERALIZATION_FUNC_WEIGHTS]))
    print('Internal models: %i' % sum([weight for func, weight in INTERNAL_MODELS_FUNC_WEIGHTS]))

def _add_blackouts_to_arena(arena):
    blackout = int(np.random.choice([-20, -20, -40]))
    arena.blackouts = [blackout]
