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

    def __getattr__(self, attr):
        # see if this object has attr
        # NOTE do not use hasattr, it goes into
        # infinite recurrsion
        if attr in self.__dict__:
            # this object has it
            return getattr(self, attr)
        # proxy to the wrapped object
        return getattr(self._env, attr)
