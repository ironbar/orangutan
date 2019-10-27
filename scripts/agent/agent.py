import yaml
import glob
import numpy as np
from animalai_train.trainers.ppo.policy import PPOPolicy
from animalai.envs.brain import BrainParameters


class Agent(object):

    def __init__(self):
        """
         Load your agent here and initialize anything needed
        """

        # Load the configuration and model using ABSOLUTE PATHS
        self.configuration_file = '/aaio/data/trainer_config.yaml'
        self.model_path = glob.glob('/aaio/data/*/Learner')[0]
        print('model_path', self.model_path)

        self.brain = BrainParameters(brain_name='Learner',
                                     camera_resolutions=[{'height': 84, 'width': 84, 'blackAndWhite': False}],
                                     num_stacked_vector_observations=1,
                                     vector_action_descriptions=['', ''],
                                     vector_action_space_size=[3, 3],
                                     vector_action_space_type=0,  # corresponds to discrete
                                     vector_observation_space_size=3
                                     )
        self.trainer_params = yaml.load(open(self.configuration_file))['Learner']
        self.trainer_params['keep_checkpoints'] = 0
        self.trainer_params['model_path'] = self.model_path

        self.policy = PPOPolicy(brain=self.brain,
                                seed=0,
                                trainer_params=self.trainer_params,
                                is_training=False,
                                load=True)
        self.memory_in = None
        self.use_recurrent = self.trainer_params['model_architecture']['use_recurrent']
        self._arena_map = None
        if self.trainer_params['model_architecture']['architecture'] in ['map', 'wba_prize']:
            self._map_side = self.trainer_params['model_architecture']['map_encoding']['map_side']
        else:
            self._map_side = None

    def reset(self, t=250):
        """
        Reset is called before each episode begins
        Leave blank if nothing needs to happen there
        :param t the number of timesteps in the episode
        """
        self.memory_in = None
        if self._map_side is not None:
            self._arena_map = ArenaMap()

    def step(self, obs, reward, done, info):
        """
        A single step the agent should take based on the current
        :param brain_info:  a single BrainInfo containing the observations and reward for a single step for one agent
        :return:            a list of actions to execute (of size 2)
        """
        brain_info = info['brain_info']
        if self.use_recurrent:
            if self.memory_in is not None:
                brain_info.memories = self.memory_in
        if self._map_side is not None:
            self._update_map(brain_info)
            brain_info = self._add_map_to_brain_info(brain_info)

        ret = self.policy.evaluate(brain_info=brain_info)
        if self.use_recurrent:
            self.memory_in = ret['memory_out']
        action = ret['action']
        return action

    def _update_map(self, brain_info):
        speed = brain_info.vector_observations[0][[0, 2]]
        previous_action = brain_info.previous_vector_actions
        self._arena_map.add_point(speed, previous_action)

    def _add_map_to_brain_info(self, brain_info):
        heatmap = self._arena_map.get_heatmap(self._map_side)
        heatmap = np.expand_dims(np.expand_dims(heatmap, axis=2), axis=0)
        brain_info.trajectory_map = heatmap
        return brain_info

class ArenaMap():
    """
    Creates a map of the previous positions of the agent in the arena
    """
    def __init__(self):
        self._orientation = 0
        self._orientations = [self._orientation]
        self._position = np.zeros(2)
        self._positions = [self._position.copy()]

    def add_point(self, speed, previous_action):
        # print(speed.shape, previous_action.shape)
        rotation = previous_action[0, 1]
        if rotation == 1:
            self._orientation += 6
        elif rotation == 2:
            self._orientation -= 6
        alpha = -1
        speed_factor = 1./10/1.625
        self._position[1] += speed_factor*np.sum(speed*np.array([
            alpha*np.sin(self._orientation*np.pi/180), np.cos(self._orientation*np.pi/180)]))
        self._position[0] -= speed_factor*np.sum(speed*np.array([
            alpha*np.cos(self._orientation*np.pi/180), -np.sin(self._orientation*np.pi/180)]))
        self._positions.append(self._position.copy())
        self._orientations.append(self._orientation)

    def _get_normalized_positions_to_last_state(self):
        positions = np.array(self._positions)
        positions -= positions[-1:]
        angles = np.arctan2(positions[:, 0], positions[:, 1]) -self._orientation*np.pi/180
        radius = np.sqrt(np.sum(positions**2, axis=1))
        positions[:, 0] = radius*np.sin(angles)
        positions[:, 1] = radius*np.cos(angles)
        return positions

    def get_heatmap(self, side=60):
        assert side % 2 == 0
        scale = side/2/(40*2**0.5*1.05)
        positions = (self._get_normalized_positions_to_last_state()*scale + side//2).astype(np.int)
        heatmap = np.zeros((side, side))
        for position in positions:
            heatmap[position[1], position[0]] = 1
        heatmap = heatmap[::-1]
        return heatmap
