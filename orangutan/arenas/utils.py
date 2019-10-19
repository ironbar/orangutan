from animalai.envs.arena_config import RGB
from animalai.envs.arena_config import ArenaConfig

GRAY = RGB(153, 153, 153)
PINK = RGB(255, 0, 255)
BLUE = RGB(0, 0, 255)

def _str_Vector3(vector3):
    return '(%.1f, %1.f, %.1f)' % (vector3.x, vector3.y, vector3.z)

def merge(arena_config, config_to_add_path):
    new_arena_config = ArenaConfig(config_to_add_path)
    idx = max(list(arena_config.arenas.keys())) + 1
    for arena in new_arena_config.arenas.values():
        arena_config.arenas[idx] = arena
        idx += 1
    return arena_config

def set_all_arenas_to_same_time(arena_config, t):
    for arena in arena_config.arenas.values():
        arena.t = t
