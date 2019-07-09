# Business Understanding
<!--- --->
## Challenge description
<!--- Look at the challenge description, understand the goal of the challenge
and write it here with your own words. Use images if they improve the explanation--->

The goal of the challenge is to gather the food as fast as possible while avoiding predator or traps.  
The environment has great flexibility and it's possible to design quite difficult tests.

> We are proposing a new kind of AI competition. Instead of providing a specific task, we will provide a well-defined arena (available at the end of April) and a list of cognitive abilities that we will test for in that arena. The tests will all use the same agent with the same inputs and actions. The goal will always be to retrieve the same food items by interacting with previously seen objects. However, the exact layout and variations of the tests will not be released until after the competition.

> We expect this to be hard challenge. Winning this competition will require an AI system that can behave robustly and generalise to unseen cases. A perfect score will require a breakthrough in AI, well beyond current capabilities. However, even small successes will show that it is possible, not just to find useful patterns in data, but to extrapolate from these to an understanding of how the world works.

<img src="http://animalaiolympics.com/figs/environment.png" alt="drawing" width="500"/>


## Evaluation
<!--- Understand the metric used on the challenge, write it here and study
the characteristics of the metric --->

There are [300](https://mdcrosby.com/blog/animalailaunch.html) tests with a pass/no pass structure. There are 10 categories of tests with increasing difficulty.

>The evaluation runs your agent on all 300 tests and returns the total score for each category. All tests are pass-fail (based on achieving a score above a threshold) so the maximum score possible is 300.

All the categories have the same number of tests: 30.

>For the mid-way evaluation (for those opting in for a share of the $10,000 AWS prizes) and final evaluation we will (resources permitting) run more extensive testing with 3 variations per test (so 900 tests total). The variations will include minor perturbations to the configurations. The agent will have to pass all 3 variations to pass each individual test, still giving a total score out of 300, but with more strict requirements. This means that your final test score will probably be lower than the score achieved in normal feedback and that the competition leaderboard on EvalAI may not exactly match the final results.

The evaluation will be hosted on [EvalAI](https://evalai.cloudcv.org/web/challenges/challenge-page/396/leaderboard/1107), an open source platform for evaluating and comparing machine learning (ML) and artificial intelligence algorithms (AI) at scale.

>All the tests will have one of the following lengths (in steps): 250, 500, 1000
This information is passed to the agent by the reset function.

A docker is required for creating the evaluation.


## Assess situation
<!---This task involves more detailed fact-finding about all of the resources,
constraints, assumptions, and other factors that should be considered in determining
the data analysis goal and project plan

* timeline. Is there any week where I could not work on the challenge?
* resources. Is there any other project competing for resources?
* other projects. May I have other more interesting projects in the horizon?
 --->

**Timeline.** There are four months for the challenge. Even when we have to learn many things it seems like a reasonable timeline.

**Resources.** I will devote myself to this project because I don't expect to find another challenge that it is more lined with the goal of general intelligence. Creating a team could be very interesting because this is a very big challenge.

### Terminology
<!--- Sometimes the field of the challenge has specific terms, if that is the
case write them here, otherwise delete this section.--->


## Project Plan
<!--- Write initial ideas for the project. This is just initial thoughts,
during the challenge I will have a better understanding of the project and
with better information I could decide other actions not considered here.--->

### Initial Plan

1. Understand the challenge
2. Design levels
3. Baseline agent and submission
3. Validation strategy
4. Design agent
5. Train
6. Evaluate

### Iterative plan

Another option could be to approach the challenge as an iterative process. The syllabus could be approached
category by category. Once we have train a model that is able to solve one category we can proceed to the next one.

This could be a better choice than solving the challenge at once because there are many things to learn. If I had more
experience I could try to design a ultimate model from scratch, but my experience with reinforcement learning is not
that big.