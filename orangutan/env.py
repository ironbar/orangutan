import numpy as np
from animalai.envs.environment import UnityEnvironment

from orangutan.map import ArenaMap

class EnvWrapper(object):
    '''
    Wrapper around UnityEnvironment that resets each arena if the episode is done

    It will only work correctly if using a single arena on each environment
    '''
    def __init__(self, *args, **kwargs):
        '''
        Check UnityEnvironment parameters
        '''
        self._env = UnityEnvironment(*args, **kwargs)
        self._arenas_configurations = None

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self._env, attr)

    def reset(self, arenas_configurations=None, train_mode=True):
        """ Shuffle arenas and reset configuration """
        if arenas_configurations is not None:
            self._arenas_configurations = arenas_configurations
        self._arenas_configurations.shuffle_arenas()
        return self._env.reset(self._arenas_configurations, train_mode)

    def step(self, *args, **kwargs):
        ret = self._env.step(*args, **kwargs)
        if ret['Learner'].local_done[0]:
            new_ret = self.reset()
            ret['Learner'].visual_observations = new_ret['Learner'].visual_observations
        return ret

class MapEnv(object):
    '''
    Wrapper around UnityEnvironment that resets each arena if the episode is done
    and creates a map with the trajectory of the agent.

    It will only work correctly if using a single arena on each environment
    '''
    def __init__(self, *args, map_side=60, **kwargs):
        '''
        Check UnityEnvironment parameters
        '''
        self._env = EnvWrapper(*args, **kwargs)
        self._arena_map = None
        self._map_side = map_side

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self._env, attr)

    def reset(self, arenas_configurations=None, train_mode=True):
        ret = self._env.reset(arenas_configurations, train_mode)
        self._reset_map()
        ret = self._add_map_to_brain_info(ret)
        return ret

    def step(self, *args, **kwargs):
        ret = self._env.step(*args, **kwargs)
        if ret['Learner'].local_done[0]:
            self._reset_map()
        else:
            self._update_map(ret)
        ret = self._add_map_to_brain_info(ret)
        return ret

    def _add_map_to_brain_info(self, ret):
        heatmap = self._arena_map.get_heatmap(self._map_side)
        heatmap = np.expand_dims(np.expand_dims(heatmap, axis=2), axis=0)
        ret['Learner'].trajectory_map = heatmap
        return ret

    def _update_map(self, ret):
        speed = ret['Learner'].vector_observations[0][[0, 2]]
        previous_action = ret['Learner'].previous_vector_actions
        self._arena_map.add_point(speed, previous_action)

    def _reset_map(self):
        self._arena_map = ArenaMap()
