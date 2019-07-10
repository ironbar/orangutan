# Modeling

## Select modeling technique
<!---Document the actual modeling technique that is to be used. If multiple
techniques are applied, perform this task separately for each technique.
Many modeling techniques make specific assumptions about the data—for example,
that all attributes have uniform distributions, no missing values allowed,
class attribute must be symbolic, etc. Record any such assumptions made. --->

### State of the art

#### [Andrej Karpathy Deep Reinforcement Learning](http://karpathy.github.io/2016/05/31/rl/)

_May 31, 2016_

>  It turns out that Q-Learning is not a great algorithm (you could say that DQN is so 2013 (okay I’m 50% joking)). In fact most people prefer to use Policy Gradients, including the authors of the original DQN paper who have shown Policy Gradients to work better than Q Learning when tuned well. PG is preferred because it is end-to-end: there’s an explicit policy and a principled approach that directly optimizes the expected reward.

He explains how Policy Gradients works and illustrates it with an example of playing Pong.

#### [Proximal Policy Optimization](https://openai.com/blog/openai-baselines-ppo/)

Publication by OpenAI that explains PPO. This method is used in the examples of AnimalAI challenge. It seems that Policy Gradients are difficult to train and one way to make it easier is to make changes in the weights that do not modify the distribution too much.

It should be implemented in [github](https://github.com/openai/baselines)

#### [Policy Gradient methods and Proximal Policy Optimization (Video)](https://www.youtube.com/watch?v=5P7I-xPq8u8)

Nice video that explains PPO. The plots show that PPO is the best PG method. At the begginning it says that DQN needs less samples than PG, however it also says that PPO is more data efficient.

If I look at the plots I can see that DQN is faster than A2C but PPO is faster than A2C so hopefully PPO and DQN will be of comparable efficiency.

<p align="center">
  <img src="https://flyyufelix.github.io/img/performance_chart.png">
</p>

<p align="center">
  <img src="media/ppo_comparison.png">
</p>

#### TOREAD

* https://towardsdatascience.com/proximal-policy-optimization-ppo-with-sonic-the-hedgehog-2-and-3-c9c21dbed5e
* https://medium.com/@jonathan_hui/rl-proximal-policy-optimization-ppo-explained-77f014ec3f12
* https://medium.com/deep-math-machine-learning-ai/ch-13-deep-reinforcement-learning-deep-q-learning-and-policy-gradients-towards-agi-a2a0b611617e
* https://flyyufelix.github.io/2017/10/12/dqn-vs-pg.html

## Generate test design
<!---Describe the intended plan for training, testing, and evaluating the models.
A primary component of the plan is determining how to divide the available dataset
into training, test, and validation datasets.

Doing a plot of score vs train size could be helpful to decide the validation strategy

Depending on the size of the data we have to decide how we are going to use submissions.
The less the submissions the most confidence we can have on the score. However sometimes
the data distribution is very different, or the size of the data is small and we have
to make a lot of submissions. Sometimes is not easy to have a good correlation between
validation score and LB score
--->

## Iteration 1. Iteration_title
<!---
The work is done using short iterations. Each iteration needs to have a very
clear goal. This allows to gain greater knowledge of the problem on each iteration.
--->

### Goal

### Development

### Results
