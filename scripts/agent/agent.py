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
        self.print_next_eval = True
        self.memory_in = None

    def reset(self, t=250):
        """
        Reset is called before each episode begins
        Leave blank if nothing needs to happen there
        :param t the number of timesteps in the episode
        """
        self.print_next_eval = True
        self.memory_in = None

    def step(self, obs, reward, done, info):
        """
        A single step the agent should take based on the current
        :param brain_info:  a single BrainInfo containing the observations and reward for a single step for one agent
        :return:            a list of actions to execute (of size 2)
        """
        brain_info = info['brain_info']
        if self.memory_in is not None:
            brain_info.memories = self.memory_in
        # print('vars(brain_info)', vars(brain_info))
        # print('brain_info.memories', brain_info.memories)
        ret = self.policy.evaluate(brain_info=brain_info)
        self.memory_in = ret['memory_out']
        # print('list(ret.keys())', list(ret.keys()))
        # print("ret['memory_out']", ret['memory_out'])
        action = ret['action']
        # action[0, 1] = np.argmax(ret['log_probs'][0, 3:])
        # action = [np.argmax(ret['log_probs'][0, :3]), np.argmax(ret['log_probs'][0, 3:])]
        # action = [np.argmax(ret['log_probs'][0, :2]), np.argmax(ret['log_probs'][0, 3:])]
        if self.print_next_eval:
            # print(ret, action)
            # print(ret['log_probs'])
            self.print_next_eval = False
        return action
