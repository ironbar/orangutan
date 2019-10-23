from animalai.envs.environment import UnityEnvironment

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
