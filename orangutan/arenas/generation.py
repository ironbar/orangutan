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
    arena_config = ArenaConfig()
    _add_food_levels(arena_config, t, n)
    _add_preference_levels(arena_config, t, n)
    _shuffle_arenas(arena_config)
    return arena_config

def _add_food_levels(arena_config, t, n):
    funcs_weights = [
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
    ]
    _add_arenas_using_functions_and_weights(arena_config, funcs_weights, t, n)

def _add_preference_levels(arena_config, t, n):
    funcs_weights = [
        (create_arena_with_different_sizes_green_goal_in_front_of_agent, 1),
        (create_arena_with_same_size_one_close_and_one_farther_goal_in_front_of_agent, 1),
        (create_arena_with_different_sizes_green_goal_separated_by_wall, 2),
        (create_arena_with_same_size_green_goal_separated_by_wall, 1),
        (create_arena_with_yellow_goal_separated_by_wall, 2),
    ]
    _add_arenas_using_functions_and_weights(arena_config, funcs_weights, t, n)

def _shuffle_arenas(arena_config):
    arenas_copy = arena_config.arenas.copy()
    keys = list(arena_config.arenas.keys())
    np.random.shuffle(keys)
    for key, new_key in zip(arena_config.arenas, keys):
        arena_config.arenas[key] = arenas_copy[new_key]

def _add_arenas_using_functions_and_weights(arena_config, funcs_weights, t, n):
    for func, weight in funcs_weights:
        for _ in range(weight*n):
            idx = len(arena_config.arenas)
            arena_config.arenas[idx] = func(t=t)
