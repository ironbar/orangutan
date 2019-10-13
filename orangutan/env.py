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
        # print('reset')
        if arenas_configurations is not None:
            self._arenas_configurations = arenas_configurations
        self._arenas_configurations.shuffle_arenas()
        return self._env.reset(self._arenas_configurations, train_mode)

    def step(self, *args, **kwargs):
        # print('step')
        ret = self._env.step(*args, **kwargs)
        # print(ret['Learner'].local_done)
        if ret['Learner'].local_done[0]:
            new_ret = self.reset()
            ret['Learner'].visual_observations = new_ret['Learner'].visual_observations
        # print(ret)
        # print(ret['Learner'].local_done)
        return ret

    def _reset_individual_arena(self, ret, arena_idx):
        pass