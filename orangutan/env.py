from animalai.envs.environment import UnityEnvironment

class EnvWrapper(object):
    '''
    Wrapper around UnityEnvironment that resets each arena if the episode is done
    '''
    def __init__(self, *args, **kwargs):
        '''
        Check UnityEnvironment parameters
        '''
        # wrap the object
        self._env = UnityEnvironment(*args, **kwargs)
        self._arenas_configurations = None

    def __getattr__(self, attr):
        # see if this object has attr
        # NOTE do not use hasattr, it goes into
        # infinite recurrsion
        if attr in self.__dict__:
            # this object has it
            return getattr(self, attr)
        # proxy to the wrapped object
        return getattr(self._env, attr)

    def reset(self, arenas_configurations=None, train_mode=True):
        """ Shuffle arenas and reset configuration """
        print('reset')
        if arenas_configurations is not None:
            self._arenas_configurations = arenas_configurations
        self._arenas_configurations.shuffle_arenas()
        return self._env.reset(self._arenas_configurations, train_mode)

    def step(self, *args, **kwargs):
        print('step')
        return self._env.step(*args, **kwargs)
